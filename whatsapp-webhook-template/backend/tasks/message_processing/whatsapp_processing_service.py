import logging
from pprint import pformat

from backend.api.v1.webhook.models import (
    WhatsappEntry,
    WhatsappEntryMessageInfo,
    WhatsappWebhookUpdates,
)
from backend.api.v1.webhook.repositories import (
    MessageProcessingRepository,
    MessageRepository,
    MessageStatusRepository,
    SessionRepository,
    UserRepository,
)
from backend.core.constants import (
    CommunicationChannel,
    MessageStatus,
    WhatsappMessageType,
)
from backend.core.models import ProcessEntryCallback
from backend.core.utils import get_current_timestamp, is_older_than_24_hours
from backend.core.whatsapp.whatsapp_mixin import WhatsappMixin
from backend.settings import get_settings
from backend.tasks.message_processing.exceptions import MessageProcessingError
from backend.tasks.message_processing.message_processing_service_base import (
    MessageProcessingMixin,
)
from fastapi import FastAPI
from shared_lib_template.db.postgres import get_postgres_connector


logger = logging.getLogger(__name__)


class WhatsappMessageProcessingService(MessageProcessingMixin, WhatsappMixin):
    """Whatsapp webhook processing runner"""

    def __init__(self, app: FastAPI) -> None:
        self._settings = get_settings()
        self._errors: list[str] = []
        self._messages_to_delete_from_processing: set[int] = set()
        self._postgres_conn = get_postgres_connector(logger=logger, app=app)

        super().__init__()
        super(MessageProcessingMixin, self).__init__()

    async def process_updates(
        self,
        data: WhatsappWebhookUpdates,
    ) -> None:
        """Process Whatsapp updates"""
        logger.info("Found %s updates, processing...", len(data.entry))
        logger.debug("Entries: %s", data.model_dump_json(indent=2))

        session_repository = SessionRepository(conn=self._postgres_conn)
        user_repository = UserRepository(conn=self._postgres_conn)
        message_status_repository = MessageStatusRepository(conn=self._postgres_conn)
        message_repository = MessageRepository(conn=self._postgres_conn)
        message_processing_repository = MessageProcessingRepository(
            conn=self._postgres_conn
        )

        try:
            for entry in data.entry:
                try:
                    processing_info = await self._process_entry(
                        entry=entry,
                        session_repository=session_repository,
                        user_repository=user_repository,
                        message_status_repository=message_status_repository,
                        message_repository=message_repository,
                        message_processing_repository=message_processing_repository,
                    )

                    if processing_info:
                        self._messages_to_delete_from_processing.update(
                            processing_info.message_ids
                        )

                except Exception as e:
                    error_message = f"Error processing entry {entry.id_}. {str(e)}"
                    logger.error(error_message)
                    await self._add_error(error=error_message)

            if not self._errors:
                logger.info("Updates successfully processed")
                return None

            error_message = (
                f"An errors has occured while processing: {pformat(self._errors)}"
            )
            raise MessageProcessingError(error_message)

        finally:
            for message_id in self._messages_to_delete_from_processing:
                await message_processing_repository.delete_message_processing_entry(
                    message_id=message_id,
                )

            await self._postgres_conn.close()

    async def _process_entry(
        self,
        entry: WhatsappEntry,
        session_repository: SessionRepository,
        user_repository: UserRepository,
        message_status_repository: MessageStatusRepository,
        message_repository: MessageRepository,
        message_processing_repository: MessageProcessingRepository,
    ) -> ProcessEntryCallback | None:
        """Processing whatsapp entry"""
        if (
            len(entry.changes) == 0
            or len(entry.changes[0].value.messages) == 0
            or len(entry.changes[0].value.contacts) == 0
        ):
            if (
                len(entry.changes[0].value.statuses) > 0
                and entry.changes[0].value.statuses[0].status == "read"
            ):
                logger.info("Processing message read status")

                # fmt: off
                delivered_messages = await message_repository.get_user_delivered_messages(
                    phone_number=entry.changes[0].value.statuses[0].recipient_id,
                )
                # fmt: on

                for message in delivered_messages:
                    await message_status_repository.update_message_status(
                        status_id=message.message_status_id,
                        status=MessageStatus.OPENED,
                    )

                logger.info(
                    "Messages marked as opened and metrics event created: %s",
                    delivered_messages,
                )

            logger.debug("Entry message %s is empty", entry.id_)
            return None

        entry_info = await self._get_entry_message_info(entry=entry)

        if entry_info.type_ in (
            WhatsappMessageType.REACTION,
            WhatsappMessageType.IMAGE,
            WhatsappMessageType.DOCUMENT,
            WhatsappMessageType.AUDIO,
            WhatsappMessageType.STICKER,
            WhatsappMessageType.VIDEO,
        ):
            logger.warning(
                "Message type is %s, skipping. Message id %s",
                entry_info.type_,
                entry_info.wa_message_id,
            )
            return None

        user_id = await user_repository.get_user_id(
            user_name=entry_info.user_name,
            phone_number=entry_info.phone_number,
            phone_number_id=entry_info.phone_number_id,
        )

        if is_older_than_24_hours(entry_info.timestamp):
            logger.warning(
                "can not process entry `%s`, message `%s` due to expired session",
                entry.id_,
                entry_info.wa_message_id,
            )

            return None

        message_info = await message_repository.get_message(
            wa_message_id=entry_info.wa_message_id,
        )
        message_id = message_info.message_id if message_info else None

        if message_id and (
            await message_processing_repository.is_message_processing(message_id)
            or await message_repository.get_message_status(message_id)
            in (
                MessageStatus.DELIVERED,
                MessageStatus.OPENED,
            )
        ):
            logger.warning(
                "Message %s is already processing or processed, skipping",
                entry_info.wa_message_id,
            )
            return None

        logger.info(
            "Get message from user (%s, %s): %s",
            entry_info.user_name,
            entry_info.phone_number,
            entry_info.text,
        )

        session_info = await session_repository.get_active_session_info(
            user_id=user_id,
            timestamp=entry_info.timestamp,
            channel=CommunicationChannel.WHATSAPP,
        )
        logger.info("Working with session (id=%s)", session_info.session_id)

        if not message_id:
            message_id = await message_repository.create_message(
                session_id=session_info.session_id,
                received_timestamp=entry_info.timestamp,
                user_message=entry_info.text,
                wa_message_id=entry_info.wa_message_id,
            )
            if not message_id:
                error_message = "Message was not created, skipping entry"
                logger.error(error_message)
                await self._add_error(error_message)

                return None

        await message_processing_repository.create_processing_message(
            message_id=message_id, session_id=session_info.session_id
        )
        self._messages_to_delete_from_processing.add(message_id)

        status_id = await message_status_repository.get_message_status_id(
            message_id=message_id,
            status=MessageStatus.PROCESSING,
            timestamp=get_current_timestamp(),
        )

        logger.info(
            "Created message in DB. message_id=%s, status_id=%s",
            message_id,
            status_id,
        )

        is_message_marked_as_read = await self._mark_message_as_read(
            phone_number_id=entry_info.phone_number_id,
            wa_message_id=entry_info.wa_message_id,
        )
        logger.info("Message marking as read status: %s", is_message_marked_as_read)

        if not is_message_marked_as_read:
            error_message = (
                f"Message marking as read failed for message with id {message_id}"
            )
            logger.error(error_message)
            await self._add_error(error_message)

            return None

        await message_status_repository.update_message_status(
            status_id=status_id,
            status=MessageStatus.READ,
        )

        if session_info.is_new_session:
            entry_info.text = await self._format_new_session_first_message(
                entry_info.text
            )

        logger.debug("Prepared message to OpenAI: `%s`", entry_info.text)

        processing_info = await self._wait_for_new_messages(
            session_id=session_info.session_id,
            is_new_session=session_info.is_new_session,
            message_id=message_id,
            status_id=status_id,
            message_repository=message_repository,
            message_status_repository=message_status_repository,
            message_processing_repository=message_processing_repository,
            waiting_interval=self._settings.WHATSAPP_CONCATENATED_MESSAGE_WAITING_SECONDS,
        )

        if processing_info.need_to_stop:
            self._messages_to_delete_from_processing.discard(message_id)

            return ProcessEntryCallback(
                message_ids=processing_info.processing_message_ids_to_clear,
            )

        if processing_info.new_message_text:
            entry_info.text = processing_info.new_message_text

        # Put your answer logic here
        bot_reply = entry_info.text

        await message_repository.update_message(
            message_id=message_id,
            bot_message=bot_reply,
        )

        message_callback = await self._send_message(
            phone_number=entry_info.phone_number,
            phone_number_id=entry_info.phone_number_id,
            text=bot_reply,
        )

        logger.info("Message sending status: %s", bool(message_callback))
        logger.debug("Message sending callback: %s", message_callback)

        if message_callback:
            await self._process_message_success_callback(
                status_id=status_id,
                message_id=message_id,
                user_id=user_id,
                message_status_repository=message_status_repository,
                message_repository=message_repository,
                channel=CommunicationChannel.WHATSAPP,
            )

        else:
            await self._process_message_failed_callback(
                message_id=message_id,
                message_status_repository=message_status_repository,
                status_id=status_id,
                user_id=user_id,
                channel=CommunicationChannel.WHATSAPP,
            )
            return None

        return ProcessEntryCallback(
            message_ids=processing_info.processing_message_ids_to_clear or [message_id],
        )

    async def _get_entry_message_info(
        self, entry: WhatsappEntry
    ) -> WhatsappEntryMessageInfo:
        """Get model of entry metadata from entry instance"""

        text = None

        if entry.changes[0].value.messages[0].text:
            text = entry.changes[0].value.messages[0].text.body

        if entry.changes[0].value.messages[0].button:
            text = entry.changes[0].value.messages[0].button.text

        if text is None and entry.changes[0].value.messages[0].type_ in (
            WhatsappMessageType.REACTION,
            WhatsappMessageType.IMAGE,
            WhatsappMessageType.DOCUMENT,
            WhatsappMessageType.AUDIO,
            WhatsappMessageType.STICKER,
            WhatsappMessageType.VIDEO,
        ):
            text = ""  # placeholder to confirm str type in model

        if text is None:
            raise ValueError("Message text not provided")

        return WhatsappEntryMessageInfo(
            text=text,
            user_name=entry.changes[0].value.contacts[0].profile.name,
            phone_number=entry.changes[0].value.messages[0].from_,
            phone_number_id=entry.changes[0].value.metadata.phone_number_id,
            timestamp=entry.changes[0].value.messages[0].timestamp,
            wa_message_id=entry.changes[0].value.messages[0].id_,
            type_=entry.changes[0].value.messages[0].type_,
        )

    async def _add_error(self, error: str) -> None:
        self._errors.append(error)

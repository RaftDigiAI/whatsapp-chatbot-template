import asyncio
import logging
from datetime import datetime

from backend.api.v1.webhook.constants import (
    FIRST_USER_MESSAGE_TEMPLATE,
    OPENAI_ASSISTANT_DATE_FORMAT,
)
from backend.api.v1.webhook.repositories import (
    MessageProcessingRepository,
    MessageRepository,
    MessageStatusRepository,
)
from backend.core.constants import CommunicationChannel, MessageStatus
from backend.core.models import MessageProcessingCallbackInfo
from backend.core.utils import get_current_timestamp
from backend.settings import get_settings


logger = logging.getLogger(__name__)


class MessageProcessingMixin:
    """Base message processing service"""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._messages_to_delete_from_processing: set[int] = set()

    async def _format_new_session_first_message(self, message: str) -> str:
        """Formatting message with current date"""
        return FIRST_USER_MESSAGE_TEMPLATE.format(
            message=message,
            date=datetime.now().strftime(OPENAI_ASSISTANT_DATE_FORMAT),
        )

    async def _wait_for_new_messages(
        self,
        session_id: int,
        message_id: int,
        status_id: int,
        is_new_session: bool,
        message_repository: MessageRepository,
        message_status_repository: MessageStatusRepository,
        message_processing_repository: MessageProcessingRepository,
        waiting_interval: int,
    ) -> MessageProcessingCallbackInfo:
        """Check if need to stop message processing because of new incoming message"""

        logger.info(
            "Waiting %ss for new incoming message",
            waiting_interval,
        )

        await asyncio.sleep(waiting_interval)

        processing_messages = (
            await message_processing_repository.get_processing_messages(session_id)
        )

        logger.debug(
            "Processing messages (%s): %s",
            len(processing_messages),
            processing_messages,
        )

        processing_message_ids = [item.message_id for item in processing_messages]
        need_to_check = (
            len(processing_messages) > 1 and message_id in processing_message_ids
        )

        new_message_text: str | None = None
        need_to_stop: bool = False
        processing_message_ids_to_clear: list[int] = []

        if need_to_check:
            # 1. Message is last. Concat user messages
            if message_id == processing_message_ids[-1]:
                messages_to_concat: list[str] = []
                for item in processing_messages:
                    if message_id not in (
                        item.concatenated_message_id,
                        item.message_id,
                    ):
                        continue

                    messages_to_concat.append(item.user_message)
                    processing_message_ids_to_clear.append(item.message_id)

                new_message_text = "\n".join(messages_to_concat)

            # 2. Message is first or in the middle. Stop processing and save metadata
            else:
                await message_repository.update_message(
                    message_id=message_id,
                    concatenated_message_id=processing_message_ids[-1],
                )
                await message_status_repository.update_message_status(
                    status_id=status_id, status=MessageStatus.CONCATENATED
                )
                need_to_stop = True

        if is_new_session and new_message_text:
            new_message_text = await self._format_new_session_first_message(
                new_message_text
            )

        callback = MessageProcessingCallbackInfo(
            need_to_stop=need_to_stop,
            new_message_text=new_message_text,
            processing_message_ids_to_clear=processing_message_ids_to_clear,
        )

        logger.debug("Processing callback: %s", callback)

        return callback

    async def _process_message_success_callback(
        self,
        status_id: int,
        message_id: int,
        user_id: int,
        message_status_repository: MessageStatusRepository,
        message_repository: MessageRepository,
        channel: CommunicationChannel,
    ) -> None:
        """Process success message sending. Send metadata in DB, process CRM integration and save metrics"""
        await message_status_repository.update_message_status(
            status_id=status_id,
            status=MessageStatus.DELIVERED,
        )
        await message_repository.update_message(
            message_id=message_id,
            replied_timestamp=get_current_timestamp(),
        )

    async def _process_message_failed_callback(
        self,
        message_id: int,
        message_status_repository: MessageStatusRepository,
        status_id: int,
        user_id: int,
        channel: CommunicationChannel,
    ) -> None:
        """Process failed message sending. Send metadata in DB and save metrics"""
        error_message = f"Message sending failed for message with id {message_id}"
        logger.error(error_message)

        await message_status_repository.update_message_status(
            status_id=status_id,
            status=MessageStatus.FAILED_TO_SEND,
        )

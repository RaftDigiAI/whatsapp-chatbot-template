from pydantic import TypeAdapter
from shared_lib_template.db import PostgresConnectorInterface

from backend.core.constants import MessageStatus
from backend.core.models import MessageInfo
from backend.core.models.repository.delivered_message_info import DeliveredMessageInfo
from backend.core.models.repository.dialog_history import DialogHistory


class MessageRepository:
    """Service to work with messages"""

    def __init__(
        self,
        conn: PostgresConnectorInterface,
    ) -> None:
        self._conn = conn

    async def get_message(self, wa_message_id: str) -> MessageInfo | None:
        """
        Get message message already exists in DB by wa_message_id.
        Returns MessageInfo info if exists
        """
        query = """
            select
                m.message_id,
                m.session_id,
                m.received_timestamp,
                m.replied_timestamp,
                m.user_message,
                m.bot_message,
                concatenated_message_id
              from webhook.message m
              join webhook.session s
                on s.session_id = m.session_id
               and not s.is_archived
             where wa_message_id = $1
        """

        result = await self._conn.get_query_result_as_dict(query, wa_message_id)

        return TypeAdapter(MessageInfo).validate_python(result) if result else None

    async def get_message_status(self, message_id: int) -> str:
        """Get message status by id"""
        query = """
            select ms.status
              from webhook.message m
              join webhook.message_status ms
                on ms.message_id = m.message_id
             where m.message_id = $1
        """

        result = await self._conn.get_query_result_as_dict(query, message_id)

        return result["status"] if result else None

    async def create_message(
        self,
        session_id: int,
        received_timestamp: int,
        user_message: str,
        wa_message_id: str,
    ) -> int | None:
        """Create message in DB"""
        query = """
            insert into webhook.message(session_id, received_timestamp, user_message, wa_message_id)
            values ($1, to_timestamp($2), $3, $4)
            returning message_id
        """

        result = await self._conn.get_query_result_as_dict(
            query,
            session_id,
            received_timestamp,
            user_message,
            wa_message_id,
        )

        return result["message_id"] if result else None

    async def get_message_history(self, session_id: int) -> list[DialogHistory]:
        """Get session dialog history"""
        query = """
            select user_message, bot_message
              from webhook.message m
              join webhook.message_status ms
                on ms.message_id = m.message_id
               and ms.status in ($1, $2, $3)
             where m.session_id = $4
             order by m.received_timestamp
        """

        result = await self._conn.get_query_result_as_list(
            query,
            MessageStatus.DELIVERED,
            MessageStatus.OPENED,
            MessageStatus.CONCATENATED,
            session_id,
        )

        return TypeAdapter(list[DialogHistory]).validate_python(result)

    async def get_user_delivered_messages(
        self,
        phone_number: str,
    ) -> list[DeliveredMessageInfo]:
        """Get all messages in status `delivered`"""
        query = """
            select
                m.message_id,
                ms.status_id message_status_id,
                u.user_id
              from webhook.message_status ms
              join webhook.message m
                on ms.message_id = m.message_id
              join webhook.session s
                on s.session_id = m.session_id
              join webhook.user u
                on u.user_id = s.user_id
               and u.phone_number = $1
             where ms.status = $2
        """

        result = await self._conn.get_query_result_as_list(
            query, phone_number, MessageStatus.DELIVERED
        )

        return TypeAdapter(list[DeliveredMessageInfo]).validate_python(result)

    async def update_message(
        self,
        message_id: int,
        replied_timestamp: int | None = None,
        bot_message: str | None = None,
        concatenated_message_id: int | None = None,
    ) -> None:
        """Update message instance"""
        if replied_timestamp:
            await self._update_message_replied_timestamp(message_id, replied_timestamp)

        if bot_message:
            await self._update_message_bot_response(message_id, bot_message)

        if concatenated_message_id:
            await self._update_message_concatenated_message_id(
                message_id,
                concatenated_message_id,
            )

    async def _update_message_replied_timestamp(
        self,
        message_id: int,
        replied_timestamp: int,
    ) -> None:
        """Updates message reply timestamp"""
        query = """
            update webhook.message
               set replied_timestamp = to_timestamp($1)
             where message_id = $2
        """

        await self._conn.execute_query(
            query,
            replied_timestamp,
            message_id,
        )

    async def _update_message_bot_response(
        self,
        message_id: int,
        bot_message: str,
    ) -> None:
        """Updates message bot reply"""
        query = """
            update webhook.message
               set bot_message = $1
             where message_id = $2
        """

        await self._conn.execute_query(
            query,
            bot_message,
            message_id,
        )

    async def _update_message_concatenated_message_id(
        self,
        message_id: int,
        concatenated_message_id: int,
    ) -> None:
        """Updates message concatenated message id"""
        query = """
            update webhook.message
               set concatenated_message_id = $1
             where message_id = $2
        """

        await self._conn.execute_query(
            query,
            concatenated_message_id,
            message_id,
        )

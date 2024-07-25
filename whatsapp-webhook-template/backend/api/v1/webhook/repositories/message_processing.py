from pydantic import TypeAdapter
from shared_lib_template.db import PostgresConnectorInterface

from backend.core.models import MessageProcessingInfo


class MessageProcessingRepository:
    """Service to work with message processing"""

    def __init__(
        self,
        conn: PostgresConnectorInterface,
    ) -> None:
        self._conn = conn

    async def is_message_processing(
        self,
        message_id: int,
    ) -> bool:
        """Get phone_number_id from DB"""
        query = """
            select 1
              from webhook.message_processing
             where message_id = $1
        """

        result = await self._conn.get_query_result_as_dict(query, message_id)

        return bool(result)

    async def get_processing_messages(
        self,
        session_id: int,
    ) -> list[MessageProcessingInfo]:
        """Get processing messages for active session"""

        query = """
            select distinct
                mp.message_id,
                m.user_message,
                m.received_timestamp,
                m.concatenated_message_id
              from webhook.message_processing mp
              join webhook.session s
                on s.session_id = mp.session_id
               and not s.is_archived
              join webhook.message m
                on m.message_id = mp.message_id
             where mp.session_id = $1
             order by m.received_timestamp
        """

        result = await self._conn.get_query_result_as_list(query, session_id)

        return TypeAdapter(list[MessageProcessingInfo]).validate_python(result)

    async def create_processing_message(self, message_id: int, session_id: int) -> None:
        """Create message processing entry in DB"""
        query = """
            insert into webhook.message_processing(message_id, session_id)
            values ($1, $2)
        """

        await self._conn.execute_query(query, message_id, session_id)

    async def delete_message_processing_entry(
        self,
        message_id: int,
    ) -> None:
        """Updates message status"""
        query = """
            delete from webhook.message_processing
             where message_id = $1
        """

        await self._conn.execute_query(query, message_id)

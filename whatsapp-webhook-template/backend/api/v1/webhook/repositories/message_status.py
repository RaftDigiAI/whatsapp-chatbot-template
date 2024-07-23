from shared_lib_template.db import PostgresConnectorInterface


class MessageStatusRepository:
    """Service to work with message statuses"""

    def __init__(
        self,
        conn: PostgresConnectorInterface,
    ) -> None:
        self._conn = conn

    async def get_message_status_id(
        self,
        message_id: int,
        status: str,
        timestamp: int,
    ) -> int:
        """Get message status ID. If not exists creates new"""
        if not (
            message_status_id := await self.get_message_status(
                message_id=message_id,
            )
        ):
            message_status_id = await self.create_message_status(
                message_id=message_id,
                status=status,
                timestamp=timestamp,
            )

        return message_status_id

    async def get_message_status(
        self,
        message_id: int,
    ) -> int | None:
        """Get message status ID."""
        query = """
            select status_id
              from webhook.message_status
             where message_id = $1
        """

        result = await self._conn.get_query_result_as_dict(query, message_id)

        return result["status_id"] if result else None

    async def create_message_status(
        self,
        message_id: int,
        status: str,
        timestamp: int,
    ) -> int:
        """Create message status entry in DB"""
        query = """
            insert into webhook.message_status(message_id, status, timestamp)
            values ($1, $2, to_timestamp($3))
            returning status_id
        """

        result = await self._conn.get_query_result_as_dict(
            query,
            message_id,
            status,
            timestamp,
        )

        return result["status_id"]

    async def update_message_status(
        self,
        status_id: int,
        status: str,
    ) -> None:
        """Updates message status"""
        query = """
            update webhook.message_status
               set status = $1
             where status_id = $2
        """

        await self._conn.execute_query(query, status, status_id)

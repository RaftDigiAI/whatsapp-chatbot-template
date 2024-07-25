from shared_lib_template.db import PostgresConnectorInterface


class GptResponseRepository:
    """Service to work with GPT responses"""

    def __init__(
        self,
        conn: PostgresConnectorInterface,
    ) -> None:
        self._conn = conn

    async def create_message_gpt_response(
        self,
        message_id: int,
        prompt: str,
    ) -> None:
        """Create message status entry in DB"""
        query = """
            insert into webhook.gpt_response(message_id, prompt)
            values ($1, $2)
        """

        await self._conn.execute_query(query, message_id, prompt)

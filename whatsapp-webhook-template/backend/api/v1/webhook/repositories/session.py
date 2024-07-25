from shared_lib_template.db import PostgresConnectorInterface

from backend.core.constants import CommunicationChannel
from backend.core.models import SessionInfo


class SessionRepository:
    """Service to work with user sessions"""

    def __init__(
        self,
        conn: PostgresConnectorInterface,
    ) -> None:
        self._conn = conn

    async def get_active_session_info(
        self,
        user_id: int,
        timestamp: int,
        channel: CommunicationChannel,
    ) -> SessionInfo:
        """Get active session id. If session not exists or expired, creates new

        Args:
            conn (PostgresConnectorInterface): Postgres connector
            user_id (int): User ID
            timestamp (int): Message timestamp
            channel (CommunicationChannel): Communication channel

        Returns:
            SessionInfo: session info
        """
        if not (
            session_info := await self.get_active_session(
                user_id=user_id,
                channel=channel,
            )
        ):
            session_id = await self.create_session(
                user_id=user_id,
                timestamp=timestamp,
                channel=channel,
            )
            is_new_session = True

        else:
            session_id = session_info["session_id"]
            await self.update_active_session_timestamp(
                session_id=session_id,
                timestamp=timestamp,
            )
            is_new_session = not (
                await self._is_session_messages_exists(session_id=session_id)
            )

        return SessionInfo(
            session_id=session_id,
            is_new_session=is_new_session,
        )

    async def get_active_session(
        self,
        user_id: int,
        channel: CommunicationChannel,
    ) -> dict:
        """Get active user session"""
        query = """
            select session_id
              from webhook.session s
             where s.user_id = $1
               and communication_channel = $2
               and s.end_time > now()
               and not s.is_archived
        """

        return await self._conn.get_query_result_as_dict(query, user_id, channel)

    async def update_active_session_timestamp(
        self,
        session_id: int,
        timestamp: int,
    ) -> None:
        """Update active user session end_time to actual"""
        query = """
            update webhook.session
            set end_time = to_timestamp($1) + interval '24h'
            where session_id = $2
        """

        await self._conn.execute_query(query, timestamp, session_id)

    async def create_session(
        self,
        user_id: int,
        timestamp: int,
        channel: CommunicationChannel,
    ) -> int:
        """Creates session in DB"""
        query = """
            insert into webhook.session(user_id, start_time, end_time, communication_channel)
            values (
                $1,
                to_timestamp($2),
                to_timestamp($2) + interval '24h',
                $3
            )
            returning session_id
        """

        result = await self._conn.get_query_result_as_dict(
            query,
            user_id,
            timestamp,
            channel,
        )

        return result["session_id"] if result else None

    async def archive_user_sessions(
        self,
        user_id: int,
        archive_flag: bool,
    ) -> None:
        """Archive session"""
        query = """
            update webhook.session
               set is_archived = $2
             where user_id = $1
        """

        await self._conn.execute_query(query, user_id, archive_flag)

    async def _is_session_messages_exists(self, session_id: int) -> bool:
        """Check if session already has messages"""
        query = """
            select 1 as c1
              from webhook.session s
              join webhook.message m
                on s.session_id = m.session_id
               and m.bot_message is not null
             where s.session_id = $1
               and not s.is_archived
        """

        return bool(await self._conn.get_query_result_as_dict(query, session_id))

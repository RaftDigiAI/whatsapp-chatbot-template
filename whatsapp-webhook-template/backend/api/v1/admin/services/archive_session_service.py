import logging

from fastapi import Request
from shared_lib_template.db.postgres import get_postgres_connector

from backend.api.v1.webhook.repositories import SessionRepository, UserRepository
from backend.settings import get_settings


logger = logging.getLogger(__name__)


class ArchiveSessionService:
    """Service for processing session archivation"""

    def __init__(self, request: Request) -> None:
        self._settings = get_settings()

        self._postgres_conn = get_postgres_connector(logger=logger, app=request.app)
        self._is_closed_conn = False

        self._session_repository = SessionRepository(conn=self._postgres_conn)
        self._user_repository = UserRepository(conn=self._postgres_conn)

    async def archive_user_sessions(
        self,
        phone_number: str,
    ) -> bool:
        """Archive active session by phone number"""

        user_ids = await self._user_repository.get_user_ids_by_phone_number(
            phone_number=phone_number,
        )

        if not user_ids:
            logger.warning("No user with phone_number `%s` exists", phone_number)

            return False

        logger.info("Archiving sessions for users %s", user_ids)

        for user_id in user_ids:
            await self._session_repository.archive_user_sessions(
                user_id=user_id,
                archive_flag=True,
            )

        return True

    async def close_conn(self) -> None:
        """Close instance postgres connector"""
        await self._postgres_conn.close()
        self._is_closed_conn = True

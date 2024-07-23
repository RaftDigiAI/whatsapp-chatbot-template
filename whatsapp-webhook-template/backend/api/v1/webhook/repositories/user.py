import logging

from pydantic import TypeAdapter
from shared_lib_template.db import PostgresConnectorInterface

from backend.core.models import UserInfo


logger = logging.getLogger(__name__)


class UserRepository:
    """Service to work with users"""

    def __init__(
        self,
        conn: PostgresConnectorInterface,
    ) -> None:
        self._conn = conn

    async def get_user_id(
        self,
        user_name: str,
        phone_number: str,
        phone_number_id: str,
    ) -> int:
        """Get user id by name and phone"""
        if not (
            user_id := await self.get_user(
                phone_number=phone_number,
                phone_number_id=phone_number_id,
            )
        ):
            user_id = await self.create_user(
                user_name=user_name,
                phone_number=phone_number,
                phone_number_id=phone_number_id,
            )
            logger.info(
                "New user (%s, %s) succesfully created",
                user_name,
                phone_number,
            )

        return user_id

    async def get_user(
        self,
        phone_number: str,
        phone_number_id: str,
    ) -> int | None:
        """Get user_id from DB"""
        query = """
            select user_id
              from webhook.user
             where phone_number = $1
               and phone_number_id = $2
        """

        result = await self._conn.get_query_result_as_dict(
            query, phone_number, phone_number_id
        )

        return result["user_id"] if result else None

    async def get_user_by_phone_number_and_phone_number_id(
        self,
        phone_number: str,
        phone_number_id: str,
    ) -> int | None:
        """Get user_id from DB"""
        query = """
            select user_id
              from webhook.user
             where phone_number = $1
               and phone_number_id = $2
        """

        result = await self._conn.get_query_result_as_dict(
            query, phone_number, phone_number_id
        )

        return result.get("user_id")

    async def get_user_ids_by_phone_number(
        self,
        phone_number: str,
    ) -> list[int]:
        """Get user_ids from DB by phone number"""
        query = """
            select user_id
              from webhook.user
             where phone_number = $1
        """

        result = await self._conn.get_query_result_as_list(query, phone_number)

        return [v["user_id"] for v in result]

    async def create_user(
        self,
        phone_number: str,
        phone_number_id: str,
        user_name: str | None = None,
    ) -> int:
        """Creates user in DB. returns new user id"""
        query = """
            insert into webhook.user(user_name, phone_number, phone_number_id)
            values ($1, $2, $3)
            returning user_id
        """

        result = await self._conn.get_query_result_as_dict(
            query, user_name, phone_number, phone_number_id
        )

        return result["user_id"]

    async def get_phone_number_id(
        self,
        user_id: int,
    ) -> str:
        """Get phone_number_id from DB"""
        query = """
            select phone_number_id
              from webhook.user
             where user_id = $1
        """

        result = await self._conn.get_query_result_as_dict(query, user_id)

        return result["phone_number_id"] if result else None

    async def get_user_full_info(self, user_id: int) -> UserInfo | None:
        """Get full user info by ID"""
        query = """
            select
                user_id,
                user_name,
                phone_number,
                phone_number_id,
                opt_in_status
              from webhook.user
             where user_id = $1
        """

        result = await self._conn.get_query_result_as_dict(query, user_id)

        return TypeAdapter(UserInfo).validate_python(result) if result else None

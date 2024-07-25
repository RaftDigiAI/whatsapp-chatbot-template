from typing import Type

import asyncpg

from shared_lib_template.base_settings import WhatsappBaseSettings
from shared_lib_template.db.postgres import PostgresConnectorInterface


async def create_postgres_connection_pool(settings: Type[WhatsappBaseSettings]):
    return await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        command_timeout=settings.POSTGRES_TIMEOUT,
        min_size=settings.POSTGRES_MIN_CONNECTIONS,
        max_size=settings.POSTGRES_MAX_CONNECTIONS,
    )


__all__ = [
    "create_postgres_connection_pool",
    "PostgresConnectorInterface",
]

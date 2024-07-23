from logging import Logger

from fastapi import HTTPException


async def raise_http_exception(
    logger: Logger, status_code: int, message: str, **kwargs
):
    """Throws HTTP exception"""
    logger.error(message)

    raise HTTPException(
        status_code=status_code,
        detail=message,
        **kwargs,
    )

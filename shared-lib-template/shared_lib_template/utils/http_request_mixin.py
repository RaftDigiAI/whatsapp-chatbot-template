import logging
from typing import Any

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient
from shared_lib_template.constants import RETRY_STATUSES
from shared_lib_template.types import (
    HeadersType,
    JsonType,
    RetryStatusesType,
    TypeBaseSettings,
)


logger = logging.getLogger(__name__)


class HttpRequestMixin:
    """Mixin for sending http requests"""

    def __init__(
        self,
        settings: TypeBaseSettings,
        retry_attempts: int | None = None,
        start_timeout: float | None = None,
        headers: dict | None = None,
        retry_statuses: RetryStatusesType | None = None,
    ) -> None:
        self._base_settings = settings

        self._retry_options: ExponentialRetry = ExponentialRetry(
            attempts=retry_attempts or settings.DEFAULT_API_RETRY_COUNT,
            start_timeout=start_timeout or settings.DEFAULT_API_RETRY_START_TIMEOUT,
            retry_all_server_errors=True,
            statuses=retry_statuses or RETRY_STATUSES,
        )
        self._headers = headers or {}

    async def post(
        self,
        url: str,
        headers: HeadersType | None = None,
        data: Any | None = None,
        json: JsonType | None = None,
        retry_options: ExponentialRetry | None = None,
    ) -> dict:
        """Post request"""
        retry_config = self._retry_options
        if retry_options is not None:
            retry_config = retry_options

        if not headers:
            headers = self._headers

        async with aiohttp.ClientSession() as session:
            retry_client = RetryClient(
                client_session=session,
                retry_options=retry_config,
                logger=logger,
                raise_for_status=True,
            )
            response = await retry_client.post(
                url,
                data=data,
                json=json,
                headers=headers,
                ssl=self._base_settings.DEFAULT_VERIFY_SSL,
            )
            return await response.json(content_type=None)

    async def get(self, url: str, headers: dict[str, Any] | None = None) -> dict:
        """Get request"""
        if not headers:
            headers = self._headers

        async with aiohttp.ClientSession() as session:
            retry_client = RetryClient(
                client_session=session,
                retry_options=self._retry_options,
                logger=logger,
                raise_for_status=True,
            )
            response = await retry_client.get(
                url,
                headers=headers,
                ssl=self._base_settings.DEFAULT_VERIFY_SSL,
            )
            return await response.json(content_type=None)

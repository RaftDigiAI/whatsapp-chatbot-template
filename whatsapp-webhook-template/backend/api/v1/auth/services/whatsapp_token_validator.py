import hashlib
import logging

from fastapi import Body, Header, Query, status

from backend.api.v1.auth import constants
from backend.api.v1.webhook.models import WhatsappWebhookUpdates
from backend.core.utils import raise_http_exception
from backend.settings import get_settings


logger = logging.getLogger(__name__)


class WhatsappTokenValidatorService:
    """Whatsapp Token validator Service"""

    def __init__(
        self,
        token: str | None = None,
        signature: str | None = None,
        data: WhatsappWebhookUpdates | None = None,
    ) -> None:
        self._settings = get_settings()
        self._token = token
        self._signature = signature
        self._data = data

    async def validate(self) -> None:
        """Process of token validation"""
        if not self._token and not (
            self._signature or not self._settings.WHATSAPP_VALIDATE_SIGNATURE
        ):
            logger.info("Credentials are not provided")

            await raise_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=constants.APIResponseMessageTemplate.UNAUTHORIZED,
            )

        is_valid_token = self._token and self._is_valid_token(token=self._token)
        is_valid_signature = not self._settings.WHATSAPP_VALIDATE_SIGNATURE or (
            self._signature
            and self._data
            and self._is_valid_signature(
                signature=self._signature,
                data=self._data,
            )
        )
        if not (is_valid_token or is_valid_signature):
            logger.info("Auth validation failed")

            await raise_http_exception(
                status_code=status.HTTP_403_FORBIDDEN,
                message=constants.APIResponseMessageTemplate.FORBIDDEN,
            )

    def _is_valid_token(self, token: str) -> bool:
        """Validate token"""
        return token == self._settings.WHATSAPP_WEBHOOK_TOKEN

    def _is_valid_signature(self, signature: str, data: WhatsappWebhookUpdates) -> bool:
        """Validate signature"""
        if not self._settings.WHATSAPP_VALIDATE_SIGNATURE and not self._token:
            logger.warning(
                "Skipping message signature check as flag WHATSAPP_VALIDATE_SIGNATURE disabled"
            )
            return True

        sha256_hash = hashlib.sha256()
        sha256_hash.update(
            data.model_dump_json().encode("utf-8")
        )  # TODO: figure out whatsapp encoding  # pylint: disable=W0511
        sha256_hash.update(self._settings.WHATSAPP_WEBHOOK_TOKEN.encode("utf-8"))
        calculated_signature = sha256_hash.hexdigest()

        is_valid_signature = signature.removeprefix("sha256=") == calculated_signature

        if not is_valid_signature:
            logger.debug(
                "Signature is:\n___\n%s\n___\nCalculated signature is \n___\n%s\n___",
                signature,
                calculated_signature,
            )

        return is_valid_signature


class WhatsappTokenValidator:
    """Token validator class"""

    async def __call__(
        self,
        token: str = Query(None, alias="hub.verify_token", include_in_schema=False),
        signature: str = Header(
            None, alias="x-hub-signature-256", include_in_schema=False
        ),
        data: WhatsappWebhookUpdates = Body(None, include_in_schema=False),
    ):
        _validator_service = WhatsappTokenValidatorService(
            token=token, signature=signature, data=data
        )
        await _validator_service.validate()

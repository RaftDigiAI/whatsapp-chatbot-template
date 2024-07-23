import logging
from typing import Any

from backend.api.v1.webhook.constants import MESSAGING_PRODUCT
from backend.api.v1.webhook.models import WhatsappMessageCallback
from backend.core.constants import ApplicationMode, WhatsappTemplateLanguage
from backend.settings import get_settings
from pydantic import TypeAdapter
from shared_lib_template.utils import HttpRequestMixin


logger = logging.getLogger(__name__)


class WhatsappMixin(HttpRequestMixin):
    """Mixin for whatsapp requests"""

    def __init__(
        self,
        retry_attempts: int | None = None,
        start_timeout: float | None = None,
        headers: dict | None = None,
    ) -> None:
        self._settings = get_settings()

        # fmt: off
        super().__init__(
            settings=self._settings,
            retry_attempts=retry_attempts or self._settings.WHATSAPP_API_RETRY_COUNT,
            start_timeout=start_timeout or self._settings.WHATSAPP_API_RETRY_START_TIMEOUT,
            headers=headers or {"Authorization": f"Bearer {self._settings.WHATSAPP_API_TOKEN}"},
        )
        # fmt: on

    async def _mark_message_as_read(
        self,
        phone_number_id: str,
        wa_message_id: str,
    ) -> bool:
        """Mark message as read. Returns `True` if success, else `False"""
        if (
            self._settings.APP_MODE != ApplicationMode.PROD
            and not self._settings.WHATSAPP_ENABLE_PROD_INTEGRAION
        ):
            logger.warning("Whatsapp integration disabled, skipping...")
            return True

        logger.info(
            "Marking message from %s with id %s as read",
            phone_number_id,
            wa_message_id,
        )

        url = self._settings.WHATSAPP_API_MESSAGES_URL.format(
            url=self._settings.WHATSAPP_API_BASE_URL,
            phone_number_id=phone_number_id,
        )

        try:
            result = await self.post(
                url=url,
                json={
                    "messaging_product": MESSAGING_PRODUCT,
                    "status": "read",
                    "message_id": wa_message_id,
                },
            )

            return result.get("success", False)

        except Exception as e:
            logger.error("Failed to mark message as read: %s", e)
            return False

    async def _send_message(
        self,
        phone_number: str,
        phone_number_id: str,
        text: str | None = None,
        template: (
            str | None
        ) = None,  # TODO: enum for templates  # pylint: disable=W0511
        template_language: WhatsappTemplateLanguage = WhatsappTemplateLanguage.EN,
    ) -> WhatsappMessageCallback | bool | None:
        """
        Send reply to user message.
        Returns `WhatsappMessageCallback` object if message sent or `True` if integration disabled else `None`
        """
        if (not text and not template) or (text and template):
            logger.warning(
                "Required to pass exactly one parameter: `text` or `template`"
            )
            return None

        if (
            self._settings.APP_MODE != ApplicationMode.PROD
            and not self._settings.WHATSAPP_ENABLE_PROD_INTEGRAION
        ):
            logger.warning("Whatsapp integration disabled, skipping...")
            return True

        logger.info("Sending message to user %s", phone_number)
        logger.debug("Message content: %s", text)

        url = self._settings.WHATSAPP_API_MESSAGES_URL.format(
            url=self._settings.WHATSAPP_API_BASE_URL,
            phone_number_id=phone_number_id,
        )

        body: dict[str, Any] = {
            "messaging_product": MESSAGING_PRODUCT,
            "to": phone_number,
        }

        if text:
            body["text"] = {
                "body": text,
            }

        if template:
            body["type"] = "template"
            body["template"] = {
                "name": template,
                "language": {"code": template_language},
            }

        try:
            result = await self.post(
                url=url,
                json=body,
            )

            return TypeAdapter(WhatsappMessageCallback).validate_python(result)

        except Exception as e:
            logger.error("Failed to send message: %s", e)
            return None

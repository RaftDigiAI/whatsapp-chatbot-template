import logging
from functools import lru_cache
from importlib.metadata import distribution

from shared_lib_template.base_settings import WhatsappBaseSettings


logger = logging.getLogger(__name__)


class Settings(WhatsappBaseSettings):
    """App settings"""

    WHATSAPP_ENABLE_PROD_INTEGRAION: bool = True
    WHATSAPP_WEBHOOK_TOKEN: str
    WHATSAPP_API_TOKEN: str
    WHATSAPP_VALIDATE_SIGNATURE: bool = True
    WHATSAPP_API_RETRY_COUNT: int = 5
    WHATSAPP_API_RETRY_START_TIMEOUT: float = 1
    WHATSAPP_API_VERIFY_SSL: bool = True
    WHATSAPP_API_BASE_URL: str = "https://graph.facebook.com/v19.0"
    WHATSAPP_API_MESSAGES_URL: str = "{url}/{phone_number_id}/messages"
    WHATSAPP_CONCATENATED_MESSAGE_WAITING_SECONDS: int = 30
    WHATSAPP_MESSAGE_PROCESSING_RETRIES: int = 3
    WHATSAPP_MESSAGE_PROCESSING_INTERVAL: int = 3
    WHATSAPP_MESSAGE_PROCESSING_EXPONENTIAL: int = 3


@lru_cache()
def get_settings() -> Settings:
    return Settings(  # type: ignore
        APP_VERSION=distribution("whatsapp-webhook-template").version,
    )

import logging

from fastapi import BackgroundTasks, FastAPI

from backend.api.v1.webhook.models import WhatsappWebhookUpdates
from backend.settings import get_settings
from backend.tasks.message_processing import process_message


logger = logging.getLogger(__name__)


class WhatsappService:
    """Whatsapp webhook processing service"""

    def __init__(self) -> None:
        self._settings = get_settings()

    async def process_updates(
        self,
        app: FastAPI,
        data: WhatsappWebhookUpdates,
        background_tasks: BackgroundTasks,
    ) -> None:
        """Process Whatsapp updates"""

        logger.info("Received webhook from whatsapp")

        background_tasks.add_task(process_message, data, app)

        logger.info("Webhook processed, created background processing task")

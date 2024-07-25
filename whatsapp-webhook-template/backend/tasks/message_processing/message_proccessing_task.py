import asyncio
import logging

from backend.api.v1.webhook.models import WhatsappWebhookUpdates
from backend.core.utils import exponential_backoff
from backend.settings import get_settings
from backend.tasks.message_processing.whatsapp_processing_service import (
    WhatsappMessageProcessingService,
)
from fastapi import FastAPI


logger = logging.getLogger(__name__)


async def process_message(
    data: WhatsappWebhookUpdates,
    app: FastAPI,  # pylint: disable=W0613
) -> None:
    """Process message function"""

    settings = get_settings()

    match data:
        case WhatsappWebhookUpdates():
            message_processing_retries = settings.WHATSAPP_MESSAGE_PROCESSING_RETRIES
            message_processing_interval = settings.WHATSAPP_MESSAGE_PROCESSING_INTERVAL
            message_processing_exponential = (
                settings.WHATSAPP_MESSAGE_PROCESSING_EXPONENTIAL
            )

        case _:
            raise TypeError(
                f"Type `{type(data)}` does not match `WhatsappWebhookUpdates`"
            )

    is_success = False
    attempt = 1
    while attempt <= message_processing_retries:
        try:
            logger.info(
                "Processing message attempt %s out of %s",
                attempt,
                settings.WHATSAPP_MESSAGE_PROCESSING_RETRIES,
            )
            if isinstance(data, WhatsappWebhookUpdates):
                await WhatsappMessageProcessingService(app=app).process_updates(
                    data=data
                )
            else:
                raise TypeError(f"data type `{type(data)}` is not supported")

            is_success = True
            break

        except Exception as e:
            wait_time = exponential_backoff(
                interval=message_processing_interval,
                exponential=message_processing_exponential,
                retry_number=attempt,
            )

            logger.error(
                "An error occured while provessing message, retrying in %ss: %s",
                wait_time,
                e,
            )
            await asyncio.sleep(wait_time)
            attempt += 1

    logger.debug("Processing status: attempts=%s, success=%s", attempt - 1, is_success)

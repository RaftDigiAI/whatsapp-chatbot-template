from pydantic import BaseModel

from backend.api.v1.webhook.models import WhatsappWebhookUpdates


class MessagePendingInfo(BaseModel):
    message_pending_id: int
    entry: WhatsappWebhookUpdates

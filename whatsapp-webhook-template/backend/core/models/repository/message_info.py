from datetime import datetime

from pydantic import BaseModel


class MessageInfo(BaseModel):
    """DB message info"""

    message_id: int
    session_id: int
    received_timestamp: datetime
    replied_timestamp: datetime | None = None
    user_message: str
    bot_message: str | None = None
    gpt_retry_attempts: int | None = None
    concatenated_message_id: int | None = None

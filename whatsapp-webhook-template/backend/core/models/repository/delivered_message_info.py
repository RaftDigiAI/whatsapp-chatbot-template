from pydantic import BaseModel


class DeliveredMessageInfo(BaseModel):
    """Info about message in status `delivered`"""

    user_id: int
    message_status_id: int
    message_id: int

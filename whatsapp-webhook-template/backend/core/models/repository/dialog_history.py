from pydantic import BaseModel


class DialogHistory(BaseModel):
    """Session dialog history entry"""

    user_message: str
    bot_message: str | None = None

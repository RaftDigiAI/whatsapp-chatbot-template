from pydantic import BaseModel


class ProcessEntryCallback(BaseModel):
    """Callback of processing entry"""

    message_ids: list[int]


class MessageProcessingInfo(BaseModel):
    message_id: int
    user_message: str
    concatenated_message_id: int | None = None


class MessageProcessingCallbackInfo(BaseModel):
    """Information about message processing"""

    need_to_stop: bool
    new_message_text: str | None = None
    processing_message_ids_to_clear: list[int]

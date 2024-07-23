from pydantic import BaseModel


class SessionInfo(BaseModel):
    session_id: int
    is_new_session: bool

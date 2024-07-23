from pydantic import BaseModel


class UserInfo(BaseModel):
    """User info"""

    user_id: int
    user_name: str | None = None
    phone_number: str
    phone_number_id: str | None = None

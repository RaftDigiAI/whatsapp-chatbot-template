from pydantic import BaseModel

from backend.api.v1.common_endpoints import constants
from backend.core.models import APIResponse


class AppVersionPayload(BaseModel):
    """App version model"""

    version: str


class AppVersionAPIResponse(APIResponse):
    """App version API response"""

    message: str = constants.APIResponseMessageTemplate.VERSION_INFO
    payload: AppVersionPayload

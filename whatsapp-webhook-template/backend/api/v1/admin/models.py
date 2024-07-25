from backend.api.v1.admin import constants
from backend.core.models import APIResponse


class AppVersionAPIResponse(APIResponse):
    """App version API response"""

    message: str = constants.APIResponseMessageTemplate.ARCHIVE_SESSION

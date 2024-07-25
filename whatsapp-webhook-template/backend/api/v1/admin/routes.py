import logging

from fastapi import APIRouter, Depends, status

from backend.api.v1.admin import examples, models
from backend.api.v1.admin.services.archive_session_service import ArchiveSessionService
from backend.api.v1.auth.services.token_validator import AppTokenValidator
from backend.core.utils import make_response, raise_http_exception


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get(
    "/archive_user_sessions/{phone_number}",
    response_model=models.AppVersionAPIResponse,
    name="admin_get_archive_user_sessions",
    responses={
        400: examples.bad_request_response,
        401: examples.default_unauthorized_example_response,
        403: examples.default_forbidden_example_response,
    },
    dependencies=[
        Depends(AppTokenValidator()),
    ],
)
async def archive_user_sessions(
    phone_number: str,
    service: ArchiveSessionService = Depends(),
):
    """Archive session"""

    is_session_archived = await service.archive_user_sessions(phone_number=phone_number)
    await service.close_conn()

    if not is_session_archived:
        await raise_http_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"No user with phone_number `{phone_number}` exists",
        )

    return await make_response(api_response=models.AppVersionAPIResponse())

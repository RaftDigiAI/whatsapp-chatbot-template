import logging

from fastapi import APIRouter, Depends

from backend.api.v1.auth.services.token_validator import AppTokenValidator
from backend.api.v1.common_endpoints import examples, models
from backend.core.utils import make_response
from backend.settings import Settings, get_settings


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/info",
    tags=["info"],
)
health_check_router = APIRouter(
    tags=["health_check"],
)


@router.get(
    "/version",
    response_model=models.AppVersionAPIResponse,
    name="info_get_app_version",
)
async def get_app_version(settings: Settings = Depends(get_settings)):
    """Get app version"""
    return await make_response(
        api_response=models.AppVersionAPIResponse(
            payload=models.AppVersionPayload(version=settings.APP_VERSION),
        )
    )


@health_check_router.get(
    "/health_check",
    name="common_health_check",
    responses={
        401: examples.default_unauthorized_example_response,
        403: examples.default_forbidden_example_response,
    },
    dependencies=[
        Depends(AppTokenValidator()),
    ],
)
async def health_check():
    """Health check service"""
    return "OK"

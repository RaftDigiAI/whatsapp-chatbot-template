from fastapi import APIRouter

from backend.api.v1.admin.routes import router as admin_router
from backend.api.v1.common_endpoints.routes import health_check_router
from backend.api.v1.common_endpoints.routes import router as info_router
from backend.api.v1.webhook.routes import router as webhook_router


router = APIRouter(prefix="/v1")

router.include_router(admin_router)
router.include_router(info_router)
router.include_router(health_check_router)
router.include_router(webhook_router)

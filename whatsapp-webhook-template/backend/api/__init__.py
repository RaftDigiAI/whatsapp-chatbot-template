from fastapi import APIRouter

from backend.api import v1  # noqa E402


router = APIRouter(prefix="/api")

router.include_router(v1.router)

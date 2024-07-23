import logging
from contextlib import asynccontextmanager
from importlib.metadata import distribution
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from shared_lib_template.db import create_postgres_connection_pool

from backend.config import configure_application


configure_application()

from backend import (  # noqa E402  # pylint: disable=C0413
    api,
    exception_handler,
    settings,
)


logger = logging.getLogger(__name__)

app_settings = settings.get_settings()

fastapi_kwargs: dict[str, Any] = {
    "title": "Whatsapp Chat Bot Webhook API Service",
    "description": "FastAPI app for Whatsapp Webhook API Service",
    "version": distribution("whatsapp-webhook-template").version,
}

if not app_settings.APP_ENABLE_DOCS:
    fastapi_kwargs["docs_url"] = None
    fastapi_kwargs["redoc_url"] = None
    fastapi_kwargs["openapi_url"] = None


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Lifespan FastAPI function"""
    # Events on startup app
    fastapi_app.connection_pool = await create_postgres_connection_pool(settings=app_settings)  # type: ignore
    logger.info("Connection pool established")

    yield

    # Events on shutdown app
    await fastapi_app.connection_pool.close()  # type: ignore
    logger.info("Connection pool closed")


app = FastAPI(lifespan=lifespan, **fastapi_kwargs)  # type: ignore

app.include_router(api.router)

app.exception_handler(HTTPException)(exception_handler.http_exception_handler)
app.exception_handler(Exception)(exception_handler.unexpected_exception_handler)
app.exception_handler(RequestValidationError)(
    exception_handler.unprocessable_entity_handler
)

templates = Jinja2Templates(directory="frontend")


@app.get("/", include_in_schema=False)
async def proxy_app(request: Request):
    """Root App endpoint"""
    return templates.TemplateResponse("index.html", {"request": request})

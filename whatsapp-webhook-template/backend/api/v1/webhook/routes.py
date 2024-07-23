from fastapi import APIRouter, BackgroundTasks, Depends, Header, Query, Request

from backend.api.v1.auth.services import WhatsappTokenValidator
from backend.api.v1.webhook import examples
from backend.api.v1.webhook.models import WhatsappWebhookUpdates
from backend.api.v1.webhook.services import WhatsappService


router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
)


@router.get(
    "/whatsapp",
    name="webhook_get_whatsapp_webhook_health_check",
    responses={
        401: examples.default_unauthorized_example_response,
        403: examples.default_forbidden_example_response,
    },
    dependencies=[
        Depends(WhatsappTokenValidator()),
    ],
)
async def whatsapp_webhook_health_check(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: int = Query(None, alias="hub.challenge"),
    verify_token: str = Query(None, alias="hub.verify_token"),  # pylint: disable=W0613
) -> int:
    """Whatsapp Webhooks service health check"""
    assert (
        hub_mode == "subscribe"
    ), f"Mode parameter is `{hub_mode}`, expected `subscribe`"

    return hub_challenge


@router.post(
    "/whatsapp",
    name="webhook_post_whatsapp_webhook_process",
    responses={
        401: examples.default_unauthorized_example_response,
        403: examples.default_forbidden_example_response,
        500: examples.can_not_access_api_example_response,
    },
    dependencies=[
        Depends(WhatsappTokenValidator()),
    ],
)
async def whatsapp_webhook_process(
    request: Request,
    data: WhatsappWebhookUpdates,
    background_tasks: BackgroundTasks,
    service: WhatsappService = Depends(),
    signature: str = Header(None, alias="x-hub-signature-256"),  # pylint: disable=W0613
):
    """Whatsapp Webhooks service processings"""
    await service.process_updates(
        data=data,
        app=request.app,
        background_tasks=background_tasks,
    )
    return "OK"

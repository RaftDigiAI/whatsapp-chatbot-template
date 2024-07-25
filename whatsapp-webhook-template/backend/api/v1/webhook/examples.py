from backend.api.v1.auth.examples import (  # noqa F401 pylint: disable=W0611
    default_forbidden_example_response,
    default_unauthorized_example_response,
)
from backend.core.constants import HTTPCodesMessage
from backend.core.utils import generate_example_response


_can_not_access_api_example = {
    "summary": "forbidden",
    "value": {
        "status": "error",
        "status_code": 500,
        "message": "Can not access API to send message",
        "payload": None,
    },
}

can_not_access_api_example_response = generate_example_response(
    response_examples=_can_not_access_api_example,
    description=HTTPCodesMessage.HTTP_500_INTERNAL_SERVER_ERROR,
)

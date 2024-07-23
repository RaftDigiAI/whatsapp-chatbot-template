from backend.api.v1.auth.examples import (  # noqa F401 pylint: disable=W0611
    default_forbidden_example_response,
    default_unauthorized_example_response,
)
from backend.core.constants import HTTPCodesMessage
from backend.core.utils import generate_example_response


_bad_request_example = {
    "summary": "forbidden",
    "value": {
        "status": "error",
        "status_code": 403,
        "message": "No user with phone_number `123` exists",
        "payload": None,
    },
}


bad_request_response = generate_example_response(
    response_examples=_bad_request_example,
    description=HTTPCodesMessage.HTTP_400_BAD_REQUEST,
)

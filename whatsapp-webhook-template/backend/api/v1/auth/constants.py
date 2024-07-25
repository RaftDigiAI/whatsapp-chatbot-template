from shared_lib_template.constants.base import AppStringEnum


class APIResponseMessageTemplate(AppStringEnum):
    """Response message template"""

    UNAUTHORIZED = "Credentials are not provided"
    FORBIDDEN = "Provided credentials are not valid"

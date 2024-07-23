from shared_lib_template.constants.base import AppStringEnum


class APIResponseStatus(AppStringEnum):
    """API Response statuses"""

    ERROR = "error"
    SUCCESS = "success"

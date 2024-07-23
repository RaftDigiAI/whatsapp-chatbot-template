from shared_lib_template.constants.base import AppStringEnum


class ApplicationMode(AppStringEnum):
    """App work modes"""

    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"

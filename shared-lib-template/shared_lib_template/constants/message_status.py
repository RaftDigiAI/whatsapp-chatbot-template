from shared_lib_template.constants.base import AppStringEnum


class MessageStatus(AppStringEnum):
    """Message status"""

    PROCESSING = "processing"
    READ = "read"
    DELIVERED = "delivered"
    CONCATENATED = "concatenated"
    OPENED = "opened"
    FAILED_TO_SEND = "failed_to_send"

from shared_lib_template.constants.base import AppStringEnum


class APIResponseMessageTemplate(AppStringEnum):
    """Template messages for API response"""

    VERSION_INFO = "App vesrion"


MESSAGING_PRODUCT = "whatsapp"

ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
OPENAI_ASSISTANT_DATE_FORMAT = "%-d %b %Y"

FIRST_USER_MESSAGE_TEMPLATE = "{message}\n\nTODAY UTC: {date}. Rely on this date!"

CONCATENATED_BOT_MESSAGE_PLACEHOLDER = "Replied in message with id {message_id}"

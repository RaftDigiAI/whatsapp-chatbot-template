from shared_lib_template.constants.base import AppStringEnum


class WhatsappMessageType(AppStringEnum):
    """Whatsapp message type"""

    TEXT = "text"
    REACTION = "reaction"
    IMAGE = "image"
    BUTTON = "button"
    DOCUMENT = "document"
    AUDIO = "audio"
    STICKER = "sticker"
    VIDEO = "video"

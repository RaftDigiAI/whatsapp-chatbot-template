from pydantic import BaseModel, Field

from backend.core.constants import WhatsappMessageType


class WhatsappEntryChangeValueContactProfile(BaseModel):
    name: str


class WhatsappEntryChangeValueContact(BaseModel):
    wa_id: str
    profile: WhatsappEntryChangeValueContactProfile


class WhatsappEntryChangeValueMessageText(BaseModel):
    body: str


class WhatsappEntryChangeValueButton(BaseModel):
    payload: str
    text: str


class WhatsappEntryChangeValueMessage(BaseModel):
    from_: str = Field(..., alias="from")
    id_: str = Field(..., alias="id")
    timestamp: int
    type_: WhatsappMessageType = Field(..., alias="type")
    text: WhatsappEntryChangeValueMessageText | None = None
    button: WhatsappEntryChangeValueButton | None = None


class WhatsappEntryChangeValueMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class WhatsappEntryChangeValueStatus(BaseModel):
    id_: str = Field(..., alias="id")
    status: str
    timestamp: str
    recipient_id: str


class WhatsappEntryChangeValue(BaseModel):
    messaging_product: str
    metadata: WhatsappEntryChangeValueMetadata
    contacts: list[WhatsappEntryChangeValueContact] = []
    messages: list[WhatsappEntryChangeValueMessage] = []
    statuses: list[WhatsappEntryChangeValueStatus] = []


class WhatsappEntryChange(BaseModel):
    field: str
    value: WhatsappEntryChangeValue


class WhatsappEntry(BaseModel):
    """Whatsapp webhook entry"""

    id_: str = Field(..., alias="id")
    changes: list[WhatsappEntryChange] = []


class WhatsappWebhookUpdates(BaseModel):
    object_: str = Field(..., alias="object")
    entry: list[WhatsappEntry] = []


class WhatsappMessageCallbackContact(BaseModel):
    input: str
    wa_id: str


class WhatsappMessageCallbackMessage(BaseModel):
    id_: str = Field(..., alias="id")


class WhatsappMessageCallback(BaseModel):
    """Whatsapp send message callback"""

    messaging_product: str
    contacts: list[WhatsappMessageCallbackContact]
    messages: list[WhatsappMessageCallbackMessage]


class EntryMessageBase(BaseModel):
    """Base attributes for entry"""

    text: str
    user_name: str
    phone_number: str
    wa_message_id: str
    timestamp: int


class WhatsappEntryMessageInfo(EntryMessageBase):
    """Whatsapp message metadata"""

    phone_number_id: str
    type_: WhatsappMessageType

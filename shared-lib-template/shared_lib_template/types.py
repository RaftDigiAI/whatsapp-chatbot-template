from typing import Any, TypeVar

from shared_lib_template.base_settings import WhatsappBaseSettings


HeadersType = dict[str, Any]
JsonType = dict[str, Any]
RetryStatusesType = set[int]
TypeBaseSettings = TypeVar("TypeBaseSettings", bound=WhatsappBaseSettings)

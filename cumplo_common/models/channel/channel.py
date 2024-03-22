from abc import ABC

from pydantic import Field

from cumplo_common.models.base_model import BaseModel, StrEnum
from cumplo_common.models.template import Event


class ChannelType(StrEnum):
    WHATSAPP = "WHATSAPP"
    WEBHOOK = "WEBHOOK"
    IFTTT = "IFTTT"


class ChannelMetadata(BaseModel, ABC):
    """Base class for channel metadata"""


class ChannelConfiguration(BaseModel, ABC):
    """Base class for channel configuration"""

    type_: ChannelType = Field(...)
    enabled: bool = Field(True)
    events: list[Event] = Field(default_factory=list)
    metadata: ChannelMetadata

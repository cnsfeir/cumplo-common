from abc import ABC

import ulid
from pydantic import Field, field_validator

from cumplo_common.models.base_model import BaseModel, StrEnum
from cumplo_common.models.template import Template


class ChannelType(StrEnum):
    WHATSAPP = "WHATSAPP"
    WEBHOOK = "WEBHOOK"
    IFTTT = "IFTTT"


class ChannelMetadata(BaseModel, ABC):
    """Base class for channel metadata"""


class ChannelConfiguration(BaseModel, ABC):
    """Base class for channel configuration"""

    id: ulid.ULID = Field(...)
    enabled: bool = Field(True)
    type_: ChannelType = Field(...)
    events: list[Template] = Field(default_factory=list)
    metadata: ChannelMetadata

    @field_validator("id", mode="before")
    @classmethod
    def _format_id(cls, value: ulid.default.api.ULIDPrimitive) -> ulid.ULID:
        """Formats the ID field as an ULID object"""
        return ulid.parse(value)

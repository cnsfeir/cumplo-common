import ipaddress
import re
from abc import ABC
from typing import Literal
from urllib.parse import urlparse

import ulid
from pydantic import Field, field_validator

from cumplo_common.utils.constants import PHONE_NUMBER_REGEX

from .base_model import BaseModel
from .template import Template
from .utils import StrEnum


class ChannelType(StrEnum):
    WHATSAPP = "WHATSAPP"
    WEBHOOK = "WEBHOOK"
    IFTTT = "IFTTT"


class ChannelConfiguration(BaseModel, ABC):
    """Base class for channel configuration."""

    id: ulid.ULID = Field(...)
    enabled: bool = Field(True)
    type_: ChannelType = Field(...)
    events: list[Template] = Field(default_factory=list)

    @field_validator("id", mode="before")
    @classmethod
    def _format_id(cls, value: ulid.default.api.ULIDPrimitive) -> ulid.ULID:
        """Format the ID field as an ULID object."""
        return ulid.parse(value)


class IFTTTConfiguration(ChannelConfiguration):
    type_: Literal[ChannelType.IFTTT] = ChannelType.IFTTT
    key: str = Field(...)
    event: str = Field(...)

    @field_validator("key", mode="before")
    @classmethod
    def _validate_key(cls, value: str) -> str:
        """Validate that the IFTTT webhook key is alphanumeric."""
        if not value.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Webhook key must be alphanumeric")
        return value

    @field_validator("event", mode="before")
    @classmethod
    def _validate_event(cls, value: str) -> str:
        """Validate that the IFTTT event name is alphanumeric."""
        if not value.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Event name must be alphanumeric")
        return value


class WebhookConfiguration(ChannelConfiguration):
    type_: Literal[ChannelType.WEBHOOK] = ChannelType.WEBHOOK
    url: str = Field(..., max_length=2000)

    @field_validator("url", mode="before")
    @classmethod
    def _validate_url(cls, value: str) -> str:
        """Validate the URL scheme and hostname."""
        url = urlparse(value)

        if url.scheme != "https":
            raise ValueError("Only HTTPS URLs are allowed")

        if not url.hostname:
            raise ValueError("URL must have a hostname")

        try:
            ip = ipaddress.ip_address(url.hostname)
        except ValueError:
            pass  # NOTE: Hostname is not an IP address, which is fine
        else:
            if ip.is_private:
                raise ValueError("Private IP addresses are not allowed")

        return value


class WhatsappConfiguration(ChannelConfiguration):
    type_: Literal[ChannelType.WHATSAPP] = ChannelType.WHATSAPP
    phone_number: str = Field(...)

    @field_validator("phone_number", mode="before")
    @classmethod
    def _validate_phone_number(cls, value: str) -> str:
        """Validate the phone number conforms to the E.164 format."""
        if not re.match(PHONE_NUMBER_REGEX, value):
            raise ValueError("Invalid phone number format")
        return value


CHANNEL_CONFIGURATION_BY_TYPE: dict[ChannelType, type[ChannelConfiguration]] = {
    ChannelType.WHATSAPP: WhatsappConfiguration,
    ChannelType.WEBHOOK: WebhookConfiguration,
    ChannelType.IFTTT: IFTTTConfiguration,
}

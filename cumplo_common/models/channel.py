import ipaddress
import re
from abc import ABC
from typing import Literal, Self
from urllib.parse import urlparse

import ulid
from pydantic import Field, field_validator, model_validator

from cumplo_common.utils.constants import PHONE_NUMBER_REGEX

from .base_model import BaseModel
from .event import Event
from .utils import StrEnum

ALL_EVENTS = "all"
ALL_EVENTS_TYPE = Literal["all"]


class ChannelType(StrEnum):
    WHATSAPP = "WHATSAPP"
    WEBHOOK = "WEBHOOK"
    IFTTT = "IFTTT"


class ChannelConfiguration(BaseModel, ABC):
    """Base class for channel configuration."""

    id: ulid.ULID = Field(...)
    enabled: bool = Field(True)
    type_: ChannelType = Field(...)
    enabled_events: set[Event] | ALL_EVENTS_TYPE = Field(ALL_EVENTS)
    disabled_events: set[Event] = Field(default_factory=set)

    @field_validator("id", mode="before")
    @classmethod
    def _format_id(cls, value: ulid.default.api.ULIDPrimitive) -> ulid.ULID:
        """Format the ID field as an ULID object."""
        return ulid.parse(value)

    @model_validator(mode="after")
    def _validate_events_lists(self) -> Self:
        """Validate the events lists."""
        if not self.enabled_events and not self.disabled_events:
            raise ValueError("At least one of enabled_events or disabled_events must not be empty")

        if self.disabled_events and self.enabled_events != ALL_EVENTS:
            raise ValueError("Can't use disabled_events when enabled_events is not 'all'")

        return self

    def event_enabled(self, event: Event) -> bool:
        """Check if the event is enabled."""
        if self.enabled_events == ALL_EVENTS and event not in self.disabled_events:
            return True
        return event in self.enabled_events


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


class WebhookConfiguration(ChannelConfiguration):
    enabled_events: set[Event] | ALL_EVENTS_TYPE = Field(default_factory=set)
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


CHANNEL_CONFIGURATION_BY_TYPE: dict[ChannelType, type[ChannelConfiguration]] = {
    ChannelType.WHATSAPP: WhatsappConfiguration,
    ChannelType.WEBHOOK: WebhookConfiguration,
    ChannelType.IFTTT: IFTTTConfiguration,
}

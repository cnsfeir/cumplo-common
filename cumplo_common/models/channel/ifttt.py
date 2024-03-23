from pydantic import Field, field_validator

from cumplo_common.models.channel.channel import ChannelConfiguration, ChannelType


class IFTTTConfiguration(ChannelConfiguration):
    type_: ChannelType = ChannelType.IFTTT
    key: str = Field(...)
    event: str = Field(...)

    @field_validator("key", mode="before")
    @classmethod
    def _validate_key(cls, value: str) -> str:
        """
        Validates that the IFTTT webhook key is alphanumeric
        """
        if not value.isalnum():
            raise ValueError("Webhook key must be alphanumeric")
        return value

    @field_validator("event", mode="before")
    @classmethod
    def _validate_event(cls, value: str) -> str:
        """
        Validates that the IFTTT event name is alphanumeric
        """
        if not value.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Event name must be alphanumeric")
        return value

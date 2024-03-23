import re

from pydantic import Field, field_validator

from cumplo_common.models.channel.channel import ChannelConfiguration, ChannelType
from cumplo_common.utils.constants import PHONE_NUMBER_REGEX


class WhatsappConfiguration(ChannelConfiguration):
    type_: ChannelType = ChannelType.WHATSAPP
    phone_number: str = Field(...)

    @field_validator("phone_number", mode="before")
    @classmethod
    def _validate_phone_number(cls, value: str) -> str:
        """
        Validates the phone number conforms to the E.164 format
        """
        if not re.match(PHONE_NUMBER_REGEX, value):
            raise ValueError("Invalid phone number format")
        return value

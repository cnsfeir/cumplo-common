# mypy: disable-error-code="misc, call-overload"

from collections.abc import Callable
from functools import cached_property

import ulid
from pydantic import Field, PositiveInt, field_validator

from cumplo_common.utils.constants import DEFAULT_EXPIRATION_MINUTES

from .base_model import BaseModel
from .channel import ChannelConfiguration
from .credentials import Credentials
from .filter_configuration import FilterConfiguration
from .notification import Notification
from .pydantic import ValidatorMode


class User(BaseModel):
    id: ulid.ULID = Field(...)
    api_key: str = Field(...)
    is_admin: bool = Field(False)
    name: str = Field(..., max_length=30)
    credentials: Credentials = Field(...)
    expiration_minutes: PositiveInt = Field(DEFAULT_EXPIRATION_MINUTES)

    notifications_query: Callable[[str], dict[str, Notification]] = Field(..., exclude=True)
    filters_query: Callable[[str], dict[str, FilterConfiguration]] = Field(..., exclude=True)
    channels_query: Callable[[str], dict[str, ChannelConfiguration]] = Field(..., exclude=True)

    @field_validator("id", mode=ValidatorMode.BEFORE)
    @classmethod
    def _format_id(cls, value: str) -> ulid.ULID:
        """Format the ID field as an ULID object."""
        return ulid.parse(value)

    @cached_property
    def filters(self) -> dict[str, FilterConfiguration]:
        """
        Returns the user filters.

        Returns:
            dict[str, FilterConfiguration]: A dictionary of filters

        """
        return self.filters_query(str(self.id))

    @cached_property
    def notifications(self) -> dict[str, Notification]:
        """
        Returns the user notifications.

        Returns:
            dict[str, Notification]: A dictionary of notifications

        """
        return self.notifications_query(str(self.id))

    @cached_property
    def channels(self) -> dict[str, ChannelConfiguration]:
        """
        Returns the user channels.

        Returns:
            dict[str, ChannelConfiguration]: A dictionary of channels

        """
        return self.channels_query(str(self.id))

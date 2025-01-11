# mypy: disable-error-code="misc, call-overload"


import ulid
from pydantic import Field, PositiveInt, field_validator

from cumplo_common.utils.constants import DEFAULT_EXPIRATION_MINUTES

from .base_model import BaseModel
from .channel import ChannelConfigurationType
from .credentials import Credentials
from .event_public import PublicEvent
from .filter_configuration import FilterConfiguration
from .notification import Notification
from .utils import EventModel


class User(BaseModel):
    id: ulid.ULID = Field(...)
    api_key: str = Field(...)
    is_admin: bool = Field(False)
    name: str = Field(..., max_length=30)
    credentials: Credentials = Field(...)
    expiration_minutes: PositiveInt = Field(DEFAULT_EXPIRATION_MINUTES)

    notifications: dict[str, Notification] = Field(default_factory=dict)
    filters: dict[str, FilterConfiguration] = Field(default_factory=dict)
    channels: dict[str, ChannelConfigurationType] = Field(default_factory=dict)

    @field_validator("id", mode="before")
    @classmethod
    def _format_id(cls, value: str) -> ulid.ULID:
        """Format the ID field as an ULID object."""
        return ulid.parse(value)

    def already_notified(self, event: PublicEvent, content: EventModel) -> bool:
        """
        Check if the given user has already been notified with the given event and content.

        Args:
            user (User): The user who's being notified
            event (Event): The event used to notify the user
            content (SubjectContent): The content of the notification

        Returns:
            bool: Whether the user has already been notified with the given event and content

        """
        if not event.is_recurring:
            return False

        id_notification = Notification.build_id(event, content.id)
        if not (notification := self.notifications.get(id_notification)):
            return False

        return notification.has_expired

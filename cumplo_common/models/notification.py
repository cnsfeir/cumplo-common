from datetime import datetime
from re import fullmatch
from typing import Self

import arrow
from pydantic import Field, model_validator

from cumplo_common.utils.constants import DEFAULT_EXPIRATION_MINUTES

from .base_model import BaseModel
from .event import Event


class Notification(BaseModel):
    id: str = Field(...)
    event: Event = Field(...)
    date: datetime = Field(...)
    content_id: int = Field(...)
    expiration_minutes: int = Field(DEFAULT_EXPIRATION_MINUTES)

    @model_validator(mode="before")
    @classmethod
    def format_data(cls, values: dict) -> dict:
        """Format the data before validation."""
        return cls._process_id(values)

    @classmethod
    def new(cls, event: Event, content_id: int) -> Self:
        """Create a new notification."""
        return cls.model_validate({
            "date": arrow.utcnow().datetime,
            "id": cls.build_id(event, content_id),
        })

    @staticmethod
    def _process_id(values: dict) -> dict:
        """Separate the actual ID and the event from the ID field."""
        if not (id_ := values.get("id")):
            return values

        if not fullmatch(r"^[a-zA-Z_]+\.[a-zA-Z_]+-\d+$", id_):
            raise ValueError("Invalid ID format")

        values["event"], values["content_id"] = id_.split("-")
        return values

    @property
    def has_expired(self) -> bool:
        """
        Check if the notification has expired.

        Args:
            expiration_minutes (int): Minutes until the notification expires

        Returns:
            bool: Whether the notification has expired or not

        """
        return arrow.get(self.date).shift(minutes=self.expiration_minutes) > arrow.utcnow()

    @staticmethod
    def build_id(event: Event, content_id: int) -> str:
        """
        Build the ID for a notification.

        Args:
            event (Event): Notification event
            content_id (int): Notification content ID

        Returns:
            str: Notification ID

        """
        return f"{event.value}-{content_id}"

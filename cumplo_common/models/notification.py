# mypy: disable-error-code="call-overload"
# pylint: disable=no-member

from datetime import datetime
from re import fullmatch

import arrow
from pydantic import Field, model_validator

from cumplo_common.models.base_model import BaseModel
from cumplo_common.models.event import Event
from cumplo_common.utils.constants import DEFAULT_EXPIRATION_MINUTES


class Notification(BaseModel):
    id: str = Field(...)
    date: datetime = Field(...)
    content_id: int = Field(...)
    event: Event = Field(...)
    expiration_minutes: int = Field(DEFAULT_EXPIRATION_MINUTES)

    @model_validator(mode="before")
    @classmethod
    def format_data(cls, values: dict) -> dict:
        """Formats the data before validation"""
        values = cls._process_id(values)
        return values

    @staticmethod
    def _process_id(values: dict) -> dict:
        """
        Separates the actual ID and the event from the ID field
        """
        if not (id_ := values.get("id")):
            return values

        if not fullmatch(r"^[a-zA-Z_]+\.[a-zA-Z_]+-\d+$", id_):
            raise ValueError("Invalid ID format")

        values["event"], values["content_id"] = id_.split("-")
        return values

    @property
    def has_expired(self) -> bool:
        """
        Checks if the notification has expired

        Args:
            expiration_minutes (int): Minutes until the notification expires

        Returns:
            bool: Whether the notification has expired or not
        """
        return arrow.get(self.date).shift(minutes=self.expiration_minutes) > arrow.utcnow()

    @staticmethod
    def build_id(event: Event, content_id: int) -> str:
        """
        Builds the ID for a notification

        Args:
            event (Event): Notification event
            content_id (int): Notification content ID

        Returns:
            str: Notification ID
        """
        return f"{event.value}-{content_id}"

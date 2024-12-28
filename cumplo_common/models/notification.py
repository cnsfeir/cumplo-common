# mypy: disable-error-code="call-overload"

from datetime import datetime
from re import fullmatch

import arrow
from pydantic import Field, model_validator

from cumplo_common.utils.constants import DEFAULT_EXPIRATION_MINUTES

from .base_model import BaseModel
from .pydantic import ValidatorMode
from .template import Template


class Notification(BaseModel):
    id: str = Field(...)
    date: datetime = Field(...)
    content_id: int = Field(...)
    template: Template = Field(...)
    expiration_minutes: int = Field(DEFAULT_EXPIRATION_MINUTES)

    @model_validator(mode="before")
    @classmethod
    def format_data(cls, values: dict) -> dict:
        """Format the data before validation."""
        return cls._process_id(values)

    @staticmethod
    def _process_id(values: dict) -> dict:
        """Separate the actual ID and the template from the ID field."""
        if not (id_ := values.get("id")):
            return values

        if not fullmatch(r"^[a-zA-Z]+_\d+$", id_):
            raise ValueError("Invalid ID format")

        values["template"], values["content_id"] = id_.split("_")
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
    def build_id(template: Template, content_id: int) -> str:
        """
        Build the ID for a notification.

        Args:
            template (Template): Notification template
            content_id (int): Notification content ID

        Returns:
            str: Notification ID

        """
        return f"{template.value}_{content_id}"

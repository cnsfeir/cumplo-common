# mypy: disable-error-code="call-overload"
# pylint: disable=no-member

from datetime import datetime
from re import fullmatch

import arrow
from pydantic import Field, model_validator

from cumplo_common.models import BaseModel
from cumplo_common.models.pydantic import ValidatorMode
from cumplo_common.models.template import Template
from cumplo_common.utils.constants import DEFAULT_EXPIRATION_MINUTES


class Notification(BaseModel):
    id: str = Field(...)
    date: datetime = Field(...)
    content_id: int = Field(...)
    template: Template = Field(...)
    expiration_minutes: int = Field(DEFAULT_EXPIRATION_MINUTES)

    @model_validator(mode=ValidatorMode.BEFORE)
    @classmethod
    def format_data(cls, values: dict) -> dict:
        """Formats the data before validation"""
        values = cls._process_id(values)
        return values

    @staticmethod
    def _process_id(values: dict) -> dict:
        """
        Separates the actual ID and the template from the ID field
        """
        if not (id_ := values.get("id")):
            return values

        if not fullmatch(r"^[a-zA-Z]+_\d+$", id_):
            raise ValueError("Invalid ID format")

        values["template"], values["content_id"] = id_.lower().split("_")
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
        return arrow.get(self.date).shift(minutes=self.expiration_minutes) < arrow.utcnow()

    @staticmethod
    def build_id(template: Template, content_id: int) -> str:
        """
        Builds the ID for a notification

        Args:
            template (Template): Notification template
            content_id (int): Notification content ID

        Returns:
            str: Notification ID
        """
        return f"{template.value}_{content_id}"

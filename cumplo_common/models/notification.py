# pylint: disable=no-member

from datetime import datetime

import arrow
from pydantic import Field

from cumplo_common.models import BaseModel


class Notification(BaseModel):
    id: int = Field(...)
    date: datetime = Field(...)

    def has_expired(self, expiration_minutes: int) -> bool:
        """
        Checks if the notification has expired

        Args:
            expiration_minutes (int): Minutes until the notification expires

        Returns:
            bool: Whether the notification has expired or not
        """
        return arrow.get(self.date).shift(minutes=expiration_minutes) < arrow.utcnow()

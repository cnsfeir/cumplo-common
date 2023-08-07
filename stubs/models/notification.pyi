# pylint: disable=unused-import, missing-function-docstring, unused-argument
# flake8: noqa: F401

from datetime import datetime

from pydantic import BaseModel

class Notification(BaseModel):
    id: int
    date: datetime
    def has_expired(self, expiration_minutes: int) -> bool: ...

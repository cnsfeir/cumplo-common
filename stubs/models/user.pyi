# pylint: disable=unused-import, missing-function-docstring, unused-argument
# flake8: noqa: F401

from pydantic import BaseModel

from cumplo_common.models.configuration import Configuration
from cumplo_common.models.notification import Notification

class User(BaseModel):
    id: str
    name: str
    is_admin: bool
    webhook_url: str | None
    notifications: dict[int, Notification]
    configurations: dict[int, Configuration]

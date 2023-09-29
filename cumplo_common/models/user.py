# pylint: disable=no-member

from pydantic import Field, PositiveInt
import ulid

from cumplo_common.models import BaseModel
from cumplo_common.models.channel import ChannelConfiguration, ChannelType
from cumplo_common.models.credentials import Credentials
from cumplo_common.models.filter import FilterConfiguration
from cumplo_common.models.notification import Notification
from cumplo_common.utils.constants import DEFAULT_EXPIRATION_MINUTES


class User(BaseModel):
    id: ulid.ULID = Field(...)
    api_key: str = Field(...)
    is_admin: bool = Field(False)
    name: str = Field(..., max_length=30)
    credentials: Credentials = Field(...)
    expiration_minutes: PositiveInt = Field(DEFAULT_EXPIRATION_MINUTES)
    filters: dict[int, FilterConfiguration] = Field(default_factory=dict, exclude=True)
    notifications: dict[str, Notification] = Field(default_factory=dict, exclude=True)
    channels: dict[ChannelType, ChannelConfiguration] = Field(default_factory=dict, exclude=True)

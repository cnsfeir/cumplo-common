# pylint: disable=no-member

from pydantic import Field

from cumplo_common.models import BaseModel


class Credentials(BaseModel):
    id: int = Field(...)
    email: str = Field(...)
    password: str = Field(...)

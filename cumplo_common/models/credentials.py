# pylint: disable=no-member

from pydantic import Field

from cumplo_common.models.base_model import BaseModel


class Credentials(BaseModel):
    id: int = Field(...)
    email: str = Field(...)
    password: str = Field(...)

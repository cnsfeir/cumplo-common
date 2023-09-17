# pylint: disable=no-member

from pydantic import BaseModel, Field


class Credentials(BaseModel):
    id: int = Field(...)
    email: str = Field(...)
    password: str = Field(...)

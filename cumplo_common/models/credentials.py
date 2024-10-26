from pydantic import Field

from .base_model import BaseModel


class Credentials(BaseModel):
    id: int = Field(...)
    email: str = Field(...)
    password: str = Field(...)

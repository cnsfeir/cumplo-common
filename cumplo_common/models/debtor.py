# mypy: disable-error-code="misc"

from datetime import datetime
from decimal import Decimal

from pydantic import Field

from cumplo_common.models.base_model import BaseModel


class DebtPortfolio(BaseModel):
    active: int = Field(...)
    delinquent: int = Field(...)
    completed: int = Field(...)
    in_time: int = Field(...)
    total_amount: int = Field(...)
    total_requests: int = Field(...)


class Debtor(BaseModel):
    amount: int = Field(...)
    share: Decimal = Field(...)
    name: str | None = Field(None)
    sector: str | None = Field(None)
    portfolio: DebtPortfolio = Field(...)
    description: str | None = Field(None)
    first_appearance: datetime = Field(...)
    dicom: bool | None = Field(None)

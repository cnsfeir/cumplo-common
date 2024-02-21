# mypy: disable-error-code="misc"

from datetime import datetime
from decimal import Decimal
from functools import cached_property

from pydantic import Field, computed_field

from cumplo_common.models.base_model import BaseModel
from cumplo_common.utils.constants import DICOM_STRINGS


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
    description: str | None = Field(...)
    first_appearance: datetime = Field(...)

    @computed_field
    @cached_property
    def dicom(self) -> bool | None:
        """Returns True if the borrower is in DICOM"""
        return any(string in self.description for string in DICOM_STRINGS) if self.description else None

# mypy: disable-error-code="misc, call-overload"

from datetime import datetime
from decimal import Decimal
from functools import cached_property

from pydantic import ConfigDict, Field, computed_field

from cumplo_common.models.base_model import BaseModel
from cumplo_common.utils.constants import DICOM_STRINGS


class BorrowerPortfolio(BaseModel):
    active: int = Field(...)
    completed: int = Field(...)
    total_amount: int = Field(...)
    total_requests: int = Field(...)
    in_time: Decimal = Field(...)
    cured: Decimal = Field(...)
    delinquent: Decimal = Field(...)
    outstanding: Decimal = Field(...)


class Borrower(BaseModel):
    model_config = ConfigDict(str_to_upper=True)

    id: int | None = Field(None)
    name: str | None = Field(None)
    sector: str | None = Field(None)
    description: str | None = Field(None)
    first_appearance: datetime = Field(...)
    average_days_delinquent: int | None = Field(None)
    portfolio: BorrowerPortfolio = Field(...)

    @computed_field
    @cached_property
    def dicom(self) -> bool | None:
        """Returns True if the borrower is in DICOM"""
        return any(string in self.description for string in DICOM_STRINGS) if self.description else None

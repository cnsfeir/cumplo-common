# mypy: disable-error-code="misc, call-overload"

from datetime import datetime
from decimal import Decimal
from functools import cached_property

from pydantic import Field

from cumplo_common.models.base_model import BaseModel


class BorrowerPortfolio(BaseModel):
    active: int = Field(...)
    completed: int = Field(...)
    total_amount: int = Field(...)
    total_requests: int = Field(...)

    # NOTE: The following fields are based on the total requests and should add up to 100%
    in_time: Decimal = Field(...)
    cured: Decimal = Field(...)
    delinquent: Decimal = Field(...)
    outstanding: Decimal = Field(...)

    @cached_property
    def paid_in_time(self) -> Decimal | None:
        """The percentage of paid in time based on the total paid funding requests."""
        if not (self.total_requests and self.completed):
            return None
        return min(round(Decimal(self.in_time * self.total_requests / self.completed), 3), Decimal(1))


class Borrower(BaseModel):
    id: int | None = Field(None)
    name: str | None = Field(None)
    economic_sector: str | None = Field(None)
    description: str | None = Field(None)
    first_appearance: datetime = Field(...)
    average_days_delinquent: int | None = Field(None)
    portfolio: BorrowerPortfolio = Field(...)
    dicom: bool | None = Field(None)

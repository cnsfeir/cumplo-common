# mypy: disable-error-code="misc"

from datetime import datetime
from decimal import Decimal
from functools import cached_property

from pydantic import Field

from cumplo_common.models.base_model import BaseModel


class DebtPortfolio(BaseModel):
    active: int = Field(...)
    delinquent: int = Field(...)
    completed: int = Field(...)
    in_time: int = Field(...)
    total_requests: int = Field(...)

    @cached_property
    def paid_in_time(self) -> Decimal | None:
        """
        The percentage of paid in time based on the total paid funding requests
        """
        if not (self.total_requests and self.completed):
            return None
        return min(round(Decimal(self.in_time / self.completed), 3), Decimal(1))


class Debtor(BaseModel):
    share: Decimal = Field(...)
    name: str | None = Field(None)
    sector: str | None = Field(None)
    portfolio: DebtPortfolio = Field(...)
    description: str | None = Field(None)
    first_appearance: datetime = Field(...)
    dicom: bool | None = Field(None)

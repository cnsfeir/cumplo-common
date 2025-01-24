# mypy: disable-error-code="misc, call-overload"

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from functools import cached_property

from pydantic import Field, computed_field

from .base_model import BaseModel


class BorrowerPortfolioStatus(StrEnum):
    PAID = "paid"
    TOTAL = "total"
    CURED = "cured"
    ACTIVE = "active"
    OVERDUE = "overdue"
    ON_TIME = "on_time"
    DELINQUENT = "delinquent"
    OUTSTANDING = "outstanding"


class BorrowerPortfolioUnit(BaseModel):
    percentage: Decimal = Field(...)
    amount: Decimal = Field(...)
    count: int = Field(...)


class BorrowerPortfolio(BaseModel):
    cured: BorrowerPortfolioUnit = Field(...)
    active: BorrowerPortfolioUnit = Field(...)
    overdue: BorrowerPortfolioUnit = Field(...)
    on_time: BorrowerPortfolioUnit = Field(...)
    delinquent: BorrowerPortfolioUnit = Field(...)

    @computed_field
    @cached_property
    def total(self) -> BorrowerPortfolioUnit:
        """Total is the sum of outstanding and paid."""
        return BorrowerPortfolioUnit(
            percentage=Decimal(1),
            amount=self.outstanding.amount + self.paid.amount,
            count=self.outstanding.count + self.paid.count,
        )

    @computed_field
    @cached_property
    def outstanding(self) -> BorrowerPortfolioUnit:
        """Outstanding is the sum of active, overdue and delinquent."""
        return BorrowerPortfolioUnit(
            percentage=self.active.percentage + self.overdue.percentage + self.delinquent.percentage,
            amount=self.active.amount + self.overdue.amount + self.delinquent.amount,
            count=self.active.count + self.overdue.count + self.delinquent.count,
        )

    @computed_field
    @cached_property
    def paid(self) -> BorrowerPortfolioUnit:
        """Paid is the sum of credits paid on time and cured."""
        return BorrowerPortfolioUnit(
            percentage=self.on_time.percentage + self.cured.percentage,
            amount=self.on_time.amount + self.cured.amount,
            count=self.on_time.count + self.cured.count,
        )


class Borrower(BaseModel):
    id: int | None = Field(None)
    name: str | None = Field(None)
    economic_sector: str | None = Field(None)
    description: str | None = Field(None)
    first_appearance: datetime | None = Field(None)
    average_days_delinquent: int | None = Field(None)
    portfolio: BorrowerPortfolio = Field(...)
    dicom: bool | None = Field(None)

from decimal import Decimal
from enum import StrEnum
from functools import cached_property

from pydantic import Field, computed_field

from .base_model import BaseModel


class PortfolioStatus(StrEnum):
    PAID = "paid"
    TOTAL = "total"
    CURED = "cured"
    ACTIVE = "active"
    OVERDUE = "overdue"
    ON_TIME = "on_time"
    DELINQUENT = "delinquent"
    OUTSTANDING = "outstanding"


class PortfolioUnit(BaseModel):
    percentage: Decimal = Field(...)
    amount: Decimal = Field(...)
    count: int = Field(...)


class Portfolio(BaseModel):
    cured: PortfolioUnit = Field(...)
    active: PortfolioUnit = Field(...)
    overdue: PortfolioUnit = Field(...)
    on_time: PortfolioUnit = Field(...)
    delinquent: PortfolioUnit = Field(...)

    @computed_field  # type: ignore[misc]
    @cached_property
    def total(self) -> PortfolioUnit:
        """Total is the sum of outstanding and paid."""
        return PortfolioUnit(
            percentage=Decimal(1),
            amount=self.outstanding.amount + self.paid.amount,
            count=self.outstanding.count + self.paid.count,
        )

    @computed_field  # type: ignore[misc]
    @cached_property
    def outstanding(self) -> PortfolioUnit:
        """Outstanding is the sum of active, overdue and delinquent."""
        return PortfolioUnit(
            percentage=self.active.percentage + self.overdue.percentage + self.delinquent.percentage,
            amount=self.active.amount + self.overdue.amount + self.delinquent.amount,
            count=self.active.count + self.overdue.count + self.delinquent.count,
        )

    @computed_field  # type: ignore[misc]
    @cached_property
    def paid(self) -> PortfolioUnit:
        """Paid is the sum of credits paid on time and cured."""
        return PortfolioUnit(
            percentage=self.on_time.percentage + self.cured.percentage,
            amount=self.on_time.amount + self.cured.amount,
            count=self.on_time.count + self.cured.count,
        )

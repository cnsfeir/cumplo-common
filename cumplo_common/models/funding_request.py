# pylint: disable=no-member
# mypy: disable-error-code="misc, override"

from decimal import Decimal
from functools import cached_property
from math import ceil

from pydantic import Field, computed_field

from cumplo_common.models.base_model import BaseModel, StrEnum
from cumplo_common.models.borrower import Borrower
from cumplo_common.models.credit import CreditType
from cumplo_common.models.currency import Currency
from cumplo_common.models.debtor import Debtor
from cumplo_common.models.simulation import Simulation
from cumplo_common.utils.constants import CUMPLO_BASE_URL


class DurationUnit(StrEnum):
    MONTH = "MONTH"
    DAY = "DAY"


class Duration(BaseModel):
    unit: DurationUnit = Field(...)
    value: int = Field(...)

    def __str__(self) -> str:
        return f"{self.value} {self.unit.lower()}s"


class FundingRequest(BaseModel):
    id: int = Field(...)
    amount: int = Field(...)
    irr: Decimal = Field(...)
    score: Decimal = Field(...)
    installments: int = Field(...)
    due_date: str = Field(...)
    raised_amount: int = Field(...)
    maximum_investment: int = Field(...)
    investors: int = Field(...)
    funded_percentage: Decimal = Field(...)
    supporting_documents: list[str] = Field(default_factory=list)

    debtors: list[Debtor] = Field(default_factory=list)
    credit_type: CreditType = Field(...)
    simulation: Simulation = Field(...)
    duration: Duration = Field(...)
    borrower: Borrower = Field(...)
    currency: Currency = Field(...)

    @cached_property
    @computed_field
    def profit_rate(self) -> Decimal:
        """Calculates the profit rate for the funding request"""
        if self.installments > 1:
            value = self.simulation.profit_rate
        else:
            value = (1 + self.irr / 100) ** Decimal(self.duration.value / 365) - 1
        return round(Decimal(value), ndigits=4)

    @cached_property
    @computed_field
    def monthly_profit_rate(self) -> Decimal:
        """Calculates the monthly profit rate for the funding request"""
        value = (1 + self.irr / 100) ** Decimal(1 / 12) - 1
        return round(Decimal(value), ndigits=4)

    @cached_property
    @computed_field
    def is_completed(self) -> bool:
        """Checks if the funding request is fully funded"""
        return self.funded_percentage == Decimal(1)

    @cached_property
    @computed_field
    def url(self) -> str:
        """Builds the URL for the funding request"""
        return f"{CUMPLO_BASE_URL}/{self.id}"

    def monthly_profit(self, amount: int) -> int:
        """
        Calculates the monthly profit for a given amount

        Args:
            amount (int): The amount to calculate the profit for

        Returns:
            int: The monthly profit for the given amount
        """
        return ceil(self.monthly_profit_rate * amount)

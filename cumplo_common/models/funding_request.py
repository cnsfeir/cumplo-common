# pylint: disable=no-member
# mypy: disable-error-code="misc"

from decimal import Decimal
from functools import cached_property
from math import ceil

from pydantic import Field, computed_field

from cumplo_common.models.base_model import BaseModel, StrEnum
from cumplo_common.models.borrower import Borrower
from cumplo_common.models.credit import CreditType
from cumplo_common.models.currency import Currency
from cumplo_common.utils.constants import CUMPLO_BASE_URL


class DurationUnit(StrEnum):
    MONTH = "MONTH"
    DAY = "DAY"


class FundingRequestDuration(BaseModel):
    unit: DurationUnit = Field(...)
    value: int = Field(...)

    def __str__(self) -> str:
        return f"{self.value} {self.unit.lower()}s"


class FundingRequest(BaseModel):
    id: int = Field(...)
    amount: int = Field(...)
    irr: Decimal = Field(...)
    score: Decimal = Field(...)
    borrower: Borrower = Field(...)
    currency: Currency = Field(...)
    anual_profit_rate: Decimal = Field(...)
    duration: FundingRequestDuration = Field(...)
    supporting_documents: list[str] = Field(default_factory=list)
    funded_amount_percentage: Decimal = Field(...)
    credit_type: CreditType = Field(...)

    @cached_property
    def profit_rate(self) -> Decimal:
        """Calculates the profit rate for the funding request"""
        value = (1 + self.irr / 100) ** Decimal(self.duration.value / 365) - 1
        return round(Decimal(value), ndigits=3)

    @computed_field
    @cached_property
    def monthly_profit_rate(self) -> Decimal:
        """Calculates the monthly profit rate for the funding request"""
        return round(self.profit_rate * 30 / self.duration.value, 4)

    @computed_field
    @cached_property
    def is_completed(self) -> bool:
        """Checks if the funding request is fully funded"""
        return self.funded_amount_percentage == Decimal(1)

    @computed_field
    @cached_property
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

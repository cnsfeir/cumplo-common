# mypy: disable-error-code="misc, call-overload"

from decimal import Decimal
from functools import cached_property

from pydantic import ConfigDict, Field, computed_field

from cumplo_common.models import BaseModel


class Borrower(BaseModel):
    model_config = ConfigDict(str_to_upper=True)

    id: int | None = Field(None)
    dicom: bool = Field(...)
    name: str | None = Field(None)
    irs_sector: str | None = Field(None)
    funding_requests_count: int = Field(0)
    total_amount_requested: int = Field(0)
    average_days_delinquent: int = Field(...)
    paid_funding_requests_count: int = Field(0)
    paid_in_time_percentage: Decimal = Field(...)

    @computed_field
    @cached_property
    def paid_funding_requests_percentage(self) -> Decimal:
        """Returns the percentage of instalments paid in time"""
        if not self.funding_requests_count:
            return Decimal(0)
        return round(Decimal(self.paid_funding_requests_count / self.funding_requests_count), ndigits=2)

    @computed_field
    @cached_property
    def amount_paid_in_time(self) -> int:
        """Returns the amount paid in time"""
        return round(self.total_amount_requested * self.paid_funding_requests_percentage)

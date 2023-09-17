# mypy: disable-error-code="misc, call-overload"

from decimal import Decimal
from functools import cached_property

from pydantic import BaseModel, Field, computed_field, field_validator

from cumplo_common.models.pydantic import ValidatorMode


class Borrower(BaseModel):
    id: int | None = Field(None)
    dicom: bool = Field(...)
    name: str | None = Field(None)
    irs_sector: str | None = Field(None)
    funding_requests_count: int = Field(0)
    total_amount_requested: int = Field(0)
    average_days_delinquent: int = Field(...)
    paid_funding_requests_count: int = Field(0)
    paid_in_time_percentage: Decimal = Field(...)

    @field_validator("name", mode=ValidatorMode.BEFORE)
    @classmethod
    def _format_name(cls, value: str | None) -> str | None:
        """Formats the name"""
        return value.strip().upper() if value else value

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

# mypy: disable-error-code="call-overload"

from decimal import Decimal
from json import loads
from typing import Any

import ulid
from pydantic import Field, PositiveInt, field_validator

from .base_model import BaseModel
from .credit import CreditType


class DebtorFilterConfiguration(BaseModel):
    ignore_dicom: bool = Field(False)
    minimum_requested_credits: PositiveInt | None = Field(None)
    minimum_paid_in_time_percentage: Decimal | None = Field(None, ge=0, le=1)


class BorrowerFilterConfiguration(BaseModel):
    ignore_dicom: bool = Field(False)
    minimum_requested_amount: PositiveInt | None = Field(None)
    minimum_requested_credits: PositiveInt | None = Field(None)
    maximum_average_days_delinquent: PositiveInt | None = Field(None)
    minimum_paid_in_time_percentage: Decimal | None = Field(None, ge=0, le=1)


class FilterConfiguration(BaseModel):
    """Configuration settings for filtering funding requests to determine promising investment opportunities."""

    id: ulid.ULID = Field(...)
    name: str | None = Field(None)
    minimum_score: Decimal | None = Field(None, ge=0, le=1)
    target_credit_types: list[CreditType] | None = Field(None)

    minimum_duration: PositiveInt | None = Field(None)
    maximum_duration: PositiveInt | None = Field(None)
    minimum_investment_amount: PositiveInt | None = Field(None)

    minimum_irr: Decimal | None = Field(None, ge=0)
    minimum_monthly_profit_rate: Decimal | None = Field(None, ge=0)

    debtor: DebtorFilterConfiguration | None = Field(None)
    borrower: BorrowerFilterConfiguration | None = Field(None)

    @field_validator("id", mode="before")
    @classmethod
    def _format_id(cls, value: ulid.default.api.ULIDPrimitive) -> ulid.ULID:
        """Format the ID field as an ULID object."""
        return ulid.parse(value)

    def __hash__(self) -> int:
        """Return the hash of the object."""
        return hash(self.model_dump_json(exclude={"id", "name"}, exclude_none=True))

    def json(self, *args: Any, **kwargs: Any) -> dict:  # type: ignore[override]
        """
        Return the model as a JSON parsed dict.

        Returns:     dict: JSON parsed dict representation of the model

        """
        return loads(self.model_dump_json(*args, **kwargs, exclude_defaults=True))

# mypy: disable-error-code="call-overload"
# pylint: disable=no-member

from decimal import Decimal

import ulid
from pydantic import Field, PositiveInt, field_validator
from cumplo_common.models.credit import CreditType

from cumplo_common.models.base_model import BaseModel
from cumplo_common.models.pydantic import ValidatorMode


class FilterConfiguration(BaseModel):
    """
    Represents the configuration settings for filtering funding requests
    to determine promising investment opportunities.
    """

    id: ulid.ULID = Field(...)
    name: str | None = Field(None)
    ignore_dicom: bool = Field(False)
    minimum_score: Decimal | None = Field(None, ge=0, le=1)
    target_credit_types: list[CreditType] | None = Field(None)

    minimum_duration: PositiveInt | None = Field(None)
    maximum_duration: PositiveInt | None = Field(None)
    minimum_investment_amount: PositiveInt | None = Field(None)

    minimum_irr: Decimal | None = Field(None, ge=0)
    minimum_monthly_profit_rate: Decimal | None = Field(None, ge=0)

    minimum_requested_amount: PositiveInt | None = Field(None)
    minimum_requested_credits: PositiveInt | None = Field(None)

    maximum_average_days_delinquent: PositiveInt | None = Field(None)
    minimum_paid_in_time_percentage: Decimal | None = Field(None, ge=0, le=1)

    @field_validator("id", mode=ValidatorMode.BEFORE)
    @classmethod
    def _format_id(cls, value: ulid.default.api.ULIDPrimitive) -> ulid.ULID:
        """Formats the ID field as an ULID object"""
        return ulid.parse(value)

    def __hash__(self) -> int:
        """Returns the hash of the object"""
        return hash(self.model_dump_json(exclude={"id", "name"}, exclude_none=True))

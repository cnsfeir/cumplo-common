# mypy: disable-error-code="call-overload"
# pylint: disable=no-member

from decimal import Decimal

import ulid
from pydantic import Field, PositiveInt, field_validator

from cumplo_common.models import BaseModel
from cumplo_common.models.pydantic import ValidatorMode


class FilterConfiguration(BaseModel):
    id: ulid.ULID = Field(...)
    name: str | None = Field(None)
    filter_dicom: bool = Field(False)
    irr: Decimal | None = Field(None, ge=0)
    duration: PositiveInt | None = Field(None)
    score: Decimal | None = Field(None, ge=0, le=1)
    amount_requested: PositiveInt | None = Field(None)
    credits_requested: PositiveInt | None = Field(None)
    monthly_profit_rate: Decimal | None = Field(None, ge=0)
    average_days_delinquent: PositiveInt | None = Field(None)
    paid_in_time_percentage: Decimal | None = Field(None, ge=0, le=1)

    @field_validator("id", mode=ValidatorMode.BEFORE)
    @classmethod
    def _format_id(cls, value: str) -> ulid.ULID:
        """Formats the ID field as an ULID object"""
        return ulid.parse(value)

    def __hash__(self) -> int:
        """Returns the hash of the object"""
        return hash(self.model_dump_json(exclude={"id", "name"}, exclude_none=True))

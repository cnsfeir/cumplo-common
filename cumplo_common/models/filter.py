# pylint: disable=no-member

from decimal import Decimal

from pydantic import Field, PositiveInt

from cumplo_common.models import BaseModel


class FilterConfiguration(BaseModel):
    id: int = Field(...)
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

    def __hash__(self) -> int:
        exclude = {"id", "name", "expiration_minutes"}
        return hash(self.model_dump_json(exclude=exclude, exclude_defaults=True, exclude_none=True))

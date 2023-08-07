# pylint: disable=unused-import, missing-function-docstring, unused-argument
# flake8: noqa: F401

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, PositiveInt

class Configuration(BaseModel):
    id: int
    name: str
    filter_dicom: bool
    irr: Decimal | None
    duration: PositiveInt | None
    score: Decimal | None
    amount_requested: PositiveInt | None
    credits_requested: PositiveInt | None
    expiration_minutes: PositiveInt | None
    monthly_profit_rate: Decimal | None
    average_days_delinquent: PositiveInt | None
    paid_in_time_percentage: Decimal | None
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...
    def serialize(self, to_firestore: bool = ...) -> dict[str, Any]: ...

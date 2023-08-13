from decimal import Decimal

from pydantic import BaseModel, Field


class Borrower(BaseModel):
    dicom: bool = Field(...)
    name: str | None = Field(None)
    irs_sector: str | None = Field(None)
    amount_paid_in_time: int = Field(...)
    funding_requests_count: int = Field(0)
    total_amount_requested: int = Field(0)
    average_days_delinquent: int = Field(...)
    paid_funding_requests_count: int = Field(0)
    paid_in_time_percentage: Decimal = Field(...)
    paid_funding_requests_percentage: Decimal = Field(...)

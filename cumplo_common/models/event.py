from typing import Self

from .base_model import BaseModel
from .funding_request import FundingRequest
from .investment import Investment
from .movement import Movement
from .utils import StrEnum


class Event(StrEnum):
    _name_: str
    model: BaseModel
    is_recurring: bool

    def __new__(cls, value: str, model: BaseModel, is_recurring: bool = False) -> Self:  # noqa: FBT001, FBT002
        """Create a new instance of the Enum with the given value and model."""
        obj = str.__new__(cls, value)
        obj.is_recurring = is_recurring
        obj._value_ = value
        obj.model = model
        return obj

    FUNDING_REQUEST_AVAILABLE = "funding_request.available", FundingRequest
    FUNDING_REQUEST_PROMISING = "funding_request.promising", FundingRequest, True

    INVESTMENT_INITIALIZED = "investment.initialized", Investment
    INVESTMENT_SUBMITTED = "investment.submitted", Investment
    INVESTMENT_CONFIRMED = "investment.confirmed", Investment
    INVESTMENT_FAILED = "investment.failed", Investment
    INVESTMENT_REPAID = "investment.repaid", Investment
    INVESTMENT_REFUNDED = "investment.refunded", Investment
    INVESTMENT_DELINQUENT = "investment.delinquent", Investment
    INVESTMENT_CREDITED = "investment.credited", Investment
    INVESTMENT_UPDATED = "investment.updated", Investment

    # REVIEW: Maybe we don't event need withdrawal and deposit events. Could be just defined by the sign of the amount.
    MOVEMENT_WITHDRAWAL = "movement.withdrawal", Movement
    MOVEMENT_DEPOSIT = "movement.deposit", Movement

    # REVIEW: Should we use different events for this? Maybe this could be an Enum specifying the type.
    MOVEMENT_INVESTMENT = "movement.investment", Movement
    MOVEMENT_FEE_RETENTION = "movement.fee_retention", Movement
    MOVEMENT_FEE_CHARGE = "movement.fee_charge", Movement
    MOVEMENT_FEE_REFUND = "movement.fee_refund", Movement
    MOVEMENT_RETURN = "movement.return", Movement

# mypy: disable-error-code="misc"

from datetime import datetime
from decimal import Decimal
from functools import cached_property

from pydantic import Field, computed_field

from cumplo_common.utils.constants import SIMULATION_AMOUNT

from .base_model import BaseModel


class SimulationInstallment(BaseModel):
    amount: int = Field(...)
    interest: int = Field(...)
    due_date: datetime = Field(...)


class Simulation(BaseModel):
    net_returns: int = Field(...)
    platform_fee: int = Field(...)
    cumplo_points: int = Field(...)
    payment_schedule: list[SimulationInstallment] = Field(default_factory=list)

    @cached_property
    @computed_field
    def installments(self) -> int:
        """Returns the number of installments for the simulation."""
        return len(self.payment_schedule)

    @cached_property
    @computed_field
    def investment(self) -> int:
        """Returns the investment of the simulation."""
        return SIMULATION_AMOUNT + self.cumplo_points

    @cached_property
    @computed_field
    def cash_flows(self) -> list[int]:
        """Returns the cash flows of the simulation."""
        installments = [
            installment.amount - self.platform_fee if index == len(self.payment_schedule) else installment.amount
            for index, installment in enumerate(self.payment_schedule, start=1)
        ]
        installments.insert(0, -self.investment)
        return installments

    @cached_property
    def profit_rate(self) -> Decimal:
        """Returns the profit rate of the simulation."""
        return round(Decimal((SIMULATION_AMOUNT + self.net_returns) / self.investment - 1), 4)

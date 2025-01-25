from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from functools import cached_property

import arrow
from pydantic import Field, computed_field

from cumplo_common.utils.constants import SIMULATION_AMOUNT

from .base_model import BaseModel


class SimulationInstallment(BaseModel):
    amount: int = Field(...)
    interest: int = Field(...)
    date: datetime = Field(...)


class Simulation(BaseModel):
    net_returns: int = Field(...)
    upfront_fee: int = Field(...)
    exit_fee: int = Field(...)
    payment_schedule: list[SimulationInstallment] = Field(default_factory=list, exclude=True)

    @computed_field  # type: ignore[misc]
    @cached_property
    def installments(self) -> int:
        """Returns the number of installments for the simulation."""
        return len(self.payment_schedule)

    @computed_field  # type: ignore[misc]
    @cached_property
    def investment(self) -> int:
        """Returns the investment of the simulation."""
        return SIMULATION_AMOUNT + self.upfront_fee

    @computed_field  # type: ignore[misc]
    @cached_property
    def cash_flows(self) -> list[SimulationInstallment]:
        """Returns the cash flows of the simulation."""
        installments = deepcopy(self.payment_schedule)
        installments[-1].amount -= self.exit_fee
        installments.insert(
            0,
            SimulationInstallment(
                interest=0,
                amount=-self.investment,
                date=arrow.utcnow().floor("day").datetime,
            ),
        )
        return installments

    @cached_property
    def profit_rate(self) -> Decimal:
        """Returns the profit rate of the simulation."""
        return round(Decimal((SIMULATION_AMOUNT + self.net_returns) / self.investment - 1), 4)

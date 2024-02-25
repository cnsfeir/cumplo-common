from datetime import datetime
from functools import cached_property

from pydantic import Field

from cumplo_common.models.base_model import BaseModel
from cumplo_common.utils.constants import SIMULATION_AMOUNT


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
    def cash_flows(self) -> list[int]:
        """
        Returns the cash flows of the simulation
        """
        investment = -(SIMULATION_AMOUNT + self.cumplo_points)
        installments = [
            installment.amount - self.platform_fee if index == len(self.payment_schedule) else installment.amount
            for index, installment in enumerate(self.payment_schedule, start=1)
        ]
        installments.insert(0, investment)
        return installments
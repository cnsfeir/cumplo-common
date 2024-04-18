# pylint: disable=arguments-differ, invalid-name, no-value-for-parameter

from typing import Self

from cumplo_common.models.base_model import StrEnum


class Resource(StrEnum):
    FUNDING_REQUEST = "funding_request"
    INVESTMENT = "investment"


class State(StrEnum):
    INITIALIZED = "initialized"
    SUCCESSFUL = "successful"
    PROMISING = "promising"
    FAILED = "failed"


class Event(StrEnum):
    _name_: str
    state: State
    resource: Resource
    is_recurring: bool

    def __new__(cls, value: str, resource: Resource, state: State, is_recurring: bool) -> Self:
        obj = str.__new__(cls, value)
        obj.is_recurring = is_recurring
        obj._value_ = value
        obj.resource = resource
        obj.state = state
        return obj

    @classmethod
    def new(cls, resource: Resource, state: State) -> Self:
        """Instantiates a new event from a resource and a state"""
        return cls(resource.name + "." + state.name)  # type: ignore[call-arg]

    FUNDING_REQUEST_PROMISING = "funding_request.promising", Resource.FUNDING_REQUEST, State.PROMISING, True
    INVESTMENT_INITIALIZED = "investment.initialized", Resource.INVESTMENT, State.INITIALIZED, False
    INVESTMENT_SUCCESSFUL = "investment.successful", Resource.INVESTMENT, State.SUCCESSFUL, False
    INVESTMENT_FAILED = "investment.failed", Resource.INVESTMENT, State.FAILED, False

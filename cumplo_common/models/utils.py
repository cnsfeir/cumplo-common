import enum
from collections.abc import Generator
from typing import Self

from pydantic import BaseModel


class StrEnum(enum.StrEnum):
    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        """Return the enum member case insensitively."""
        if isinstance(value, str):
            for member in cls:
                if member.casefold() == value.casefold():
                    return member
        return None

    @classmethod
    def has_member(cls, value: str) -> bool:
        """Whether the enum has a member case insensitively."""
        return any(value.casefold() == item.name.casefold() for item in cls)

    @classmethod
    def members(cls) -> Generator[Self, None, None]:
        """
        Yield the enum members.

        Yields:
            Self: The enum members.

        """
        yield from cls


class EventModel(BaseModel):
    id: int


class Event(StrEnum):
    _name_: str
    model: type[EventModel]
    is_recurring: bool

    def __new__(cls, value: str, model: type[EventModel], is_recurring: bool = False) -> Self:  # noqa: FBT001, FBT002
        """Create a new instance of the Enum with the given value and model."""
        obj = str.__new__(cls, value)
        obj.is_recurring = is_recurring
        obj._value_ = value
        obj.model = model
        return obj

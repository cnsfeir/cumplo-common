import enum
from collections.abc import Generator
from typing import Self


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

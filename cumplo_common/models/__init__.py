from abc import ABC
from json import loads
from typing import Any

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel, ABC):
    """Base class for all models in the project"""

    def __hash__(self) -> int:
        return hash(self.model_dump_json(exclude_none=True))

    def __str__(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def __repr__(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def __eq__(self, other: Any) -> bool:
        return self.__hash__() == other.__hash__()

    def json(self, *args: Any, **kwargs: Any) -> dict:  # type: ignore[override]
        """
        Returns the model as a JSON parsed dict

        Returns:
            dict: JSON parsed dict representation of the model
        """
        return loads(self.model_dump_json(exclude_none=True, *args, **kwargs))

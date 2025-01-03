from abc import ABC, abstractmethod
from typing import Any, Protocol

from google.cloud.firestore_v1.collection import CollectionReference

from cumplo_common.models import BaseModel


class User(Protocol):
    expiration_minutes: int


class UserCollection(Protocol):
    collection: CollectionReference

    def get(self, id_user: str | None = None, api_key: str | None = None) -> User:
        """Get a single element of the collection."""


class UserSubcollection(ABC):
    __id__: str

    def __init__(self, user: UserCollection) -> None:
        self.user = user

    def _collection(self, id_user: str) -> CollectionReference:
        """Get the collection reference for a given user ID."""
        document = self.user.collection.document(id_user)
        return document.collection(self.__id__)

    @abstractmethod
    def get(self, id_user: str, id_document: str) -> BaseModel:
        """Get a single element of the collection."""

    @abstractmethod
    def get_all(self, id_user: str) -> dict:
        """Get all the elements of the collection."""

    @abstractmethod
    def put(self, id_user: str, data: Any) -> None:
        """Upserts a single element of the collection."""

    @abstractmethod
    def delete(self, id_user: str, id_document: str) -> None:
        """Delete a single element of the collection."""

from collections.abc import Generator
from logging import getLogger
from typing import Any

from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1 import CollectionReference

from cumplo_common.models import User
from cumplo_common.utils.constants import DISABLED_COLLECTION, KEYS_COLLECTION, USERS_COLLECTION
from cumplo_common.utils.text import secure_key

logger = getLogger(__name__)


class UserCollection:
    collection: CollectionReference
    keys: CollectionReference
    client: FirestoreClient

    def __init__(self, client: FirestoreClient) -> None:
        self.collection = client.collection(USERS_COLLECTION)
        self.keys = client.collection(KEYS_COLLECTION)
        self.client = client

    def get(self, id_user: str | None = None, api_key: str | None = None) -> User:
        """
        Get a user.

        Args:
            id_user (str): The user ID
            api_key (str): The API key

        Raises:
            KeyError: When the user does not exist
            ValueError: When the user data is empty or the API key is not valid

        Returns:
            User: The user object containing the user data

        """
        if not (id_user or api_key):
            raise ValueError("Either ID or API key must be provided")

        if not id_user and api_key:
            logger.info(f"Getting user with API key {secure_key(api_key)} from Firestore")
            key = self.keys.document(api_key).get()

            if not key.exists or not (data := key.to_dict()):
                raise KeyError(f"User with API key {secure_key(api_key)} does not exist")

            id_user = data["id_user"]

        user = self.collection.document(id_user).get()

        if not user.exists or not (data := user.to_dict()):
            raise KeyError(f"User with ID {id_user} does not exist")

        return User(id=user.id, **data)

    def list(self) -> Generator[User, None, None]:
        """
        List all users.

        Yields:
            Generator[User, None, None]: Iterable of User objects

        """
        logger.info("Getting all users from Firestore")
        for user in self.collection.stream():
            if data := user.to_dict():
                yield User(id=user.id, **data)

    def create(self, user: User) -> None:
        """
        Create a user.

        Args:
            user (User): The user to be created

        """
        logger.info(f"Creating user {user.id} into Firestore")
        self.collection.document(str(user.id)).set(user.json(exclude={"id"}))
        self.keys.document(user.api_key).set({"id_user": str(user.id)})

    def put(self, user: User) -> None:
        """
        Create or updates a user.

        Args:
            user (User): The new user data to be upserted

        """
        logger.info(f"Upserting user {user.id} into Firestore")
        document = self.collection.document(str(user.id))
        document.set(user.json(exclude={"id"}))

    def delete(self, id_user: str) -> None:
        """
        Delete a user.

        Args:
            id_user (str): The user ID to be deleted

        """
        logger.info(f"Deleting user {id_user} from Firestore")
        document = self.collection.document(id_user)
        document.delete()


class DisabledCollection(UserCollection):
    def __init__(self, client: FirestoreClient, *args: Any, **kwargs: Any) -> None:
        super().__init__(client, *args, **kwargs)
        self.collection = client.collection(DISABLED_COLLECTION)

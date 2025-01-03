from collections.abc import Generator
from logging import getLogger

from cachetools import TTLCache, cached
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.base_query import FieldFilter

from cumplo_common.models import User
from cumplo_common.utils.constants import CACHE_MAXSIZE, CACHE_TTL, USERS_COLLECTION
from cumplo_common.utils.text import secure_key

from .channels import ChannelCollection
from .filters import FilterCollection
from .notifications import NotificationCollection

logger = getLogger(__name__)
cache = TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_TTL)


class UserCollection:
    def __init__(self, client: FirestoreClient) -> None:
        self.collection = client.collection(USERS_COLLECTION)
        self.client = client

    @cached(cache=cache)
    def get(self, id_user: str | None = None, api_key: str | None = None) -> User:
        """
        Get a user document.

        Args:
            id_user (str): The user ID
            api_key (str): The API key

        Raises:
            KeyError: When the user does not exist
            ValueError: When the user data is empty

        Returns:
            User: The user object containing the user data

        """
        if not (id_user or api_key):
            raise ValueError("Either ID or API key must be provided")

        if id_user:
            logger.info(f"Getting user with ID {id_user} from Firestore")
            user = self.collection.document(id_user).get()
            if not user.exists:
                raise KeyError(f"User with ID {id_user} does not exist")

        elif api_key:
            logger.info(f"Getting user with API key {secure_key(api_key)} from Firestore")
            filter_ = FieldFilter("api_key", "==", api_key)
            stream = self.collection.where(filter=filter_).stream()

            if not (user := next(stream, None)):  # type: ignore[arg-type]
                raise KeyError(f"User with API key {secure_key(api_key)} does not exist")

        if not (data := user.to_dict()):
            raise ValueError("User data is empty")

        return User(
            id=user.id,
            filters_query=FilterCollection(self).get_all,
            channels_query=ChannelCollection(self).get_all,
            notifications_query=NotificationCollection(self).get_all,
            **data,
        )

    def get_all(self) -> Generator[User, None, None]:
        """
        Get all the users data.

        Yields:
            Generator[User, None, None]: Iterable of User objects

        """
        logger.info("Getting all users from Firestore")
        for user in self.collection.stream():
            if data := user.to_dict():
                yield User(
                    id=user.id,
                    filters_query=FilterCollection(self).get_all,
                    channels_query=ChannelCollection(self).get_all,
                    notifications_query=NotificationCollection(self).get_all,
                    **data,
                )

    def put(self, user: User) -> None:
        """
        Create or updates a user document.

        Args:
            user (User): The new user data to be upserted

        """
        logger.info(f"Upserting user {user.id} into Firestore")
        document = self.collection.document(str(user.id))
        document.set(user.json(exclude={"id"}))

    def delete(self, id_user: str) -> None:
        """
        Delete a user document.

        Args:
            id_user (str): The user ID to be deleted

        """
        logger.info(f"Deleting user {id_user} from Firestore")
        document = self.collection.document(id_user)
        document.delete()

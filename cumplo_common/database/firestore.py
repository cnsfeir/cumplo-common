from collections.abc import Generator
from logging import getLogger

import arrow
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.document import DocumentReference

from cumplo_common.models.configuration import Configuration
from cumplo_common.models.notification import Notification
from cumplo_common.models.user import User
from cumplo_common.utils.constants import (
    CONFIGURATIONS_COLLECTION,
    NOTIFICATIONS_COLLECTION,
    PROJECT_ID,
    USERS_COLLECTION,
)
from cumplo_common.utils.text import secure_key

logger = getLogger(__name__)


class FirestoreClient:
    def __init__(self) -> None:
        firebase_credentials = credentials.ApplicationDefault()
        initialize_app(firebase_credentials, {"projectId": PROJECT_ID})
        self.client = firestore.client()

    def get_users(self) -> Generator[User, None, None]:
        """
        Gets all the users data

        Yields:
            Generator[User, None, None]: Iterable of User objects
        """
        logger.info("Getting all users from Firestore")
        user_stream = self.client.collection(USERS_COLLECTION).stream()
        for user in user_stream:
            yield User(id=user.id, **user.to_dict())

    def get_user(self, api_key: str) -> User:
        """
        Gets the user data for a given API key

        Args:
            api_key (str): User API key

        Raises:
            KeyError: When the user does not exist
            ValueError: When the user data is empty

        Returns:
            User: A User object containing the user data
        """
        logger.info(f"Getting user with API key {secure_key(api_key)} from Firestore")
        filter_ = FieldFilter("api_key", "==", api_key)
        user_stream = self.client.collection(USERS_COLLECTION).where(filter=filter_).stream()

        if not (user := next(user_stream, None)):
            raise KeyError(f"User with API key {secure_key(api_key)} does not exist")

        if not (user_data := user.to_dict()):
            raise ValueError(f"User with API key {secure_key(api_key)} data is empty")

        configurations = self._get_user_configurations(user.id)
        notifications = self._get_user_notifications(user.id)
        return User(id=user.id, configurations=configurations, notifications=notifications, **user_data)

    def update_notification(self, id_user: str, id_funding_request: int) -> None:
        """
        Updates the notification for a given user and funding request

        Args:
            id_user (str): A user ID which owns the notification
            id_funding_request (int): A funding request ID
        """
        logger.info(f"Updating notification for funding request {id_funding_request} at Firestore")
        notification = self._get_notification_document(id_user, id_funding_request)
        notification.set({"date": arrow.utcnow().datetime})

    def update_configuration(self, id_user: str, configuration: Configuration) -> None:
        """
        Updates a configuration of a given user

        Args:
            id_user (str): A user ID which owns the configuration
            configuration (Configuration): A Configuration object containing the new configuration data to be updated
        """
        logger.info(f"Updating configuration {configuration.id} of user {id_user} at Firestore")
        configuration_reference = self._get_configuration_document(id_user, configuration.id)
        configuration_reference.set(configuration.serialize(for_firestore=True))

    def delete_notification(self, id_user: str, id_funding_request: int) -> None:
        """
        Deletes a notification of a funding request for a given user

        Args:
            id_user (str): A user ID which owns the notification
            id_funding_request (int): A funding request ID to be deleted
        """
        logger.info(f"Deleting notification {id_funding_request} from Firestore")
        notification = self._get_notification_document(id_user, id_funding_request)
        notification.delete()

    def delete_configuration(self, id_user: str, id_configuration: int) -> None:
        """
        Deletes a configuration for a given user and configuration ID

        Args:
            id_user (str): A user ID which owns the configuration
            id_configuration (int): A configuration ID to be deleted
        """
        logger.info(f"Deleting configuration {id_configuration} from Firestore")
        configuration = self._get_configuration_document(id_user, id_configuration)
        configuration.delete()

    def _get_user_document(self, id_user: str) -> DocumentReference:
        """Gets a user document reference"""
        return self.client.collection(USERS_COLLECTION).document(id_user)

    def _get_notification_document(self, id_user: str, id_funding_request: int) -> DocumentReference:
        """Gets a notification document reference"""
        user_document = self._get_user_document(id_user)
        return user_document.collection(NOTIFICATIONS_COLLECTION).document(str(id_funding_request))

    def _get_configuration_document(self, id_user: str, id_configuration: int) -> DocumentReference:
        """Gets a configuration document reference"""
        user_document = self._get_user_document(id_user)
        return user_document.collection(CONFIGURATIONS_COLLECTION).document(str(id_configuration))

    def _get_user_notifications(self, id_user: str) -> dict[int, Notification]:
        """
        Gets the user notifications data
        """
        logger.info(f"Getting user {id_user} notifications from Firestore")
        user_document = self._get_user_document(id_user)
        notifications = user_document.collection(NOTIFICATIONS_COLLECTION).stream()
        return {int(n.id): Notification(id=int(n.id), **n.to_dict()) for n in notifications}

    def _get_user_configurations(self, id_user: str) -> dict[int, Configuration]:
        """
        Gets the user configurations data
        """
        logger.info(f"Getting user {id_user} configurations from Firestore")
        user_document = self._get_user_document(id_user)
        configurations = user_document.collection(CONFIGURATIONS_COLLECTION).stream()
        return {int(c.id): Configuration(id=int(c.id), **c.to_dict()) for c in configurations}


firestore_client = FirestoreClient()

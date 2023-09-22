from collections.abc import Generator
from logging import getLogger

import arrow
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.document import DocumentReference

from cumplo_common.models.channel import CHANNEL_CONFIGURATION_BY_TYPE, ChannelConfiguration, ChannelType
from cumplo_common.models.filter import FilterConfiguration
from cumplo_common.models.notification import Notification
from cumplo_common.models.user import User
from cumplo_common.utils.constants import (
    CHANNELS_COLLECTION,
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
            User: The User object containing the user data
        """
        logger.info(f"Getting user with API key {secure_key(api_key)} from Firestore")
        filter_ = FieldFilter("api_key", "==", api_key)
        user_stream = self.client.collection(USERS_COLLECTION).where(filter=filter_).stream()

        if not (user := next(user_stream, None)):
            raise KeyError(f"User with API key {secure_key(api_key)} does not exist")

        if not (user_data := user.to_dict()):
            raise ValueError(f"User with API key {secure_key(api_key)} data is empty")

        filters = self._get_user_filters(user.id)
        channels = self._get_user_channels(user.id)
        notifications = self._get_user_notifications(user.id)
        return User(
            id=user.id,
            filters=filters,
            channels=channels,
            notifications=notifications,
            **user_data,
        )

    def put_notification(self, id_user: str, id_notification: str) -> None:
        """
        Creates or updates the notification for a given user and funding request

        Args:
            id_user (str): The user ID which owns the notification
            id_notification (str): The funding request ID
        """
        logger.info(f"Updating notification for funding request {id_notification} at Firestore")
        notification = self._get_notification_document(id_user, id_notification)
        notification.set({"date": arrow.utcnow().datetime})

    def put_filter(self, id_user: str, configuration: FilterConfiguration) -> None:
        """
        Creates or updates a configuration of a given user

        Args:
            id_user (str): The user ID which owns the configuration
            configuration (Configuration): The Configuration object containing the new configuration data to be updated
        """
        logger.info(f"Updating configuration {configuration.id} of user {id_user} at Firestore")
        configuration_reference = self._get_filter_document(id_user, configuration.id)
        configuration_reference.set(configuration.json())

    def put_channel(self, id_user: str, channel: ChannelConfiguration) -> None:
        """
        Creates or updates a channel of a given user

        Args:
            id_user (str): The user ID which owns the configuration
            channel (ChannelConfiguration): The ChannelConfiguration object containing the new data to be updated
        """
        logger.info(f"Updating channel {channel.type_} of user {id_user} at Firestore")
        channel_reference = self._get_channel_document(id_user, channel.type_)
        channel_reference.set(channel.model_dump())

    def delete_notification(self, id_user: str, id_notification: str) -> None:
        """
        Deletes a notification of a funding request for a given user

        Args:
            id_user (str): The user ID which owns the notification
            id_notification (str): The ID of the notification to be deleted
        """
        logger.info(f"Deleting notification {id_notification} from Firestore")
        notification = self._get_notification_document(id_user, id_notification)
        notification.delete()

    def delete_filter(self, id_user: str, id_filter: int) -> None:
        """
        Deletes a configuration for a given user and configuration ID

        Args:
            id_user (str): The user ID which owns the configuration
            id_filter (int): The filter ID to be deleted
        """
        logger.info(f"Deleting filter {id_filter} from Firestore")
        configuration = self._get_filter_document(id_user, id_filter)
        configuration.delete()

    def delete_channel(self, id_user: str, channel_type: ChannelType) -> None:
        """
        Deletes a channel for a given user and channel ID

        Args:
            id_user (str): The user ID which owns the channel
            channel_type (ChannelType): The channel type to be deleted
        """
        logger.info(f"Deleting channel {channel_type} from Firestore")
        channel = self._get_channel_document(id_user, channel_type)
        channel.delete()

    def _get_user_document(self, id_user: str) -> DocumentReference:
        """Gets a user document reference"""
        return self.client.collection(USERS_COLLECTION).document(id_user)

    def _get_notification_document(self, id_user: str, id_notification: str) -> DocumentReference:
        """Gets a notification document reference"""
        user_document = self._get_user_document(id_user)
        return user_document.collection(NOTIFICATIONS_COLLECTION).document(id_notification)

    def _get_filter_document(self, id_user: str, id_filter: int) -> DocumentReference:
        """Gets a configuration document reference"""
        user_document = self._get_user_document(id_user)
        return user_document.collection(CONFIGURATIONS_COLLECTION).document(str(id_filter))

    def _get_channel_document(self, id_user: str, channel_type: ChannelType) -> DocumentReference:
        """Gets a channel document reference"""
        user_document = self._get_user_document(id_user)
        return user_document.collection(CHANNELS_COLLECTION).document(str(channel_type))

    def _get_user_notifications(self, user: User) -> dict[str, Notification]:
        """
        Gets the user notifications data
        """
        logger.info(f"Getting user {user.id} notifications from Firestore")
        user_document = self._get_user_document(user.id)
        notifications = user_document.collection(NOTIFICATIONS_COLLECTION).stream()
        return {
            n.id: Notification(id=n.id, expiration_minutes=user.expiration_minutes, **n.to_dict())
            for n in notifications
        }

    def _get_user_filters(self, id_user: str) -> dict[int, FilterConfiguration]:
        """
        Gets the user configurations data
        """
        logger.info(f"Getting user {id_user} configurations from Firestore")
        user_document = self._get_user_document(id_user)
        configurations = user_document.collection(CONFIGURATIONS_COLLECTION).stream()
        return {int(c.id): FilterConfiguration(id=int(c.id), **c.to_dict()) for c in configurations}

    def _get_user_channels(self, id_user: str) -> dict[ChannelType, ChannelConfiguration]:
        """
        Gets the user channels data
        """
        logger.info(f"Getting user {id_user} channels from Firestore")
        user_document = self._get_user_document(id_user)
        channels = user_document.collection(CHANNELS_COLLECTION).stream()
        return {c.id: CHANNEL_CONFIGURATION_BY_TYPE[ChannelType(c.id)](**c.to_dict()) for c in channels}


firestore_client = FirestoreClient()

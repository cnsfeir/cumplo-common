from logging import getLogger

import arrow

from cumplo_common.database.firestore.subcollections import UserSubcollection
from cumplo_common.models.notification import Notification
from cumplo_common.utils.constants import NOTIFICATIONS_COLLECTION

logger = getLogger(__name__)


class NotificationCollection(UserSubcollection):
    __id__ = NOTIFICATIONS_COLLECTION

    def get(self, id_user: str, id_document: str) -> Notification:
        """
        Get a specific Notification of a given user.

        Args:
            id_user (str): The user ID which owns the notification
            id_document (str): The notification ID to be retrieved

        Raises:
            KeyError: When the notification does not exist

        Returns:
            Notification: The notification data

        """
        logger.info(f"Getting user {id_user} notifications from Firestore")
        user = self.user.get(id_user)
        document = self._collection(id_user).document(id_document).get()
        if document.exists and (data := document.to_dict()):
            return Notification(id=document.id, expiration_minutes=user.expiration_minutes, **data)

        raise KeyError(f"Notification with ID {id_document} does not exist")

    def get_all(self, id_user: str) -> dict[str, Notification]:
        """
        Get the user notifications data.

        Args:
            id_user (str): The user ID which owns the notifications

        Returns:
            dict[int, Notification]: A dictionary containing the user notifications

        """
        logger.info(f"Getting user {id_user} notifications from Firestore")
        stream = self._collection(id_user).stream()
        user = self.user.get(id_user)
        return {
            document.id: Notification(id=document.id, expiration_minutes=user.expiration_minutes, **data)
            for document in stream
            if (data := document.to_dict())
        }

    def put(self, id_user: str, data: str) -> None:
        """
        Create or update a notification of a given user.

        Args:
            id_user (str): The user ID which owns the notification
            data (str): The ID of the notification to be upserted

        """
        logger.info(f"Upserting notification {data} of user {id_user} into Firestore")
        document = self._collection(id_user).document(data)
        document.set({"date": arrow.utcnow().datetime})

    def delete(self, id_user: str, id_document: str) -> None:
        """
        Delete a notification for a given user and notification ID.

        Args:
            id_user (str): The user ID which owns the notification
            id_document (int): The notification ID to be deleted

        """
        logger.info(f"Deleting notification {id_document} from Firestore")
        document = self._collection(id_user).document(id_document)
        document.delete()

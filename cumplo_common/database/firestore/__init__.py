from typing import TYPE_CHECKING

from firebase_admin import credentials, firestore, initialize_app

if TYPE_CHECKING:
    from google.cloud.firestore_v1 import Client as FirestoreClient

from cumplo_common.database.firestore.channels import ChannelCollection
from cumplo_common.database.firestore.filters import FilterCollection
from cumplo_common.database.firestore.notifications import NotificationCollection
from cumplo_common.database.firestore.users import UserCollection
from cumplo_common.utils.constants import PROJECT_ID


class Client:
    def __init__(self) -> None:
        initialize_app(credential=credentials.ApplicationDefault(), options={"projectId": PROJECT_ID})
        self.client: FirestoreClient = firestore.client()
        self._init_collections()

    def _init_collections(self) -> None:
        """Initialize the collections."""
        self.users = UserCollection(self.client)
        self.filters = FilterCollection(self.users)
        self.channels = ChannelCollection(self.users)
        self.notifications = NotificationCollection(self.users)


client = Client()

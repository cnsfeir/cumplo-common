from typing import TYPE_CHECKING, Self

from firebase_admin import credentials, firestore, initialize_app

if TYPE_CHECKING:
    from google.cloud.firestore_v1 import Client as FirestoreClient

from cumplo_common.utils.constants import PROJECT_ID

from .channels import ChannelCollection
from .filters import FilterCollection
from .notifications import NotificationCollection
from .users import UserCollection


class Client:
    _instance: Self | None = None
    _initialized: bool = False

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            initialize_app(credential=credentials.ApplicationDefault(), options={"projectId": PROJECT_ID})
            self.client: FirestoreClient = firestore.client()
            self._init_collections()
            self._initialized = True

    def _init_collections(self) -> None:
        """Initialize the collections."""
        self.users = UserCollection(self.client)
        self.filters = FilterCollection(self.users)
        self.channels = ChannelCollection(self.users)
        self.notifications = NotificationCollection(self.users)


client = Client()

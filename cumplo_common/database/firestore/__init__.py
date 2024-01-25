from firebase_admin import credentials, firestore, initialize_app

from cumplo_common.database.firestore.channels import ChannelCollection
from cumplo_common.database.firestore.filters import FilterCollection
from cumplo_common.database.firestore.notifications import NotificationCollection
from cumplo_common.database.firestore.users import UserCollection
from cumplo_common.utils.constants import PROJECT_ID


class Client:
    def __init__(self) -> None:
        initialize_app(credential=credentials.ApplicationDefault(), options={"projectId": PROJECT_ID})
        self.client = firestore.client()
        self.__init_collections__()

    def __init_collections__(self) -> None:
        """Initializes the collections"""
        self.users = UserCollection(self.client)
        self.filters = FilterCollection(self.client)
        self.channels = ChannelCollection(self.client)
        self.notifications = NotificationCollection(self.client)


client = Client()

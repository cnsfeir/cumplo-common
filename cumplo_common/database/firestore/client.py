from typing import Self

from firebase_admin import credentials, firestore, initialize_app

from cumplo_common.utils.constants import PROJECT_ID

from .users import DisabledCollection, UserCollection


class Client:
    _instance: Self | None = None
    _initialized: bool = False

    users: UserCollection
    disabled: DisabledCollection
    client: firestore.Client

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False  # noqa: SLF001
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            initialize_app(credential=credentials.ApplicationDefault(), options={"projectId": PROJECT_ID})
            self.client = firestore.client()
            self.users = UserCollection(self.client)
            self.disabled = DisabledCollection(self.client)
            self._initialized = True


client = Client()

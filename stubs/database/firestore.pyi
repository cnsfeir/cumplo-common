# pylint: disable=unused-import, missing-function-docstring, unused-argument
# flake8: noqa: F401

from collections.abc import Generator
from logging import Logger

from google.cloud.firestore_v1 import Client
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

logger: Logger

class FirestoreClient:
    client: Client
    def __init__(self) -> None: ...
    def get_users(self) -> Generator[User, None, None]: ...
    def get_user(self, api_key: str) -> User: ...
    def update_notification(self, id_user: str, id_funding_request: int) -> None: ...
    def update_configuration(self, id_user: str, configuration: Configuration) -> None: ...
    def delete_notification(self, id_user: str, id_funding_request: int) -> None: ...
    def delete_configuration(self, id_user: str, id_configuration: int) -> None: ...

firestore_client: FirestoreClient

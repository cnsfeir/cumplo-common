from os import getenv

from dotenv import load_dotenv

load_dotenv()

CONFIGURATIONS_COLLECTION: str = getenv("CONFIGURATIONS_COLLECTION", "configurations")
LOCATION: str = getenv("LOCATION", "us-central1")
NOTIFICATIONS_COLLECTION: str = getenv("NOTIFICATIONS_COLLECTION", "notifications")
PROJECT_ID: str = getenv("PROJECT_ID", "")
USERS_COLLECTION: str = getenv("USERS_COLLECTION", "users")

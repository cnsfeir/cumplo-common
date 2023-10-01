from os import getenv

from dotenv import load_dotenv

load_dotenv()

CHANNELS_COLLECTION: str = getenv("CHANNELS_COLLECTION", "channels")
CUMPLO_BASE_URL: str = getenv("CUMPLO_BASE_URL", "")
DEFAULT_EXPIRATION_MINUTES: int = int(getenv("DEFAULT_EXPIRATION_MINUTES", "30"))
FILTERS_COLLECTION: str = getenv("FILTERS_COLLECTION", "filters")
LOCATION: str = getenv("LOCATION", "us-central1")
NOTIFICATIONS_COLLECTION: str = getenv("NOTIFICATIONS_COLLECTION", "notifications")
PROJECT_ID: str = getenv("PROJECT_ID", "")
SERVICE_ACCOUNT_EMAIL: str = getenv("SERVICE_ACCOUNT_EMAIL", "")
USERS_COLLECTION: str = getenv("USERS_COLLECTION", "users")

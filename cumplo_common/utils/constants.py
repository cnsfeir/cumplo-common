from os import getenv

from dotenv import load_dotenv

load_dotenv()

CONFIGURATIONS_COLLECTION = getenv("CONFIGURATIONS_COLLECTION", "configurations")
LOCATION = getenv("LOCATION", "us-central1")
NOTIFICATIONS_COLLECTION = getenv("NOTIFICATIONS_COLLECTION", "notifications")
PROJECT_ID = getenv("PROJECT_ID", "")
USERS_COLLECTION = getenv("USERS_COLLECTION", "users")

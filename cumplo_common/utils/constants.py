import os

from dotenv import load_dotenv

load_dotenv()

# Basics
LOCATION = os.getenv("LOCATION", "us-central1")
PROJECT_ID = os.getenv("PROJECT_ID", "")
LOG_FORMAT = "\n%(levelname)s: %(message)s"
IS_TESTING = bool(os.getenv("IS_TESTING"))
SERVICE_ACCOUNT_EMAIL: str = os.getenv("SERVICE_ACCOUNT_EMAIL", "")

# Firestore Collections
CHANNELS_COLLECTION: str = os.getenv("CHANNELS_COLLECTION", "channels")
FILTERS_COLLECTION: str = os.getenv("FILTERS_COLLECTION", "filters")
NOTIFICATIONS_COLLECTION: str = os.getenv("NOTIFICATIONS_COLLECTION", "notifications")
USERS_COLLECTION: str = os.getenv("USERS_COLLECTION", "users")

# Cumplo
CUMPLO_BASE_URL: str = os.getenv("CUMPLO_BASE_URL", "")
SIMULATION_AMOUNT = int(os.getenv("SIMULATION_AMOUNT", "1000000"))

# Defaults
DEFAULT_EXPIRATION_MINUTES: int = int(os.getenv("DEFAULT_EXPIRATION_MINUTES", "60"))

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
KEYS_COLLECTION: str = os.getenv("KEYS_COLLECTION", "keys")
USERS_COLLECTION: str = os.getenv("USERS_COLLECTION", "users")
DISABLED_COLLECTION: str = os.getenv("DISABLED_COLLECTION", "disabled")

# Cumplo
CUMPLO_BASE_URL: str = os.getenv("CUMPLO_BASE_URL", "")
SIMULATION_AMOUNT = int(os.getenv("SIMULATION_AMOUNT", "1000000"))

# Defaults
DEFAULT_EXPIRATION_MINUTES: int = int(os.getenv("DEFAULT_EXPIRATION_MINUTES", "60"))

# Validators
PHONE_NUMBER_REGEX = r"^\+[1-9]\d{1,14}$"

# Cache
CACHE_MAXSIZE = int(os.getenv("CACHE_MAXSIZE", "1000"))
USERS_CACHE_TTL = int(os.getenv("USERS_CACHE_TTL", "600"))

# Encryption
PASSWORDS_ENCRYPTION_KEY: str = os.getenv("PASSWORDS_ENCRYPTION_KEY", "")

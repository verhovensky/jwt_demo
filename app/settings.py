import os
from dotenv import load_dotenv
from utils import gen_secure_key

load_dotenv()

db_settings = {
    'DB_HOST': os.getenv("DB_HOST"),
    'DB_NAME': os.getenv("DB_NAME"),
    'DB_PASS': os.getenv("DB_PASS"),
    'DB_USER': os.getenv("DB_USER")
}

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET") or gen_secure_key()

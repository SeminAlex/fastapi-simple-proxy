import os
import dotenv

dotenv.load_dotenv("app/.env")


class Settings:
    CACHE_URL = os.environ["CACHE_URL"]
    MAIN_URL = os.environ["MAIN_URL"]
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]


import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_GREEN_CITY_API_URL = os.getenv("BASE_GREEN_CITY_API_URL")
    BASE_GREEN_CITY_USER_API_URL = os.getenv("BASE_GREEN_CITY_USER_API_URL")
    BASE_UI_GREEN_CITY_URL = os.getenv("BASE_UI_GREEN_CITY_URL")
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True").lower() in ("true", "1", "yes")
    IMPLICITLY_WAIT = int(os.getenv("IMPLICITLY_WAIT", 10))
    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_ID = int(os.getenv("USER_ID"))
    USER_LOCATION = os.getenv("USER_LOCATION")
    USER_NAME = os.getenv("USER_NAME")
    USER_PASSWORD = os.getenv("USER_PASSWORD")

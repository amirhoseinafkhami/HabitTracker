import os
from pathlib import Path
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    BASE_DIR = Path(__file__).resolve().parent.parent

    DATABASE_NAME = "habits.db"

    DATABASE_PATH = BASE_DIR / DATABASE_NAME

    DEBUG = True

settings = Settings()
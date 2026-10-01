#Configuration variables - Imported from env file
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

class Settings(BaseSettings):
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()



BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
PROFILE_PICS_DIR = MEDIA_DIR / "profile_images"
PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)

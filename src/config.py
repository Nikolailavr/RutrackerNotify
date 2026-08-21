from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

SRC_DIR = Path(__file__).resolve().parent
BASE_PATH = Path(__file__).resolve().parent.parent

class Telegram(BaseModel):
    admin_id: str
    token: str

class Site(BaseModel):
    forum_id: int
    check_interval: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            SRC_DIR / ".env.template",
            SRC_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    telegram: Telegram
    site: Site

settings = Settings()

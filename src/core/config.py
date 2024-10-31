import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings
# from rpws.server import sroots

from core.constants import (
    BASE_DIR,
    ENV_PATH,
    LOG_DIR,
    LOG_FILE,
    LOG_FORMAT,
)


class Settings(BaseSettings):
    """Settings for current project."""

    # name_company: str = "SomeCompany"

    # tg_token: str = "tg_token"

    # postgres_db: str = Field(alias="POSTGRES_DB")
    # postgres_user: str = Field(alias="POSTGRES_USER")
    # postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    # db_host: str = Field(alias="POSTGRES_SERVER")
    # db_port: str = Field(alias="POSTGRES_PORT")

    secret: str = Field(alias="SECRET")

    first_superuser_email: Optional[EmailStr] = Field(
        alias="FIRST_SUPERUSER_EMAIL"
    )
    first_superuser_password: Optional[str] = Field(
        alias="FIRST_SUPERUSER_PASSWORD"
    )

    # admin_user_model: str = Field(alias="ADMIN_USER_MODEL")
    # admin_user_model_username_field: str = Field(
    #     alias="ADMIN_USER_MODEL_USERNAME_FIELD"
    # )
    # admin_secret_key: str = Field(alias="ADMIN_SECRET_KEY")

    # consultate_number: str = Field(alias="CONSULTATE_NUMBER")
    # consultate_url: str = Field(alias="CONSULTATE_URL")
    # consultate_mail: str = Field(alias="CONSULTATE_MAIL")
    # consultate_telegram: str = Field(alias="CONSULTATE_TELEGRAM")

    # drectory_logo_maker: str = Field(alias="DIRECTORY_LOGO_MAKER")
    # drectory_image_equipment: str = Field(alias="DIRECTORY_IMAGE_EQUIPMENT")
    # drectory_pdf: str = Field(alias="DIRECTORY_PDF")

    @property
    def database_url(self) -> str:
        """Return database url from .env ."""
        # return "postgresql+asyncpg://{}:{}@{}:{}/{}"s
        return f"sqlite+aiosqlite://{BASE_DIR}"

    class Config:
        """Config for the meta class in current settings."""

        env_file = ENV_PATH
        extra = "ignore"


def configure_logging() -> None:
    """Configure logging from this project."""
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler: RotatingFileHandler = RotatingFileHandler(
        LOG_FILE, maxBytes=10**6, backupCount=5
    )
    rotating_handler.setFormatter(LOG_FORMAT)
    project_logger = logging.getLogger("bim_web_app_logging")
    project_logger.setLevel(logging.INFO)
    project_logger.addHandler(rotating_handler)
    project_logger.addHandler(logging.StreamHandler())


global sroots: dict[str: str] = {

}

settings = Settings()

configure_logging()

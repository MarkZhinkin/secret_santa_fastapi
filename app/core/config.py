from typing import List, Optional, Literal

from pydantic import BaseSettings, HttpUrl, constr, root_validator
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Config:
        env_file = ".env"

    SECRET_KEY: str
    APP_ENV: Literal["production", "develop"]
    DEBUG_MODE: bool = True

    @root_validator()
    def validate_app_env(cls, values):
        if values['APP_ENV'] == 'production' and values['DEBUG_MODE'] is True:
            raise ValueError('Production mode and Debug mode cannot be activated simultaneously')
        return values

    PROJECT_NAME: str = "secret_santa_python"

    # SENTRY_DSN: Optional[HttpUrl] = None

    DOMAIN: HttpUrl
    FRONTEND_DOMAIN: HttpUrl

    API_PATH: str = "/api"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    SENDGRID_FROM_EMAIL: constr(min_length=1)
    SENDGRID_API_KEY: constr(min_length=1)

    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DATABASE: str

    def get_mysql_connection_string(self) -> str:
        return f"mysql+aiomysql://" \
               f"{self.DB_USERNAME}:" \
               f"{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:" \
               f"{self.DB_PORT}/" \
               f"{ self.DB_DATABASE}?" \
               f"charset=utf8mb4"


settings = Settings()

from functools import lru_cache

from app.core.config import settings, Settings


@lru_cache()
def get_settings() -> Settings:
    return settings

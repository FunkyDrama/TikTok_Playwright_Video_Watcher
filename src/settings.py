from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ініціалізація змінних оточення"""

    TIKTOK_EMAIL: str
    TIKTOK_PASS: str
    SKIP_PERCENT: str
    MAX_VIDEOS: str
    SEARCH_QUERY: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()  # type: ignore

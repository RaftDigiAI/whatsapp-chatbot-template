from pydantic_settings import BaseSettings


class WhatsappBaseSettings(BaseSettings):
    """Apps Base settings"""

    class ConfigDict:
        env_file = ".env"

    APP_VERSION: str
    APP_MODE: str
    APP_CONTAINERIZED: str
    APP_ENABLE_DOCS: bool = True

    APP_LOG_LEVEL: str
    APP_LOG_PATH: str | None = None

    APP_TOKEN: str

    DEFAULT_VERIFY_SSL: bool = True
    DEFAULT_API_RETRY_COUNT: int = 3
    DEFAULT_API_RETRY_START_TIMEOUT: int = 1

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_TIMEOUT: int = 60
    POSTGRES_MIN_CONNECTIONS: int = 2
    POSTGRES_MAX_CONNECTIONS: int = 10

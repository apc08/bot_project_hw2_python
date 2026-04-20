from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app_name: str = "Bot Service"
    env: str = "local"

    # бот
    bot_token: str

    # jwt токены
    jwt_secret: str
    jwt_alg: str = "HS256"

    redis_url: str = "redis://localhost:6379/0"
    token_ttl: int = 432000
    result_ttl: int = 600


    # для celery
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672//"

    # апи ключ
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openai/gpt-3.5-turbo"
    openrouter_site_url: str = "http://localhost:8001"
    openrouter_app_name: str = "Bot Service"


settings = Settings()

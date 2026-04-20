import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt
from fakeredis import FakeAsyncRedis
from unittest.mock import AsyncMock, patch


@pytest.fixture(autouse=True)
def mock_settings():
    from app.core.config import Settings

    settings = Settings(
        app_name="Bot Service Test",
        env="test",
        bot_token="test_bot_token",
        jwt_secret="test-secret-key",
        jwt_alg="HS256",
        redis_url="redis://localhost:6379/0",
        rabbitmq_url="amqp://guest:guest@localhost:5672//",
        openrouter_api_key="test_openrouter_key",
        openrouter_base_url="https://openrouter.ai/api/v1",
        openrouter_model="openai/gpt-3.5-turbo",
        openrouter_site_url="http://localhost:8001",
        openrouter_app_name="Bot Service Test",
        token_ttl=86400,
        result_ttl=300,
    )

    with patch("app.core.config.settings", settings), \
         patch("app.core.jwt.settings", settings), \
         patch("app.infra.redis.settings", settings), \
         patch("app.services.openrouter_client.settings", settings):
        yield settings


@pytest.fixture
async def fake_redis():
    redis_client = FakeAsyncRedis(decode_responses=False)

    with patch("app.infra.redis.get_redis", return_value=redis_client), \
         patch("app.infra.redis_operations.get_redis", return_value=redis_client):
        yield redis_client

    await redis_client.flushdb()
    await redis_client.aclose()


@pytest.fixture
def valid_jwt_token(mock_settings):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=1)

    payload = {
        "sub": "123",
        "role": "user",
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        mock_settings.jwt_secret,
        algorithm=mock_settings.jwt_alg
    )

    return token


@pytest.fixture
def expired_jwt_token(mock_settings):
    now = datetime.now(timezone.utc)
    expire = now - timedelta(hours=1)

    payload = {
        "sub": "123",
        "role": "user",
        "iat": now - timedelta(hours=2),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        mock_settings.jwt_secret,
        algorithm=mock_settings.jwt_alg
    )

    return token


@pytest.fixture
def mock_celery_task():
    mock_task = AsyncMock()
    mock_task.delay = AsyncMock(return_value=AsyncMock(id="test-task-id"))
    return mock_task


@pytest.fixture
def mock_openrouter_response():
    return {
        "id": "gen-test-id",
        "model": "openai/gpt-3.5-turbo",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a test response from LLM"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }

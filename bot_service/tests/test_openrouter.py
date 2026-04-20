import pytest
import respx
from httpx import Response
from app.services.openrouter_client import OpenRouterClient, OpenRouterSyncClient
from app.core.exceptions import OpenRouterError


@pytest.mark.asyncio
@respx.mock
async def test_openrouter_async_client_success(mock_settings, mock_openrouter_response):
    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(200, json=mock_openrouter_response)
    )

    client = OpenRouterClient()
    messages = [{"role": "user", "content": "Test question"}]

    result = await client.chat(messages)
    assert result == "This is a test response from LLM"


@pytest.mark.asyncio
@respx.mock
async def test_openrouter_async_client_api_error(mock_settings):
    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(500, text="Internal Server Error")
    )

    client = OpenRouterClient()
    messages = [{"role": "user", "content": "Test question"}]

    with pytest.raises(OpenRouterError) as exc_info:
        await client.chat(messages)

    assert "500" in str(exc_info.value)


@respx.mock
def test_openrouter_sync_client_success(mock_settings, mock_openrouter_response):
    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(200, json=mock_openrouter_response)
    )

    client = OpenRouterSyncClient()
    messages = [{"role": "user", "content": "Test question"}]

    result = client.chat(messages)
    assert result == "This is a test response from LLM"


@respx.mock
def test_openrouter_sync_client_api_error(mock_settings):
    # rate limit
    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(429, text="Rate limit exceeded")
    )

    client = OpenRouterSyncClient()
    messages = [{"role": "user", "content": "Test question"}]

    with pytest.raises(OpenRouterError) as exc_info:
        client.chat(messages)

    assert "429" in str(exc_info.value)


@respx.mock
def test_openrouter_sync_client_network_error(mock_settings):
    import httpx

    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        side_effect=httpx.RequestError("Network error")
    )

    client = OpenRouterSyncClient()
    messages = [{"role": "user", "content": "Test question"}]

    with pytest.raises(OpenRouterError) as exc_info:
        client.chat(messages)

    assert "failed" in str(exc_info.value).lower()

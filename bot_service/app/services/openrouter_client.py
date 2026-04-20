import logging
import httpx
from app.core.config import settings
from app.core.exceptions import OpenRouterError

logger = logging.getLogger(__name__)

# клиент для openrouter api
class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.openrouter_base_url
        # заголовки для запросов
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
            "Content-Type": "application/json"
        }

    async def chat(self, messages, temperature=0.7):
        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=60.0,
                )

                if response.status_code != 200:
                    error_msg = f"OpenRouter API error: {response.status_code} - {response.text}"
                    raise OpenRouterError(error_msg)

                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return content

            except httpx.RequestError as e:
                raise OpenRouterError(f"OpenRouter request failed: {e}")


# для celery
class OpenRouterSyncClient:
    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
            "Content-Type": "application/json"
        }

    def chat(self, messages, temperature=0.7):
        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature,
        }

        with httpx.Client() as client:
            try:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=60.0,
                )

                if response.status_code != 200:
                    error_msg = f"OpenRouter API error: {response.status_code} - {response.text}"
                    raise OpenRouterError(error_msg)

                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return content


            except httpx.RequestError as e:
                raise OpenRouterError(f"OpenRouter request failed: {e}")

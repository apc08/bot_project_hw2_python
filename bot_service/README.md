# Bot Service

телеграм бот для LLM консультаций через OpenRouter. использует jwt авторизацию от Auth Service, celery для асинхронной обработки.

## как работает

1. юзер получает jwt токен в Auth Service
2. отправляет /token <jwt> боту
3. бот валидирует токен и сохраняет в redis
4. при вопросе - задача идет в RabbitMQ -> Celery -> OpenRouter
5. результат сохрняется в redis, бот делает polling и отвечает


## установка

### докер (рекомендуется)

```bash
cd hw2
cp .env.example .env
# заполни BOT_TOKEN, JWT_SECRET, OPENROUTER_API_KEY

docker compose up -d
docker compose logs -f bot_service_bot
```

### локально

```bash
cd bot_service
uv sync --dev
cp .env.example .env

# нужны redis и rabbitmq
docker compose up -d redis rabbitmq

# в разных терминалах:
uv run uvicorn app.main:app --port 8001
uv run celery -A app.infra.celery_app worker --loglevel=info
uv run python bot.py
```


## команды бота

- /start - привествие
- /token <jwt> - сохранить токен
- /revoke - удалить токен
- /help - помощь


## переменные окружения

```
BOT_TOKEN=...           # от @BotFather
JWT_SECRET=...          # должен совпадть с Auth Service!
REDIS_URL=redis://...
RABBITMQ_URL=amqp://...
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```


## тесты

```bash
uv run pytest
uv run pytest tests/test_jwt.py -v
```

используется fakeredis и respx для моков


## траблшутинг

### бот не отвечает
- проверь логи: `docker compose logs bot_service_bot`
- jwt_secret совпадает?
- токен не истек?

### worker не обрабатывает
- проверь rabbitmq: http://localhost:15672 (guest/guest)
- проверь openrouter api key

### polling timeout
- openrouter перегружен (есть retry 3 раза)
- worker не запущен


## технологии

- aiogram 3.x
- celery + rabbitmq
- redis
- fastapi
- httpx
- python-jose

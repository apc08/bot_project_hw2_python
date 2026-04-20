# Homework 2: LLM бот с jwt авторизацией

Телеграм бот для консультаций через LLM с jwt токенами.

## структура

- **auth_service** - выдача jwt токенов (FastAPI)
- **bot_service** - телеграм бот + celery для обработки запросов

## технологии

- FastAPI
- Telegram Bot (aiogram)
- Celery + RabbitMQ
- Redis
- SQLite
- Docker

## запуск

```bash
cp .env.example .env
# заполни BOT_TOKEN, JWT_SECRET, OPENROUTER_API_KEY

docker compose up -d
```

проверка:
- auth: http://localhost:8000/docs
- бот: @ваш_бот в телеграм

## использование

1. зарегистрируйся в http://localhost:8000/docs (POST /auth/register)
2. получи токен (POST /auth/login)
3. отправь боту /start
4. отправь боту /token <твой_jwt>
5. задавай вопросы боту

## тесты

```bash
cd auth_service && uv run pytest
cd bot_service && uv run pytest
```

## требования

- Python 3.11+
- Docker и docker compose
- Телеграм бот токен от @BotFather
- OpenRouter API ключ

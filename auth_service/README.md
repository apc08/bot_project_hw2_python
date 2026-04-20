# Auth Service

Сервис аутентификации для LLM-консультаций. Выдает jwt токены.

## Технолоогии

- fast API
- SqLite + aiosqlite
- python-jose для jwt
- bcrypt хеширование паролей


## Установка

```bash
cp .env.example .env
# отредактируте JWT_SECRET
uv sync
```

## Запуск

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

сваггер: http://localhost:8000/docs

## API

### POST /auth/register
регистрация пользоваетля

### POST /auth/login
логин, возвращает access_token

### GET /auth/me
профиль по токену (Authorization: Bearer <token>)

### GET /health
статус сервиса

## JWT формат

```
{
  "sub": "user_id",
  "role": "user",
  "iat": ...,
  "exp": ...
}
```

## Структура

```
app/
├── core/        # конфиг, security
├── db/          # модели, сессия
├── schemas/     # pydantic
├── repositories/
├── usecases/
├── api/
└── main.py
```

## Тесты

```bash
uv run pytest
```

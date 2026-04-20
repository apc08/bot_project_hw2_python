# Dockerfile для Auth Service
FROM python:3.11-slim

WORKDIR /app

# Установить uv и curl для healthcheck
RUN pip install --no-cache-dir uv && \
    apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Копировать файлы проекта
COPY pyproject.toml .
COPY app/ ./app/

# Установить зависимости через uv
RUN uv pip install --system --no-cache -e .

# Создать директорию для данных
RUN mkdir -p /data

# Открыть порт
EXPOSE 8000

# Запустить uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

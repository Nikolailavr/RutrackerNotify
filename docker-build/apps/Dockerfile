FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копируем зависимости из корня контекста (./)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Копируем исходный код
COPY src/ ./src/

# Запускаем скрипт
CMD ["uv", "run", "src/main.py"]
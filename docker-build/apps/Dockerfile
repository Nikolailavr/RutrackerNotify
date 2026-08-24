FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /src

# Копируем зависимости из корня контекста (./)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Копируем исходный код
COPY src/ .

# Запускаем скрипт
CMD ["uv", "run", "main.py"]
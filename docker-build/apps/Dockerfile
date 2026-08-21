FROM python:3.14-slim

# Копируем бинарник uv из официального образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Скопируем файлы зависимостей для эффективного кэширования слоев
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Копируем исходный код
COPY . .

CMD ["uv", "run", "main.py"]
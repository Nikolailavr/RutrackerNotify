FROM python:3.14-slim

# Копируем бинарники uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Рабочая директория — корень проекта
WORKDIR /app

# Копируем описания зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen --no-cache

# Копируем весь исходный код
COPY . .

# Запускаем через uv из корня проекта
CMD ["uv", "run", "src/main.py"]
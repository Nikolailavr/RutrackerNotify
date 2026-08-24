FROM python:3.14-slim

# Копируем бинарник uv из официального образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Рабочая директория приложения
WORKDIR /app

# 1. Сначала копируем только конфигурацию зависимостей для кэширования слоев
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# 2. Копируем весь исходный код проекта (включая папку src)
COPY . .

# 3. Указываем точный путь к скрипту запуска
CMD ["uv", "run", "src/main.py"]
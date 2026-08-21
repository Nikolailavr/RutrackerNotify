import asyncio
import logging

from src.bot import send_notification, bot
from src.config import settings
from src.db import is_notified, mark_as_notified, init_db
from src.parser import RutrackerParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


async def check_and_notify(first_run: bool = False):
    logging.info("Проверка новых публикаций...")

    # Вызываем классовый метод парсера
    items = RutrackerParser.fetch_feed()

    if not items:
        logging.info("Новых или актуальных элементов не найдено.")
        return

    new_count = 0
    for item in items:
        if not is_notified(item.topic_id):
            if not first_run:
                await send_notification(item.title, item.link, item.author)
                logging.info(f"Отправлено уведомление: {item.title}")

            mark_as_notified(item.topic_id)
            new_count += 1

    if first_run:
        logging.info(f"Первичный запуск: записано {new_count} существующих тем без отправки уведомлений.")


async def main():
    init_db()
    logging.info("Сервис успешно запущен.")

    # Первичный запуск без отправки спама
    await check_and_notify(first_run=True)

    while True:
        await asyncio.sleep(settings.site.check_interval)
        await check_and_notify(first_run=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        # Корректное закрытие сессии бота при завершении
        asyncio.run(bot.session.close())
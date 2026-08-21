import logging
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings

# Инициализируем бота с дефолтной разметкой HTML
bot = Bot(
    token=settings.telegram.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def send_notification(title: str, link: str, author: str) -> bool:
    """Отправляет уведомление в Telegram-чат админа."""
    clean_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    message = (
        f"🎬 <b>Новая тема на Rutracker!</b>\n\n"
        f"<b>Название:</b> {clean_title}\n"
        f"🔗 <a href='{link}'>Перейти к теме</a>"
    )

    try:
        await bot.send_message(
            chat_id=settings.telegram.admin_id,
            text=message,
            disable_web_page_preview=False
        )
        return True
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения в Telegram: {e}")
        return False
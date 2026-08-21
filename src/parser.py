import logging
import re
from typing import NamedTuple
import feedparser
import requests

from config import settings


class FeedItem(NamedTuple):
    topic_id: str
    title: str
    link: str
    author: str


class RutrackerParser:
    BASE_URL = "https://feed.rutracker.cc/atom/f"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    @classmethod
    def fetch_feed(cls, forum_id: int | None = None) -> list[FeedItem]:
        """Классовый метод для получения и парсинга Atom-ленты форума."""
        target_forum_id = forum_id or settings.site.forum_id
        feed_url = f"{cls.BASE_URL}/{target_forum_id}.atom"

        try:
            response = requests.get(
                feed_url,
                headers={"User-Agent": cls.USER_AGENT},
                timeout=15,
            )
            response.raise_for_status()

            parsed = feedparser.parse(response.content)
            items: list[FeedItem] = []

            # Обрабатываем записи от старых к новым
            for entry in reversed(parsed.entries):
                # Извлекаем ID темы из ссылки viewtopic.php?t=XXXXXX или entry.id
                link = entry.get("link", "")
                topic_id_match = re.search(r"t=(\d+)", link) or re.search(r"/t/(\d+)", entry.id)
                topic_id = topic_id_match.group(1) if topic_id_match else entry.id

                author = entry.get("author", "Неизвестен")

                items.append(
                    FeedItem(
                        topic_id=topic_id,
                        title=entry.title,
                        link=link or entry.id,
                        author=author,
                    )
                )

            return items

        except Exception as e:
            logging.error(f"Ошибка при получении или парсинге ленты Rutracker ({feed_url}): {e}")
            return []
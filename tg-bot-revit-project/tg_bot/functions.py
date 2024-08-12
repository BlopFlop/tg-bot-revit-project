import asyncio
import csv
import logging
from datetime import datetime as dt
from functools import wraps
from pathlib import Path

from telegram import Bot, Update
from telegram.error import InvalidToken
from telegram.ext import ContextTypes

from tg_bot.constants import BASE_DIR, TG_TOKEN


def init_tg_bot(tg_token: str) -> Bot | None:
    """Инициализация телеграм бота."""
    try:
        bot_: Bot = Bot(token=tg_token)
        asyncio.run(asyncio.run(bot_.get_me()))
        logging.info("Телеграм бот инициализирован.")
        return bot_

    except InvalidToken:
        logging.error("Токен переданный в .env неккоректен.")


class DataChat:
    NAME_CSV = "chats.csv"

    def __init__(self, base_dir: Path) -> None:
        self.csv_file: Path = self._get_or_create(base_dir / self.NAME_CSV)

    def _get_or_create(self, path_file: Path) -> Path:
        if not path_file.is_file():
            with open(path_file, mode="w", encoding="utf-8"):
                pass
        return path_file

    def _change_file(self, data: list[str]) -> None:
        csv_path = self._get_or_create(self.csv_file)
        with open(file=csv_path, mode="w", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data)

    def get(self) -> list[int]:
        def set_type_int(item):
            try:
                return int(item)
            except ValueError:
                return None

        none_filter = lambda x: not (x is None)

        csv_path = self._get_or_create(self.csv_file)

        with open(file=csv_path, mode="r", encoding="utf-8") as csv_file:
            data: list[str] = csv_file.read().split(",")
            data: list[int] = list(map(set_type_int, data))
            return list(filter(none_filter, data))

    def add(self, chat_id: int) -> list[int]:
        data: list[int] = self.get()
        if not (chat_id in data):
            data.append(chat_id)
            data = list(map(str, data))
            self._change_file(data)
        return data

    def remove(self, chat_id: int) -> int:
        data: list[int] = self.get()
        if chat_id in data:
            data.remove(chat_id)
            data = list(map(str, data))
            self._change_file(data)
        return data


def send_message_all_chats(bot: Bot, message: str) -> None:
    chat_ids = DataChat(base_dir=BASE_DIR).get()
    if chat_ids:
        for chat_id in chat_ids:
            try:
                bot.send_message(chat_id=chat_id, text=message)
            except Exception:
                logging.warning(
                    f"При отправке сообщения пользователю {chat_id}, "
                    "возникла ошибка."
                )

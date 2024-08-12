import asyncio
import csv
import logging
from datetime import datetime as dt
from functools import wraps
from pathlib import Path

from telegram import Bot
from telegram.error import InvalidToken

from tg_bot.functions import DataChat, send_message_all_chats


def init_tg_bot(tg_token: str) -> Bot | None:
    """Инициализация телеграм бота."""
    try:
        bot_: Bot = Bot(token=tg_token)
        logging.info("Телеграм бот инициализирован.")
        return bot_

    except InvalidToken:
        logging.error("Токен переданный в .env неккоректен.")


def result_cmd_program(base_dir: Path, end_message: str, tg_token: str = ""):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            SEC_IN_MIN: int = 60

            bot = init_tg_bot(tg_token=tg_token)
            tg_mode = kwargs.pop("tg_mode", False)

            time_start = dt.now()

            # if tg_mode and bot:
            #     send_message_all_chats(base_dir, bot, start_meesage)

            result = func(*args, **kwargs)

            time_end = dt.now()
            time_work = (time_end - time_start).seconds // SEC_IN_MIN

            time_work_message = (
                end_message + f" Процесс длился {time_work} минут(ы|у). "
            )
            search_model_message = f"Модели искать по пути {result}"
            result_message = time_work_message + search_model_message

            if tg_mode and bot:
                send_message_all_chats(
                    bot=bot,
                    message=result_message,
                )
            return result

        return wrapper

    return decorator

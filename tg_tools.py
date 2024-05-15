import logging

from telegram import Bot
from telegram.ext import Updater
import telegram


def init_tg_bot(tg_token: str) -> tuple[Bot, Updater] | Exception:
    '''Инициализация телеграм бота.'''
    try:
        bot_: Bot = Bot(token=tg_token)
        updater_: Bot = Updater(token=tg_token)
        return (bot_, updater_)

    except telegram.error.InvalidToken:
        error_message = (
            'Токен переданный в .env неправильный, пожалуйста пересоздайте '
            'файл .env.'
        )
        logging.exception(error_message, stack_info=True)


def send_message(
        bot_: Bot, text: str, chats_id: list[str]) -> None | Exception:
    '''Отправка сообщения ботом в чатик'''
    for chat_id in chats_id:
        try:
            bot_.send_message(int(chat_id), text)
        except Exception:
            logging.warning(f'Чат Id {chat_id} заблокировал тг бота.')

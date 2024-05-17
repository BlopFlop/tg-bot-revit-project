<<<<<<< HEAD
from subprocess import Popen
from pathlib import Path
import logging
import time
import sys

from telegram import ReplyKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, PrefixHandler

from constants import (
    NAME_PROJECT, PATH_DIR_CHECKS_EXE, KEY_JSON_CHAT_ID, TG_TOKEN,
    PATH_CMD_PROGRAM_EXE, PATH_TG_BOT_EXE,

    ARG_RUN_NAWIS, ARG_RUN_FTP, ARG_RUN_PUBLISH, ARG_UPDATE_JSON_SHORT,
    ARG_NAME_ALBUM_SHORT, ARG_RUN_ALBUM, BOT_HELP_MESSAGE, BOT_START_MESSAGE,

    BUTTON_START, BUTTON_HELP, BUTTON_ADD_IN_PROJECT, BUTTON_REMOVE_IN_PROJECT,
    BUTTON_FTP, BUTTON_NAWIS, BUTTON_PUB
)
from tg_tools import init_tg_bot, send_message
from json_data import JSON_OBJ
from utils import check_dir_or_file


class TgBot:
    process_arch: Popen = None
    process_ftp: Popen = None
    process_nawis: Popen = None
    process_pub: Popen = None

    def __init__(self, tg_token) -> None:
        _bot, _updater = init_tg_bot(tg_token=tg_token)

        self._bot: Bot = _bot
        self._updater: Updater = _updater
=======
from os import path
import os
import time

from settings import (
    BOT, PATH_DATA_JSON, RVT_EXTENTION, NAME_SHEET_FTP,
    KEY_JSON_CHAT_ID, KEY_JSON_DIR_PATHS, logging
)
from json_data import JsonFile

JSON_OBJ = JsonFile(PATH_DATA_JSON)
>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9

    def start_updater(self) -> None:
        '''Запуск апдейтера телеграм бота.'''
        self._updater.dispatcher.add_handler(
            CommandHandler(BUTTON_START, self._command_wake_up)
        )
        self._updater.dispatcher.add_handler(
            CommandHandler(BUTTON_HELP, self._command_help)
        )
        self._updater.dispatcher.add_handler(
            CommandHandler(BUTTON_ADD_IN_PROJECT, self._command_add_in_project)
        )
        self._updater.dispatcher.add_handler(
            CommandHandler(
                BUTTON_REMOVE_IN_PROJECT,
                self._command_remove_in_project
            )
        )
        self._updater.dispatcher.add_handler(
            CommandHandler(BUTTON_FTP, self._command_ftp)
        )
        self._updater.dispatcher.add_handler(
            CommandHandler(BUTTON_NAWIS, self._command_nawis)
        )
        self._updater.dispatcher.add_handler(
            CommandHandler(BUTTON_PUB, self._command_publish)
        )
        self._updater.dispatcher.add_handler(
            PrefixHandler(['#'], ['d'], self._command_arch_album)
        )
        self._updater.start_polling(poll_interval=3)
        self._updater.idle()

    def send_message(self, text: str):
        '''Отправка сообщения в телеграм бот.'''
        chats_id: list[str] = JSON_OBJ.get(KEY_JSON_CHAT_ID)
        send_message(self._bot, text=text, chats_id=chats_id)

    def _track_process(self, update, context, track_process: Popen) -> bool:
        '''Трекинг запущенных процессов, предотвращает запуск одних и тех же
        процессов'''
        chat_id = update.effective_chat.id
        if isinstance(track_process, Popen):
            if track_process.poll() is None:
                track_text: str = 'Данный процесс уже запущен.'
                context.bot.send_message(chat_id=chat_id, text=track_text)
                return False
        return True

<<<<<<< HEAD
    def _command_wake_up(self, update, context):
        '''Функция приветствие при запуске программы.'''
        chat = update.effective_chat
        name = update.message.chat.first_name
        button = ReplyKeyboardMarkup(
            [
                [f'/{BUTTON_HELP}'],
                [f'/{BUTTON_ADD_IN_PROJECT}', f'/{BUTTON_REMOVE_IN_PROJECT}'],
                [f'/{BUTTON_FTP}', f'/{BUTTON_NAWIS}', f'/{BUTTON_PUB}'],
            ], resize_keyboard=True
        )
        message = (
            f'Привет {name}, ты в ТГ боте проекта {NAME_PROJECT}.'
        )
        context.bot.send_message(
            chat_id=chat.id, text=message, reply_markup=button
        )
        logging.debug('BotCommand: Вызов команды пробуждения бота.')
        self._command_add_in_project(update, context)

    def _command_help(self, update, context):
        '''Команда для получения информации о функционале бота.'''
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text=BOT_HELP_MESSAGE)

        info_message = (
            'BotCommand: Вызов команды для получения информации о '
            'функционале чат бота'
        )
        logging.info(info_message)

    def _command_add_in_project(self, update, context):
        '''Добавление человека в проект.'''
        chats_id = JSON_OBJ.get(KEY_JSON_CHAT_ID)
=======
def send_message(text) -> None:
    '''Отправка сообщения ботом в чатик'''
    chats_id = JSON_OBJ.get(KEY_JSON_CHAT_ID)

    for chat_id in chats_id:
        try:
            BOT.send_message(int(chat_id), text)
        except Exception:
            logging.warning(f'Чат Id {chat_id} заблокировал тг бота.')
>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9

        chat = update.effective_chat
        message = 'Вы были добавлены в рассылку по проекту.'

<<<<<<< HEAD
        if str(chat.id) in chats_id:
            message = 'Вы уже рассылке'
=======
def check_file(path_dir: str) -> None:
    '''Функция наблоюдает за действиями над
    Revit файлами в необходимой директории'''
    file_info = {}
    while True:
        file_info_now = get_info_file(path_dir)
        if file_info:
            new_files = []
            update_files = []
            delete_files = []

            for file_now_path, time_now_create in file_info_now.items():
                file_name = path.basename(file_now_path)
                if file_now_path not in file_info.keys():
                    new_files.append(file_name)

                elif time_now_create != file_info[file_now_path]:
                    update_files.append(file_name)

            for file_path in file_info.keys():
                if file_path not in file_info_now.keys():
                    file_name = path.basename(file_path)
                    delete_files.append(file_name)

            messages = [
                (new_files, 'В папке проекта FTP появились новые модели: \n'),
                (update_files, 'В папке проекта FTP обновились модели: \n'),
                (delete_files, 'В папке проекта FTP удалили модели: \n'),
            ]

            for name_file, message in messages:
                text = message + '\n'.join(name_file)
                name_file = [
                    name for name in name_file if '_UNI_' not in name
                ]
                if name_file:
                    logging.debug(text)
                    send_message(text)

>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9
        else:
            JSON_OBJ.patch({KEY_JSON_CHAT_ID: [str(chat.id)]})
            info_message = (
                f'Пользователь с id {str(chat.id)} был добавлен в рассылку.'
            )
            logging.info(info_message)

        context.bot.send_message(chat_id=chat.id, text=message)

    def _command_remove_in_project(self, update, context):
        '''Удаление человека из проекта.'''
        chats_id = JSON_OBJ.get(KEY_JSON_CHAT_ID)
        chat = update.effective_chat

        if str(chat.id) in chats_id:
            JSON_OBJ.delete({KEY_JSON_CHAT_ID: str(chat.id)})
            message = 'Вы были удалены из рассылки по проекту.'
            info_message = (
                f'Пользователь с id {str(chat.id)} удалил себя из рассылки.'
            )
            logging.info(info_message)
        else:
            message = 'Вас нет в рассылке'

        context.bot.send_message(chat_id=chat.id, text=message)

    def _command_start_process(
            self, update, context, process: Popen, argument: str) -> None:
        '''Запуск процесса.'''
        popen_args: tuple[Path, str, str] = (
            PATH_CMD_PROGRAM_EXE, argument, ARG_UPDATE_JSON_SHORT
        )
        if self._track_process(update, context, process):
            self.process_ftp = Popen(popen_args)

    def _command_ftp(self, update, context):
        '''Процесс выгрузки моделей на сервер FTP.'''
        self._command_start_process(
            update, context, self.process_ftp, ARG_RUN_FTP
        )

    def _command_nawis(self, update, context):
        '''Команда выгрузки нэвисворкс.'''
        self._command_start_process(
            update, context, self.process_nawis, ARG_RUN_NAWIS
        )

    def _command_publish(self, update, context):
        '''Команда публикации моделей заказчику.'''
        self._command_start_process(
            update, context, self.process_pub, ARG_RUN_PUBLISH
        )

    def _command_arch_album(self, update, context):
        '''Команда архивации моделей после выгрузки альбомов.'''
        name_album = '_'.join(context.args)
        popen_args: tuple[Path, str, str] = (
            PATH_CMD_PROGRAM_EXE, ARG_RUN_ALBUM, ARG_UPDATE_JSON_SHORT,
            ARG_NAME_ALBUM_SHORT, name_album
        )
        if self._track_process(update, context, self.process_arch):
            self.process_ftp = Popen(popen_args)


if __name__ == '__main__':
<<<<<<< HEAD
    except_message = (
        f'Файла {PATH_DIR_CHECKS_EXE.name} нет в директории с ботом.'
    )
    check_dir_or_file(PATH_DIR_CHECKS_EXE, except_message)
    dir_checker_process: Popen = Popen((PATH_DIR_CHECKS_EXE))
    except_message: str = (
        f'Файла {PATH_CMD_PROGRAM_EXE.name} нет в директории с ботом.'
    )
    check_dir_or_file(PATH_CMD_PROGRAM_EXE, except_message=except_message)
    telegram_bot: TgBot = TgBot(tg_token=TG_TOKEN)
    telegram_bot.send_message(BOT_START_MESSAGE)
    try:
        telegram_bot.start_updater()
    except Exception:
        dir_checker_process.kill()
        Popen((PATH_TG_BOT_EXE))
        time.sleep(30)
        sys.exit()
=======
    print('Ты в программе бота, для Revit проекта.')

    debug_message = 'tg_bot запущен.'
    logging.debug(debug_message)
    send_message(
        'Привет, меня запустили, нажми кнопку /start, для обновления кнопок.'
    )
    path_dir = JSON_OBJ.get(KEY_JSON_DIR_PATHS).get(NAME_SHEET_FTP)
    check_file(path_dir)
>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9

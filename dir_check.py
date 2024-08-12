from os import path
from pathlib import Path
import os
import time
import logging

from telegram import Bot

from cmd_revit_program.core.constants import (
    RVT_EXTENTION, TG_TOKEN
)
from cmd_program import project
from cmd_revit_program.loader.functions import get_file_from_extention
from telegram_revit_project.functions import send_message_all_chats
from telegram_revit_project import TgBot


def get_info_file(path_dir: str) -> dict[str: int]:
    '''Получение информации о файле'''
    files = {}
    for file in get_file_from_extention(path_dir, RVT_EXTENTION):
        time_file = (
            path.getctime(file)
            + path.getatime(file)
            + path.getmtime(file)
        )
        files[file] = time_file
    return files


def check_file(bot_: Bot, path_dir: str) -> None:
    '''Функция наблоюдает за действиями над
    Revit файлами в необходимой директории'''
    file_info = {}
    while True:
        try:
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
                    (new_files, 'В папке проекта FTP появились модели: \n'),
                    (update_files, 'В папке проекта FTP обновили модели: \n'),
                    (delete_files, 'В папке проекта FTP удалили модели: \n'),
                ]

                for name_file, message in messages:
                    text = message + '\n'.join(name_file)
                    name_file = [
                        name for name in name_file if '_UNI_' not in name
                    ]
                    if name_file:
                        logging.debug(text)
                        send_message_all_chats(bot_, message=text)

            else:
                logging.info('Папка пуста, либо это первый запуск программы.')
            file_info = {key: item for key, item in file_info_now.items()}
        except Exception as ex:
            logging.error(ex('При осмотре директории произошла ошибка'))
            continue
        time.sleep(120)


if __name__ == '__main__':
    debug_message = 'dir_checker запущен.'
    logging.debug(debug_message)
    bot_: Bot = TgBot(TG_TOKEN).bot
    path_dir = project.ftp_dir.shared
    check_file(bot_, path_dir)

from os import path
import os
import time
import logging

from telegram import Bot

from constants import (
    RVT_EXTENTION, NAME_SHEET_FTP, TG_TOKEN,
    KEY_JSON_CHAT_ID, KEY_JSON_DIR_PATHS
)
from configs import configure_logging
from tg_tools import send_message, init_tg_bot
from json_data import JSON_OBJ


def get_info_file(path_dir: str) -> dict[str: int]:
    '''Получение информации о файле'''
    files = {}
    for dirpath, dirnames, filenames in os.walk(path_dir):
        for file_name in filenames:
            if RVT_EXTENTION in file_name:
                file = path.join(dirpath, file_name)
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
                        bot_: Bot = init_tg_bot(tg_token=TG_TOKEN)[0]
                        chats_id = JSON_OBJ.get(KEY_JSON_CHAT_ID)
                        send_message(bot_, text, chats_id)

            else:
                print('Папка пуста, либо это первый запуск программы.')
            file_info = {key: item for key, item in file_info_now.items()}
        except Exception as ex:
            logging.error(ex('При осмотре директории произошла ошибка'))
            print('Произошла ошибка...')

        time.sleep(30)


if __name__ == '__main__':
    configure_logging()
    debug_message = 'dir_checker запущен.'
    logging.debug(debug_message)
    JSON_OBJ.update_json_from_google_tab()
    path_dir = JSON_OBJ.get(KEY_JSON_DIR_PATHS).get(NAME_SHEET_FTP)
    check_file(path_dir)

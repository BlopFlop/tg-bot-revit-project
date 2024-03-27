from os import path
import os
import time
import json
import logging

from google_services.tab import get_dir_paths
from settings.constants import (
    BOT, PATH_CHATS_JSON, FILE_NAME_LOG, RVT_EXTENTION, NAME_SHEET_FTP
)


logging.basicConfig(
    handlers=[logging.FileHandler(FILE_NAME_LOG, 'a', 'utf-8')],
    level=logging.DEBUG,
    format='%(asctime)s, [%(levelname)s] %(message)s',
)


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


def get_chat_ids():
    '''Получение всех айди чатов'''
    with open(PATH_CHATS_JSON, 'r') as json_file:
        chat = json.load(json_file)
    return chat.keys()


def send_message(text) -> None:
    '''Отправка сообщения ботом в чатик'''
    data_id = get_chat_ids()

    for chat_id in data_id:
        BOT.send_message(int(chat_id), text)


def check_file(path_dir: str) -> None:
    '''Функция наблоюдает за действиями над
    Revit файлами необходимой в директории'''
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
                    send_message(text)

        else:
            print('Папка пуста, либо это первый запуск программы.')

        file_info = {key: item for key, item in file_info_now.items()}
        time.sleep(30)


if __name__ == '__main__':
    print('Ты в программе бота, для Revit проекта.')
    send_message(
        'Привет, меня запустили, нажми кнопку /start, для обновления кнопок.'
    )
    path_dir = get_dir_paths().get(NAME_SHEET_FTP)
    check_file(path_dir)

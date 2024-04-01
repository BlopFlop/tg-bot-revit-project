from datetime import datetime as dt
import os
import logging
import sys
import time

import shutil

from google_tab import get_archive_paths
from tg_bot import send_message
from env_file import flush_print

from settings import (
    ARCH_START_MESSAGE, ARCH_END_MESSAGE, EXTENSION_FILE,
    DEPLOY_ALBUM_START_MESSAGE, DEPLOY_ALBUM_END_MESSAGE,
    DATE_MASK
)


time_start = dt.now()

logging.basicConfig(
    level=logging.INFO,
    filename='AddAllModelInArch_log.log',
    filemode='w',
    format="%(asctime)s %(levelname)s %(message)s"
)


def get_path_for_extension(path_dir: str) -> list[str]:
    '''Получение пути файлов с необходимым расширением в директории.'''
    result_list = []
    for addres, dirs, files in os.walk(path_dir):
        for name in files:
            if name.split('.')[-1] in EXTENSION_FILE:
                result_list.append(os.path.join(addres, name))
    return result_list


def make_dir(path: str, name_dir: str) -> str:
    '''Создание папки для копирования туда файлов'''
    name_args = [time_start.strftime(DATE_MASK), name_dir]

    if len(sys.argv) > 1:
        name_args.append(sys.argv[1])

    name_folder = '_'.join(name_args)
    path_dir = os.path.join(path, name_folder)

    try:
        os.mkdir(path_dir)
    except FileExistsError:
        warning_message = f'Папка << {path_dir} >> уже существует'
        print(warning_message)
        logging.info(warning_message)
    return path_dir


def copy_files_in_dir(first_path: str, path_dir: str) -> None:
    '''Копирование файлов из директории.'''
    if os.path.exists(first_path):
        name_file = os.path.basename(first_path)
        path_return = shutil.copy2(first_path, path_dir)
        if path_return:
            flush_print('Файл скопирован ' + f"<<< {name_file} >>>")
            print('_' * 100)


def create_arch():
    db_data = get_archive_paths()
    for first_path_dir, second_path_dir, name_dir in db_data:
        files = get_path_for_extension(first_path_dir)
        if files:
            path_dir = make_dir(second_path_dir, name_dir)
            for file in files:
                copy_files_in_dir(file, path_dir)
        info_message = f'В папке <<{first_path_dir}>> нет файлов.'
        print(info_message)
        logging.info(info_message)

    print(
        'Выгрузка закончена, '
        f'время выгрузки {dt.now() - time_start}'
    )


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            send_message(DEPLOY_ALBUM_START_MESSAGE + f' Альбом {sys.argv[1]}')
            create_arch()
            send_message(DEPLOY_ALBUM_END_MESSAGE)
        else:
            send_message(ARCH_START_MESSAGE)
            create_arch()
            send_message(ARCH_END_MESSAGE)
    except Exception:
        except_message = 'При архивации произошла ошибка.'
        print(except_message)
        logging.error(except_message)
        time.sleep(5)
    sys.exit()

from datetime import datetime as dt
from multiprocessing import Pool
import os
import re
import subprocess
import shutil
import sys

from google_services.tab import get_nwc_paths, get_nwd_paths
from tg_bot import send_message

from settings.constants import (
    NAWIS_OR_REVIT_VERSION, PATH_NAWIS_FTR, PATH_NAWIS_ROAMER, FIRST_FLAG,
    SECOND_FLAG, THIRD_FLAG, NWF_EXTENTION, NWC_EXTENTION,
    NWD_EXTENTION, FLAG_NWD, PATH_COPY_DIR, COUNT_RUN_MULTIPROSECCING,
    SECONDS_IN_MINUTE, DATE_NOW
)


def get_path_work_dir(file_path: str = __file__) -> str:
    '''Получение пути рабочей директории'''
    number = re.search(r'\w+.py', file_path).span()[0]
    return file_path[0: number]


def search_file(path_dir: str, file_extension: str) -> str:
    '''Поиск файлов в папке с необходимым разширением'''
    result_file_in_dir = []
    for root, dirs, files in os.walk(path_dir):
        for filename in files:
            if file_extension in filename:
                result_file_in_dir.append(
                    os.path.join(root, filename)
                )
    if result_file_in_dir:
        return result_file_in_dir


def get_path_extension_file(path_rvt_file: str, file_extension: str) -> str:
    """Получение необходимого расширения файла."""
    name_nwf_file = (
        os.path.basename(path_rvt_file).split('.')[0] + file_extension
    )
    return os.path.join(os.path.dirname(path_rvt_file), name_nwf_file)


def create_and_get_path_txt_file(path_rvt_file: str) -> str:
    """Создание, и получение пути необходимого текстового файла."""
    path_txt_file = path_rvt_file.replace('.rvt', '.txt')
    txt_file = open(path_txt_file, 'w+', encoding='utf-8')
    txt_file.write(path_rvt_file)
    txt_file.close()
    return path_txt_file


def start_create_nawis_file(path_txt_file: str, path_nwf: str) -> str:
    """Запуск утилиты для выгрузки файлов Navisworks."""
    subprocess.run(
        (
            PATH_NAWIS_FTR, FIRST_FLAG, path_txt_file, SECOND_FLAG,
            path_nwf, THIRD_FLAG, NAWIS_OR_REVIT_VERSION
        )
    )
    return get_path_extension_file(path_nwf, NWC_EXTENTION)


def rename_file(path_file: str, rename_name: str) -> str:
    """Переименование файлов"""
    extention_file = '.' + os.path.basename(path_file).split('.')[-1]
    rename_path = (
        os.path.join(os.path.dirname(path_file), rename_name + extention_file)
    )
    os.rename(path_file, rename_path)
    return rename_path


def main(path_files: tuple[str, str, str]) -> str:
    path_rvt, move_dir_path, name = path_files

    if all((path_rvt, move_dir_path, name)):
        copy_dir = (
            os.path.join(
                PATH_COPY_DIR, os.path.basename(path_rvt).split('.')[0]
            )
        )
        try:
            os.makedirs(copy_dir)
            path_rvt = shutil.copy2(path_rvt, copy_dir)
            paht_txt = create_and_get_path_txt_file(path_rvt)
            path_nwc = get_path_extension_file(path_rvt, NWF_EXTENTION)
            create_path_nwc = start_create_nawis_file(paht_txt, path_nwc)
            rename_file_nwc = rename_file(create_path_nwc, name)
            shutil.copy(rename_file_nwc, move_dir_path)
        except Exception:
            name_nwc = os.path.basename(create_path_nwc)
            print(f'При выгрузке файла {name_nwc} произошла ошибка')
        shutil.rmtree(copy_dir)


def start_create_file_nwc(path_files: list[str]) -> None | FileExistsError:
    path_work_dir = PATH_COPY_DIR
    try:
        os.mkdir(path_work_dir)
    except FileExistsError:
        shutil.rmtree(path_work_dir)
        os.mkdir(path_work_dir)
    p = Pool(processes=COUNT_RUN_MULTIPROSECCING)
    p.map(main, path_files)


def create_nwd_file(end_path_nwd: str, source_path_nwf: str) -> str:
    '''Создание nwd файла'''
    subprocess.run((
        PATH_NAWIS_ROAMER, FLAG_NWD, end_path_nwd, source_path_nwf
    ))


def start_create_file_nwd(source_path_nwf: str, load_dir: str) -> str:
    '''Старт создания nawis файла'''
    time_name = str(dt.now().strftime(DATE_NOW + '_%H-%M'))
    name_file = (
        ''.join(os.path.basename(source_path_nwf).split('.')[:-1])
        + time_name + NWD_EXTENTION
    )
    end_path_nwd = os.path.join(load_dir, name_file)
    create_nwd_file(end_path_nwd, source_path_nwf)
    return os.path.join(load_dir, name_file)


if __name__ == '__main__':
    time_work = dt.now()
    try:
        start_create_file_nwc(get_nwc_paths())
    except PermissionError:
        except_message = (
            'При выгрузке Navisworks, произошла ошибка '
            'пожалуйста попросите специалиста перезагрузить бота. \n'
            'Причина: При прошлой выгрузке в Navisworks, процесс завершился '
            'раньше выгрузки, тем самым заняв все побочные файлы. Программа '
            'не может создать побочные файлы для создания файлов Navisworks.'
        )
        print(except_message)
        send_message(except_message)
        sys.exit()
    source_path_nwf, load_dir = get_nwd_paths()
    path_file_nwd = start_create_file_nwd(source_path_nwf, load_dir)
    print(path_file_nwd)
    time_work = (dt.now() - time_work).seconds // SECONDS_IN_MINUTE
    message = (
        'Файлы Nawisworks выгружены.\n'
        f'Время выгрузки составило: {time_work} минут(ы|у).'
    )
    send_message(message)
    sys.exit()

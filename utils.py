from pathlib import Path
import time
# import winapps
import shutil
import logging

from constants import (
    SECONDS_IN_HOUR, SECONDS_IN_DAY, SECONDS_IN_WEEK, SECONDS_IN_MONTH
)


def check_dir_or_file(
        file_path: Path, except_message: str) -> None | Exception:
    '''Проверка существует ли директория ли файл'''
    if not (file_path.is_file() or file_path.is_dir()):
        logging.error(except_message, exc_info=True, stack_info=True)
        raise FileNotFoundError(except_message)


def make_achive(
        root_dir: Path,
        arch_dir_path: Path,
        format_: str = 'zip') -> Path:
    '''Формирование архива'''

    return Path(shutil.make_archive(
        base_name=arch_dir_path,
        format=format_,
        root_dir=root_dir,
        base_dir=arch_dir_path.name
    ))


def check_file_creation_date(file: Path, period: str = 'week') -> bool:
    '''Проверка даты создания файла, исходя из временного периода.'''
    CORRECT_COEFFICIENT: float = 1.2
    SECONDS_PERIOD: dict[str: int] = {
        'hour': SECONDS_IN_HOUR * CORRECT_COEFFICIENT,
        'day': SECONDS_IN_DAY * CORRECT_COEFFICIENT,
        'week': SECONDS_IN_WEEK * CORRECT_COEFFICIENT,
        'month': SECONDS_IN_MONTH * CORRECT_COEFFICIENT,
    }
    ctime_now: float = time.time()
    ctime_file: float = file.lstat().st_mtime
    if (ctime_now - ctime_file) > SECONDS_PERIOD.get(period):
        logging.info(
            f'Файл << {file.name} >> старый, он не будет'
            ' копироваться.'
        )
        return False
    return True


def get_file_from_extention(
        source_dir: Path, extention: str = None) -> list[Path]:
    '''Рекурсивное получение путей до файлов в древе директориий.'''
    pattern = '*' if extention is None else f'*{extention}'
    return [Path(file) for file in source_dir.rglob(pattern)]

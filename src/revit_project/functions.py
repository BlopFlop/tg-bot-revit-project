from src.core.exceptions import DirectoryNotFoundError, ProgramNotSetup

import logging
import shutil
from multiprocessing import Pool
from pathlib import Path
from subprocess import run
from typing import Callable

import rpws
import rpws.exceptions
from rpws import RevitServer
from rpws.models import ModelInfo
from rpws.server import sroots

from src.core.constants import PATH_REVIT_RST


class control_workdir:
    def __init__(self, path_dir: Path) -> None:
        self.path_dir = path_dir

    def __enter__(self) -> Path:
        self.path_dir.mkdir(exist_ok=True)
        return self.path_dir

    def __exit__(self, *args) -> None:
        shutil.rmtree(self.path_dir, ignore_errors=True)


def get_file_from_extention(
    source_dir: Path, extention: str = None
) -> list[Path]:
    """Рекурсивное получение путей до файлов в древе директориий."""
    DOT_SYMBOL: str = "."

    if DOT_SYMBOL not in extention:
        except_message: str = (
            "Расширение файла должно быть обязательно"
            f" с точкой, а передан {extention}."
        )
        raise ValueError(except_message)

    pattern = "*" if extention is None else f"*{extention}"
    return [Path(file) for file in source_dir.rglob(pattern)]


def hascyr(s: str) -> bool:
    RU_WORDS: set = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    return RU_WORDS.intersection(s.lower()) != set()


def get_support_version_revit(
        start_age_ver: int, end_age_ver: int
) -> dict[str: str]:
    URL_PATH_FROM_RS: str = (
        "/RevitServerAdminRESTService{}/AdminRESTService.svc"
    )
    sroots = {
        str(version): URL_PATH_FROM_RS.format(version)
        for version in range(start_age_ver, end_age_ver+1)
    }
    return sroots


def pool_func(start_process_func: Callable, pool_items: list) -> None:
    COUNT_PROCESSES: int = 6
    with Pool(COUNT_PROCESSES) as pool:
        pool.map(start_process_func, pool_items)


def get_file_from_extention(
    source_dir: Path, extention: str = None
) -> list[Path]:
    """Рекурсивное получение путей до файлов в древе директориий."""
    DOT_SYMBOL: str = "."

    if DOT_SYMBOL not in extention:
        except_message: str = (
            "Расширение файла должно быть обязательно"
            f" с точкой, а передан {extention}."
        )
        raise ValueError(except_message)

    pattern = "*" if extention is None else f"*{extention}"
    return [Path(file) for file in source_dir.rglob(pattern)]


def make_achive(
    root_dir: Path, arch_dir_path: Path, format_: str = "zip"
) -> Path:
    """Формирование архива"""

    return Path(
        shutil.make_archive(
            base_name=arch_dir_path,
            format=format_,
            root_dir=root_dir,
        )
    )


def get_all_models_in_revit_server(revit_server_name: str) -> list[ModelInfo]:
    """Get all models in revit server."""
    result_model_items = []

    try:
        for version in sroots:
            revit_server = RevitServer(revit_server_name, version)

            try:
                revit_server.getinfo()
            except rpws.exceptions.ServerFileNotFound:
                continue

            for items in revit_server.walk():
                models: list[ModelInfo] = items[3]
                if models:
                    for model in models:
                        result_model_items.append(model)
    except Exception:
        warning_message = (
            "Переданное имя ревит сервера неккоректное, или такого ревит"
            " сервера не существует в сети пк."
        )
        logging.warning(warning_message)

    return result_model_items


def get_model_for_mask(
    all_revit_models: list[ModelInfo], search_pattern: str
) -> list[ModelInfo]:
    """Get models for support mask."""
    WORK_REVIT_SERVER_DIRECTORY = "wip"

    result_model_items = []

    for revit_model in all_revit_models:
        revit_model_name = revit_model.name
        revit_model_path = str(revit_model.path)

        if (
            search_pattern in revit_model_name
            and WORK_REVIT_SERVER_DIRECTORY in revit_model_path.lower()
        ):
            result_model_items.append(revit_model)

    return result_model_items


def command_run_model_in_rs(
    server_name: str, source_path_model: Path, end_path_model: Path
) -> Path | None:
    """Старт выгрузки моделей из ревит сервера"""
    RST_COMMAND_CREATE_LOCAL_MODEL = "l"
    RST_FLAG_SERVER = "-d"
    RST_FLAG_DESTINATION = "-s"
    RST_FLAG_OVERWRITE = "-o"

    name_model = source_path_model.name

    logging.info(f"Старт выгрузки моделей << {name_model} >>")
    try:
        run(
            [
                PATH_REVIT_RST,
                RST_COMMAND_CREATE_LOCAL_MODEL,
                source_path_model,
                RST_FLAG_DESTINATION,
                server_name,
                RST_FLAG_SERVER,
                end_path_model,
                RST_FLAG_OVERWRITE,
            ]
        )
        logging.info(f"Модель << {name_model} >> выгружена.")
        return end_path_model

    except Exception:
        error_message = (
            f"<<< Произошла ошибка при выгрузке модели {name_model}"
            " она не будет выгружена. >>>"
        )
        logging.error(error_message)


def get_or_create_dir(path_dir: Path) -> Path:
    if path_dir.is_file():
        except_message = (
            "Произошла ошибка вы передали в функцию путь "
            "до файла, а не директории."
        )
        logging.error(except_message, stack_info=True)
        raise DirectoryNotFoundError(except_message)

    if not path_dir.is_dir():
        path_dir.mkdir()
        info_message = f"Директория {path_dir.name} создана"
        logging.info(info_message)

    return path_dir


def is_dir_or_file(
    path: Path, confirm_message: str, except_message: str
) -> None | ProgramNotSetup:
    if not (path.is_dir() or path.is_file()):
        logging.error(except_message)
        raise ProgramNotSetup(except_message)

    logging.info(confirm_message)

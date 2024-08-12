import logging
import shutil
from multiprocessing import Pool
from pathlib import Path
from subprocess import run
from typing import Callable, Final

import rpws
import rpws.exceptions
from rpws import RevitServer
from rpws.models import ModelInfo
from rpws.server import sroots

from cmd_revit_program.core.constants import (
    NWC_EXTENTION,
    NWF_EXTENTION,
    PATH_NAWIS_FTR,
    PATH_NAWIS_ROAMER,
    PATH_REVIT_RST,
    PATH_WORKDIR_NAWIS,
    RVT_EXTENTION,
)

# from transliterate import translit


class control_workdir:
    def __init__(self, path_dir: Path) -> None:
        self.path_dir = path_dir

    def __enter__(self) -> Path:
        self.path_dir.mkdir(exist_ok=True)
        return self.path_dir

    def __exit__(self, *args) -> None:
        shutil.rmtree(self.path_dir, ignore_errors=True)


def hascyr(s: str) -> bool:
    RU_WORDS: set = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    return RU_WORDS.intersection(s.lower()) != set()


def pool_func(start_process_func: Callable, pool_items: list) -> None:
    COUNT_PROCESSES: int = 6
    with Pool(COUNT_PROCESSES) as pool:
        pool.map(start_process_func, pool_items)


def start_nwc_process_from_pool(file) -> None:
    file.load_rvt_to_nwc()


def start_backup_process_from_pool(file) -> None:
    file.copy_to_backup()


def start_ftp_process_from_pool(file) -> None:
    file.copy_to_ftp()


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
            # base_dir=arch_dir_path.name,
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


def _mk_txt_from_rvt(path_rvt_file: Path) -> Path:
    """Формирование txt из rvt файла."""
    name_txt_file: Path = path_rvt_file.name.replace(RVT_EXTENTION, ".txt")
    path_txt_file: Path = path_rvt_file.parent / name_txt_file

    with open(path_txt_file, mode="w", encoding="utf-8") as txt_file:
        logging.info(f"txt файл, создан по пути {path_txt_file}.")
        txt_file.write(str(path_rvt_file))

    return path_txt_file


def transliterate(name: str):
    translist_items = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "cz",
        "ш": "sh",
        "щ": "scz",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "u",
        "я": "ja",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "E",
        "Ж": "ZH",
        "З": "Z",
        "И": "I",
        "Й": "I",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "H",
        "Ц": "C",
        "Ч": "CZ",
        "Ш": "SH",
        "Щ": "SCH",
        "Ъ": "",
        "Ы": "y",
        "Ь": "",
        "Э": "E",
        "Ю": "U",
        "Я": "YA",
        ",": "",
        "?": "",
        " ": "_",
        "~": "",
        "!": "",
        "@": "",
        "#": "",
        "$": "",
        "%": "",
        "^": "",
        "&": "",
        "*": "",
        "(": "",
        ")": "",
        "-": "",
        "=": "",
        "+": "",
        ":": "",
        ";": "",
        "<": "",
        ">": "",
        "'": "",
        '"': "",
        "\\": "",
        "/": "",
        "№": "",
        "[": "",
        "]": "",
        "{": "",
        "}": "",
        "ґ": "",
        "ї": "",
        "є": "",
        "Ґ": "g",
        "Ї": "i",
        "Є": "e",
        "—": "",
    }
    for key in translist_items:
        if key in name:
            name = name.replace(key, translist_items[key])
    return name


def command_run_export_rvt_to_nwc(source_path: Path, end_dir_path: Path):
    """Старт выгрузки в формат nwc."""

    VER_NAWIS_2019: Final[str] = "2019"

    FTR_FIRST_FLAG: Final[str] = r"/i"
    FTR_SECOND_FLAG: Final[str] = r"/of"
    FTR_THIRD_FLAG: Final[str] = r"/version"

    if RVT_EXTENTION not in source_path.name:
        except_message = (
            "Возникла ошибка при создании txt файла, в функцифю передан "
            + f"путь {source_path}, без расширения {RVT_EXTENTION}."
        )
        logging.error(except_message, exc_info=True)
        raise ValueError(except_message)

    str_in_ru_sybmols = hascyr(str(source_path.stem))

    if str_in_ru_sybmols:
        translit_name_dir = transliterate(source_path.stem)
        copy_dir = PATH_WORKDIR_NAWIS / str(translit_name_dir)
    else:
        copy_dir = PATH_WORKDIR_NAWIS / source_path.stem

    if not copy_dir.is_dir():
        copy_dir.mkdir(exist_ok=True)

    source_path = Path(shutil.copy2(source_path, copy_dir))

    if str_in_ru_sybmols:
        translit_name_revit_file = transliterate(source_path.name)
        rename_path = source_path.resolve().parent / translit_name_revit_file
        source_path = source_path.rename(rename_path)

    path_txt = _mk_txt_from_rvt(source_path)

    name_nwf: str = source_path.stem + NWF_EXTENTION
    path_nwf: Path = copy_dir / name_nwf

    name_nwc: str = source_path.stem + NWC_EXTENTION
    path_nwc: Path = copy_dir / name_nwc

    info_message = "Запуск утилиты для выгрузки файла " + source_path.name
    logging.info(info_message)

    command_items: tuple[str] = (
        PATH_NAWIS_FTR,
        FTR_FIRST_FLAG,
        path_txt,
        FTR_SECOND_FLAG,
        path_nwf,
        FTR_THIRD_FLAG,
        VER_NAWIS_2019,
    )

    run(command_items)

    if not path_nwc.is_file():
        warning_message = (
            f"При выгрузке модели {source_path.name} в .nwc возникла ошибка"
        )
        logging.warning(warning_message)
    else:
        end_dir_path: Path = end_dir_path.parent / (
            end_dir_path.stem + path_nwc.suffix
        )
        shutil.copy(path_nwc, end_dir_path)

    shutil.rmtree(copy_dir, ignore_errors=True)
    return end_dir_path


def run_load_nwd(nwd_path: Path, nwf_path: Path) -> Path:
    """Старт выгрузки моделей в формат nwd"""
    ROAMER_FLAG_NWD: str = "-nwd"

    command_items = (PATH_NAWIS_ROAMER, ROAMER_FLAG_NWD, nwd_path, nwf_path)
    run(command_items)
    debug_message = f"Сформирован nwd файл {nwd_path.name}"
    logging.debug(debug_message)
    return nwd_path

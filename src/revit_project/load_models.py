import logging
from pathlib import Path
from typing import Final
from shutil import copy2, rmtree
from subprocess import run

from transliterate import translit

from src.revit_project.functions import hascyr
from src.core.constants import RVT_EXTENTION, NWF_EXTENTION, NWC_EXTENTION


def _mk_txt_from_rvt(path_rvt_file: Path) -> Path:
    """Формирование txt из rvt файла."""
    name_txt_file: Path = path_rvt_file.name.replace(RVT_EXTENTION, ".txt")
    path_txt_file: Path = path_rvt_file.parent / name_txt_file

    with open(path_txt_file, mode="w", encoding="utf-8") as txt_file:
        logging.info(f"txt файл, создан, путь {path_txt_file}.")
        txt_file.write(str(path_rvt_file))

    return path_txt_file


def load_model_in_rs(
    paht_revit_rst: Path,
    server_name: str,
    source_path_model: Path,
    end_path_model: Path
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
                paht_revit_rst,
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


def export_rvt_to_nwc(
    path_nawis_ftr: Path,
    local_nawisworks_path: Path,
    source_path: Path,
    end_dir_path: Path
) -> Path:
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
        translit_name_dir = translit(source_path.stem, 'ru')
        copy_dir = local_nawisworks_path / str(translit_name_dir)
    else:
        copy_dir = local_nawisworks_path / source_path.stem

    if not copy_dir.is_dir():
        copy_dir.mkdir(exist_ok=True)

    source_path = Path(copy2(source_path, copy_dir))

    if str_in_ru_sybmols:
        rename_path = source_path.resolve().parent / translit_name_dir
        source_path = source_path.rename(rename_path)

    path_txt = _mk_txt_from_rvt(source_path)

    name_nwf: str = source_path.stem + NWF_EXTENTION
    path_nwf: Path = copy_dir / name_nwf

    name_nwc: str = source_path.stem + NWC_EXTENTION
    path_nwc: Path = copy_dir / name_nwc

    info_message = "Запуск утилиты для выгрузки файла " + source_path.name
    logging.info(info_message)

    command_items: tuple[str] = (
        path_nawis_ftr,
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
        copy2(path_nwc, end_dir_path)

    rmtree(copy_dir, ignore_errors=True)
    return end_dir_path


def export_nwf_to_nwd(
    path_nawis_roamer: Path,
    nwd_path: Path,
    nwf_path: Path
) -> Path | None:
    """Старт выгрузки моделей в формат nwd"""
    ROAMER_FLAG_NWD: str = "-nwd"

    if not nwf_path.is_file():
        warning_message: str = (
            f"Файл {nwd_path.name} не был создан, "
            f"т.к. модели {nwf_path.name} не существует"
        )
        logging.warning(warning_message)
        return None

    command_items = (path_nawis_roamer, ROAMER_FLAG_NWD, nwd_path, nwf_path)
    run(command_items)
    debug_message = f"Сформирован nwd файл {nwd_path.name}"
    logging.debug(debug_message)
    return nwd_path

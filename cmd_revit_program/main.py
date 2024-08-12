import argparse
import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import Callable

from cmd_revit_program.core.constants import (
    ARG_NAME_ALBUM_LONG,
    ARG_NAME_ALBUM_SHORT,
    ARG_START_ARCH,
    ARG_START_BACKUP,
    ARG_START_FTP,
    ARG_START_NAWIS,
    ARG_START_PUBLISH,
    ARG_TG_MODE_LONG,
    ARG_TG_MODE_SHORT,
    ARGPARS_HELP_LOAD_MODEL,
    ARGPARS_HELP_NAME_ALBUM_MODEL,
    ARGPARS_HELP_TG_MODE,
    BASE_DIR,
    END_LOAD_MESSAGE_ARCH,
    END_LOAD_MESSAGE_BACKUP,
    END_LOAD_MESSAGE_FTP,
    END_LOAD_MESSAGE_NAWISWORKS,
    END_LOAD_MESSAGE_PUBLISH,
    TG_TOKEN,
)
from cmd_revit_program.core.tg_bot import result_cmd_program
from cmd_revit_program.loader import Project


@result_cmd_program(
    base_dir=BASE_DIR,
    end_message=END_LOAD_MESSAGE_ARCH,
    tg_token=TG_TOKEN,
)
def start_arch(project: Project, name_album: str = None) -> Path:
    """Архивация проекта."""
    project.load_in_backup()
    project.load_in_ftp()
    project.load_in_nwc()
    project.load_in_nwd()
    project.load_in_arch(name_album)
    return project.arch_dir.arch


@result_cmd_program(
    base_dir=BASE_DIR,
    end_message=END_LOAD_MESSAGE_BACKUP,
    tg_token=TG_TOKEN,
)
def start_backup(project: Project) -> Path:
    """Бэкап Revit моделей."""
    project.load_in_backup()
    return project.arch_dir.backup


@result_cmd_program(
    base_dir=BASE_DIR,
    end_message=END_LOAD_MESSAGE_NAWISWORKS,
    tg_token=TG_TOKEN,
)
def start_nawisworks(project: Project) -> Path:
    """Выгрузка nawisworks."""
    project.load_in_backup()
    project.load_in_ftp()
    project.load_in_nwc()
    project.load_in_nwd()
    return project.project_dir.nawisworks


@result_cmd_program(
    base_dir=BASE_DIR,
    end_message=END_LOAD_MESSAGE_FTP,
    tg_token=TG_TOKEN,
)
def start_ftp(project: Project) -> Path:
    """Выгрузка Revit моделей на сервер FTP."""
    project.load_in_ftp()
    return project.ftp_dir.revit_models


@result_cmd_program(
    base_dir=BASE_DIR,
    end_message=END_LOAD_MESSAGE_PUBLISH,
    tg_token=TG_TOKEN,
)
def start_publish(project: Project) -> Path:
    """Публикация проекта."""
    project.load_in_backup()
    project.load_in_ftp()
    project.load_in_nwc()
    project.load_in_nwd()
    project.load_in_publish()
    return project.ftp_dir.publish


choises = {
    ARG_START_ARCH: start_arch,
    ARG_START_BACKUP: start_backup,
    ARG_START_FTP: start_ftp,
    ARG_START_NAWIS: start_nawisworks,
    ARG_START_PUBLISH: start_publish,
}


def parser(project: Project, tg_token: str = None) -> None:
    logging.info("Консольная программа запущена!")

    parser: ArgumentParser = ArgumentParser(
        description="Консольная программа выгрузки Revit моделей.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "load_model", help=ARGPARS_HELP_LOAD_MODEL, choices=choises.keys()
    )
    parser.add_argument(
        ARG_NAME_ALBUM_SHORT,
        ARG_NAME_ALBUM_LONG,
        help=ARGPARS_HELP_NAME_ALBUM_MODEL,
    )
    parser.add_argument(
        ARG_TG_MODE_SHORT,
        ARG_TG_MODE_LONG,
        action="store_true",
        help=ARGPARS_HELP_TG_MODE,
    )

    args: tuple = parser.parse_args()
    mode_load_model: Callable = choises.get(args.load_model)

    info_message: str = f"Программа запущена режиме: {mode_load_model.__doc__}"
    logging.info(info_message)

    if args.name_album:
        mode_load_model(project, args.name_album, tg_mode=args.tg_mode)
    else:
        mode_load_model(project, tg_mode=args.tg_mode)

    logging.info("Скрипт закончил работу.")

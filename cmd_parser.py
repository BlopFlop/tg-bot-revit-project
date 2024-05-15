from argparse import ArgumentParser
from types import FunctionType
import argparse
import logging

from constants import (
    ARGPARS_HELP_LOAD_MODEL, ARGPARS_HELP_SILENCE_MODE,
    ARGPARS_HELP_UPDATE_JSON,

    ARG_UPDATE_JSON_SHORT, ARG_UPDATE_JSON_LONG, ARG_SILENCE_MODE_SHORT,
    ARG_SILENCE_MODE_LONG, ARG_RUN_ARCH, ARG_RUN_BACKUP, ARG_RUN_FTP,
    ARG_RUN_NAWIS, ARG_RUN_PUBLISH, ARG_RUN_ALBUM, ARG_NAME_ALBUM_LONG,
    ARG_NAME_ALBUM_SHORT, ARGPARS_HELP_NAME_ALBUM_MODEL
)
from load_models import LoadModel


def arch(load_obj: LoadModel) -> str:
    '''Архивация моделей'''
    load_obj.arch()


def arch_album(load_obj: LoadModel, name_album: str) -> str:
    '''Архивация моделей после выдачи альбомов'''
    load_obj.arch_album(append_name_arch=name_album)


def backup(load_obj: LoadModel) -> str:
    '''Бэкап моделей'''
    load_obj.backup()


def ftp(load_obj: LoadModel) -> str:
    '''Выгрузка на сервер ftp'''
    load_obj.ftp()


def nawisworks(load_obj: LoadModel) -> str:
    '''Выгрузка Navisworks моделей'''
    load_obj.nawisworks()


def publish(load_obj: LoadModel) -> str:
    '''Публикация моделей'''
    load_obj.publish()


CHOISES: dict[str: FunctionType] = {
    ARG_RUN_ARCH: arch,
    ARG_RUN_ALBUM: arch_album,
    ARG_RUN_BACKUP: backup,
    ARG_RUN_FTP: ftp,
    ARG_RUN_NAWIS: nawisworks,
    ARG_RUN_PUBLISH: publish
}


def parser_() -> None:
    logging.info('Скрипт запущен!')

    parser: ArgumentParser = ArgumentParser(
        description='Скрипт выгрузки Revit моделей.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'load_model',
        help=ARGPARS_HELP_LOAD_MODEL,
        choices=CHOISES.keys()
    )
    parser.add_argument(
        ARG_NAME_ALBUM_SHORT,
        ARG_NAME_ALBUM_LONG,
        help=ARGPARS_HELP_NAME_ALBUM_MODEL,
    )
    parser.add_argument(
        ARG_UPDATE_JSON_SHORT,
        ARG_UPDATE_JSON_LONG,
        action='store_true',
        help=ARGPARS_HELP_UPDATE_JSON
    )
    parser.add_argument(
        ARG_SILENCE_MODE_SHORT,
        ARG_SILENCE_MODE_LONG,
        action='store_true',
        help=ARGPARS_HELP_SILENCE_MODE
    )

    args: tuple = parser.parse_args()
    mode_load_model: FunctionType = CHOISES.get(args.load_model)
    update_json: bool = args.update_json
    silence_mode: bool = args.silence_mode_for_tg_bot

    info_message: str = 'Скрипт запущен режиме: '
    info_message += mode_load_model.__doc__
    if update_json:
        info_message += ', обновляется json'
    if silence_mode:
        info_message += ', в режиме тишины'
    logging.info(info_message)

    load_model_obj: LoadModel = (
        LoadModel(update_json_mode=update_json, silence_mode=silence_mode)
    )
    if args.load_model == ARG_RUN_ALBUM:
        mode_load_model(load_model_obj, args.name_album)
    else:
        mode_load_model(load_model_obj)

    logging.info('Скрипт закончил работу.')

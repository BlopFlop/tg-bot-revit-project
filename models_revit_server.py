import os
import logging

from subprocess import run

from settings import PATH_REVTI_RST, START_LOAD_MODEL, END_LOAD_MODEL


logging.basicConfig(
    level=logging.INFO,
    filename='load_model_log.log',
    format='%(asctime)s, %(levelname)s, %(message)s',
    filemode='w'
)


def load_rvt_in_revit_server(
        server_name: str,
        first_path: str,
        second_path: str) -> None:
    '''Выгрузка моделей из ревит сервера с помощью утилиты RevitServerTools'''

    name_model = os.path.basename(first_path)
    error_message = (
        f'<<< Произошла ошибка при выгрузке модели {name_model}'
        ' она не будет выгружена. >>>'
    )

    second_path = os.path.join(second_path, name_model)
    command_create_local_model = 'l'
    param_server = '-d'
    param_destination = '-s'
    param_overwrite = '-o'
    try:
        run(
            [
                PATH_REVTI_RST,
                command_create_local_model,
                first_path,
                param_destination,
                server_name,
                param_server,
                second_path,
                param_overwrite
            ]
        )
        logging.info(f'Модель << {name_model} >> выгружена.')
    except Exception:
        logging.error(error_message)


def start_load_models(data) -> None:
    '''Начало выгрузки моделей.'''
    print(START_LOAD_MODEL)
    logging.info(START_LOAD_MODEL)
    for values in data:
        load_rvt_in_revit_server(*values)
    print(END_LOAD_MODEL)
    logging.info(END_LOAD_MODEL)

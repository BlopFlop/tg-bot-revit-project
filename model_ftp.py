from datetime import datetime as dt
import time
import sys

from models_revit_server import start_load_models
from tg_bot import send_message
from json_data import JsonFile
from settings import SECONDS_IN_MINUTE, KEY_JSON_FTP, PATH_DATA_JSON, logging


JSON_OBJ = JsonFile(PATH_DATA_JSON)


if __name__ == '__main__':
    time_work = dt.now()
    path_ftp = JSON_OBJ.get(KEY_JSON_FTP)
    if not path_ftp:
        warning_message = (
            'Список с путями до файлов для выгрузки моделей на FTP, пуст '
            'выгрузка не была запущена.'
        )
        logging.warning(warning_message)
        print(warning_message)
        time.sleep(10)
        sys.exit()

    debug_message = 'Старт выгрузки моделей на FTP'
    logging.debug(debug_message)

    start_load_models(path_ftp)
    time_work = (dt.now() - time_work).seconds // SECONDS_IN_MINUTE

    message = (
        'Файлы выгружены на сервер FTP.\n'
        f'Время выгрузки составило: {time_work} минут(ы|у).'
    )
    send_message(message)
    logging.debug(message)
    sys.exit()

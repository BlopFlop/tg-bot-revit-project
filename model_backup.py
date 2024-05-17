import sys
import time

from models_revit_server import start_load_models
from json_data import JsonFile
from settings import PATH_DATA_JSON, KEY_JSON_BACKUP, logging

JSON_OBJ = JsonFile(PATH_DATA_JSON)

if __name__ == '__main__':
    backup_path_models = JSON_OBJ.get(KEY_JSON_BACKUP)
    logging.debug('Старт выгрузки бекапов моделей')

    if not backup_path_models:
        warning_message = (
            'Список с путями до файлов для бекапа моделей, пуст '
            'выгрузка не была запущена.'
        )
        logging.warning(warning_message)
        print(warning_message)
        time.sleep(10)
        sys.exit()

    start_load_models(backup_path_models)
    sys.exit()

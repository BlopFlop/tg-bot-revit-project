from datetime import datetime as dt
import sys

from google_tab import get_ftp_paths
from models_revit_server import start_load_models
from tg_bot import send_message

from constants import SECONDS_IN_MINUTE


if __name__ == '__main__':
    time_work = dt.now()
    start_load_models(get_ftp_paths())
    time_work = (dt.now() - time_work).seconds // SECONDS_IN_MINUTE

    message = (
        'Файлы выгружены на сервер FTP.\n'
        f'Время выгрузки составило: {time_work} минут(ы|у).'
    )
    send_message(message)
    sys.exit()

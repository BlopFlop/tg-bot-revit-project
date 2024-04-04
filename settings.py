from datetime import datetime as dt
import time
import os
import sys
import logging

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater

from env_file import get_env


logging.basicConfig(
    handlers=[logging.FileHandler('tg_program.log', 'a', 'utf-8')],
    level=logging.DEBUG,
    format='%(asctime)s, [%(levelname)s] %(message)s',
)


def check_file(file_path, except_message) -> None | Exception:
    if not os.path.isfile(file_path):
        logging.error(except_message)
        print(FileNotFoundError(except_message))
        time.sleep(10)
        sys.exit()


def get_file_run_load_models(file_name: str) -> str:
    exe_ext = '.exe'
    py_ext = '.py'

    path_exe = os.path.join(BASE_DIR, (file_name + exe_ext))
    path_py = os.path.join(BASE_DIR, (file_name + py_ext))

    except_message = (
        f'Файла {file_name}, c расширением exe или py нет в папке с проектом.'
    )
    path_run_load = (
        path_exe if os.path.isfile(path_exe) else path_py
    )
    check_file(path_run_load, except_message)
    return path_run_load


load_dotenv()

DATE_MASK = '%Y-%m-%d'
DATE_NOW = dt.now().strftime(DATE_MASK)

# paths const
NAME_CREDS_JSON = 'creds.json'
NAME_DATA_JSON = 'data.json'

BASE_DIR = os.path.dirname(sys.argv[0])

CREDENTIALS_FILE_PATH = os.path.join(BASE_DIR, NAME_CREDS_JSON)
PATH_DATA_JSON = os.path.join(BASE_DIR, NAME_DATA_JSON)

PATH_COPY_DIR = os.path.join(BASE_DIR, 'load_nawis')

NAME_FTP_FILE = 'model_ftp'
NAME_PUB_FILE = 'model_publish'
NAME_NAWIS_FILE = 'model_nawisworks'
NAME_DEPLOY_ALBUM_FILE = 'model_arch'

FILE_LOAD_FTP = get_file_run_load_models(NAME_FTP_FILE)
FILE_PUB_MODELS = get_file_run_load_models(NAME_PUB_FILE)
FILE_LOAD_NAWIS = get_file_run_load_models(NAME_NAWIS_FILE)
FILE_DEPLOY_ALBUM = get_file_run_load_models(NAME_DEPLOY_ALBUM_FILE)

sys.path.append(BASE_DIR)
check_file(
    CREDENTIALS_FILE_PATH,
    f'Файла {NAME_CREDS_JSON} в папке со скриптом не существует, '
    'его можно получить создав в google console, инструкция > '
    'https://qna.habr.com/q/560988'
)
get_env(BASE_DIR)

# env const
NAME_PROJECT = os.getenv('NAME_PROJECT')
NAWIS_OR_REVIT_VERSION = os.getenv('NAWIS_OR_REVIT_VERSION')

FAMILY_NAME_BIM_SPECIALIST = (
    os.getenv('FAMILY_NAME_BIM_SPECIALIST').replace('$', ' ')
)
PHONE_NUMBER_BIM_SPECIALIST = os.getenv('PHONE_NUMBER_BIM_SPECIALIST')

TG_TOKEN = os.getenv('TG_TOKEN')

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
GOOGLE_DISK_FOLDER_ID = os.getenv('GOOGLE_DISK_FOLDER_ID')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
TO_EMAIL_USER = os.getenv('TO_EMAIL_USER')

# google const
NAME_SHEET_DIR_PATH = '00_Dir_paths'
NAME_SHEET_BACKUP = '01_Backup'
NAME_SHEET_ARCHIVE = '02_Archive'
NAME_SHEET_FTP = '03_FTP'
NAME_SHEET_NWC = '04_NWC'

NAME_FIELD_PATH_NWF = 'Paths_NWF'
NAME_FIELD_NWD = '05_NWD'
NAME_FIELD_PUBLISH = '06_Publish'

START_LOAD_MODEL = '<< Начало выгрузки моделей из Ревит сервера >>'
END_LOAD_MODEL = '<< Конец выгрузки моделей из Ревит сервера >>'

# tg bot const
BOT = Bot(token=TG_TOKEN)
UPDATER = Updater(token=TG_TOKEN)

BOT_INFO_MESSAGE = (
    'Доступные команды:\n'
    '• /info - Информация о функционале бота.\n'
    '• /add_in_project - Добавление вас в рассылку, для получения информации о'
    ' выгрузке моделей подрядчиком.\n'
    '• /remove_in_project - Удаляет вас из рассылки сообщений чат бота\n'
    '• /load_in_ftp - Выгрузка моделей на FTP(публикация для подрядчика)\n'
    '• /load_nawis_file - Выгрузка Navisworks моделей'
    '(В том числе консолидированная сборка модели nwd)\n'
    '• /publish_models - Публикация моделей заказчику.\n'
    '• #d <Имя альбома> - Архивация моделей после выдачи альбомов '
    'Пример: вписав команду << #d 01AR 02AR >> вам создадут архив с именем'
    f'<< {DATE_NOW}_RVT_01AR-02AR >>\n\n'
    '* - По всем вопросам обращаться к вашему BIM специалисту: '
    f'{FAMILY_NAME_BIM_SPECIALIST}. Номер {PHONE_NUMBER_BIM_SPECIALIST}'
)

DEPLOY_ALBUM_START_MESSAGE = (
    'Сейчас начинается архивация моделей после выдачи альбомов. '
)
DEPLOY_ALBUM_END_MESSAGE = (
    'Архивация моделей после выдачи альбомов закончена.'
)
ARCH_START_MESSAGE = (
    f'Начинается еженедельная архивация проекта {NAME_PROJECT}'
)
ARCH_END_MESSAGE = (
    f'Еженедельная архивация {NAME_PROJECT} закончена.'
)
LOAD_FTP_START_MESSAGE = (
    'Ваш карманный BIM специалист начал, выгрузку на сервер'
    f' FTP, проекта: {NAME_PROJECT}, вся выгрузка продлится около 10 минут.'
)
LOAD_NAWIS_START_MESSAGE = (
    'Ваш карманный BIM специалист начал, выгрузку моделей'
    f' Navisworks, проекта: {NAME_PROJECT}, вся выгрузка продлится около'
    ' 20 минут'
)
PUBLISH_MODELS_MESSAGE = (
    'Ваш карманный BIM специалист начал публикацию моделей заказчику.'
)

# load file const
RVT_EXTENTION = '.rvt'
NWF_EXTENTION = '.nwf'
NWC_EXTENTION = '.nwc'
NWD_EXTENTION = '.nwd'
EXTENSION_FILE = (
    RVT_EXTENTION[1:], NWF_EXTENTION[1:], NWC_EXTENTION[1:], NWD_EXTENTION[1:]
)

PATH_REVIT = rf'C:\Program Files\Autodesk\Revit {NAWIS_OR_REVIT_VERSION}'
PATH_REVTI_RST = (
    os.path.join(PATH_REVIT, r'RevitServerToolCommand\RevitServerTool.exe')
)

PATH_NAWISWORKS = (
    rf'C:\Program Files\Autodesk\Navisworks Manage {NAWIS_OR_REVIT_VERSION}'
)
PATH_NAWIS_FTR = os.path.join(PATH_NAWISWORKS, 'FiletoolsTaskRunner.exe')
PATH_NAWIS_ROAMER = os.path.join(PATH_NAWISWORKS, 'Roamer.exe')

FIRST_FLAG, SECOND_FLAG, THIRD_FLAG = r'/i', r'/of', r'/version'

FLAG_NWD = '-nwd'

COUNT_RUN_MULTIPROSECCING = 6

# other const
SECONDS_IN_MINUTE = 60

KEY_JSON_DIR_PATHS = 'dir_paths'
KEY_JSON_ARCH = 'archive'
KEY_JSON_BACKUP = 'backup'
KEY_JSON_FTP = 'ftp'
KEY_JSON_NWC = 'nwc'
KEY_JSON_NWD = 'nwd'
KEY_JSON_PUB = 'pub'
KEY_JSON_CHAT_ID = 'chat_id'

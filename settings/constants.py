from datetime import datetime as dt
import os
import sys

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater

load_dotenv()


def check_file(file_path, except_message) -> None | Exception:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(except_message)


def create_json(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json_file.read()
        if data:
            return True

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json_file.write('{}')


DATE_MASK = '%Y-%m-%d'
DATE_NOW = dt.now().strftime(DATE_MASK)


# env const
NAME_PROJECT = os.getenv('NAME_PROJECT')
NAWIS_OR_REVIT_VERSION = os.getenv('NAWIS_OR_REVIT_VERSION')

TG_TOKEN = os.getenv('TG_TOKEN')

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
GOOGLE_DISK_FOLDER_ID = os.getenv('GOOGLE_DISK_FOLDER_ID')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
TO_EMAIL_USER = os.getenv('TO_EMAIL_USER')

FAMILY_NAME_BIM_SPECIALIST = (
    ' '.join(os.getenv('FAMILY_NAME_BIM_SPECIALIST').split('.'))
)
PHONE_NUMBER_BIM_SPECIALIST = os.getenv('PHONE_NUMBER_BIM_SPECIALIST')

# paths const
NAME_CREDS_JSON = 'creds.json'
NAME_CHATS_JSON = 'chats.json'

PATH_FOLDER = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PATH_FOLDER)

CREDENTIALS_FILE_PATH = os.path.join(PATH_FOLDER, NAME_CREDS_JSON)
PATH_CHATS_JSON = os.path.join(os.path.dirname(__file__), NAME_CHATS_JSON)

PATH_COPY_DIR = os.path.join(BASE_DIR, 'load_nawis')
FILE_LOAD_FTP = os.path.join(BASE_DIR, 'model_ftp.py')
FILE_PUB_MODELS = os.path.join(BASE_DIR, 'model_publish.py')
FILE_LOAD_NAWIS = os.path.join(BASE_DIR, 'model_nawisworks.py')
FILE_DEPLOY_ALBUM = os.path.join(BASE_DIR, 'model_arch.py')

sys.path.append(BASE_DIR)
create_json(PATH_CHATS_JSON)

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
    f'<< {DATE_NOW}_RVT_01AR-02AR >>'
)

DEPLOY_ALBUM_START_MESSAGE = (
    'Привет, сейчас мы начинаем архивацию моделей после выдачи альбомов. '
)
DEPLOY_ALBUM_END_MESSAGE = (
    'Привет, архивация моделей после выдачи альбомов закончена. '
)
ARCH_START_MESSAGE = (
    f'Привет, сейчас мы начинаем еженедельную архивацию проекта {NAME_PROJECT}'
)
ARCH_END_MESSAGE = (
    f'Пора прощатся, еженедельная архивация {NAME_PROJECT} закончена.'
)
LOAD_FTP_START_MESSAGE = (
    'Привет, ваш карманный BIM специалист начал, выгрузку на сервер'
    f' FTP, проекта: {NAME_PROJECT}, вся выгрузка продлится около 10 минут.'
)
LOAD_NAWIS_START_MESSAGE = (
    'Привет, ваш карманный BIM специалист начал, выгрузку моделей'
    f' Navisworks, проекта: {NAME_PROJECT}, вся выгрузка продлится около'
    ' 20 минут'
)
PUBLISH_MODELS_MESSAGE = (
    'Привет, ваш карманный BIM специалист начал публикацию моделей '
    'заказчику.'
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

FILE_NAME_LOG = 'bot_logging.log'

# other const
SECONDS_IN_MINUTE = 60

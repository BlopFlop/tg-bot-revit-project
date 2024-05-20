from datetime import datetime as dt
from pathlib import Path
from dotenv import load_dotenv
import os
import sys

from _env_file import EnvFile


DATE_FORMAT: str = '%Y-%m-%d'
DATE_NOW: str = dt.now().strftime(DATE_FORMAT)

# paths
NAME_CREDS_JSON: str = 'creds.json'
NAME_DATA_JSON: str = 'data.json'
BASE_DIR: Path = Path(sys.argv[0]).parent
CREDENTIALS_FILE_PATH: Path = BASE_DIR / NAME_CREDS_JSON

PATH_TG_BOT_EXE: Path = BASE_DIR / 'tg_bot.exe'
PATH_CMD_PROGRAM_EXE: Path = BASE_DIR / 'cmd_program.exe'
PATH_DIR_CHECKS_EXE: Path = BASE_DIR / 'dir_checks.exe'
PATH_DATA_JSON: Path = BASE_DIR / NAME_DATA_JSON
PATH_COPY_DIR: Path = BASE_DIR / 'load_nawis'

# env
ENV_: EnvFile = EnvFile(BASE_DIR)
sys.path.append((str(BASE_DIR)))
os.chdir(str(BASE_DIR))
load_dotenv()

NAME_PROJECT: str = os.getenv('NAME_PROJECT')
NAWIS_OR_REVIT_VERSION: str = os.getenv('NAWIS_OR_REVIT_VERSION')
FAMILY_NAME_BIM_SPECIALIST: str = (
    os.getenv('FAMILY_NAME_BIM_SPECIALIST').replace('$', ' ')
)
PHONE_NUMBER_BIM_SPECIALIST: str = os.getenv('PHONE_NUMBER_BIM_SPECIALIST')

TG_TOKEN: str = os.getenv('TG_TOKEN')
SPREADSHEET_ID: str = os.getenv('SPREADSHEET_ID')
GOOGLE_DISK_FOLDER_ID: str = os.getenv('GOOGLE_DISK_FOLDER_ID')

# google const
NAME_SHEET_DIR_PATH: str = '00_Dir_paths'
NAME_SHEET_BACKUP: str = '01_Backup'
NAME_SHEET_ARCHIVE: str = '02_Archive'
NAME_SHEET_FTP: str = '03_FTP'
NAME_SHEET_NWC: str = '04_NWC'
NAME_FIELD_PATH_NWF: str = 'Paths_NWF'
NAME_FIELD_NWD: str = '05_NWD'
NAME_FIELD_PUBLISH: str = '06_Publish'

# argparse
ARG_RUN_ARCH: str = 'arch'
ARG_RUN_ALBUM: str = 'arch-album'
ARG_RUN_BACKUP: str = 'backup'
ARG_RUN_FTP: str = 'ftp'
ARG_RUN_NAWIS: str = 'nawisworks'
ARG_RUN_PUBLISH: str = 'publish'

ARG_UPDATE_JSON_SHORT: str = '-uj'
ARG_UPDATE_JSON_LONG: str = '--update_json'
ARG_SILENCE_MODE_SHORT: str = '-sm'
ARG_SILENCE_MODE_LONG: str = '--silence_mode_for_tg_bot'
ARG_NAME_ALBUM_SHORT: str = '-na'
ARG_NAME_ALBUM_LONG: str = '--name_album'

ARGPARS_HELP_LOAD_MODEL: str = (
    '\tОписание вариантов работы программы:\n'
    f'{ARG_RUN_ARCH} - архивация моделей;\n'
    f'{ARG_RUN_ALBUM} - архивация моделей именем альбома\n'
    f'\t(При использовании обязателен аргумент {ARG_NAME_ALBUM_LONG});\n'
    f'{ARG_RUN_BACKUP} - бэкап моделей;\n'
    f'{ARG_RUN_FTP} - выгрузка на сервер ftp;\n'
    f'{ARG_RUN_NAWIS} - выгрузка моделей в формат nawisworks;\n'
    f'{ARG_RUN_PUBLISH} - публикация моделей заказчику.'
)
ARGPARS_HELP_NAME_ALBUM_MODEL: str = (
    f'* - Обязателен в режиме работы {ARG_NAME_ALBUM_LONG} \n'
    '\tЗадает имя альбома при архивации.'
)
ARGPARS_HELP_SILENCE_MODE: str = '''\
Если данный режим указан, то прогресс работы
программы не будет отображаться чате Telegram бота.
'''
ARGPARS_HELP_UPDATE_JSON: str = '''\
Определяет нужно ли обновлять данные в json файле из GoogleTab.
'''

# tg bot
BUTTON_HELP: str = 'help'
BUTTON_START: str = 'start'
BUTTON_ADD_IN_PROJECT: str = 'add_in_project'
BUTTON_REMOVE_IN_PROJECT: str = 'remove_in_project'
BUTTON_FTP: str = ARG_RUN_FTP
BUTTON_NAWIS: str = ARG_RUN_NAWIS
BUTTON_PUB: str = ARG_RUN_PUBLISH

BOT_START_MESSAGE: str = 'Нажми кнопку /start, для обновления кнопок.'
BOT_HELP_MESSAGE: str = (
    'Доступные команды:\n'
    f'• /{BUTTON_HELP} - Информация о функционале бота.\n'
    f'• /{BUTTON_ADD_IN_PROJECT} - Добавление вас в рассылку уведомлений, '
    'о статусе выгрузок.\n'
    f'• /{BUTTON_REMOVE_IN_PROJECT} - Удаляет вас из рассылки уведомлений. \n'
    f'• /{BUTTON_FTP} - Выгрузка моделей на FTP(публикация для подрядчика)\n'
    f'• /{BUTTON_NAWIS} - Выгрузка Navisworks моделей'
    '(В том числе консолидированная сборка модели "NWD")\n'
    f'• /{BUTTON_PUB} - Публикация моделей заказчику.\n'
    '• #d <Имя альбома> - Архивация моделей после выдачи альбомов '
    'Пример: вписав команду << #d 01AR02AR >> вам создадут архив с именем'
    f'<< {DATE_NOW}_RVT_01AR02AR >>\n\n'
    '* - По всем вопросам обращаться к вашему BIM специалисту: '
    f'{FAMILY_NAME_BIM_SPECIALIST}. Номер {PHONE_NUMBER_BIM_SPECIALIST}'
)
START_LOAD_MESSAGE_ARCH: str = (
    'Старт архивации моделей (перед этим , будут выгружены модели'
    ' на ftp и в nawisworks).'
)
START_LOAD_MESSAGE_ARCH_ALBUM: str = (
    'Старт архивации моделей после выдачи альбомов. (перед этим ,'
    'будут выгружены модели на ftp и в nawisworks).'
)
START_LOAD_MESSAGE_BACKUP: str = 'Старт бэкапа моделей.'
START_LOAD_MESSAGE_FTP: str = 'Старт выгрузки моделей на сервер FTP.'
START_LOAD_MESSAGE_NAWISWORKS: str = (
    'Старт выгрузки моделй Nawisworks (перед этим Revit модели будут выгружены'
    'на FTP).'
)
START_LOAD_MESSAGE_PUBLISH: str = (
    'Старт публикации моделей заказчику. (перед этим, будут выгружены модели '
    'на ftp и в nawisworks).'
)
END_LOAD_MESSAGE_ARCH: str = 'Архивация, закончена, '
END_LOAD_MESSAGE_ARCH_ALBUM: str = 'Архивация после выдачи альбомов, закончена, '
END_LOAD_MESSAGE_BACKUP: str = 'Бэкап моделей, завершен,'
END_LOAD_MESSAGE_FTP: str = 'Выгрузка моделей на FTP, завершена,'
END_LOAD_MESSAGE_NAWISWORKS: str = 'Выгрузка моделей Navisworks, завершена,'
END_LOAD_MESSAGE_PUBLISH: str = 'Публикация моделей, завершена,'

# load file const
NAME_PROGRAM_REVIT: str = (
    f'Autodesk Navisworks Manage {NAWIS_OR_REVIT_VERSION}'
)
NAME_PROGRAM_NAWIS: str = f'Autodesk Revit {NAWIS_OR_REVIT_VERSION}'
NAME_WORKDIR_NAWIS: str = 'load_from_nawis'
PATH_WORKDIR_NAWIS: Path = BASE_DIR / NAME_WORKDIR_NAWIS

RVT_EXTENTION: str = '.rvt'
NWF_EXTENTION: str = '.nwf'
NWC_EXTENTION: str = '.nwc'
NWD_EXTENTION: str = '.nwd'
IFC_EXTENTION: str = '.ifc'
EXTENSION_FILE: list[str] = (
    RVT_EXTENTION[1:], NWF_EXTENTION[1:], NWC_EXTENTION[1:], NWD_EXTENTION[1:],
    IFC_EXTENTION[1:]
)

PATH_REVIT: Path = (
    Path(rf'C:\Program Files\Autodesk\Revit {NAWIS_OR_REVIT_VERSION}')
)
PATH_REVIT_RST: Path = (
    PATH_REVIT / r'RevitServerToolCommand\RevitServerTool.exe'
)

PATH_NAWISWORKS: Path = Path(
    rf'C:\Program Files\Autodesk\Navisworks Manage {NAWIS_OR_REVIT_VERSION}'
)
PATH_NAWIS_FTR: Path = PATH_NAWISWORKS / 'FiletoolsTaskRunner.exe'
PATH_NAWIS_ROAMER: Path = PATH_NAWISWORKS / 'Roamer.exe'

FTR_FIRST_FLAG: str = r'/i'
FTR_SECOND_FLAG: str = r'/of'
FTR_THIRD_FLAG: str = r'/version'

ROAMER_FLAG_NWD: str = '-nwd'

RST_COMMAND_CREATE_LOCAL_MODEL = 'l'
RST_FLAG_SERVER = '-d'
RST_FLAG_DESTINATION = '-s'
RST_FLAG_OVERWRITE = '-o'

COUNT_PROCESSES: int = 6

# other const
LOG_FORMAT: str = '"%(asctime)s - [%(levelname)s] - %(message)s"'

SEC_IN_MIN: int = 60
MIN_IN_HOUR: int = 60
HOUR_IN_DAY: int = 24
DAY_IN_WEEK: int = 7
DAY_IN_MOTH: int = 30

SECONDS_IN_HOUR: int = SEC_IN_MIN * MIN_IN_HOUR
SECONDS_IN_DAY: int = SECONDS_IN_HOUR * HOUR_IN_DAY
SECONDS_IN_WEEK: int = DAY_IN_WEEK * SECONDS_IN_DAY
SECONDS_IN_MONTH: int = DAY_IN_MOTH * SECONDS_IN_DAY

SECONDS_PERIOD: dict[str: int] = {
    'hour': SECONDS_IN_HOUR,
    'day': SECONDS_IN_DAY,
    'week': SECONDS_IN_WEEK,
    'month': SECONDS_IN_MONTH,
}

# json const
KEY_JSON_DIR_PATHS: str = 'dir_paths'
KEY_JSON_ARCH: str = 'archive'
KEY_JSON_BACKUP: str = 'backup'
KEY_JSON_FTP: str = 'ftp'
KEY_JSON_NWC: str = 'nwc'
KEY_JSON_NWD: str = 'nwd'
KEY_JSON_PUB: str = 'pub'
KEY_JSON_CHAT_ID: str = 'chat_id'

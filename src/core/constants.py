import sys
import os
from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(sys.argv[0]).resolve().parent.parent

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "bim_web_app_logging.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

ENV_PATH: Final[Path] = BASE_DIR.parent / r"infra//.env"

STATIC_PATH: Final[Path] = BASE_DIR / "static"
LOGO_PNG_PATH: Final[Path] = STATIC_PATH / "logo.png"


RE_PATTERN_NUMBER_PHONE: Final[str] = (
    r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
)
RE_PATTERN_NAME: Final[str] = r"^[а-яА-Яa-zA-Z0-9]+$"
RE_PATTERN_EMAIL: Final[str] = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

BASE_DIR: Final[Path] = Path(sys.argv[0]).parent

sys.path.append((str(BASE_DIR)))
os.chdir(str(BASE_DIR))

CMD_SERVER_NAME: Final[str] = os.getenv("CMD_SERVER_NAME", default="10.10.1.30")
CMD_NAME_PROJECT: Final[str] = os.getenv(key="CMD_NAME_PROJECT", default="999_TEST")
CMD_SEARCH_PATTERN: Final[str] = os.getenv(key="CMD_SEARCH_PATTERN", default="TEST")
CMD_NAWIS_OR_REVIT_VERSION: Final[str] = os.getenv(
    key="CMD_NAWIS_OR_REVIT_VERSION", default="2021"
)
CMD_PROJECT_DIR: Final[Path] = Path(
    os.getenv(key="CMD_PROJECT_DIR", default=r"R:\101_BIM-Projects")
)
CMD_ARCH_DIR: Final[Path] = Path(
    os.getenv(key="CMD_ARCH_DIR", default=r"R:\100_Archive")
)
CMD_FTP_DIR: Final[Path] = Path(
    os.getenv(key="CMD_FTP_DIR", default=r"\\l-ftp\Root\Unipro_FTP-01")
)

TG_TOKEN: Final[str] = os.getenv(key="TG_TOKEN", default="notTelegramToken")

DATE_FORMAT: Final[str] = "%Y-%m-%d"
DATE_NOW: Final[str] = dt.now().strftime(DATE_FORMAT)
LOG_FORMAT: str = '"%(asctime)s - [%(levelname)s] - %(message)s"'

PATH_JSON_DB: Path = BASE_DIR / "data.json"

PATH_REVIT: Final[Path] = Path(
    rf"C:\Program Files\Autodesk\Revit {CMD_NAWIS_OR_REVIT_VERSION}"
)
PATH_NAWISWORKS: Final[Path] = Path(
    rf"C:\Program Files\Autodesk\Navisworks Manage {CMD_NAWIS_OR_REVIT_VERSION}"
)

PATH_REVIT_RST: Final[Path] = PATH_REVIT / r"RevitServerToolCommand\RevitServerTool.exe"

PATH_NAWIS_FTR: Final[Path] = PATH_NAWISWORKS / "FiletoolsTaskRunner.exe"
PATH_NAWIS_ROAMER: Final[Path] = PATH_NAWISWORKS / "Roamer.exe"

NAME_WORKDIR_NAWIS: Final[str] = "load_from_nawis"

PATH_WORKDIR_NAWIS: Final[Path] = BASE_DIR / NAME_WORKDIR_NAWIS

RVT_EXTENTION: Final[str] = ".rvt"
NWF_EXTENTION: Final[str] = ".nwf"
NWC_EXTENTION: Final[str] = ".nwc"
NWD_EXTENTION: Final[str] = ".nwd"
IFC_EXTENTION: Final[str] = ".ifc"

# argparse
ARG_START_ARCH: Final[str] = "arch"
ARG_START_BACKUP: Final[str] = "backup"
ARG_START_FTP: Final[str] = "ftp"
ARG_START_NAWIS: Final[str] = "nawisworks"
ARG_START_PUBLISH: Final[str] = "publish"

ARG_NAME_ALBUM_SHORT: Final[str] = "-na"
ARG_NAME_ALBUM_LONG: Final[str] = "--name_album"
ARG_TG_MODE_SHORT: Final[str] = "-tg"
ARG_TG_MODE_LONG: Final[str] = "--tg_mode"

ARGPARS_HELP_LOAD_MODEL: Final[str] = (
    "\tОписание вариантов работы программы:\n"
    f"{ARG_START_ARCH} - архивация моделей;\n"
    f"{ARG_START_ARCH} {ARG_NAME_ALBUM_LONG} <<Имя альбома>> - архивация "
    "моделей c именем альбома\n"
    f"{ARG_START_BACKUP} - бэкап моделей;\n"
    f"{ARG_START_FTP} - выгрузка на сервер ftp;\n"
    f"{ARG_START_NAWIS} - выгрузка моделей в формат nawisworks;\n"
    f"{ARG_START_PUBLISH} - публикация моделей заказчику."
)
ARGPARS_HELP_NAME_ALBUM_MODEL: Final[str] = "* - Задает имя альбома при архивации."
ARGPARS_HELP_TG_MODE: Final[
    str
] = """\
Если данный режим указан, то прогресс работы
программы будет отображаться чате Telegram бота.
"""

# tg bot
END_LOAD_MESSAGE_ARCH: Final[str] = "Архивация, закончена, "
END_LOAD_MESSAGE_BACKUP: Final[str] = "Бэкап моделей, завершен,"
END_LOAD_MESSAGE_FTP: Final[str] = "Выгрузка моделей на FTP, завершена,"
END_LOAD_MESSAGE_NAWISWORKS: Final[str] = "Выгрузка моделей Navisworks, завершена,"
END_LOAD_MESSAGE_PUBLISH: Final[str] = "Публикация моделей, завершена,"


def configure_logging() -> None:
    """Configure logging from this project"""
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "bim_web_app_logging.log"
    rotating_handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=5)
    logging.basicConfig(
        datefmt=DATE_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler()),
    )


configure_logging()


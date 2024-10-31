import sys
import os
from pathlib import Path
from typing import Final

# BASE_DIR: Final[Path] = Path(sys.argv[0]).resolve().parent.parent
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
# sys.path.append((str(BASE_DIR)))
# os.chdir(str(BASE_DIR))

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "tg_bot_logging.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

ENV_PATH: Final[Path] = BASE_DIR.parent / r"infra//.env"

STATIC_PATH: Final[Path] = BASE_DIR / "static"
LOCAL_REVIT_PATH: Final[Path] = BASE_DIR / "local_revit_models"
LOCAL_NAWISWORKS_PATH: Final[Path] = BASE_DIR / "load_from_nawis"

# LOGO_PNG_PATH: Final[Path] = STATIC_PATH / "logo.png"


# CMD_SERVER_NAME: Final[str] = os.getenv(
#     "CMD_SERVER_NAME", default="10.10.1.30"
# )
# CMD_NAME_PROJECT: Final[str] = os.getenv(
#     key="CMD_NAME_PROJECT", default="999_TEST"
# )
# CMD_SEARCH_PATTERN: Final[str] = os.getenv(
#     key="CMD_SEARCH_PATTERN", default="TEST"
# )
# CMD_NAWIS_OR_REVIT_VERSION: Final[str] = os.getenv(
#     key="CMD_NAWIS_OR_REVIT_VERSION", default="2021"
# )

PROJECT_DIR: Final[Path] = Path(
    os.getenv(key="CMD_PROJECT_DIR", default=r"R:\101_BIM-Projects")
)
ARCH_DIR: Final[Path] = Path(
    os.getenv(key="CMD_ARCH_DIR", default=r"R:\100_Archive")
)
FTP_DIR: Final[Path] = Path(
    os.getenv(key="CMD_FTP_DIR", default=r"\\l-ftp\Root\Unipro_FTP-01")
)

TG_TOKEN: Final[str] = os.getenv(key="TG_TOKEN", default="notTelegramToken")

PATH_REVIT: Final[str] = r"C:\Program Files\Autodesk\Revit {}"
PATH_NAWISWORKS: Final[str] = r"C:\Program Files\Autodesk\Navisworks Manage {}"

PATH_REVIT_RST: Final[str] = (
    "\\".join((PATH_REVIT, r"RevitServerToolCommand\RevitServerTool.exe"))
)

PATH_NAWIS_FTR: Final[str] = (
    "\\".join((PATH_NAWISWORKS, "FiletoolsTaskRunner.exe"))
)
PATH_NAWIS_ROAMER: Final[str] = "\\".join((PATH_NAWISWORKS, "Roamer.exe"))

RVT_EXTENTION: Final[str] = ".rvt"
NWF_EXTENTION: Final[str] = ".nwf"
NWC_EXTENTION: Final[str] = ".nwc"
NWD_EXTENTION: Final[str] = ".nwd"
IFC_EXTENTION: Final[str] = ".ifc"

# argparse
# ARG_START_ARCH: Final[str] = "arch"
# ARG_START_BACKUP: Final[str] = "backup"
# ARG_START_FTP: Final[str] = "ftp"
# ARG_START_NAWIS: Final[str] = "nawisworks"
# ARG_START_PUBLISH: Final[str] = "publish"

# ARG_NAME_ALBUM_SHORT: Final[str] = "-na"
# ARG_NAME_ALBUM_LONG: Final[str] = "--name_album"
# ARG_TG_MODE_SHORT: Final[str] = "-tg"
# ARG_TG_MODE_LONG: Final[str] = "--tg_mode"

# ARGPARS_HELP_LOAD_MODEL: Final[str] = (
#     "\tОписание вариантов работы программы:\n"
#     f"{ARG_START_ARCH} - архивация моделей;\n"
#     f"{ARG_START_ARCH} {ARG_NAME_ALBUM_LONG} <<Имя альбома>> - архивация "
#     "моделей c именем альбома\n"
#     f"{ARG_START_BACKUP} - бэкап моделей;\n"
#     f"{ARG_START_FTP} - выгрузка на сервер ftp;\n"
#     f"{ARG_START_NAWIS} - выгрузка моделей в формат nawisworks;\n"
#     f"{ARG_START_PUBLISH} - публикация моделей заказчику."
# )
# ARGPARS_HELP_NAME_ALBUM_MODEL: Final[str] = (
#     "* - Задает имя альбома при архивации."
# )
# ARGPARS_HELP_TG_MODE: Final[
#     str
# ] = """\
# Если данный режим указан, то прогресс работы
# программы будет отображаться чате Telegram бота.
# """

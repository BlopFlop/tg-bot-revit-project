import os
import sys
from datetime import datetime as dt
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

DATE_FORMAT: Final[str] = "%Y-%m-%d"
DATE_NOW: Final[str] = dt.now().strftime(DATE_FORMAT)

BASE_DIR: Final[Path] = Path(sys.argv[0]).parent

sys.path.append((str(BASE_DIR)))
os.chdir(str(BASE_DIR))
load_dotenv()

TG_TOKEN: Final[str] = os.getenv(key="TG_TOKEN", default="notTelegramToken")
CMD_NAME_PROJECT: Final[str] = os.getenv(
    key="CMD_NAME_PROJECT", default="999_TEST"
)

PATH_JSON_DB: Path = BASE_DIR / "data.json"

START_LOAD_MESSAGE_ARCH: Final[str] = (
    "Старт архивации моделей (перед этим , будут выгружены модели "
    "на ftp и в nawisworks)."
)
START_LOAD_MESSAGE_ARCH_ALBUM: Final[str] = (
    "Старт архивации моделей после выдачи альбомов. (перед этим, "
    "будут выгружены модели на ftp и в nawisworks)."
)
START_LOAD_MESSAGE_BACKUP: Final[str] = "Старт бэкапа моделей."
START_LOAD_MESSAGE_FTP: Final[str] = "Старт выгрузки моделей на сервер FTP."
START_LOAD_MESSAGE_NAWISWORKS: Final[str] = (
    "Старт выгрузки моделй Nawisworks (перед этим Revit модели будут выгружены"
    "на FTP)."
)
START_LOAD_MESSAGE_PUBLISH: Final[str] = (
    "Старт публикации моделей заказчику. (перед этим, будут выгружены модели "
    "на ftp и в nawisworks)."
)
END_LOAD_MESSAGE_ARCH: Final[str] = "Архивация, закончена, "
END_LOAD_MESSAGE_ARCH_ALBUM: Final[str] = (
    "Архивация после выдачи альбомов, закончена, "
)
END_LOAD_MESSAGE_BACKUP: Final[str] = "Бэкап моделей, завершен,"
END_LOAD_MESSAGE_FTP: Final[str] = "Выгрузка моделей на FTP, завершена,"
END_LOAD_MESSAGE_NAWISWORKS: Final[str] = "Выгрузка моделей Navisworks, завершена,"
END_LOAD_MESSAGE_PUBLISH: Final[str] = "Публикация моделей, завершена,"

BUTTON_HELP: Final[str] = "help"
BUTTON_START: Final[str] = "start"
BUTTON_ADD_IN_PROJECT: Final[str] = "add_in_project"
BUTTON_REMOVE_IN_PROJECT: Final[str] = "remove_in_project"
BUTTON_FTP: Final[str] = "ftp"
BUTTON_NAWIS: Final[str] = "nawisworks"
BUTTON_PUB: Final[str] = "publish"

BOT_HELP_MESSAGE: Final[str] = (
    "Доступные команды:\n"
    f"• /{BUTTON_HELP} - Информация о функционале бота.\n"
    f"• /{BUTTON_ADD_IN_PROJECT} - Добавление вас в рассылку уведомлений, "
    "о статусе выгрузок.\n"
    f"• /{BUTTON_REMOVE_IN_PROJECT} - Удаляет вас из рассылки уведомлений. \n"
    f"• /{BUTTON_FTP} - Выгрузка моделей на FTP(публикация для подрядчика)\n"
    f"• /{BUTTON_NAWIS} - Выгрузка Navisworks моделей"
    '(В том числе консолидированная сборка модели "NWD")\n'
    f"• /{BUTTON_PUB} - Публикация моделей заказчику.\n"
    "• #d <Имя альбома> - Архивация моделей после выдачи альбомов "
    "Пример: вписав команду << #d 01AR02AR >> вам создадут архив с именем"
    f"<< {DATE_NOW}_RVT_01AR02AR >>\n\n"
    # '* - По всем вопросам обращаться к вашему BIM специалисту: '
    # f'{FAMILY_NAME_BIM_SPECIALIST}. Номер {PHONE_NUMBER_BIM_SPECIALIST}'
)

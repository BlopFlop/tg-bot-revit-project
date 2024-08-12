import os
import sys
from datetime import datetime as dt
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

DATE_FORMAT: Final[str] = "%Y-%m-%d"
DATE_NOW: Final[str] = dt.now().strftime(DATE_FORMAT)


if __name__ == "__main__":
    BASE_DIR: Final[Path] = Path(sys.argv[0]).parent
else:
    BASE_DIR: Final[Path] = Path().parent

load_dotenv()

TG_TOKEN: Final[str] = os.getenv(key="TG_TOKEN", default="")

PATH_JSON_DB: Path = BASE_DIR / "data.json"

START_LOAD_MESSAGE_ARCH: str = (
    "Старт архивации моделей (перед этим , будут выгружены модели "
    "на ftp и в nawisworks)."
)
START_LOAD_MESSAGE_BACKUP: str = "Старт бэкапа моделей."
START_LOAD_MESSAGE_FTP: str = "Старт выгрузки моделей на сервер FTP."
START_LOAD_MESSAGE_NAWISWORKS: str = (
    "Старт выгрузки моделй Nawisworks (перед этим Revit модели будут выгружены"
    "на FTP)."
)
START_LOAD_MESSAGE_PUBLISH: str = (
    "Старт публикации моделей заказчику. (перед этим, будут выгружены модели "
    "на ftp и в nawisworks)."
)

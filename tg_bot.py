from pathlib import Path
import subprocess

from telegram.error import InvalidToken

from telegram_revit_project import TG_TOKEN, TgBot

if __name__ == "__main__":
    dir_check: Path = Path('dir_check.exe')
    if dir_check.is_file():
        subprocess.Popen(args=(dir_check,))
    tg_bot = TgBot(TG_TOKEN)
    try:
        tg_bot.message_start()
        updater = tg_bot.start_updater()
    except InvalidToken as ex:
        raise ex("Передайте корректный токен.")

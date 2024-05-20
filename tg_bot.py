from subprocess import Popen

from _constants import (
    PATH_DIR_CHECKS_EXE, TG_TOKEN,
    PATH_CMD_PROGRAM_EXE, BOT_START_MESSAGE,
)
from _tg_tools import TgBot
from _utils import check_dir_or_file


if __name__ == '__main__':
    except_message = (
        f'Файла {PATH_DIR_CHECKS_EXE.name} нет в директории с ботом.'
    )
    check_dir_or_file(PATH_DIR_CHECKS_EXE, except_message)
    dir_checker_process: Popen = Popen((PATH_DIR_CHECKS_EXE))
    except_message: str = (
        f'Файла {PATH_CMD_PROGRAM_EXE.name} нет в директории с ботом.'
    )
    check_dir_or_file(PATH_CMD_PROGRAM_EXE, except_message=except_message)
    telegram_bot: TgBot = TgBot(tg_token=TG_TOKEN)
    telegram_bot.send_message(BOT_START_MESSAGE)
    telegram_bot.start_updater()

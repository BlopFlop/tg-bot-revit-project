import logging
import subprocess
from pathlib import Path
from subprocess import Popen

from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.error import InvalidToken
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
    Updater,
)

# from cmd_program import project
from tg_bot.constants import BASE_DIR, DATE_NOW
from tg_bot.functions import DataChat, send_message_all_chats

NAME_PROJECT = "teST"

BUTTON_HELP: str = "help"
BUTTON_START: str = "start"
BUTTON_ADD_IN_PROJECT: str = "add_in_project"
BUTTON_REMOVE_IN_PROJECT: str = "remove_in_project"
BUTTON_FTP: str = "ftp"
BUTTON_NAWIS: str = "nawisworks"
BUTTON_PUB: str = "publish"

BOT_HELP_MESSAGE: str = (
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
START_LOAD_MESSAGE_ARCH: str = (
    "Старт архивации моделей (перед этим , будут выгружены модели "
    "на ftp и в nawisworks)."
)
START_LOAD_MESSAGE_ARCH_ALBUM: str = (
    "Старт архивации моделей после выдачи альбомов. (перед этим, "
    "будут выгружены модели на ftp и в nawisworks)."
)
START_LOAD_MESSAGE_BACKUP: str = "Старт бэкапа моделей."
START_LOAD_MESSAGE_FTP: str = "Старт выгрузки моделей на сервер FTP."
START_LOAD_MESSAGE_NAWISWORKS: str = (
    "Старт выгрузки моделй Nawisworks (перед этим Revit модели будут выгружены"
    " на FTP)."
)
START_LOAD_MESSAGE_PUBLISH: str = (
    "Старт публикации моделей заказчику. (перед этим, будут выгружены модели "
    "на ftp и в nawisworks)."
)
END_LOAD_MESSAGE_ARCH: str = "Архивация, закончена, "
END_LOAD_MESSAGE_ARCH_ALBUM: str = (
    "Архивация после выдачи альбомов, закончена, "
)
END_LOAD_MESSAGE_BACKUP: str = "Бэкап моделей, завершен,"
END_LOAD_MESSAGE_FTP: str = "Выгрузка моделей на FTP, завершена,"
END_LOAD_MESSAGE_NAWISWORKS: str = "Выгрузка моделей Navisworks, завершена,"
END_LOAD_MESSAGE_PUBLISH: str = "Публикация моделей, завершена,"


class TgBot:
    process_: Popen = None
    cmd_exe_program = "cmd_program.exe"

    def __init__(self, token: str) -> None:
        self.bot: Bot
        self.updater: Updater

        self.chats = DataChat(base_dir=BASE_DIR)
        self._init_tg_bot(token=token)

    def _get_cmd_program(self) -> Path | None:
        exe_path = BASE_DIR / self.cmd_exe_program
        if exe_path.is_file():
            logging.info(f"Файл {exe_path.name} для запуска моделей найден.")
            return exe_path
        logging.warning(
            f"Файл {exe_path.name} для запуска моедей не найден, процессы"
            " выгрузки не будут запущены."
        )

    def _init_tg_bot(self, token: str) -> None:
        """Инициализация телеграм бота."""
        try:
            self.bot = Bot(token=token)
            self.updater = Updater(token=token)

        except InvalidToken:
            error_message = (
                "Токен переданный в .env неправильный, пожалуйста "
                "пересоздайте файл .env."
            )
            logging.exception(error_message, stack_info=True)

    def _track_process(
        self,
        update: Update,
        context: ContextTypes,
    ) -> bool:
        """Трекинг запущенных процессов, предотвращает запуск одних и тех же
        процессов"""
        chat_id = update.effective_chat.id
        if isinstance(self.process_, Popen):
            if self.process_.poll() is None:
                track_text: str = (
                    "Сейчас вызов процесса невозможен, дождитесь "
                    "окончания прошлого процесса."
                )
                context.bot.send_message(chat_id=chat_id, text=track_text)
                return False
        return True

    def wake_up(
        self, update: Update, context: ContextTypes
    ) -> None:
        chat = update.effective_chat
        name = update.message.chat.first_name
        button = ReplyKeyboardMarkup(
            [
                [f"/{BUTTON_HELP}"],
                [f"/{BUTTON_ADD_IN_PROJECT}", f"/{BUTTON_REMOVE_IN_PROJECT}"],
                [f"/{BUTTON_FTP}", f"/{BUTTON_NAWIS}", f"/{BUTTON_PUB}"],
            ],
            resize_keyboard=True,
        )

        message = f"Привет {name}, ты в ТГ боте проекта {NAME_PROJECT}."
        context.bot.send_message(
            chat_id=chat.id, text=message, reply_markup=button
        )
        logging.debug("BotCommand: Вызов команды пробуждения бота.")
        self.add_in_project(update, context)

    def help(
        self, update: Update, context: ContextTypes
    ) -> None:
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text=BOT_HELP_MESSAGE)

        info_message = (
            "BotCommand: Вызов команды для получения информации о "
            "функционале чат бота"
        )
        logging.info(info_message)

    def no_run(
        self, update: Update, context: ContextTypes
    ) -> None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Данная функция сейчас недоступна.",
        )

    def add_in_project(
        self, update: Update, context: ContextTypes
    ) -> None:
        """Добавление человека в проект."""
        current_chat_id = update.effective_chat.id

        if current_chat_id in self.chats.get():
            message = "Вы в уже в рассылке по проекту."
        else:
            self.chats.add(current_chat_id)
            message = "Вы были добавлены в рассылку по проекту."
            info_message = (
                f"Пользователь {update.effective_chat.first_name} с id"
                f" {current_chat_id} был добавлен в рассылку."
            )
            logging.info(info_message)

        context.bot.send_message(chat_id=current_chat_id, text=message)

    def remove_in_project(
        self, update: Update, context: ContextTypes
    ) -> None:
        current_chat_id = update.effective_chat.id

        if current_chat_id not in self.chats.get():
            message = "Вы не в рассылке."
        else:
            self.chats.remove(current_chat_id)
            message = "Вы были удалены из рассылки по проекту."
            info_message = (
                f"Пользователь {update.effective_chat.first_name} с id"
                f" {current_chat_id} был удален из рассылки."
            )
            logging.info(info_message)

        context.bot.send_message(chat_id=current_chat_id, text=message)

    def ftp(
        self, update: Update, context: ContextTypes
    ) -> None:

        cmd_arguments = (self.cmd_exe_program, "ftp", "--tg_mode")

        chat_id = update.effective_chat.id
        bot = context.bot
        bot.send_message(chat_id=chat_id, text=START_LOAD_MESSAGE_FTP)

        if self._track_process(update, context):
            self.process_ = subprocess.Popen(args=cmd_arguments)

    def nawisworks(
        self, update: Update, context: ContextTypes
    ) -> None:

        cmd_arguments = (self.cmd_exe_program, "nawisworks")

        if self._track_process(update, context):
            chat_id = update.effective_chat.id
            bot = context.bot
            bot.send_message(
                chat_id=chat_id, text=START_LOAD_MESSAGE_NAWISWORKS
            )
            self.process_ = subprocess.Popen(args=cmd_arguments)

    def publish(
        self, update: Update, context: ContextTypes
    ) -> None:

        cmd_arguments = (self.cmd_exe_program, "publish")

        if self._track_process(update, context):
            chat_id = update.effective_chat.id
            bot = context.bot
            bot.send_message(
                chat_id=chat_id, text=START_LOAD_MESSAGE_NAWISWORKS
            )
            self.process_ = subprocess.Popen(args=cmd_arguments)

    def arch_album(
        self, update: Update, context: ContextTypes
    ) -> None:
        name_album = '_'.join(context.args)
        cmd_arguments = (self.cmd_exe_program, "arch", "--name_album", name_album)

        if self._track_process(update, context):
            chat_id = update.effective_chat.id
            bot = context.bot
            bot.send_message(
                chat_id=chat_id, text=START_LOAD_MESSAGE_ARCH_ALBUM
            )
            self.process_ = subprocess.Popen(args=cmd_arguments)

    def message_start(self):
        send_message_all_chats(
            self.bot,
            message="Телеграм бот запущен нажми /start, для обновления кнопок.",
        )

    def start_updater(self) -> Updater:
        start_handler = CommandHandler(BUTTON_START, self.wake_up)
        help_handler = CommandHandler(BUTTON_HELP, self.help)
        add_user_in_project_handler = CommandHandler(
            BUTTON_ADD_IN_PROJECT, self.add_in_project
        )
        remove_user_in_project_handler = CommandHandler(
            BUTTON_REMOVE_IN_PROJECT, self.remove_in_project
        )
        if self._get_cmd_program() is not None:
            load_ftp_handler = CommandHandler(BUTTON_FTP, self.ftp)
            load_nawis_handler = CommandHandler(BUTTON_NAWIS, self.nawisworks)
            publish_project_handler = CommandHandler(BUTTON_PUB, self.publish)
            arch_album_handler = PrefixHandler(["#"], ["d"], self.arch_album)
        else:
            load_ftp_handler = CommandHandler(BUTTON_FTP, self.no_run)
            load_nawis_handler = CommandHandler(BUTTON_NAWIS, self.no_run)
            publish_project_handler = CommandHandler(BUTTON_PUB, self.no_run)
            arch_album_handler = PrefixHandler(["#"], ["d"], self.no_run)

        self.updater.dispatcher.add_handler(start_handler)
        self.updater.dispatcher.add_handler(help_handler)
        self.updater.dispatcher.add_handler(add_user_in_project_handler)
        self.updater.dispatcher.add_handler(remove_user_in_project_handler)
        self.updater.dispatcher.add_handler(load_ftp_handler)
        self.updater.dispatcher.add_handler(load_nawis_handler)
        self.updater.dispatcher.add_handler(publish_project_handler)
        self.updater.dispatcher.add_handler(arch_album_handler)

        while True:
            try:
                self.updater.start_polling(poll_interval=3)
                self.updater.idle()
            except Exception as ex:
                logging.error(stack_info=True, exc_info=ex)
                continue

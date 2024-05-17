import os
import subprocess

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, PrefixHandler

from settings import (
    FILE_LOAD_FTP, FILE_PUB_MODELS, FILE_LOAD_NAWIS, PATH_DATA_JSON,
    NAME_PROJECT, UPDATER, BOT_INFO_MESSAGE, LOAD_FTP_START_MESSAGE,
    LOAD_NAWIS_START_MESSAGE, PUBLISH_MODELS_MESSAGE, FILE_DEPLOY_ALBUM,
    KEY_JSON_CHAT_ID, KEY_JSON_NWD, logging
)
from json_data import JsonFile, update_json

JSON_OBJ = JsonFile(PATH_DATA_JSON)


obj_process_load_navis = None
pull_process_load_navis = 0
obj_process_load_ftp = None
pull_process_load_ftp = 0
obj_process_pub_model = None
pull_process_pub_model = 0
obj_process_deploy_album = None
pull_process_deploy_album = 0


def remove_in_project(update, context):
    '''Удаление человека из проекта.'''
    chats_id = JSON_OBJ.get(KEY_JSON_CHAT_ID)
    chat = update.effective_chat

    if str(chat.id) in chats_id:
        JSON_OBJ.delete({KEY_JSON_CHAT_ID: str(chat.id)})
        message = 'Вы были удалены из рассылки по проекту.'
        info_message = (
            f'Пользователь с id {str(chat.id)} удалил себя из рассылки.'
        )
        logging.info(info_message)
    else:
        message = 'Вас нет в рассылке'

    context.bot.send_message(chat_id=chat.id, text=message)


def add_in_project(update, context):
    '''Добавление человека в проект.'''
    chats_id = JSON_OBJ.get(KEY_JSON_CHAT_ID)

    chat = update.effective_chat
    message = 'Вы были добавлены в рассылку по проекту.'

    if str(chat.id) in chats_id:
        message = 'Вы уже рассылке'
    else:
        JSON_OBJ.patch({KEY_JSON_CHAT_ID: [str(chat.id)]})
        info_message = (
            f'Пользователь с id {str(chat.id)} был добавлен в рассылку.'
        )
        logging.info(info_message)

    context.bot.send_message(chat_id=chat.id, text=message)


def wake_up(update, context):
    '''Функция приветствие при запуске программы.'''
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [
            ['/info'],
            ['/add_in_project', '/remove_in_project'],
            ['/load_in_ftp', '/load_nawis_file', '/publish_models'],
        ], resize_keyboard=True
    )
    message = (
        f'Привет {name}, ты в ТГ боте проекта {NAME_PROJECT}.'
    )
    context.bot.send_message(
        chat_id=chat.id, text=message, reply_markup=button
    )

    logging.debug('Вызов команды пробуждения бота.')


def get_info(update, context):
    '''Команда для получения информации о функционале бота.'''
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=BOT_INFO_MESSAGE)

    info_message = (
        'BotCommand: Вызов команды для получения информации о '
        'функционале чат бота'
    )
    logging.info(info_message)


def load_model_in_ftp(update, context):
    '''Команда для загрузки моделей на сервер FTP.'''
    global obj_process_load_ftp
    global pull_process_load_ftp

    chat = update.effective_chat

    if isinstance(obj_process_load_ftp, subprocess.Popen):
        pull_process_load_ftp = obj_process_load_ftp.poll()

    if pull_process_load_ftp == 0:
        update_json()
        context.bot.send_message(chat_id=chat.id, text=LOAD_FTP_START_MESSAGE)
        obj_process_load_ftp = subprocess.Popen((FILE_LOAD_FTP))

        debug_message = (
            'BotCommand: Запуск скрипта выгрузки моделей на сервер FTP'
        )
        logging.debug(debug_message)
    else:
        message = 'Выгрузка моделей на FTP, уже запущена.'
        context.bot.send_message(chat_id=chat.id, text=message)


def load_nawis_model(update, context):
    '''Команда для загрузки модели Nawisworks.'''
    global obj_process_load_navis
    global pull_process_load_navis

    chat = update.effective_chat

    if isinstance(obj_process_load_navis, subprocess.Popen):
        pull_process_load_navis = obj_process_load_navis.poll()

    if pull_process_load_navis == 0:
        update_json()
        source_path_nwf, load_dir = JSON_OBJ.get(KEY_JSON_NWD)
        message = ' '.join(
            (
                LOAD_NAWIS_START_MESSAGE,
                '. Файлы искать по пути:',
                os.path.dirname(load_dir)
            )
        )
        context.bot.send_message(chat_id=chat.id, text=message)
        obj_process_load_navis = subprocess.Popen((FILE_LOAD_NAWIS))

        debug_message = (
            'BotCommand: Запуск скрипта выгрузки моделей в Navisworks.'
        )
        logging.debug(debug_message)
    else:
        message = (
            'Выгрузка моделей в Navisworks уже запущена, дождитесь выгрузки.'
        )
        context.bot.send_message(chat_id=chat.id, text=message)


def publish_models(update, context):
    '''Публикация моделей заказчику'''
    global obj_process_pub_model
    global pull_process_pub_model

    chat = update.effective_chat

    if isinstance(obj_process_pub_model, subprocess.Popen):
        pull_process_pub_model = obj_process_pub_model.poll()

    if pull_process_pub_model == 0:
        update_json()
        context.bot.send_message(chat_id=chat.id, text=PUBLISH_MODELS_MESSAGE)
        obj_process_pub_model = (
            subprocess.Popen((FILE_PUB_MODELS))
        )

        debug_message = (
            'BotCommand: Запуск скрипта публикации моделей заказчику.'
        )
        logging.debug(debug_message)
    else:
        message = (
            'Выгрузка моделей для выгрузки заказчику уже '
            'запущена, дождитесь выгрузки.'
        )
        context.bot.send_message(chat_id=chat.id, text=message)


def arch_models_after_deploy_album(update, context):
    '''Архивация моделей после выпуска альбомов'''
    global obj_process_deploy_album
    global pull_process_deploy_album

    arg_cmd = '_'.join(context.args)
    chat = update.effective_chat

    if isinstance(obj_process_deploy_album, subprocess.Popen):
        pull_process_deploy_album = obj_process_deploy_album.poll()

    if pull_process_deploy_album == 0:
        update_json()
        obj_process_deploy_album = (
            subprocess.Popen((FILE_DEPLOY_ALBUM, arg_cmd))
        )
        debug_message = 'BotCommand: Запуск скрипта архиващии моделей.'
        logging.debug(debug_message)
    else:
        message = (
            'Архивация моделей после выдачи альбомов уже запущена. Подождите.'
        )
        context.bot.send_message(chat_id=chat.id, text=message)


def check_bot(update, context):
    '''Проверка работы бота'''
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='status_bot: working')


def main():
    print('Ты в программе апдейтера бота, для Revit проекта.')
    UPDATER.dispatcher.add_handler(CommandHandler('start', wake_up))
    UPDATER.dispatcher.add_handler(CommandHandler('info', get_info))
    UPDATER.dispatcher.add_handler(
        CommandHandler('remove_in_project', remove_in_project)
    )
    UPDATER.dispatcher.add_handler(
        CommandHandler('add_in_project', add_in_project)
    )
    UPDATER.dispatcher.add_handler(
        CommandHandler('load_in_ftp', load_model_in_ftp)
    )
    UPDATER.dispatcher.add_handler(
        CommandHandler('load_nawis_file', load_nawis_model)
    )
    UPDATER.dispatcher.add_handler(
        CommandHandler('publish_models', publish_models)
    )
    UPDATER.dispatcher.add_handler(
        CommandHandler('check_bot', check_bot)
    )
    UPDATER.dispatcher.add_handler(
        PrefixHandler(['#'], ['d'], arch_models_after_deploy_album)
    )
    UPDATER.start_polling(poll_interval=3)
    UPDATER.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        logging.error(ex)
        raise ex

import os
import json
import subprocess
import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, PrefixHandler

from google_tab import get_nwd_paths
from constants import (
    FILE_LOAD_FTP, FILE_PUB_MODELS, FILE_LOAD_NAWIS, NAME_JSON_FILE,
    NAME_PROJECT, UPDATER, BOT_INFO_MESSAGE, LOAD_FTP_START_MESSAGE,
    LOAD_NAWIS_START_MESSAGE, PUBLISH_MODELS_MESSAGE, FILE_NAME_LOG,
    FILE_DEPLOY_ALBUM
)


obj_process_load_navis = None
pull_process_load_navis = 0
obj_process_load_ftp = None
pull_process_load_ftp = 0
obj_process_pub_model = None
pull_process_pub_model = 0
obj_process_deploy_album = None
pull_process_deploy_album = 0

logging.basicConfig(
    handlers=[logging.FileHandler(FILE_NAME_LOG, 'a', 'utf-8')],
    level=logging.DEBUG,
    format='%(asctime)s, [%(levelname)s] %(message)s',
)


def get_json():
    '''Получение json, в папке с проектом.'''
    # dirname = os.path.dirname(sys.executable)
    dirname = os.path.dirname(__file__)
    path_json = os.path.join(dirname, NAME_JSON_FILE)
    if not os.path.isfile(path_json):
        file = open(path_json, 'w+')
        file.write('{}')
        file.close()
    return path_json


def remove_in_project(update, context):
    '''Удаление человека из проекта.'''
    with open(get_json(), 'r') as json_file:
        data = json.load(json_file)
    chat = update.effective_chat
    message = 'Вы были удалены из рассылки по проекту.'

    if str(chat.id) in data.keys():
        data.pop(str(chat.id))
    else:
        message = 'Вас нет в рассылке'

    with open(get_json(), 'w') as json_file:
        json.dump(data, json_file)

    context.bot.send_message(chat_id=chat.id, text=message)


def add_in_project(update, context):
    '''Добавление человека в проект.'''
    with open(get_json(), 'r') as json_file:
        data = json.load(json_file)
    chat = update.effective_chat
    message = 'Вы были добавлены в рассылку по проекту.'

    if str(chat.id) in data.keys():
        message = 'Вы уже рассылке'
    else:
        data[chat.id] = update.message.chat.first_name
        with open(get_json(), 'w') as json_file:
            json.dump(data, json_file)

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
        f'Привет {name}, ты в ТГ боте проекта {NAME_PROJECT}, и ты был '
        'подписан на рассылку о состоянии проекта.'
    )
    context.bot.send_message(
        chat_id=chat.id, text=message, reply_markup=button
    )

    with open(get_json(), 'r') as json_file:
        data = json.load(json_file)

    if str(chat.id) not in data.keys():
        data[chat.id] = name

        with open(get_json(), 'w') as file:
            json.dump(data, file)


def get_info(update, context):
    '''Команда для получения информации о функционале бота.'''
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=BOT_INFO_MESSAGE)


def load_model_in_ftp(update, context):
    '''Команда для загрузки моделей на сервер FTP.'''
    global obj_process_load_ftp
    global pull_process_load_ftp

    chat = update.effective_chat

    if isinstance(obj_process_load_ftp, subprocess.Popen):
        pull_process_load_ftp = obj_process_load_ftp.poll()

    if pull_process_load_ftp == 0:
        context.bot.send_message(chat_id=chat.id, text=LOAD_FTP_START_MESSAGE)
        obj_process_load_ftp = subprocess.Popen(('py', '-3.11', FILE_LOAD_FTP))
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
        source_path_nwf, load_dir = get_nwd_paths()
        message = ' '.join(
            (
                LOAD_NAWIS_START_MESSAGE,
                '. Файлы искать по пути:',
                os.path.dirname(load_dir)
            )
        )
        context.bot.send_message(chat_id=chat.id, text=message)
        obj_process_load_navis = (
            subprocess.Popen(('py', '-3.11', FILE_LOAD_NAWIS))
        )
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
        context.bot.send_message(chat_id=chat.id, text=PUBLISH_MODELS_MESSAGE)
        obj_process_pub_model = (
            subprocess.Popen(('py', '-3.11', FILE_PUB_MODELS))
        )
    else:
        message = (
            'Выгрузка моделей для выгрузки заказчику уже запущена, дождитесь'
            ' выгрузки.'
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
        obj_process_deploy_album = (
            subprocess.Popen(('py', '-3.11', FILE_DEPLOY_ALBUM, arg_cmd))
        )
    else:
        message = (
            'Архивация моделей после выдачи альбомов уже запущена. Подождите.'
        )
        context.bot.send_message(chat_id=chat.id, text=message)


def check_bot(update, context):
    '''Проверка работы бота'''
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='OK')


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

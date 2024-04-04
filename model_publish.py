from datetime import datetime as dt
import os
import shutil
# import sys

# from googleapiclient.errors import ResumableUploadError
# from google_disk import load_file_in_google_disk
# from function import send_email

from model_nawisworks import search_file
from tg_bot import send_message
from json_data import JsonFile
from settings import (
    NAME_PROJECT, NAME_FIELD_PUBLISH, SECONDS_IN_MINUTE,
    PATH_DATA_JSON, KEY_JSON_DIR_PATHS, KEY_JSON_PUB, logging
)


JSON_OBJ = JsonFile(PATH_DATA_JSON)


def create_dir(path):
    '''Создание директории.'''
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)
    return path


def start_pub_models():
    '''Начало публикации моделей.'''
    time_name = str(dt.now().strftime("%y%m%d"))

    start_message = 'Начало публикации моделей.'
    print(start_message)
    logging.debug(start_message)

    end_path = os.path.join(
        JSON_OBJ.get(KEY_JSON_DIR_PATHS).get(NAME_FIELD_PUBLISH),
        '_'.join((time_name, NAME_PROJECT))
    )
    create_dir(end_path)

    for models_paths, extention_file, end_dir in JSON_OBJ.get(KEY_JSON_PUB):
        end_dir = os.path.join(end_path, end_dir)
        create_dir(end_dir)

        if extention_file == '.nwd':
            pahts = sorted(search_file(models_paths, extention_file))
            path = pahts[-1]
            shutil.copy(path, end_dir)
        else:
            for path in search_file(models_paths, extention_file):
                shutil.copy(path, end_dir)

    start_arch_message = (
        'Формирование архива с моделями для публикациии заказчику.'
    )
    logging.debug(start_arch_message)

    path_archive = shutil.make_archive(
        base_name=end_path,
        format='zip',
        root_dir=JSON_OBJ.get(KEY_JSON_DIR_PATHS).get(NAME_FIELD_PUBLISH),
        base_dir=os.path.basename(end_path)
    )
    # shutil.rmtree(end_path)
    # google_disk_url = (
    #     load_file_in_google_disk(path_archive, GOOGLE_DISK_FOLDER_ID)
    # )
    return path_archive


if __name__ == '__main__':
    time_work = dt.now()
    start_message = (
        'Начинается формирование архива для публикации моделей заказчику. '
        'Время выгрузки зависит от размера всех моделей.'
    )
    send_message(start_message)
    logging.debug(start_message)

    # try:
    #     google_disk_url = start_pub_models()
    # except ResumableUploadError:
    #     error_message = (
    #         'При загрузке файла на Google Disk произошла ошибка. '
    #         'Google хранилище переполнено, архив с проектом доступен на FTP, '
    #         'сообщение на почту заказчика НЕ было отправлено.'
    #     )
    #     send_message(error_message)
    #     sys.exit()

    # tg_message = (
    #     f'Архив опубликован на гугл диске: {google_disk_url}\n'
    #     f'Время выгрузки составило {time_work} минут(ы|у).'
    # )
    # theme_message = f'Передача проекта {NAME_PROJECT}'
    # mail_message = (
    #     'Архив опубликован на гугл диске\n'
    #     f'{google_disk_url}\n'
    #     'ссылка действительна в течение 24 часов.\n'
    #     '--\n'
    #     'Данное письмо создано автоматически, по всем\n'
    #     'вопросам обращаться к BIM-Менеджеру\n'
    #     f'ФИО специалиста: {FAMILY_NAME_BIM_SPECIALIST}\n'
    #     '\n'
    #     'ООО «ЮНИПРО»\n'
    #     '+7 (495) 543-43-41\n'
    #     f'{PHONE_NUMBER_BIM_SPECIALIST}\n'
    # )
    # if TO_EMAIL_USER.count(','):
    #     for to_email_user in TO_EMAIL_USER.split(','):
    #         send_email(to_email_user, theme_message, mail_message)
    # else:
    #     send_email(TO_EMAIL_USER, theme_message, mail_message)

    time_work = (dt.now() - time_work).seconds // SECONDS_IN_MINUTE
    arch_path = start_pub_models()
    tg_message = (
        f'Архив собран по пути {arch_path} и готов к отправке заказчику. \n'
        f'Время выгрузки составило {time_work} минут(у|ы)'
    )
    send_message(tg_message)
    logging.debug(tg_message)

from datetime import datetime as dt
import os
import shutil
import sys

from googleapiclient.errors import ResumableUploadError

from google_tab import (
    get_dir_paths, get_publish_paths
)
from google_disk import load_file_in_google_disk
from model_nawisworks import search_file
from tg_bot import send_message
from send_mail import send_email

from constants import (
    NAME_PROJECT, TO_EMAIL_USER, NAME_FIELD_PUBLISH, GOOGLE_DISK_FOLDER_ID,
    FAMILY_NAME_BIM_SPECIALIST, PHONE_NUMBER_BIM_SPECIALIST, SECONDS_IN_MINUTE
)


def create_dir(path):
    '''Создание директории.'''
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)
    return path


def main():
    '''Начало публикации моделей.'''
    time_name = str(dt.now().strftime("%y%m%d"))
    end_path = os.path.join(
        get_dir_paths().get(NAME_FIELD_PUBLISH),
        '_'.join((time_name, NAME_PROJECT))
    )
    create_dir(end_path)

    for models_paths, extention_file, end_dir in get_publish_paths():
        end_dir = os.path.join(end_path, end_dir)
        create_dir(end_dir)

        if extention_file == '.nwd':
            pahts = sorted(search_file(models_paths, extention_file))
            path = pahts[-1]
            shutil.copy(path, end_dir)
        else:
            for path in search_file(models_paths, extention_file):
                shutil.copy(path, end_dir)

    path_archive = shutil.make_archive(
        base_name=end_path,
        format='zip',
        root_dir=get_dir_paths().get(NAME_FIELD_PUBLISH),
        base_dir=os.path.basename(end_path)
    )
    shutil.rmtree(end_path)
    google_disk_url = (
        load_file_in_google_disk(path_archive, GOOGLE_DISK_FOLDER_ID)
    )
    return google_disk_url


if __name__ == '__main__':
    time_work = dt.now()
    send_message(
        'Начинается формирование архива для публикации моделей заказчику. '
        'Время выгрузки зависит от размера всех моделей. (+- 20 минут)'
    )
    try:
        google_disk_url = main()
    except ResumableUploadError as ex:
        error_message = (
            'При загрузке файла на Google Disk произошла ошибка. '
            'Google хранилище переполнено, архив с проектом доступен на FTP, '
            'сообщение на почту заказчика НЕ было отправлено.'
        )
        send_message(error_message)
        raise ex
        sys.exit()

    time_work = (dt.now() - time_work).seconds // SECONDS_IN_MINUTE
    tg_message = (
        f'Архив опубликован на гугл диске: {google_disk_url}\n'
        f'Время выгрузки составило {time_work} минут(ы|у).'
    )
    theme_message = f'Передача проекта {NAME_PROJECT}'
    mail_message = (
        'Архив опубликован на гугл диске\n'
        f'{google_disk_url}\n'
        'ссылка действительна в течение 24 часов.\n'
        '--\n'
        'Данное письмо создано автоматически, по всем\n'
        'вопросам обращаться к BIM-Менеджеру\n'
        f'ФИО специалиста: {FAMILY_NAME_BIM_SPECIALIST}\n'
        '\n'
        'ООО «ЮНИПРО»\n'
        '+7 (495) 543-43-41\n'
        f'{PHONE_NUMBER_BIM_SPECIALIST}\n'
    )
    if TO_EMAIL_USER.count(','):
        for to_email_user in TO_EMAIL_USER.split(','):
            send_email(to_email_user, theme_message, mail_message)
    else:
        send_email(TO_EMAIL_USER, theme_message, mail_message)
    send_message(tg_message)

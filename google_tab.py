import os
import sys
import time

from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import apiclient

from settings import (
    NAME_SHEET_ARCHIVE, NAME_SHEET_BACKUP, NAME_SHEET_DIR_PATH,
    NAME_SHEET_NWC, NAME_SHEET_FTP, NAME_FIELD_NWD, NAME_FIELD_PATH_NWF,
    NAME_FIELD_PUBLISH, CREDENTIALS_FILE_PATH, SPREADSHEET_ID,
    KEY_JSON_ARCH, KEY_JSON_BACKUP, KEY_JSON_FTP, KEY_JSON_NWC,
    KEY_JSON_NWD, KEY_JSON_PUB, KEY_JSON_DIR_PATHS, logging
)


def check_cred() -> None | Exception:
    '''Проверка наличия файла creds.json в директории со скриптом'''
    if not os.path.isfile(CREDENTIALS_FILE_PATH):
        except_message = 'Не найден файл creds.json в папке со скриптом'
        logging.error(except_message)
        raise FileNotFoundError(except_message)


def get_data_in_google_tab() -> list[tuple[str, str]]:
    '''Получение данных из гугл таблицы.'''
    logging.debug('Происходит получение данных из гугл таблицы.')

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE_PATH,
        [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    http_auth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    try:
        sheets = (
            service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        )
    except apiclient.errors.HttpError:
        error_message = (
            'Вы передали неверный id гугл таблицы, исправте это в .env.'
        )
        print(error_message)
        logging.error(error_message)
        time.sleep(5)
        sys.exit()

    sheets_id = {}
    for sheet in sheets.get('sheets'):
        title = sheet.get('properties').get('title')

        data_tab = (
            service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=title,
                majorDimension='ROWS'
            ).execute()
        )
        sheets_id[title] = data_tab.get('values')
    return sheets_id


def get_dir_paths(data_in_google_tab) -> dict[str]:
    '''Получение путей до директорий.'''
    return {
        path[0]: path[1]
        for path in data_in_google_tab.get(NAME_SHEET_DIR_PATH)[1:]
        if path[0] and path[1]
    }


def get_backup_paths(data_in_google_tab, dir_paths) -> list[tuple[str, str]]:
    '''Получение путей для бэкапа моделей'''
    return [
        (path[0], path[1], dir_paths.get(NAME_SHEET_BACKUP))
        for path in data_in_google_tab.get(NAME_SHEET_BACKUP)[1:]
        if path[0] and path[1]
    ]


def get_archive_paths(data_in_google_tab, dir_paths) -> list[tuple[str, str]]:
    '''Получение путей для архивации моделей'''
    return [
        (path[0], dir_paths.get(NAME_SHEET_ARCHIVE), path[1])
        for path in data_in_google_tab.get(NAME_SHEET_ARCHIVE)[1:]
        if path[0] and path[1]
    ]


def get_ftp_paths(data_in_google_tab, dir_paths) -> list[tuple[str, str]]:
    '''Получение путей для выгрузки моделей на сервер FTP'''
    return [
        (path[0], path[1], dir_paths.get(NAME_SHEET_FTP))
        for path in data_in_google_tab.get(NAME_SHEET_FTP)[1:]
        if path[0] and path[1]
    ]


def get_nwc_paths(data_in_google_tab, dir_paths) -> list[tuple[str, str]]:
    '''Получение путей для выгрузки nwc моделей'''
    return [
        (path[0], dir_paths.get(NAME_SHEET_NWC), path[1])
        for path in data_in_google_tab.get(NAME_SHEET_NWC)[1:]
        if path[0] and path[1]
    ]


def get_nwd_paths(dir_paths) -> tuple[str, str]:
    '''Получение путей для выгрузки nwd моделей'''
    return (
            dir_paths.get(NAME_FIELD_PATH_NWF),
            dir_paths.get(NAME_FIELD_NWD)
        )


def get_publish_paths(data_in_google_tab) -> list[tuple[str, str, str]]:
    '''Получение путей для формирования директории,
    для публикации модели заказчику'''
    return [
        (path[0], path[1], path[2])
        for path in data_in_google_tab.get(NAME_FIELD_PUBLISH)[1:]
        if path[0] and path[1] and path[2]
    ]


def get_json_data() -> dict[list[str]]:
    '''Получение путей для формирования json файла'''
    data_in_google_tab = get_data_in_google_tab()
    dir_paths = get_dir_paths(data_in_google_tab)
    data = {
        KEY_JSON_ARCH: get_archive_paths(data_in_google_tab, dir_paths),
        KEY_JSON_BACKUP: get_backup_paths(data_in_google_tab, dir_paths),
        KEY_JSON_FTP: get_ftp_paths(data_in_google_tab, dir_paths),
        KEY_JSON_NWC: get_nwc_paths(data_in_google_tab, dir_paths),
        KEY_JSON_NWD: get_nwd_paths(dir_paths),
        KEY_JSON_PUB: get_publish_paths(data_in_google_tab),
        KEY_JSON_DIR_PATHS: dir_paths
    }
    return data

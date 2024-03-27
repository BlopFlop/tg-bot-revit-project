import os
import logging

from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import apiclient

from constants import (
    NAME_SHEET_ARCHIVE, NAME_SHEET_BACKUP, NAME_SHEET_DIR_PATH,
    NAME_SHEET_NWC, NAME_SHEET_FTP, NAME_FIELD_NWD, NAME_FIELD_PATH_NWF,
    NAME_FIELD_PUBLISH, CREDENTIALS_FILE_PATH, SPREADSHEET_ID,
)


logging.basicConfig(
    level=logging.INFO,
    filename='google_tab_log.log',
    format='%(asctime)s, %(levelname)s, %(message)s',
    filemode='w'
)


def check_cred() -> None | Exception:
    '''Проверка наличия файла creds.json в директории со скриптом'''
    if not os.path.isfile(CREDENTIALS_FILE_PATH):
        except_message = 'Не найден файл creds.json в папке со скриптом'
        logging.error(except_message)
        raise FileNotFoundError(except_message)


def get_data_in_google_tab() -> list[tuple[str, str]]:
    '''Получение данных из гугл таблицы.'''
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE_PATH,
        [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    http_auth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    sheets = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()

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


def get_dir_paths() -> dict[str]:
    '''Получение путей до директорий.'''
    data_in_google_tab = get_data_in_google_tab()
    return {
        path[0]: path[1]
        for path in data_in_google_tab.get(NAME_SHEET_DIR_PATH)[1:]
    }


def get_backup_paths() -> list[tuple[str, str]]:
    '''Получение путей для бэкапа моделей'''
    data_in_google_tab = get_data_in_google_tab()
    dir_paths = get_dir_paths()
    return [
        (path[0], path[1], dir_paths.get(NAME_SHEET_BACKUP))
        for path in data_in_google_tab.get(NAME_SHEET_BACKUP)[1:]
    ]


def get_archive_paths() -> list[tuple[str, str]]:
    '''Получение путей для архивации моделей'''
    data_in_google_tab = get_data_in_google_tab()
    dir_paths = get_dir_paths()
    return [
        (path[0], dir_paths.get(NAME_SHEET_ARCHIVE), path[1])
        for path in data_in_google_tab.get(NAME_SHEET_ARCHIVE)[1:]
    ]


def get_ftp_paths() -> list[tuple[str, str]]:
    '''Получение путей для выгрузки моделей на сервер FTP'''
    data_in_google_tab = get_data_in_google_tab()
    dir_paths = get_dir_paths()
    return [
        (path[0], path[1], dir_paths.get(NAME_SHEET_FTP))
        for path in data_in_google_tab.get(NAME_SHEET_FTP)[1:]
    ]


def get_nwc_paths() -> list[tuple[str, str]]:
    '''Получение путей для выгрузки nwc моделей'''
    data_in_google_tab = get_data_in_google_tab()
    dir_paths = get_dir_paths()
    return [
        (path[0], dir_paths.get(NAME_SHEET_NWC), path[1])
        for path in data_in_google_tab.get(NAME_SHEET_NWC)[1:]
    ]


def get_nwd_paths() -> tuple[str, str]:
    '''Получение путей для выгрузки nwd моделей'''
    dir_paths = get_dir_paths()
    return (
            dir_paths.get(NAME_FIELD_PATH_NWF),
            dir_paths.get(NAME_FIELD_NWD)
        )


def get_publish_paths() -> list[tuple[str, str, str]]:
    '''Получение путей для формирования директории,
    для публикации модели заказчику'''
    data_in_google_tab = get_data_in_google_tab()
    return [
        (path[0], path[1], path[2])
        for path in data_in_google_tab.get(NAME_FIELD_PUBLISH)[1:]
    ]

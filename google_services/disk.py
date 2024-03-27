import os
import sys

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaFileUpload
import httplib2
import apiclient

from settings.constants import CREDENTIALS_FILE_PATH


def check_cred() -> None | Exception:
    '''Проверка наличия файла creds.json в директории со скриптом'''
    if not os.path.isfile(CREDENTIALS_FILE_PATH):
        except_message = 'Не найден файл creds.json в папке со скриптом'
        raise FileNotFoundError(except_message)


def load_file_in_google_disk(file_path: str, folder_id: str) -> str:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE_PATH,
        [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    http_auth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('drive', 'v3', http=http_auth)

    basename = os.path.basename(file_path)
    file_metadata = {'name': basename, 'parents': [folder_id]}

    media = MediaFileUpload(file_path, resumable=True)
    created = (
        service.files().create(
            body=file_metadata, media_body=media, fields="id,webViewLink"
        )
    ).execute()
    file_permission = {"role": "reader", "type": "anyone"}

    service.permissions().create(
        body=file_permission, fileId=created.get("id")
    ).execute()

    return created.get("webViewLink")

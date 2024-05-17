import os
import json

<<<<<<< HEAD
from constants import (
    PATH_DATA_JSON, KEY_JSON_ARCH, KEY_JSON_BACKUP, KEY_JSON_CHAT_ID,
    KEY_JSON_FTP, KEY_JSON_NWC, KEY_JSON_NWD, KEY_JSON_PUB, KEY_JSON_DIR_PATHS,
    CREDENTIALS_FILE_PATH, NAME_CREDS_JSON
)
from utils import check_dir_or_file
=======
from settings import (
    PATH_DATA_JSON, KEY_JSON_ARCH, KEY_JSON_BACKUP, KEY_JSON_CHAT_ID,
    KEY_JSON_FTP, KEY_JSON_NWC, KEY_JSON_NWD, KEY_JSON_PUB, KEY_JSON_DIR_PATHS
)
>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9
from google_tab import get_json_data


class JsonFile:
    CONST_FIELDS = (
        KEY_JSON_ARCH, KEY_JSON_BACKUP, KEY_JSON_FTP, KEY_JSON_NWC,
        KEY_JSON_DIR_PATHS, KEY_JSON_NWD, KEY_JSON_PUB, KEY_JSON_CHAT_ID
    )

    def __init__(self, path_file: str) -> None:
        self.path_file = self._check_or_create_file(path_file)

    def _check_or_create_file(self, path_json: str) -> str:
        if not os.path.isfile(path_json):
            with open(path_json, mode='w', encoding='utf-8') as json_file:
<<<<<<< HEAD
                write_data: str = '{' + ', '.join(
=======
                write_data = '{' + ', '.join(
>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9
                    f'"{field}": ""' for field in self.CONST_FIELDS
                ) + '}'
                json_file.write(write_data)
        return path_json

    def _read_file(self) -> str:
        path_file = self._check_or_create_file(self.path_file)
<<<<<<< HEAD
        with open(str(path_file), mode='r', encoding='utf-8') as json_file:
=======
        with open(path_file, mode='r', encoding='utf-8') as json_file:
>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9
            data = json.load(json_file)
        return data

    def _change_file(self, new_data: dict[str]) -> str:
        path_file = self._check_or_create_file(self.path_file)
<<<<<<< HEAD
        with open(str(path_file), mode='w', encoding='utf-8') as json_file:
            json.dump(new_data, json_file)
        return new_data

    def get(self, key_data: str = None) -> dict[str:list[str]] | list[str]:
=======
        with open(path_file, mode='w', encoding='utf-8') as json_file:
            json.dump(new_data, json_file)
        return new_data

    def get(self, key_data: str = None) -> dict[str] | list[str]:
>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9
        data: dict[str:list[str]] = self._read_file()

        if key_data:
            if key_data not in data.keys():
                except_message = (
                    'Вы хотите получить информацию из json, передав'
                    f' несуществующий ключ {key_data}.'
                )
                raise KeyError(except_message)
            return data[key_data]
        return data

    def patch(self, patch_data: dict[str]) -> dict[str]:
        data: dict[str:list[str]] = self._read_file()
        for key, value in patch_data.items():
            if key not in data.keys():
                data[key] = value
            else:
                if hasattr(value, '__iter__') and not isinstance(value, str):
                    add_data = [
                        item for item in value
                        if item not in data[key]
                    ]
                    data[key] = [*data[key], *add_data]
                else:
                    data[key].append(value)
        data = self._change_file(data)
        return patch_data

    def put(self, put_data: dict[str]) -> dict[str]:
        data: dict[str:list[str]] = self._read_file()
        for key, value in put_data.items():
            data[key] = value
        data = self._change_file(data)
        return put_data

    def delete(self, delete_data: dict[str: str]) -> dict[str]:
        data: dict[str:list[str]] = self._read_file()
        for key, value in delete_data.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                data[key] = [
                    item for item in data[key]
                    if item not in delete_data
                ]
            else:
                data[key].remove(delete_data[key])
        data: dict[str:list[str]] = self._change_file(data)
        return delete_data

<<<<<<< HEAD
    def update_json_from_google_tab(self) -> None:
        except_message = (
            f'Файл {NAME_CREDS_JSON} не существует, создайте его в гугл '
            'сервисах.'
        )
        check_dir_or_file(CREDENTIALS_FILE_PATH, except_message)
        data = get_json_data()
        self.put(data)


JSON_OBJ: JsonFile = JsonFile(str(PATH_DATA_JSON))

if __name__ == '__main__':
    JSON_OBJ.update_json_from_google_tab()
=======

def update_json() -> None:
    json_obj: type[JsonFile] = JsonFile(PATH_DATA_JSON)
    data = get_json_data()
    json_obj.put(data)


if __name__ == '__main__':
    json_obj: type[JsonFile] = JsonFile(PATH_DATA_JSON)
    data = get_json_data()
    json_obj.put(data)
>>>>>>> 6985548735c0bde6118e09c3f523d759e5d80bb9

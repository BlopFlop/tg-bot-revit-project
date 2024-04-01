import os
import time


CREATE_ENV_DATA = {
    'FAMILY_NAME_BIM_SPECIALIST': '',
    'PHONE_NUMBER_BIM_SPECIALIST': '',
    'NAME_PROJECT': '',
    'NAWIS_OR_REVIT_VERSION': '',
    'EMAIL_HOST_USER': '',
    'TO_EMAIL_USER': '',
    'TG_TOKEN': '',
    'SPREADSHEET_ID': '',
    'GOOGLE_DISK_FOLDER_ID': '',
    'EMAIL_HOST_PASSWORD': '',
    'EMAIL_HOST': 'smtp.mail.ru',
    'EMAIL_PORT': '587',
    'EMAIL_USE_TLS': 'False',
    'EMAIL_USE_SSL': 'True',
}
REQUIRED_FIELD = {
    'FAMILY_NAME_BIM_SPECIALIST': 'Фамилия, имя. BIM Специалиста.',
    'EMAIL_HOST_USER': 'Емейл|почта.',
    'PHONE_NUMBER_BIM_SPECIALIST': 'Номер телефона.',
    'TO_EMAIL_USER': (
        'Почты получателей (записть через пробел'
        ' или запятую если почт несколько)'),
    'NAME_PROJECT': 'Имя проекта.',
    'NAWIS_OR_REVIT_VERSION': 'Версия Revit|Navis (Пример 2021)',
    'EMAIL_HOST_PASSWORD': (
        'Пароль от вашей почты (сгенерированный '
        'для сторонних приложений.)'
    ),
    'TG_TOKEN': 'Токен телеграм бота.',
    'SPREADSHEET_ID': 'Айди гугл таблицы.',
    'GOOGLE_DISK_FOLDER_ID': 'Айди папки на гугл диске.',
}


def flush_print(text: str):
    for symb in text:
        time.sleep(0.005)
        print(symb, end='', flush=True)
    print()


def get_data_env(path: str) -> dict[str: str]:
    env_data = {}
    with open(path, mode='r', encoding='utf-8') as env_file:
        for data in env_file.read().split('\n'):
            key, value = data.split('=')
            env_data[key] = value
    return env_data


def add_data_env(path: str, data_env: dict[str, str]) -> None:
    with open(path, mode='w', encoding='utf-8') as env_file:
        data_env = '\n'.join(
            [f'{key}={value}' for key, value in data_env.items()]
        )
        env_file.write(data_env)


def check_env(path: str) -> None:
    if os.path.isfile(path):
        env_data = get_data_env(path)
        env_data = fill_env(env_data)
        if env_data:
            add_data_env(path, env_data)
    else:
        create_env(path=path)


def create_env(path: str) -> None:
    create_env_data = fill_env(CREATE_ENV_DATA.copy())

    add_data_env(path, create_env_data)


def fill_env(env_data: dict[str: str]) -> None:
    if '' not in env_data.values():
        return None

    flush_print(
        'В файле .env где находятся секретные данные, есть '
        'незаполненнеые поля, сейчас вам предложат их заполнить.'
    )
    for key, item in env_data.items():
        if not item:
            flush_print(('Поле: ' + REQUIRED_FIELD.get(key)))
            input_message = 'Введите данные поля >>> '
            value = input(input_message)
            if ',' in value:
                value = '$'.join(value.split(','))
            elif ' ' in value:
                value = '$'.join(value.split())
            env_data[key] = value
    return env_data


def get_env(base_dir) -> str:
    flush_print('Получение данных из .env')
    path_env = os.path.join(base_dir, '.env')
    flush_print('Проверка на заполенность полей.')
    check_env(path=path_env)
    flush_print('Все ок все данные из файла .env подгружены.')
    return path_env

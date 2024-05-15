import os


class EnvFile:
    CREATE_DATA = {
        'FAMILY_NAME_BIM_SPECIALIST': '',
        'PHONE_NUMBER_BIM_SPECIALIST': '',
        'NAME_PROJECT': '',
        'NAWIS_OR_REVIT_VERSION': '',
        'EMAIL_HOST_USER': 'None',
        'TO_EMAIL_USER': 'None',
        'TG_TOKEN': '',
        'SPREADSHEET_ID': '',
        'GOOGLE_DISK_FOLDER_ID': '...',
        'EMAIL_HOST_PASSWORD': 'None',
        'EMAIL_HOST': 'smtp.mail.ru',
        'EMAIL_PORT': '587',
        'EMAIL_USE_TLS': 'False',
        'EMAIL_USE_SSL': 'True',
    }
    REQUIRED_FIELD = {
        'FAMILY_NAME_BIM_SPECIALIST': 'Фамилия, имя. BIM Специалиста.',
        'PHONE_NUMBER_BIM_SPECIALIST': 'Номер телефона.',
        'NAME_PROJECT': 'Имя проекта.',
        'NAWIS_OR_REVIT_VERSION': 'Версия Revit|Navis (Пример 2021)',
        'TG_TOKEN': 'Токен телеграм бота.',
        'SPREADSHEET_ID': 'Айди гугл таблицы.',
    }
    FILE_EXTENTION = '.env'

    def __init__(self, base_dir) -> None:
        self.path = base_dir / self.FILE_EXTENTION
        self.check_or_create()

    def check_or_create(self):
        if not os.path.isfile(self.path):
            self._create()
        self._receivig_data_from_cmd()

    def _get(self):
        env_data = {}
        with open(self.path, mode='r', encoding='utf-8') as env_file:
            for data in env_file.read().split('\n'):
                key, value = data.split('=')
                env_data[key] = value
        return env_data

    def _push(self, data_env):
        with open(self.path, mode='w', encoding='utf-8') as env_file:
            data_env = '\n'.join(
                [f'{key}={value}' for key, value in data_env.items()]
            )
            env_file.write(data_env)

    def _create(self):
        self._push(self.CREATE_DATA)

    def _receivig_data_from_cmd(self):
        data = self._get()
        if '' not in data.values():
            return None

        print(
            'В файле .env где находятся секретные данные, есть '
            'незаполненнеые поля, сейчас вам предложат их заполнить.'
        )
        for key, item in data.items():
            if not item:
                print(('Поле: ' + self.REQUIRED_FIELD.get(key)))
                input_message = 'Введите данные поля >>> '
                value = input(input_message)
                if ',' in value:
                    value = '$'.join(value.split(','))
                elif ' ' in value:
                    value = '$'.join(value.split())
                data[key] = value

        self._push(data)

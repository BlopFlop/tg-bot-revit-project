# tg-bot-revit-project
Проект представляет собой

# Технологии
Python 3.11
Telegram API
Google Sheets API
Google Disk API

# Авторы
BlopFlop(ArturYoungBlood)


# Документация
Telegram API - https://docs.python-telegram-bot.org/en/v21.0.1/
Google Sheets API - https://developers.google.com/sheets?hl=ru
Google Disk API - https://developers.google.com/drive?hl=ru


# Инструкции
Создать телеграм бота, ссылка на инструкцию:
```
https://habr.com/ru/articles/442800/
```
Создать проект на https://console.cloud.google.com/, ссылка на инструкцию:
```
https://habr.com/ru/articles/483302/
```
```
https://www.youtube.com/watch?v=caiR7WAGMVM&ab_channel=TheLookin
```

Получить от сервисного google аккаунта, json файл с ключами =>
Переименовать в 'creeds.json' и положить файл в папку settings.

В папке settings cоздать файл .env заполнить его следующим образом:

```
NAME_PROJECT=MJVAL
NAWIS_OR_REVIT_VERSION=2021
TG_TOKEN=6533579547:AAH-OXNvJHMJs2Amz3Fmc2dYA5xNaDUh13c
SPREADSHEET_ID=1NcpCgzaH-NO4iZ5zUaUvK_FxMrDO7W5fCpHHSb6v2SM
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=587
EMAIL_HOST_PASSWORD=WDUts1f2UQ5NVt9BrpVP
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER=a.yungblyud@upgroup.ru
TO_EMAIL_USER=k.melnik@upgroup.ru,yu.gordienko@upgroup.ru,arturungb@gmail.com
GOOGLE_DISK_FOLDER_ID=1oqZjIz_H2m-CsaBtbcJUgDDFFQT8lu60
FAMILY_NAME_BIM_SPECIALIST=Юнгблюд,Артур,Владимирович
PHONE_NUMBER_BIM_SPECIALIST=+7(912)318-59-32
```

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:BlopFlop/tg-bot-revit-project.git
```

```
cd /tg-bot-revit-project
```

Cоздать и активировать виртуальное окружение:

```
py -3.11 -m venv venv
```

```
source venv/Skripts/Activate
```

```
py -3.11 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```



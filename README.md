# tg-bot-revit-project
Проект tg-bot-revit-project представляет собой 3 программы:
1) tg_bot.exe - Телеграмм бот.
2) cmd_command.exe - Консольное приложение, функция которого, выгружать модели.
3) dir_checks.exe - Программа следящая за директорией.
Функционал Телеграм бота(tg_bot.exe):
1) Информирует проектировщиков о действиях над Revit/Nawis файлами: обновление/удаление/замена моделей подрядчиком,
еженедельная архивация и ежедневный бэкап моделей. 
2) Команда FTP, запускает cmd_command.exe с аргументами "ftp, -ud(update json)", выгружает на сервер FTP, 
для актуализации моделей подрядчику.
3) Команда Nawisworks, запускает cmd_command.exe с аргументами "nawisworks, -ud(update json)", выгружает моедели 
из формата .rvt(RevitModel) в .nwc(NaiwsModel) и .nwd(Сборка NaiwsModel)
4) Команда publish, запускает cmd_command.exe с аргументами "publish, -ud(update json)", после происходит формирование
архива с моделями.
5) Сообщение  #d <Имя альбома>, запускает cmd_command.exe с аргументами "arch_album, -na(--name_album) <Имя альбома>, 
-ud(--update_json)", и формирует архив после выдачи альбомов с датой и именем указанным в <Имя альбома>
Функционал...

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

Файл env создается автоматически, при создании консольное приложение попросит вас заполнить форму:

```
FAMILY_NAME_BIM_SPECIALIST={ФИО BIM специалиста}
PHONE_NUMBER_BIM_SPECIALIST={Номер BIM специалиста}
NAME_PROJECT={Имя проекта}
NAWIS_OR_REVIT_VERSION={Версия Revit в формате 2021}
EMAIL_HOST_USER={Почта исходная, с нее будут отправлятся сообщения в telegram боте}
TO_EMAIL_USER={Почта конечная(Можно записать через запятую несколько почт), на нее будут отправлятся сообщения о выгруженных моделей}
TG_TOKEN={Токен телеграм бота}
SPREADSHEET_ID={Id Google таблицы}
GOOGLE_DISK_FOLDER_ID={Id Google диска}
EMAIL_HOST={smtp.mail.ru}
EMAIL_PORT={587}
EMAIL_HOST_PASSWORD={WDUts1f2UQ5NVt9BrpVP}
EMAIL_USE_TLS={По умолчанию False}
EMAIL_USE_SSL={По умолчанию True}
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



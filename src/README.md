# tg-bot-revit-project
---
h1 Проект tg-bot-revit-project представляет собой 3 программы:
1. tg_bot.exe - Телеграмм бот.
2. cmd_command.exe - Консольное приложение, функция которого, выгружать модели.
3. dir_checks.exe - Программа следящая за директорией.
h2 Функционал Телеграм бота(tg_bot.exe):
1. Информирует проектировщиков о действиях над Revit/Nawis файлами: обновление/удаление/замена моделей подрядчиком,
еженедельная архивация и ежедневный бэкап моделей. 
2. Команда FTP, запускает cmd_command.exe с аргументами "ftp, -ud(update json)", выгружает на сервер FTP, 
для актуализации моделей подрядчику.
3. Команда Nawisworks, запускает cmd_command.exe с аргументами "nawisworks, -ud(update json)", выгружает моедели 
из формата .rvt(RevitModel) в .nwc(NaiwsModel) и .nwd(Сборка NaiwsModel)
4. Команда publish, запускает cmd_command.exe с аргументами "publish, -ud(update json)", после происходит формирование
архива с моделями.
5. Сообщение  #d <Имя альбома>, запускает cmd_command.exe с аргументами "arch_album, -na(--name_album) <Имя альбома>, 
-ud(--update_json)", и формирует архив после выдачи альбомов с датой и именем указанным в <Имя альбома>
h2 Функционал консольного приложения(cmd_command.exe), возможен запуск отдельно от телеграм бота со следующими аргументами:
1. arch - Архивация всех моделей(.rvt, .nwc, .nwf, .nwd, .ifc) младше 1-ой недели.
2. arch-album --name_album <Имя архива после выдачи альбомов> - То-же что и arch, но при этом добавляется к имени
архива имя альбома.
3. backup - Бэкап моделей из RevitServer.
4. ftp - Выгрузка моделей для подрядчика.
5. nawisworks - Экспорт моделей в формат моделей Nawisworks.
6. publish - Публикация моделей заказчику.
7. -h --help - Необязательный аргумент. Получение информации о функционале программы.
9. -sm --silence-mode - Необязательный аргумент. Запускает программу в тихом режиме, не информируя пользователей tg бота
о процессах.
* - Вся информация о путях до моделей на сервере, берется из RevitServer.
h2 Функционал программы следящей за директорией (dir_checks.exe):
Проверяет действия в папке указанную в гугл доке, запускается одновременно с tg_bot.exe.


# Технологии
Python 3.11
Telegram API


# Авторы
BlopFlop(ArturYoungBlood)


# Документация
[Telegram API](https://docs.python-telegram-bot.org/en/v21.0.1/)
[Google Sheets API](https://developers.google.com/sheets?hl=ru)
[Google Disk API](https://developers.google.com/drive?hl=ru)


# Инструкции
[Создать телеграм бота](https://habr.com/ru/articles/442800/):
Файл env:

```
CMD_SERVER_NAME={Имя Revit Server}
CMD_NAME_PROJECT={Имя проекта}
CMD_SEARCH_PATTERN={Паттерн поиска моделей на ревит сервере}
CMD_NAWIS_OR_REVIT_VERSION={Версия Revit моеделй}
CMD_PROJECT_DIR={Путь до папки проекта}
CMD_ARCH_DIR={Путь архивации проекта}
CMD_FTP_DIR={Путь до FTP сервера}
TG_TOKEN={Токен телеграм бота}
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

Запуск приложений происходит из exe файлов, они формируются в директории dist после запуска батника,
далее копируем exe в любую удобную для вас директорию закидываем туда файл .env, при первом запуске
необходимо заполнить .env.



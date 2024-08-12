from telegram.error import InvalidToken

from tg_bot import TG_TOKEN, TgBot

if __name__ == "__main__":
    tg_bot = TgBot(TG_TOKEN)
    try:
        tg_bot.message_start()
        updater = tg_bot.start_updater()
    except InvalidToken as ex:
        raise ex("Передайте корректный токен.")

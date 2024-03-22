import telebot
from telebot import types
from database.connection import Settings
from database.connection import users

settings = Settings()
TOKEN = settings.TG_TOKEN
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['help'])
def help(message):
    help_message = """Доступны следующие команды:
/start старт бота
/connect связать логин в базе с аккаунтом телеграмма
"""
    bot.send_message(message.from_user.id, help_message)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Здравствуйте! Используйте /connect для связи бота со своим аккаунтом в базе")


@bot.message_handler(commands=['connect'])
def model(message):
    bot.send_message(message.from_user.id, "Введите логин в базе")
    bot.register_next_step_handler(message, users.connect_user_to_tgid)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
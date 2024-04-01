import telebot
from models.base_types import User
from typing import Any, List, Optional
from pydantic import BaseSettings
import requests

class Settings(BaseSettings):
    TG_TOKEN: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
TOKEN = settings.TG_TOKEN
bot = telebot.TeleBot(TOKEN)


users = {}




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
    users[message.from_user.id] = {}
    bot.register_next_step_handler(message, save_login)

def save_login(message):
    user, tg_id = message.text, message.from_user.id
    users[tg_id]['name'] = user
    bot.send_message(message.from_user.id, "Введите пароль")
    bot.register_next_step_handler(message, save_password)

def save_password(message):
    password, tg_id = message.text, message.from_user.id
    r = requests.post('http://157.136.253.53:24000/user/connect', json={
        'name': users[tg_id]['name'],
        'password': password,
        'tg_id': tg_id
    })
    if r.status_code != 200:
        bot.send_message(message.from_user.id, f'Сервер вернул ошибку {r.status_code}. Текст ошибки: {r.text}')
    else:
        bot.send_message(message.from_user.id, f'Логин {users[tg_id]["name"]} успешно связан с tg_id {tg_id}')



    #     bot.send_message(message.from_user.id, "Успешно!")
    # bot.send_message(message.from_user.id,
    #                  "Что-то пошло не так. Вероятно, пользователь с таким именем не найден в базе")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
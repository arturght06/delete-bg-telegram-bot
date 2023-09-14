from keyboard import greet_key
from aiogram import Dispatcher
from create_bot import dp, bot 
from config import admin_id
from connect import write, check_exist
import time
import json
from aiogram import types, Dispatcher






async def process_hi_command(message):
    # print(str(f'LOG --- Такой пользователь запустил бота{message.from_user}'))
    print(await check_exist(str(message.from_user.id)))


    for i in admin_id:
        await bot.send_message(chat_id=i,  text=str(f'LOG --- Такой пользователь запустил бота{message.from_user}'))

    await bot.send_message(chat_id=message.from_user.id, text='''<b>Привіт 👋</b>
Цей бот видаляє фон з фото. 

На початку даруємо 40 безкоштовних видалення 🙌
Натискай кнопку обробка внизу для початку роботи 👇

<b>Створив @netut_true</b>''', reply_markup=greet_key)


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(process_hi_command, text = ['Назад'])
    dp.register_message_handler(process_hi_command, commands=["start"])
    

    # dp.register_message_handler(process_hi_command, text = ['Увійти'])
    # dp.register_message_handler(echo)
from keyboard import greet_key
from aiogram import Dispatcher
from create_bot import dp, bot 
from config import admin_id
import time
import json

# @dp.message_handler(commands=['start'])
async def process_hi_command(message):
    print(str(f'LOG --- Такой пользователь запустил бота{message.from_user}'))



    for i in admin_id:
        await bot.send_message(chat_id=i,  text=str(f'LOG --- Такой пользователь запустил бота{message.from_user}'))

    await bot.send_photo(chat_id=message.from_user.id, photo='https://i.imgur.com/EDWw6KT.jpg', caption='''<b><i>Вітаю друже 👋</i>
Мене звати king👑p2p bot🤖
І я допоможу тобі заробити на р2р-обмінах 💰😏

Я можу шукати курс на різних біржах, а головне на p2p обмінах 
А можу, навіть, і там і там одночасно🤤

Сподіваюсь ти вже готовий попрацювати зі мною😆
А я з 10 біржами, щоб знайти для тебе найкращий курси і спреди🔥

<i>Обирай що цікавить 👇</i></b>''', reply_markup=greet_key)


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(process_hi_command, text = ['Назад'])
    dp.register_message_handler(process_hi_command, commands=["start"])

    # dp.register_message_handler(process_hi_command, text = ['Увійти'])
    # dp.register_message_handler(echo)
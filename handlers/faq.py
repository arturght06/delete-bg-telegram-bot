from keyboard import greet_key
from aiogram import Dispatcher
from create_bot import dp, bot 
from config import admin_id

# @dp.message_handler(commands=['start'])
async def process_hi_command(message):
    await bot.send_message(chat_id=message.from_user.id, text='''🤖<b> Цей бот видаляє фон з фото</b>
Моя порада надсилати фото без стискання, щоб якість була кращою. 
Якщо треба більше видалень, то - пиши, домовимось 😉

Маю надію цей бот буде корисний багатьом. Можна покращити свої презентації, наробити стікерів і так далі)🙃

<b>🤟Розробник: @netut_true</b>''', reply_markup=greet_key)
    


def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(process_hi_command, text = ['FAQ📜'])
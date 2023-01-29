from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key
from config import admin_id
from api import pricesString, prices
from connect import check
from photoeditor import photo_with_currencies
import base64
from io import BytesIO

class FSMcreate(StatesGroup):
    writing = State()

async def c_spot(message: types.Message, state: FSMContext):
	print(str(f'LOG --- Користувач {message.from_user} запитав курс'))
	await FSMcreate.writing.set()
	await bot.send_message(chat_id = message.from_user.id, text = "<b><i>☑️ Напиши торгову пару👇\n🔸 Наприклад:</i></b> <code>Usdt uah</code>" , reply_markup=brcs_key)


async def c_gen(message: types.Message, state: FSMContext):
	# s1, s2 = message.split(' ')

	try:
		s1 = (message.text).split(' ')[0]
		s2 = (message.text).split(' ')[1]
		print(message, s1, s2)
		prices_string_result = await pricesString(s1, s2, prices)
		text_message = f'📊{s1.upper()}/{s2.upper()}\n{prices_string_result[0]}'
		prices_list_anarchy = prices_string_result[1]
		print(prices_list_anarchy)
		ph = await photo_with_currencies(prices_list_anarchy)
		media = types.MediaGroup()
		media.attach_photo(ph, text_message)


		await bot.send_media_group(chat_id=message.from_user.id, media=media)
	except:
		await bot.send_message(chat_id=message.from_user.id, text='<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>')
		


async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Назад'])
    dp.register_message_handler(back, Text(equals='назад', ignore_case=True), state='*')
    dp.register_message_handler(c_spot, text=["Курси 📊"], state = None)
    dp.register_message_handler(c_gen, state = FSMcreate.writing)
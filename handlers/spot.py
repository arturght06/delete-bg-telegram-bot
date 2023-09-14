from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key
from config import admin_id
# from api import count_from_api
from connect import write_key, print_all_keys, get_count, delete_key, check, get_info_db, print_all, write, delete, check
# from photoeditor import photo_with_currencies
import base64
import random
import string
from PIL import Image, ImageFilter
from io import BytesIO
from mainforphoto import request_photo, give_apikey

class FSMcreate(StatesGroup):
    writing = State()

async def file_start(message: types.Message, state: FSMContext):
	print(str(f'LOG --- Користувач {message.from_user} запитав курс'))
	user_id = str(message.from_user.id)
	if await check(user_id):
		await FSMcreate.writing.set()
		number_real = await get_info_db(user_id)
		await bot.send_message(chat_id = message.from_user.id, text = f"В тебе залишилось <code>{number_real}</code> безкоштовних обробок. \n\nНадішли фото для видалення фону\n<b></b>" , reply_markup=brcs_key)
	else:
		await bot.send_message(chat_id = message.from_user.id, text = "Закінчились безкоштовні обробки фото, напиши адміну @netut_true щоб отримати ще🙃" , reply_markup=greet_key)

async def get_file_id_p(message: types.Message):
	check_status = await check(str(message.from_user.id))

	if check_status:
		# await message.reply(message)
		if message.document:
			file_id = message.document.file_id
		elif message.photo:
			file_id = message.photo[-1].file_id


		file = await bot.get_file(file_id)
		file_path = file.file_path
		file_bytes = BytesIO()
		image1 = await bot.download_file(file_path, file_bytes)
		resultPhotoBytes = await request_photo(image1)
		if resultPhotoBytes == False:
			await bot.send_message(chat_id = message.from_user.id, text = "Сталась помилка" , reply_markup=brcs_key)
			return 0

		number_real = await get_info_db(str(message.from_user.id))
		await write(str(message.from_user.id), number_real-1)
		caption = f"<b>Фон успішно видалено </b>✅\n\n<i>Розробник:</i> <b>@netut_true</b>"
		await bot.send_document(chat_id=message.from_user.id, document=resultPhotoBytes, caption=caption)

	else:
		# await state.finish()
		await bot.send_message(chat_id = message.from_user.id, text = "В тебе закінчились безкоштовні обробки" , reply_markup=greet_key)


	for id_admin in admin_id:
		if message.from_user.username:
			username = message.from_user.username
		else:
			username = ""

		if message.photo:
		    file_id = message.photo[-1].file_id
		    caption = f"От: {username}\n{message.from_user}"
		    await bot.send_photo(chat_id=id_admin, photo=file_id, caption=caption)
		if message.document:
		    file_id = message.document.file_id
		    caption = f"От: {username}\n{message.from_user}"
		    await bot.send_document(chat_id=id_admin, document=file_id, caption=caption)



# {"message_id": 9246, "from": {"id": 904245039, "is_bot": false, "first_name": "Art_kar", "username": "netut_true", "language_code": "uk"}, 
# "chat": {"id": 904245039, "first_name": "Art_kar", "username": "netut_true", "type": "private"}, 
# "date": 1680017552, "document": {"file_name": "Frame 1 (19).png", "mime_type": "image/png", 
# "thumbnail": {"file_id": "AAMCAgADGQEAAiQeZCMIkD0QzJD_WQ3lDZu9H-WPUUEAAgcnAAJFxBhJXXoJ9bfiBigBAAdtAAMvBA", "file_unique_id": "AQADBycAAkXEGEly", "file_size": 8246, "width": 320, "height": 156}, 
# "thumb": {"file_id": "AAMCAgADGQEAAiQeZCMIkD0QzJD_WQ3lDZu9H-WPUUEAAgcnAAJFxBhJXXoJ9bfiBigBAAdtAAMvBA", "file_unique_id": "AQADBycAAkXEGEly", "file_size": 8246, "width": 320, "height": 156}, 
# "file_id": "BQACAgIAAxkBAAIkHmQjCJA9EMyQ_1kN5Q2bvR_lj1FBAAIHJwACRcQYSV16CfW34gYoLwQ", "file_unique_id": "AgADBycAAkXEGEk", "file_size": 235437}}


# {"message_id": 9251, "from": {"id": 904245039, "is_bot": false, "first_name": "Art_kar", "username": "netut_true", "language_code": "uk"}, 
# "chat": {"id": 904245039, "first_name": "Art_kar", "username": "netut_true", "type": "private"}, "date": 1680018215, 
# "photo": [{"file_id": "AgACAgIAAxkBAAIkI2QjCydmQjaisIc67lYKpEUTDL_CAALVxjEbRcQYSa8h9z4ClwAB8QEAAwIAA3MAAy8E", 
# "file_unique_id": "AQAD1cYxG0XEGEl4", "file_size": 951, "width": 90, "height": 44}, 
# {"file_id": "AgACAgIAAxkBAAIkI2QjCydmQjaisIc67lYKpEUTDL_CAALVxjEbRcQYSa8h9z4ClwAB8QEAAwIAA20AAy8E", "file_unique_id": "AQAD1cYxG0XEGEly", "file_size": 9376, "width": 320, "height": 156}, 
# {"file_id": "AgACAgIAAxkBAAIkI2QjCydmQjaisIc67lYKpEUTDL_CAALVxjEbRcQYSa8h9z4ClwAB8QEAAwIAA3gAAy8E", "file_unique_id": "AQAD1cYxG0XEGEl9", "file_size": 21319, "width": 628, "height": 306}]}



# @dp.message_handler(commands=['start'])


# async def c_gen(message: types.Message, state: FSMContext):
# 	# s1, s2 = message.split(' ')


# 	try:
# 		s1 = (message.text).split(' ')[0]
# 		s2 = (message.text).split(' ')[1]
# 		log_text = f"Цей користувач зробив запит на {s1}/{s2}:\n{message.from_user}"
# 		for id_admin in admin_id:
# 			await bot.send_message(chat_id=id_admin, text=log_text)
# 		a = await bot.send_message(chat_id=message.from_user.id, text='<b>⏳ Обробляємо запит</b>')
# 		idd = a.message_id
# 		print(idd)

# 		prices_string_result = await pricesString(s1, s2, prices)
# 		text_message = f'📊{s1.upper()}/{s2.upper()}\n{prices_string_result[0]}'
# 		# prices_list_anarchy = prices_string_result[1]
# 		# print(prices_list_anarchy)
# 		# ph = await photo_with_currencies(prices_list_anarchy)
# 		# media = types.MediaGroup()
# 		# media.attach_photo(ph, text_message)
# 		photo_id = 'AgACAgIAAxkBAAJrYWQXLsFV7l0k_gKbuDeGGASwF9YLAAJ2xjEbqUu4SEic-TmHsTN4AQADAgADeQADLwQ'

# 		await bot.send_photo(chat_id=message.from_user.id, photo=photo_id, caption=text_message)
# 		await bot.delete_message(chat_id=message.from_user.id, message_id=idd)
	
# 	# await bot.edit_message_text(chat_id=message.from_user.id, message_id=idd, media=types.InputMediaPhoto(media=photo_id, caption=text_message))

# 		# await bot.send_media_group(chat_id=message.from_user.id, media=media)
# 	except:
# 		await bot.send_message(chat_id=message.from_user.id, text='<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>')
		


async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Назад'])
    dp.register_message_handler(back, Text(equals='назад', ignore_case=True), state='*')
    dp.register_message_handler(file_start, text=['Обробка'], state = None)
    dp.register_message_handler(get_file_id_p, content_types=['photo', 'document'], state=FSMcreate.writing)
    # dp.register_message_handler(c_gen, state = FSMcreate.writing)
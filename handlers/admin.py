from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key, admin_key
from config import admin_id, adminPanelPasswords
from api import count_from_api
from connect import write_key, print_all_keys, get_count, delete_key, check, get_info_db, print_all, write, delete, get_real_count
import datetime as DT
from time import sleep
import xlsxwriter
# ean = barcode.get('ean13', barcode_init, writer=ImageWriter())

class FSMcreate(StatesGroup):
    admin_panel = State()
    add_user = State()
    del_user = State()
    check_user = State()
    add_price = State()
    delete_price = State()
    tbmain = State()
    send_all_main = State()
    send_one_main = State()

async def admin_start(message: types.Message):
	await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\n{message.from_user}\n<b>Цей адмін увійшов в адмін панель</b>')
	await FSMcreate.admin_panel.set()
	await bot.send_message(chat_id = message.from_user.id, text = "Вітаю👋\nЦе зручна адмін панель в якій ти можеш керувати підписки користувачів.\n\n<b>\"Додати\"</b><i> - відповідає за додавання підписки користувачу</i>\n<b>\"Видалити\"</b><i> - відповідає за видалення підписки користувача з бд</i>\n<b>\"Перевірити інфо\"</b><i> - перевірка часу користувач</i>а\n<b>\"Список акаунтів\"</b><i> - Виводить абсолютно всіх підписки користувачів</i>\n\nУсі функції перераховані нижче😉" , reply_markup=admin_key)


# add user to db 
# add user to db 
# add user to db
async def add_user_start(message: types.Message, state: FSMContext):
	await FSMcreate.add_user.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши <b>id</b> користувача та кількість безкоштовних видалень фона\n\n<i>Якщо користувач вже має кількість, то його час буде перезаписаний!</i>', reply_markup=brcs_key)

async def add_user_main(message: types.Message, state: FSMContext):
	try:
		user_id, user_count = str(message.text).split(" ", 1)

		await write(user_id, int(user_count))
		await bot.send_message(chat_id = -1001551885182, text=f'<i>LOG-Admin panel--!</i>\nКористувачу:  <code>{user_id}</code>, записана кількість - <code>{user_count}</code>')
		await bot.send_message(chat_id = message.from_user.id, text=f'<i>LOG-Admin panel--!</i>\nКористувачу:  <code>{user_id}</code>, записана кількість - <code>{user_count}</code>', reply_markup=brcs_key)
		await bot.send_message(chat_id = int(user_id), text = f'<i><b>Повідомлення</b>\nКількість безкоштовних видалень змінена адміністратором ✅</i>')
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при зчитуванні даних</i>', reply_markup=brcs_key)

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
 
async def del_user_start(message: types.Message, state: FSMContext):
	await FSMcreate.del_user.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши <b>id</b> користувача для видалення', reply_markup=brcs_key)

async def del_user_main(message: types.Message, state: FSMContext):
	try:
		user_id = str(message.text)
		delete_process = await delete(user_id)
		if delete_process == True:
			await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\nКористувач:<code>{user_id}</code> - видалений!')
			await bot.send_message(chat_id=message.from_user.id, text=f'<b>Готово!</b>\nКористувач:<code>{user_id}</code> - видалений!', reply_markup=brcs_key)
		elif delete_process == False:
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при видаленні користувача</i>', reply_markup=brcs_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при видаленні користувача</i>', reply_markup=brcs_key)

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

async def send_csv(id_user, arr):
	workbook = xlsxwriter.Workbook(f'all_users.xlsx')
	worksheet = workbook.add_worksheet()
	
	names = ['ID юзера', "кількість"]
	row = 0
	column = 0


	for i in arr:
		user_id = i
		user_count = arr.get(i)

		worksheet.write(row, 0, user_id)
		worksheet.write(row, 1, user_count)
		row += 1
	workbook.close()
	with open(f'all_users.xlsx', 'rb') as f:
		await bot.send_document(id_user, f)


async def list_users(message: types.Message, state: FSMContext):
	list_of_users = await print_all()
	list_for_sheet = {}
	await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\n{message.from_user}\n<b>Цей адмін запитав базу підписок користувачів</b>')
	if len(list_of_users) == 0:
		result_text = '<i>В базі не знайдено жодного користувача🤷‍♂️</i>'
		await bot.send_message(chat_id=message.from_user.id, text=f'{result_text}')

	else:
		result_text = '<b>Всі користувачі:</b>\n'
		inx = 1
		for i in list_of_users:
			list_for_sheet[i] = str(list_of_users.get(i))
			result_text += f'<i>{inx}</i>.) id: <code>{i}</code>, кількість: <code>{str(list_of_users.get(i))}</code>\n'
			inx += 1
			if inx % 50 == 0 or len(list_of_users)+1 == inx:
				await bot.send_message(chat_id=message.from_user.id, text=f'{result_text}')
				# sleep(0.25)
				result_text = ''
	await send_csv(message.from_user.id, list_for_sheet)
	# print(list_for_sheet)

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

async def check_user_start(message: types.Message, state: FSMContext):
	await FSMcreate.check_user.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши <b>id</b> користувача для перевірки', reply_markup=brcs_key)

async def check_user_main(message: types.Message, state: FSMContext):
	try:
		user_id = str(message.text)
		check_info = await get_info_db(user_id)
		if check_info != False:
			await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\n{message.from_user}\n<b>Цей адмін запитав деталі підписки у {user_id}</b>')
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Кількість у <code>{user_id}</code>\nдорівнює: {check_info}</i>', reply_markup=brcs_key)
		elif check_info == False:
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при перевірці користувача</i>', reply_markup=brcs_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при перевірці користувача</i>', reply_markup=brcs_key)





async def list_prices(message: types.Message, state: FSMContext):
	list_of_prices = await print_all_keys()
	await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\n{message.from_user}\n<b>Цей адмін запитав базу ключів на пидписки</b>')
	if len(list_of_prices) == 0:
		result_text = '<i>В базі не знайдено жодних ключів🤷‍♂️</i>'
	else:
		result_text = '<b>Всі ключі:</b>\n'
		inx = 1
		for i in list_of_prices:
			count = int(await get_real_count(i))
			result_text += f'<i>{inx}</i>.) ключ: <code>{i}</code>, кількість: <code>{count}</code>\n'
			inx += 1
	await bot.send_message(chat_id=message.from_user.id, text=f'{result_text}')


async def add_price_start(message: types.Message, state: FSMContext):
	await FSMcreate.add_price.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши <b>ключ</b> та <b>кількість</b>\n(наприклад: <code>6TYGKYE15K6x7ZfpY2TeTFkD</code>)\n\n<i>Якщо ключ на цей час вже існує, то цого кількість буде перезаписана!</i>', reply_markup=brcs_key)

async def add_price_main(message: types.Message, state: FSMContext):
	try:
		key= str(message.text)
		count = int(await get_real_count(key))
		await write_key(str(key))
		result_text = str(f'<b>Готово!</b> Токену:  <code>{key}</code>, записана кількість - <code>{count}</code>')
		# print(result_text)
		await bot.send_message(chat_id=message.from_user.id, text=result_text)

	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при зчитуванні даних</i>', reply_markup=brcs_key)




async def del_price_start(message: types.Message, state: FSMContext):
	await FSMcreate.delete_price.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши <b>ключ</b> для видалення', reply_markup=brcs_key)

async def del_price_main(message: types.Message, state: FSMContext):
	try:
		key = str(message.text)
		delete_process = await delete_key(key)
		if delete_process == True:
			await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\nКлюч <b>{days}</b> - видалений!')
			await bot.send_message(chat_id=message.from_user.id, text=f'<b>Готово!</b>\nКлюч <b>{days}</b> дні - видалений!', reply_markup=brcs_key)
		elif delete_process == False:
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при видаленні ключу</i>', reply_markup=brcs_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при видаленні ключу</i>', reply_markup=brcs_key)

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


async def get_all_refs(message: types.Message, state: FSMContext):
	list_refs = await print_all_referrers()
	result = '<b>Всі реферали:</b>\n'
	inx = 1
	for i in list_refs:
		result += f'<i>{inx}.)</i> id: <code>{i}</code>, запрошений: <code>{list_refs.get(i)}</code> \n'
		inx += 1
		if inx % 50 == 0 or len(list_refs) == inx-1:
			await bot.send_message(chat_id=message.from_user.id, text=f'{result}')
			result = ''




######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


async def send_all(message: types.Message, state: FSMContext):
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши текст для розсилки всім користувачам бота', reply_markup=brcs_key)
	await FSMcreate.send_all_main.set()

async def send_all_main(message: types.Message, state: FSMContext):
	list_users = await print_all()
	# list_users = ['904245039']
	inx = 0
	temporary_list = []
	n = 0
	for i in list_users:
		# print(i)
		i = int(i)
		inx += 1
		
		# temporary_list.append(i)
		# if inx % 15 == 0 or len(temporary_list) == inx:
			# for id_u in temporary_list:
		n += 1
		try:
			await bot.send_message(chat_id=i, text=message.text)
		except:
			for adm_id in admin_id:
				await bot.send_message(chat_id=adm_id, text=f"{n}. Не вдалось надіслати до: {i}")

		# temporary_list = []
		sleep(0.1)
		if inx % 100 == 0:
			sleep(10)


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


async def send_one(message: types.Message, state: FSMContext):
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши ID користувача та текст з тегами з нового рядку', reply_markup=brcs_key)
	await FSMcreate.send_one_main.set()

async def send_one_main(message: types.Message, state: FSMContext):
	try:
		id_u, text = (message.text).split('\n', 1)
		await bot.send_message(chat_id = id_u, text = text)
		await bot.send_message(chat_id = message.from_user.id, text = '<b>Готово✅</b>')
		print(id_u, text)
	except:
		await bot.send_message(chat_id = message.from_user.id, text = '<i>Помилка при зчитуванні даних</i>')


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


#
#
#
async def post_in_channel(dp: Dispatcher):
	print(123)
	prices_text = await pricesString('USDT', 'UAH', prices)
	await bot.send_message(-1001551885182, text=prices_text)
#
#
#




async def back(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	elif str(current_state) in ["FSMcreate:add_user", "FSMcreate:del_user", "FSMcreate:check_user", "FSMcreate:delete_price", "FSMcreate:add_price", "FSMcreate:tbmain", "FSMcreate:send_all_main"]:
		await FSMcreate.admin_panel.set()
		await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=admin_key)
		return
	else:
		await state.finish()
		await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)
		return

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Назад'])
    dp.register_message_handler(back, Text(equals='назад', ignore_case=True), state='*')

    dp.register_message_handler(admin_start, text=adminPanelPasswords, state = None)
    dp.register_message_handler(add_user_start, text=["Додати"], state = FSMcreate.admin_panel)
    dp.register_message_handler(add_user_main, state = FSMcreate.add_user)
    dp.register_message_handler(del_user_start, text=["Видалити"], state = FSMcreate.admin_panel)
    dp.register_message_handler(del_user_main, state = FSMcreate.del_user)

    dp.register_message_handler(list_users, text=["Список акаунтів"], state = FSMcreate.admin_panel)
    dp.register_message_handler(check_user_start, text=["Перевірити інфо"], state = FSMcreate.admin_panel)
    dp.register_message_handler(check_user_main, state = FSMcreate.check_user)

    dp.register_message_handler(list_prices, text=["Ключі"], state = FSMcreate.admin_panel)
    dp.register_message_handler(add_price_start, text=["Додати ключ"], state = FSMcreate.admin_panel)
    dp.register_message_handler(add_price_main, state = FSMcreate.add_price)
    dp.register_message_handler(del_price_start, text=["Видалити ключ"], state = FSMcreate.admin_panel)
    dp.register_message_handler(del_price_main, state = FSMcreate.delete_price)

    dp.register_message_handler(send_all, text=['Розіслати текст'], state = FSMcreate.admin_panel)
    dp.register_message_handler(send_all_main, state = FSMcreate.send_all_main)
    dp.register_message_handler(send_one, text=['Надіслати текст'], state = FSMcreate.admin_panel)
    dp.register_message_handler(send_one_main, state = FSMcreate.send_one_main)




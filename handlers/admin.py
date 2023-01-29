from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key, admin_key
from config import admin_id
from api import pricesString, prices
from connect import check, write, delete, print_all, get_info_db, print_all_price, write_price, delete_price, print_all_balances, get_user_balance, write_balance, print_all_referrers, write_ref_balance, get_ref_balance, get_referrer_id, print_all_ref_balances
import datetime as DT
from time import sleep
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
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши <b>id</b> користувача та <b>час кінця підписки (в форматі UTC)</b>\n(наприклад: <code>904245039 2022 06 22 22:00</code>)\n\n<i>Якщо користувач вже має підписку, то його час буде перезаписаний!</i>', reply_markup=brcs_key)

async def add_user_main(message: types.Message, state: FSMContext):
	try:
		user_id, user_time = str(message.text).split(" ", 1)
		user_time = int((DT.datetime.strptime(user_time, '%Y %m %d %H:%M')).timestamp())
		# print(user_time, user_id)
		return_time_string = DT.datetime.utcfromtimestamp(int(user_time)).strftime('%Y-%m-%d %H:%M')
		await write(user_id, str(user_time))
		await bot.send_message(chat_id = -1001551885182, text=f'<i>LOG-Admin panel--!</i>\nКористувачу:  <code>{user_id}</code>, записаний час - <code>{return_time_string}</code>')
		await bot.send_message(chat_id = message.from_user.id, text=f'<b>Готово!</b>\nКористувачу:  <code>{user_id}</code>, записаний час - <code>{return_time_string}</code>', reply_markup=brcs_key)
		await bot.send_message(chat_id = int(user_id), text = f'<i><b>Повідомлення</b>\nПідписка подовжена ✅</i>')
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

async def list_users(message: types.Message, state: FSMContext):
	list_of_users = await print_all()
	await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\n{message.from_user}\n<b>Цей адмін запитав базу підписок користувачів</b>')
	if len(list_of_users) == 0:
		result_text = '<i>В базі не знайдено жодного користувача🤷‍♂️</i>'
		await bot.send_message(chat_id=message.from_user.id, text=f'{result_text}')

	else:
		result_text = '<b>Всі користувачі:</b>\n'
		inx = 1
		for i in list_of_users:
			return_time_string = DT.datetime.utcfromtimestamp(int(list_of_users.get(i))).strftime('%Y-%m-%d %H:%M')
			result_text += f'<i>{inx}</i>.) id: <code>{i}</code>, кінець підписки: <code>{return_time_string}</code>\n'
			inx += 1
			if inx % 50 == 0 or len(list_of_users)+1 == inx:
				await bot.send_message(chat_id=message.from_user.id, text=f'{result_text}')
				# sleep(0.25)
				result_text = ''

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
			return_time_string = DT.datetime.utcfromtimestamp(check_info).strftime('%Y-%m-%d %H:%M')
			await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\n{message.from_user}\n<b>Цей адмін запитав деталі підписки у {user_id}</b>')
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Підписка у <code>{user_id}</code>\ncкінчиться: {return_time_string}</i>', reply_markup=brcs_key)
		elif check_info == False:
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при перевірці користувача</i>', reply_markup=brcs_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при перевірці користувача</i>', reply_markup=brcs_key)





async def list_prices(message: types.Message, state: FSMContext):
	list_of_prices = await print_all_price()
	await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\n{message.from_user}\n<b>Цей адмін запитав базу цін на пидписки</b>')
	if len(list_of_prices) == 0:
		result_text = '<i>В базі не знайдено жодних цін🤷‍♂️</i>'
	else:
		result_text = '<b>Всі ціни:</b>\n'
		inx = 1
		for i in list_of_prices:
			return_price_string = float(list_of_prices.get(i))
			result_text += f'<i>{inx}</i>.) строк: <b>{i}</b>, ціна: <code>{return_price_string}</code>\n'
			inx += 1
	await bot.send_message(chat_id=message.from_user.id, text=f'{result_text}')


async def add_price_start(message: types.Message, state: FSMContext):
	await FSMcreate.add_price.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши <b>строк дії (у днях)</b> підписки та <b>ціну</b>\n(наприклад: <code>31 99.99</code>)\n\n<i>Якщо підписка на цей час вже існує, то її ціна буде перезаписана!</i>', reply_markup=brcs_key)

async def add_price_main(message: types.Message, state: FSMContext):
	try:
		days, price = str(message.text).split(" ", 1)
		await write_price(days, float(price))
		await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\nПідписці на:  <code>{days}</code>, записана ціна - <code>{price}</code>')
		await bot.send_message(chat_id=message.from_user.id, text=f'<b>Готово!</b>', reply_markup=brcs_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при зчитуванні даних</i>', reply_markup=brcs_key)




async def del_price_start(message: types.Message, state: FSMContext):
	await FSMcreate.delete_price.set()
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши який <b>час</b> у підписки для видалення', reply_markup=brcs_key)

async def del_price_main(message: types.Message, state: FSMContext):
	try:
		days = str(message.text)
		delete_process = await delete_price(days)
		if delete_process == True:
			await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\nПідпискa строком на <b>{days}</b> дні - видалена!')
			await bot.send_message(chat_id=message.from_user.id, text=f'<b>Готово!</b>\nПідпискa строком на <b>{days}</b> дні - видалена!', reply_markup=brcs_key)
		elif delete_process == False:
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при видаленні підписки</i>', reply_markup=brcs_key)
	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при видаленні підписки</i>', reply_markup=brcs_key)

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

async def get_all_balances(message: types.Message, state: FSMContext):
	list_balances = await print_all_balances()
	result = '<b>Всі баланси:</b>\n'
	inx = 1
	for i in list_balances:
		result += f'<i>{inx}.)</i> id: <code>{i}</code>, баланс: <code>{list_balances.get(i)}</code> ₴\n'
		inx += 1
		if inx % 50 == 0 or len(list_balances) == inx-1:
			await bot.send_message(chat_id=message.from_user.id, text=f'{result}')
			result = ''

async def add_to_balance(message: types.Message, state: FSMContext):
	await bot.send_message(chat_id=message.from_user.id, text=f'✍️Напиши <b>id</b> користувача та скільки йому додати до балансу\n(наприклад: <code>904245039 100.99</code>)', reply_markup=brcs_key)
	await FSMcreate.tbmain.set()

async def add_tb_main(message: types.Message, state: FSMContext):
	try:
		user_id, adding = str(message.text).split(' ')
		balance = float(await get_user_balance(user_id))
		referrer_id_ofuser = (await print_all_referrers())[str(user_id)]
		ref_balance = await get_ref_balance(str(referrer_id_ofuser))
		print(ref_balance, str(referrer_id_ofuser), balance)
		await write_ref_balance(str(referrer_id_ofuser), float(ref_balance + (round(float(adding), 2) * 0.2)))


		if balance == False:
			await write_balance(user_id, float(adding))
			await bot.send_message(chat_id=referrer_id_ofuser, text=f"✅ <b>Ваш реферальний баланс зільшено на {round(float(adding), 2) * 0.2} ₴</b>🔥")
			await bot.send_message(chat_id=user_id, text=f'✅ <b>Поповнення підтверджене</b>🔥\n➡️ Надійшло: <b>{round(float(adding), 2)} ₴</b>\n💰 Тепер баланс: <b>{round(float(adding), 2)}  ₴</b>')
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Користувачу вперше записаний баланс</i>', reply_markup=brcs_key)
		else:
			await bot.send_message(chat_id=referrer_id_ofuser, text=f"✅ <b>Ваш реферальний баланс зільшено на {round(float(adding), 2) * 0.2} ₴</b>🔥")
			await bot.send_message(chat_id=message.from_user.id, text=f'<i>Користувачу додано <b>{adding}uah.</b> до балансу</i>', reply_markup=brcs_key)
			await bot.send_message(chat_id=user_id, text=f'✅ <b>Поповнення підтверджене</b>🔥\n➡️ Надійшло: <b>{round(float(adding), 2)} ₴</b>\n💰 Тепер баланс: <b>{round(balance + float(adding), 2)}  ₴</b>')
			adding = balance + float(adding)
			await write_balance(user_id, float(adding))

	except:
		await bot.send_message(chat_id=message.from_user.id, text=f'<i>Помилка при зчитуванні даних</i>', reply_markup=brcs_key)

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

async def get_all_refs_balance(message: types.Message, state: FSMContext):
	list_refs = await print_all_ref_balances()
	result = '<b>Всі баланси рефералів:</b>\n'
	inx = 1
	for i in list_refs:
		result += f'<i>{inx}.)</i> id: <code>{i}</code>, баланс: <code>{list_refs.get(i)}</code> \n'
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
	list_users = await print_all_balances()
	# list_users = ['904245039']
	inx = 0
	temporary_list = []

	for i in list_users:
		# print(i)
		i = int(i)
		inx += 1
		temporary_list.append(i)
		if inx % 20 == 0 or len(temporary_list) == inx:
			for id_u in temporary_list:
				await bot.send_message(chat_id=id_u, text=message.text)
			temporary_list = []
			sleep(1)


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
    dp.register_message_handler(admin_start, text=["/adminD4cSrCeI7XMYdjnTP2eOJ"], state = None)
    dp.register_message_handler(add_user_start, text=["Додати"], state = FSMcreate.admin_panel)
    dp.register_message_handler(add_user_main, state = FSMcreate.add_user)
    dp.register_message_handler(del_user_start, text=["Видалити"], state = FSMcreate.admin_panel)
    dp.register_message_handler(del_user_main, state = FSMcreate.del_user)
    dp.register_message_handler(list_users, text=["Список акаунтів"], state = FSMcreate.admin_panel)
    dp.register_message_handler(check_user_start, text=["Перевірити інфо"], state = FSMcreate.admin_panel)
    dp.register_message_handler(check_user_main, state = FSMcreate.check_user)
    dp.register_message_handler(list_prices, text=["Ціни на підписку"], state = FSMcreate.admin_panel)
    dp.register_message_handler(add_price_start, text=["Додати ціну"], state = FSMcreate.admin_panel)
    dp.register_message_handler(add_price_main, state = FSMcreate.add_price)
    dp.register_message_handler(del_price_start, text=["Видалити ціну"], state = FSMcreate.admin_panel)
    dp.register_message_handler(del_price_main, state = FSMcreate.delete_price)
    dp.register_message_handler(get_all_balances, text=["Список балансів"], state = FSMcreate.admin_panel)
    dp.register_message_handler(add_to_balance, text=["Додати ₴"], state = FSMcreate.admin_panel)
    dp.register_message_handler(add_tb_main, state = FSMcreate.tbmain)
    dp.register_message_handler(get_all_refs, text=["Всі реферали"], state = FSMcreate.admin_panel)
    dp.register_message_handler(get_all_refs_balance, text=["Всі реф-баланси"], state = FSMcreate.admin_panel)
    dp.register_message_handler(send_all, text=['Розіслати текст'], state = FSMcreate.admin_panel)
    dp.register_message_handler(send_all_main, state = FSMcreate.send_all_main)
    dp.register_message_handler(send_one, text=['Надіслати текст'], state = FSMcreate.admin_panel)
    dp.register_message_handler(send_one_main, state = FSMcreate.send_one_main)




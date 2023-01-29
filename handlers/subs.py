from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key
from config import admin_id
import time
from datetime import datetime
from connect import get_info_db, check, print_all_price, get_user_balance, get_user_balance, write, write_balance, write_ref_balance, get_ref_balance, print_all_referrers


# ean = barcode.get('ean13', barcode_init, writer=ImageWriter())
            


'''
functions(hendlers)
'''
class FSMcreate(StatesGroup):
    checking = State()
    cont = State()
    add = State()
    end = State()

async def sub_start(message: types.Message):
	print(str(f'LOG --- User {message.from_user} asked his time'))
	await FSMcreate.checking.set()
	await bot.send_message(chat_id = message.from_user.id, text = "<b><i>☑️ Обирай функцію ⚙️</i></b>" , reply_markup=sub_key)

async def checker_time(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    end_time = await get_info_db(str(user_id))
    print(end_time, user_id)
    if end_time >= int(time.time()):
        real_time = int(time.time())
        print(real_time)
        if end_time >= real_time:
            dat = datetime.fromtimestamp(end_time).strftime('%d-%m-%Y \n%Hгод. %Mхв.')
            data = f'⏳<i><b>Підписка cкінчиться:</b></i>\n<b>{dat}</b>'
    else:
        data = f'<b>Нажаль, підписка відсутня🩸\nДля подовження дії зайди в 👉 <i>Підписка 👉 Купити підписку</i></b>\n'
    await bot.send_message(chat_id=message.from_user.id, text=f'{data}')


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


async def continue_sub(message: types.Message, state: FSMContext):
    list_subs = await print_all_price()
    result_string_list = "☑️ <i><b>Обери тип підписки що цікавить і напиши її номер </b></i>👇\n"
    inx = 1
    for i in list_subs:
        result_string_list += f'▪️ Номер {inx}: <i>на</i> <b>{i}</b> <i>дні за</i> <b>{list_subs.get(i)}</b>\n'
        inx += 1
    result_string_list += '\n<i>*Обов\'язково переконайся в тарифі, потім його не можна буде відмінити!</i>'

    await bot.send_message(chat_id=message.from_user.id, text = f"{result_string_list}", reply_markup=await res_key())
    await FSMcreate.cont.set()

async def sub_sender(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if True:
        dict_subs = dict(await print_all_price())
        price_arr = [(x, dict_subs.get(x)) for x in dict_subs]
        price = price_arr[int(message.text)-1][1]
        timing = int(price_arr[int(message.text)-1][0])
        balance = await get_user_balance(user_id)
        if balance < price:
            await bot.send_message(chat_id=message.from_user.id, text='<b>Не вистачає грошей для покупки цього тарифу😢\nСпробуй обрати інший😉</b>')
        else:
            new_balance = balance - price
            await write_balance(str(message.from_user.id), new_balance)
            if await check(str(message.from_user.id)) is True:
                my_time = int(await get_info_db(str(message.from_user.id)))
                dat = my_time + (timing * 86400) + 10800
            else:
                dat = int(time.time()) + (timing * 86400) + 10800
            await write(user_id, dat)
            await bot.send_message(chat_id=user_id, text='<b>Готово✅\nПідписка подовжена😉</b>', reply_markup=sub_key)
            await FSMcreate.checking.set()
#         dict_subs = dict(await print_all_price())
#         price = [(x, dict_subs.get(x)) for x in dict_subs]
#         print(price[int(message.text)-1])
#         # print(await check(message.from_user.id))
#         if await check(str(message.from_user.id)) is True:
#             my_time = int(await get_info_db(str(message.from_user.id)))
#             print(f'My_time:{my_time}, time: {time.time()}')
#             dat = datetime.fromtimestamp(my_time + (int(price[int(message.text)-1][0]) * 86400) + 10800).strftime('%Y %m %d %H:%M')
#         else:
#             dat = datetime.fromtimestamp(int(time.time()) + (int(price[int(message.text)-1][0]) * 86400) + 10800).strftime('%Y %m %d %H:%M')
#         await bot.send_message(chat_id=message.from_user.id, text=
# f'''💸 <i>До сплати: <b>{price[int(message.text)-1][1]}</b> ₴

# 👉 Для сплати треба поповнити <b>банку Monobank</b> за посиланням нижче
# 👉 В коментар додай свiй id - <code>{message.from_user.id}</code>, щоб ми могли швидше все перевiрити</i>
# https://send.monobank.ua/jar/4wbdHDhyeK

# <i>👇 Наостанок напиши точний час транзакції для уточнення</i>''', reply_markup=brcs_key)
#         await FSMcreate.complete.set()
#         async with state.proxy() as data:
#             data['result'] = f'Користувач {message.from_user} сплатив {price[int(message.text)-1][1]} за {message.text} тарифом.\nГотовий текст для додавання в адмін панелі - <code>{message.from_user.id} {dat}</code>'
    else:
        await bot.send_message(chat_id=message.from_user.id, text='<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>')
        print('faillllll')


#######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

async def balance_start(message: types.Message, state: FSMContext):
    current_balance = await get_user_balance(str(message.from_user.id))
    await bot.send_message(chat_id=message.from_user.id, text=f'🧮 Баланс: <b>{current_balance}</b> ₴')


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

async def add_balance(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='👉 <b>Напиши суму поповнення:</b>\n➖ Мінімум: <b>100.00₴</b>\n➖ Наприклад: <code>150.99</code>\n\n<i>*Або обери запропоновані нижче😉</i>', reply_markup=examples_key)
    await FSMcreate.add.set()

async def add_balance_main(message: types.Message, state: FSMContext):
    try:
        summ = float(message.text)
        if summ < 100:
            await bot.send_message(chat_id=message.from_user.id, text='<i><b>Сума менша за мінімум🤕\nСпробуй ще раз❗️</b></i>')
            return
        await bot.send_message(chat_id=message.from_user.id, text=
f'''💸 <i>До сплати: <b>{summ}</b> ₴

👉 Для сплати треба поповнити <b>банку Monobank</b> за посиланням нижче
👉 В коментар додай свiй id - <code>{message.from_user.id}</code>, щоб ми могли швидше все перевiрити</i>
https://send.monobank.ua/jar/4wbdHDhyeK

<i>👇 Наостанок напиши точний час транзакції для уточнення</i>''', reply_markup=brcs_key)
        await FSMcreate.end.set()
        async with state.proxy() as data:
            data['summ'] = summ
    except:
        await bot.send_message(chat_id=message.from_user.id, text='<i><b>Щось не так🤔\nСпробуй ще раз❗️</b></i>')

async def add_balance_end(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        summ = data['summ']
        for i in admin_id:
            await bot.send_message(chat_id=i, text=f'<b>**********************************************\nЦей користувач мав поповнити банку на {summ}</b>:\n<i>{message.from_user}</i>\n<b>Вказаний час поповнення:</b><i>{message.text}</i>\n\nКод для вставки: <code>{message.from_user.id} {summ}</code>')
        await bot.send_message(chat_id=message.from_user.id, text='<b>Безмежно дякуємо за довіру</b> 🤗\nПідтримка максимально швидко опрацює запит🌪\nЯкщо знадобиться допомога, то обов\'язково напиши нам \n👉 @p2pBot_support', reply_markup=sub_key)
    await FSMcreate.checking.set()

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


async def ref_program(message: types.Message, state: FSMContext):
    ref_balance = await get_ref_balance(str(message.from_user.id))
    ref_link = f'https://t.me/P2P_prices_bot?start={message.from_user.id}'
    arr = await print_all_referrers()
    # print(arr)
    num_refs = 0
    for i in arr:
        # print(arr.get(i), message.from_user.id)
        if int(arr.get(i)) == int(message.from_user.id):
            num_refs += 1

    await bot.send_message(chat_id=message.from_user.id, text=
f'''😍 <b>Реферальна програмa</b> 🔥
👉 Від кожного поповнення твого друга ти отримаєш <b>20%</b>

💰 Баланс: {round(ref_balance, 2)}
🫂 Кіл-ть запрошених: {num_refs}
Посилання: {ref_link}

За виведенням пиши в підтримку: @p2pBot_support
''')







######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################




async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Назад'])
    dp.register_message_handler(back, Text(equals='назад', ignore_case=True), state='*')
    dp.register_message_handler(sub_start, text=["Підписка🔑"], state = None)
    dp.register_message_handler(balance_start, text=['Баланс🧮'], state = FSMcreate.checking)
    dp.register_message_handler(checker_time, text=["Скільки залишилось⌛️"], state = FSMcreate.checking)
    dp.register_message_handler(ref_program, text=["Реферальна программа🔥"], state = FSMcreate.checking)


    dp.register_message_handler(add_balance, text=["Поповнити📥"], state = FSMcreate.checking)
    dp.register_message_handler(add_balance_main, state = FSMcreate.add)
    dp.register_message_handler(add_balance_end, state = FSMcreate.end)


    dp.register_message_handler(continue_sub, text=['Купити підписку💸'], state = FSMcreate.checking)
    dp.register_message_handler(sub_sender, state = FSMcreate.cont)

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from connect import print_all_price
import asyncio



button_cancel = KeyboardButton('Назад')

button_complete = KeyboardButton('Готово✅')
complete_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_complete).add(button_cancel)



brcs_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

#
#
#
#
#
#


button_spot = KeyboardButton('Курси 📊')
button_faq = KeyboardButton('FAQ📜')

# greet_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_spred_p2p_spot, button_courses_spot).row(button_courses_p2p, button_allp2p).row(button_subscribe)
greet_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_spot, button_faq)


button_add_user = KeyboardButton('Додати')
button_delete_user = KeyboardButton('Видалити')
button_check_user = KeyboardButton('Перевірити інфо')
button_check_all = KeyboardButton('Список акаунтів')
button_prices = KeyboardButton('Ціни на підписку')
button_delete_price = KeyboardButton('Видалити ціну')
button_add_price = KeyboardButton('Додати ціну')
button_bal_all = KeyboardButton('Список балансів')
button_bal_add = KeyboardButton('Додати ₴')
button_all_refs = KeyboardButton('Всі реферали')
button_all_refs_b = KeyboardButton('Всі реф-баланси')
button_send_all = KeyboardButton('Розіслати текст')
button_send_one = KeyboardButton('Надіслати текст')



admin_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_user, button_delete_user).add(button_check_user, button_check_all).add(button_prices, button_delete_price, button_add_price).add(button_bal_all, button_bal_add).add(button_all_refs_b, button_all_refs).add(button_send_all, button_send_one).add(button_cancel)

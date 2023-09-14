from config import admin_id
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import keyboard
from create_bot import bot, dp
# from api import pricesString, prices
from time import sleep
from handlers.admin import post_in_channel

async def send_admin(dp):
    for i in admin_id:
        await bot.send_message(chat_id = i, text = "Bot was started")
    await bot.send_message(chat_id=-1001551885182, text="Bot was started")
    
    # while True:
    #     await post_in_channel(dp)

    #     await asyncio.sleep(10)

from handlers import settings, admin, spot, faq

settings.register_handlers_settings(dp)
faq.register_handlers_create(dp)

spot.register_handlers_create(dp)
admin.register_handlers_create(dp)




executor.start_polling(dp, on_startup=send_admin, skip_updates=True)

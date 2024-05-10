import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv
from telegram_bot.common.bot_cmds_list import private
from telegram_bot.handlers.user_private import user_private_router
from price_parser.parser import parser
import datetime

load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(user_private_router)


async def update_database():
    while True:
        now = datetime.datetime.now()
        seconds_to_next_hour = (60 - now.minute) * 60 - now.second
        delta = datetime.timedelta(seconds=seconds_to_next_hour)
        print(f"There are {delta} left until the next hour starts\nWaiting for the next hour to update the price...")
        await asyncio.sleep(seconds_to_next_hour)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, parser.update_price, datetime.datetime.now()
                                   .replace(second=0, microsecond=0))


async def prepare_and_run_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    # delete commands from panel
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


async def main():
    asyncio.create_task(update_database())
    await prepare_and_run_bot()

if __name__ == '__main__':
    asyncio.run(main())

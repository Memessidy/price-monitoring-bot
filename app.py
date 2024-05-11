import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv
from telegram_bot.common.bot_cmds_list import private
from telegram_bot.handlers.user_private import user_private_router
from data_updater.data_updater import Updater


load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(user_private_router)


async def prepare_and_run_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    # delete commands from panel
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


async def main():
    asyncio.create_task(updater.update_by_time())
    await prepare_and_run_bot()


if __name__ == '__main__':
    updater = Updater()
    asyncio.run(main())

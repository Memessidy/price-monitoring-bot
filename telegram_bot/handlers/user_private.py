import os
from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from dotenv import find_dotenv, load_dotenv
from aiogram.types import FSInputFile
import asyncio
from price_parser.parser import MyParser
from telegram_bot.date_nad_time_by_timezone.date_and_time import DateAndTime

load_dotenv(find_dotenv())
user_private_router = Router()
parser = MyParser()
date_and_time = DateAndTime()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Hello! This bot displays information on the dynamics of the dollar to hryvnia exchange rate")


@user_private_router.message(Command('get_exchange_rate'))
async def get_exchange_rate(message: types.Message):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, parser.get_current_prices_sheet)
    if not result:
        await message.answer(f"Currently, there is no data in the database for today. "
                             f"Next data update in {date_and_time.time_to_next_hour}")
    else:
        file = FSInputFile(os.getenv('XLSX_PATH'))
        await message.answer_document(file)
        await message.answer(f"Next data update in {date_and_time.time_to_next_hour}")


@user_private_router.message(Command('get_timezone'))
async def get_current_timezone(message: types.Message):
    await message.reply(f'Current timezone: {date_and_time.current_timezone}')

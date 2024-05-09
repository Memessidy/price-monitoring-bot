import os
from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from dotenv import find_dotenv, load_dotenv
from aiogram.types import FSInputFile
import asyncio
from price_parser.parser import parser
load_dotenv(find_dotenv())
user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Hello")


@user_private_router.message(Command('get_exchange_rate'))
async def echo(message: types.Message):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, parser.get_current_prices_sheet)
    file = FSInputFile(os.getenv('XLSX_PATH'))
    await message.answer_document(file)

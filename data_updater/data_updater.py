from price_parser.parser import MyParser
from telegram_bot.date_nad_time_by_timezone.date_and_time import DateAndTime
import asyncio


class Updater:
    def __init__(self):
        self.__parser = MyParser()
        self.__date_time = DateAndTime()

    async def __update_database(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.__parser.update_price, self.__date_time.current_date_and_time
                                   .replace(second=0, microsecond=0))

    async def update_by_time(self):
        while True:
            print(f"There are {self.__date_time.time_to_next_hour} "
                  f"left until the next hour starts\nWaiting for the next hour to update the price...")
            await asyncio.sleep(self.__date_time.seconds_to_next_hour)
            await self.__update_database()

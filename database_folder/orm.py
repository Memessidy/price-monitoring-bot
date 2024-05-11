from database_folder.core import sync_engine, sync_session_factory
from telegram_bot.date_nad_time_by_timezone.date_and_time import DateAndTime
from .models import Data
from .core import Base
import datetime


class DataBase:
    def __init__(self):
        self.dt = DateAndTime()

    @staticmethod
    def create_tables():
        # Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert_data(price, date):
        with sync_session_factory() as session:
            row = Data(price=price, date=date)
            session.add(row)
            session.commit()

    def get_current_prices(self):
        with sync_session_factory() as session:
            today = self.dt.current_date_and_time.date()
            today_start = datetime.datetime.combine(today, datetime.datetime.min.time())
            today_prices = session.query(Data).filter(Data.date >= today_start).all()
        return today_prices

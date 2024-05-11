import requests
from bs4 import BeautifulSoup
from database_folder.orm import DataBase
from price_parser.settings import headers, columns_width
from xlsx_folder.get_xlsx import ExcelWriter


# Class - Singleton
class MyParser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__url = 'https://www.google.com/finance/quote/USD-UAH'
        self.__database = DataBase()
        self.__database.create_tables()
        self.__excel_writer = ExcelWriter()
        self.__header = ['datetime', 'exchange_rate']

        self.__new_data_available = False
        self.__sheet_exists = False

    def __get_price(self):
        page = requests.get(self.__url, headers=headers).content
        soup = BeautifulSoup(page, 'html.parser')
        current_price = (soup.find('div', {'jsname': 'AS5Pxb'})
                         .find('div', {'jsname': 'ip75Cb'}).find('div').text)
        return current_price

    def __get_new_sheet(self, values):
        self.__excel_writer.create_new_book()
        self.__excel_writer.add_header(self.__header)
        self.__excel_writer.add_data(values)
        self.__excel_writer.set_column_width(columns_width)
        self.__excel_writer.save()
        self.__sheet_exists = True

    def update_price(self, current_datetime):
        current_price = self.__get_price()
        self.__database.insert_data(price=current_price, date=current_datetime)
        self.__new_data_available = True
        print("Database updated")

    def get_current_prices_sheet(self):
        if self.__new_data_available:
            vals = [(str(item.date.strftime("%d.%m.%Y %H:%M:%S")), item.price)
                    for item in self.__database.get_current_prices()]
            if vals:
                self.__get_new_sheet(vals)
            self.__new_data_available = False

    @property
    def sheet_exists(self):
        return self.__sheet_exists

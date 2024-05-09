import requests
from bs4 import BeautifulSoup
from database_folder.orm import DataBase
from price_parser.settings import headers, columns_width
from xlsx_folder.get_xlsx import ExcelWriter


class MyParser:
    def __init__(self):
        self.__url = 'https://www.google.com/finance/quote/USD-UAH'
        self.__database = DataBase()
        self.__database.create_tables()
        self.__excel_writer = ExcelWriter()
        self.__relevant_sheet = False

    def __get_price(self):
        page = requests.get(self.__url, headers=headers).content
        soup = BeautifulSoup(page, 'html.parser')
        current_price = (soup.find('div', {'jsname': 'AS5Pxb'})
                         .find('div', {'jsname': 'ip75Cb'}).find('div').text)
        return current_price

    def update_price(self, current_datetime):
        current_price = self.__get_price()
        self.__database.insert_data(price=current_price, date=current_datetime)
        self.__relevant_sheet = False
        print("Database updated")

    def get_current_prices_sheet(self):
        if not self.__relevant_sheet:
            self.__excel_writer.create_new_book()

            header = ['datetime', 'exchange_rate']

            vals = [(str(item.date.strftime("%d.%m.%Y %H:%M:%S")), item.price)
                    for item in self.__database.get_current_prices()]

            self.__excel_writer.add_header(header)
            self.__excel_writer.add_data(vals)
            self.__excel_writer.set_column_width(columns_width)
            self.__excel_writer.save()
            self.__relevant_sheet = True
            print('Sheets updated')


parser = MyParser()

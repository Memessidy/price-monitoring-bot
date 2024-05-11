from aiogram.types import BotCommand

private = [
    BotCommand(command='get_exchange_rate', description='Sends an xlsx file with exchange'
                                                        ' rate values for the current date'),
    BotCommand(command='get_timezone', description='Displays the time zone')
]

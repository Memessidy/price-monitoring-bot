from datetime import datetime, timedelta
import pytz


class DateAndTime:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__tz = pytz.timezone('Europe/Kiev')

    @property
    def current_date_and_time(self):
        return datetime.now(self.__tz)

    @property
    def current_timezone(self):
        return self.__tz

    @property
    def seconds_to_next_hour(self):
        return ((60 - self.current_date_and_time.minute) * 60 -
                self.current_date_and_time.second)

    @property
    def time_to_next_hour(self):
        return timedelta(seconds=self.seconds_to_next_hour)

    @property
    def timezones(self):
        return [tz for tz in pytz.all_timezones]

    def set_timezone(self, timezone):
        if timezone not in self.timezones:
            raise ValueError(f'Timezone {timezone} is not supported')
        else:
            self.__tz = timezone


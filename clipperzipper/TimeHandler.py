from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
import logging
import re


class Timestamp:

    def __init__(self, timestamp_raw):
        # UTC TIMESTAMP FORMAT: [YYYY-MM-DD HH:MM:SS UTC]
        self.raw = timestamp_raw
        self.timestamp = self.formatted_timestamp(timestamp_raw)
        self.datetime = self.set_datetime()
        self.update()

    def __repr__(self):
        return self.raw

    def __str__(self):
        return self.raw

    def __iadd__(self, other):
        # overload the += operator to increment the date by 1 day
        return self.add(days=other)

    def __add__(self, other):
        # overload the + operator to decrement the date by 1 day
        return self.add(days=other)

    def __sub__(self, other):
        # overload the - operator to decrement the date by 1 day
        return self.subtract(days=other)

    def __isub__(self, other):
        # overload the -= operator to decrement the date by 1 day
        return self.subtract(days=other)

    def add(self, **kwargs):
        self.datetime = self.datetime + relativedelta(**kwargs)
        self.timestamp = self.formatted_timestamp(self.datetime)
        self.update()
        return self

    def subtract(self, **kwargs):
        self.datetime = self.datetime - relativedelta(**kwargs)
        self.timestamp = self.formatted_timestamp(self.datetime)
        self.update()
        return self

    def set(self, **kwargs):
        """Set a new value in the timestamp (reassign the year, month, etc)"""
        datetimes = {"year": 0, "month": 1, "day": 2, "hour": 3, "minute": 4, "second": 5}
        ts_list = self.timestamp.split("-")
        for arg in kwargs:
            for key in datetimes:
                if arg == key:
                    ts_list[datetimes[key]] = str(kwargs[arg]).zfill(2)
        new_ts = '-'.join(ts_list)
        if self.valid_datetime(new_ts):
            self.timestamp = new_ts
            self.update()

    def set_datetime(self):
        """convert UTCHandler timestamp to datetime.datetime for comparisons"""
        if self.valid_datetime(self.timestamp):
            return dt.strptime(self.timestamp, "%Y-%m-%d-%H-%M-%S")
        else:
            # issue warning
            return self.timestamp

    def update(self):
        """Updates all the time values based on the current timestamp"""
        self.year = int(self.timestamp.split("-")[0].zfill(2))
        self.month = int(self.timestamp.split("-")[1].zfill(2))
        self.day = int(self.timestamp.split("-")[2].zfill(2))
        self.hour = int(self.timestamp.split("-")[3].zfill(2))
        self.minute = int(self.timestamp.split("-")[4].zfill(2))
        self.second = int(self.timestamp.split("-")[5].zfill(2))
        self.datetime = self.set_datetime()  # reset the datetime
        self.raw = self.format_raw(self.timestamp)

    @staticmethod
    def format_raw(ts_in):
        ts_list = ts_in.split("-")
        date = '-'.join(ts_list[0:3])
        time = ':'.join(ts_list[3:])
        return '[' + date + ' ' + time + ' UTC]'

    @staticmethod
    def valid_datetime(timestamp):
        try:
            dt.strptime(timestamp, "%Y-%m-%d-%H-%M-%S")
            return True
        except ValueError as ve:
            logging.info(ve)
            return False

    @staticmethod
    def valid_raw_timestamp(time_in):
        pattern = re.compile("\[(\d){4}-(\d){2}-(\d){2}\s(\d){2}:(\d){2}:(\d){2}\sUTC]")
        if re.findall(pattern, time_in):
            if Timestamp.valid_datetime(Timestamp.formatted_timestamp(time_in)):
                return True
            return False
        return False

    @staticmethod
    def formatted_timestamp(tsr):
        """Format raw timestamp from logs"""
        if "UTC" not in str(tsr):
            tsr = '[' + str(tsr) + ' UTC]'
        symbols = {" ": "-", ":": "-", "[": "", "]": "", "UTC": ""}  # chars to remove from raw timestamp
        for s in symbols:
            tsr = str(tsr).replace(s, symbols[s])
        return tsr[:-1]

    @staticmethod
    def get_now():
        now = str(dt.utcnow()).split('.')[0]
        return '[' + now + ' UTC]'

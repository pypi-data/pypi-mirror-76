import datetime as dt
from colorama import Fore

class Logger:

    def __init__(self):
        self._format_date = "%d/%m/%Y %H:%M:%S.%f"

    def info(self, str_msg):
        print(Fore.BLACK + "{} - INFO - {}".format(dt.datetime.now().strftime(self._format_date), str_msg))

    def warning(self, str_msg):
        print(Fore.YELLOW + "{} - WARNING - {}".format(dt.datetime.now().strftime(self._format_date), str_msg))

    def error(self, str_msg):
        print(Fore.RED + "{} - ERROR - {}".format(dt.datetime.now().strftime(self._format_date), str_msg))
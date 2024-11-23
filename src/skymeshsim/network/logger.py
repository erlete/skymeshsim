"""Logger module.

Author:
    Paulo Sanchez (@erlete)
"""


import datetime

from colorama import Fore, Style, init

init(autoreset=True)


class Logger:
    """Logger class.

    Attributes:
        level (int): The logging level.
        prefix (str): The prefix to add to each log message.
    """

    _LEVELS = {
        0: 'DEBUG',
        1: 'INFO',
        2: 'WARNING',
        3: 'ERROR'
    }

    _COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW + Style.BRIGHT,
        'ERROR': Fore.RED + Style.BRIGHT,
    }

    def __init__(self, level, prefix) -> None:
        self.level = level
        self.prefix = prefix

    def log(self, message, level) -> None:
        """Log a message to console."""
        if level >= self.level:
            level_name = self._LEVELS.get(level, 'LOG')
            color = self._COLORS.get(level_name, Fore.WHITE)
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timestamp = f"{Style.DIM}({timestamp}){Style.NORMAL}"
            print(
                f"{color}{timestamp}{color} "
                + f"{self.prefix} [{level_name}] "
                + f"{message}{Style.RESET_ALL}"
            )

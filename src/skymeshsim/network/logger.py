import datetime

from colorama import Fore, Style, init

init(autoreset=True)


class Logger:
    LEVELS = {
        0: 'DEBUG',
        1: 'INFO',
        2: 'WARNING',
        3: 'ERROR'
    }

    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW + Style.BRIGHT,
        'ERROR': Fore.RED + Style.BRIGHT,
    }

    def __init__(self, level, prefix) -> None:
        self.level = level
        self.prefix = prefix

    def log(self, message, level) -> None:
        if level >= self.level:
            level_name = self.LEVELS.get(level, 'LOG')
            color = self.COLORS.get(level_name, Fore.WHITE)
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timestamp = f"{Style.DIM}({timestamp}){Style.NORMAL}"
            print(
                f"{color}{timestamp}{color} {self.prefix} [{level_name}] {message}{Style.RESET_ALL}")

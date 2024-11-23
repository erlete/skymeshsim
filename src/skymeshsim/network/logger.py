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
            print(
                f"{color}{timestamp} - {self.prefix} [{level_name}] {message}{Style.RESET_ALL}")

# Example usage:
# logger = Logger(1, '[MyApp]')
# logger.log('This is an info message', 1)
# logger.log('This is a debug message', 0)
# logger.log('This is a warning message', 2)
# logger.log('This is an error message', 3)

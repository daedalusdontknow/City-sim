from colorama import Fore, Style

from config import Preview


class Logger:

    providers = {
        "[Main]": Fore.BLUE,
        "[Error]": Fore.RED,
        "[Saver]": Fore.GREEN,
        "[Tick]": Fore.LIGHTWHITE_EX,
        "[Renderer]": Fore.CYAN,
        "[StatManager]": Fore.CYAN,

        "[Death]": Fore.BLACK,
        "[Human]": Fore.MAGENTA,

        "[House]": Fore.MAGENTA,
        "[Shop]": Fore.YELLOW,
        "[Office]": Fore.YELLOW,
    }

    @staticmethod
    def log(prov, message):
        # check if prov is in Preview.ignore_logger, if so dont print anything
        if prov in Preview.ignore_logger: return
        print(f"{Logger.providers[prov]} {prov} {Style.RESET_ALL}: {message}")
import crescent

from bot.config import CONFIG


class Bot(crescent.Bot):
    def __init__(self) -> None:
        super().__init__(token=CONFIG.token)

        self.plugins.load_folder("bot.plugins")
        print(self._command_handler.registry.values())


def run() -> None:
    bot = Bot()
    bot.run()

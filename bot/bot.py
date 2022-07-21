import crescent
from bot.config import CONFIG


class Bot(crescent.Bot):
    def __init__(self) -> None:
        super().__init__(token=CONFIG.token)

        self.plugins.load_folder("bot.plugins")


def run() -> None:
    Bot().run()

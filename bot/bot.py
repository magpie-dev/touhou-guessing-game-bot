from __future__ import annotations

import typing
import crescent
import hikari

from bot.config import CONFIG
from db.database import Database


EVENTS = []

def delayed_sub(event: type[hikari.Event]) -> typing.Callable[[typing.Callable[[Bot], typing.Awaitable[None]]], None]:
    def inner(func: typing.Callable[[Bot], typing.Awaitable[None]]) -> None:
        EVENTS.append((event, func))
    return inner

class Bot(crescent.Bot):
    def __init__(self) -> None:
        super().__init__(token=CONFIG.token)

        self.plugins.load_folder("bot.plugins")
        self._db: Database | None = None

    @property
    def db(self) -> Database:
        if not self._db:
            raise
        return self._db


def run() -> None:
    bot = Bot()

    @bot.listen()
    async def _(event: hikari.StartingEvent) -> None:
        bot = typing.cast("Bot", event.app)
        bot._db = Database("migrations")
        await bot.db.connect(
            host="localhost",
            database="touhoubot",
            user="touhoubot",
            password="Rookie1001",
        )

        if bot.db.must_create_migrations():
            bot.db.create_migrations()
        if await bot.db.must_apply_migrations():
            await bot.db.apply_migrations()


    bot.run()


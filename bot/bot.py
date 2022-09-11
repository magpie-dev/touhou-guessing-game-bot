from __future__ import annotations

import asyncio
import typing

import crescent
import hikari

import characters
import db
from bot.config import CONFIG


class Bot(crescent.Bot):
    def __init__(self) -> None:
        super().__init__(token=CONFIG.token)

        self.plugins.load_folder("bot.plugins")
        self._db: db.Database | None = None

    @property
    def db(self) -> db.Database:
        if not self._db:
            raise
        return self._db


def run() -> None:
    bot = Bot()

    @bot.listen()
    async def _(event: hikari.StartingEvent) -> None:
        bot = typing.cast("Bot", event.app)
        bot._db = db.Database("migrations")
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

        print(list(characters.all_characters()))

        async def create_char(character: str) -> None:
            if not await db.Character().exists(name=character):
                await db.Character(name=character).create()

        asyncio.gather(
            *(create_char(character) for character in characters.all_characters())
        )

    bot.run()

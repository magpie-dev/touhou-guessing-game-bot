from __future__ import annotations

import typing

import crescent
import hikari

from bot.guessing_game.abstract_game import AbstractGame
from characters.utils import get_character_url, random_character
import db

if typing.TYPE_CHECKING:
    from bot.bot import Bot


class Game(AbstractGame):
    def __init__(self, ctx: crescent.Context, bot: Bot) -> None:
        super().__init__(ctx, bot, round_timeout=30, game_mode=db.GameMode.NORMAL)
        self._character = random_character()
        print(self._character)

    @property
    def character(self) -> str:
        return self._character

    async def on_win(self) -> None:
        embed = hikari.Embed(title="Correct!").set_image(
            get_character_url(self.character, hidden=False)
        )
        await self.ctx.respond(embeds=[embed])
        await self.stop()

    async def on_start(self) -> None:
        embed = hikari.Embed(title="Guess the Touhou!").set_image(
            get_character_url(self.character, hidden=True)
        )
        await self.ctx.respond(embeds=[embed])

    async def on_timeout(self) -> None:
        embed = (
            hikari.Embed(title=self.character)
            .set_image(get_character_url(self.character, hidden=False))
            .set_author(name="Nobody guessed the answer :(")
        )
        await self.ctx.respond(embeds=[embed])
        await self.stop()

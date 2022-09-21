from __future__ import annotations

import asyncio
import typing

import crescent
import hikari
import miru

import characters
import db
import utils
from bot.guessing_game.abstract_game import AbstractGame

if typing.TYPE_CHECKING:
    from bot.bot import Bot


class Game(AbstractGame):
    def __init__(self, ctx: crescent.Context, bot: Bot) -> None:
        super().__init__(ctx, bot)
        self._character = characters.random_character()

    @property
    def character(self) -> str:
        return self._character

    @property
    def game_mode(self) -> db.GameMode:
        return db.GameMode.NORMAL

    @property
    def timeout(self) -> int:
        return 60

    async def on_win(self) -> None:
        embed = hikari.Embed(title="Correct!").set_image(
            characters.get_character_url(self.character, hidden=False)
        )
        await self.ctx.respond(embeds=[embed])
        await self.stop()

    async def on_start(self) -> None:
        embed = hikari.Embed(title="Guess the Touhou!").set_image(
            characters.get_character_url(self.character, hidden=True)
        )
        await Buttons.respond_with_view(self, embeds=[embed])

    async def on_timeout(self) -> None:
        embed = (
            hikari.Embed(title=self.character)
            .set_image(characters.get_character_url(self.character, hidden=False))
            .set_author(name="Nobody guessed the answer :(")
        )
        await self.ctx.respond(embeds=[embed])
        await self.stop()


class Buttons(utils.GameView):
    @miru.button(label="End Game", style=hikari.ButtonStyle.DANGER)
    async def end_game(self, _: miru.Button[typing.Any], ctx: miru.Context) -> None:
        embed = (
            hikari.Embed(title="Game Over!")
            .set_image(characters.get_character_url(self.game.character, hidden=False))
            .set_footer(
                f"Game ended by {utils.get_name_or_nickname(ctx.user, ctx.member)}"
            )
        )
        self.stop()
        await asyncio.gather(self.game.stop(), ctx.respond(embeds=[embed]))

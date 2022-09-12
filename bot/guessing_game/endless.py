from __future__ import annotations
import asyncio

from bot.guessing_game.abstract_game import AbstractGame

import db
import crescent
import characters
import hikari
import miru

import typing
from bot import utils

if typing.TYPE_CHECKING:
    from bot.bot import Bot


class EndlessGame(AbstractGame):
    def __init__(self, ctx: crescent.Context, bot: Bot) -> None:
        super().__init__(ctx, bot)
        self._character = characters.random_character()

    @property
    def character(self) -> str:
        return self._character

    @property
    def game_mode(self) -> db.GameMode:
        return db.GameMode.ENDLESS

    @property
    def timeout(self) -> int:
        return 60

    async def on_start(self) -> None:
        embed = hikari.Embed(title="Guess the Touhou!").set_image(
            characters.get_character_url(self.character, hidden=True)
        )
        await Buttons.respond_with_view(self, embeds=[embed])

    async def on_win(self) -> None:
        embed = (
            hikari.Embed(title="Round Over!")
            .set_image(characters.get_character_url(self.character, hidden=False))
            .set_footer(f"Round skipped by {self.ctx.user.username}")
        )

        await asyncio.gather(self.next_round(), self.ctx.respond(embeds=[embed]))

    async def on_timeout(self) -> None:
        await self.next_round()

    async def next_round(self, miru_ctx: miru.Context | None = None) -> None:
        last_char = self.character
        self._character = characters.random_character()

        embed = (
            hikari.Embed(title=f"Round Over! Last round was {last_char}.")
            .set_image(characters.get_character_url(self.character, hidden=True))
            .set_thumbnail(characters.get_character_url(last_char, hidden=False))
            .set_footer(f"Round skipped by {self.ctx.user.username}")
        )

        await Buttons.respond_with_view(self, embeds=[embed], miru_ctx=miru_ctx)
        self.schedule_timeout()


class Buttons(utils.GameView):
    @miru.button(label="Skip", style=hikari.ButtonStyle.PRIMARY)
    async def skip(self, _: miru.Button[typing.Any], ctx: miru.Context) -> None:
        asyncio.ensure_future(
            db.Guess(
                character_id=await self.game.get_character_id(),
                game_mode=self.game.game_mode,
            ).create()
        )

        self.stop()
        await asyncio.gather(self.game.next_round(miru_ctx=ctx))

    @miru.button(label="End Game", style=hikari.ButtonStyle.DANGER)
    async def end_game(self, _: miru.Button[typing.Any], ctx: miru.Context) -> None:
        embed = (
            hikari.Embed(title="Game Over!")
            .set_image(characters.get_character_url(self.game.character, hidden=False))
            .set_footer(f"Game ended by {utils.get_name_or_nickname(ctx.user, ctx.member)}")
        )
        self.stop()
        await asyncio.gather(self.game.stop(), ctx.respond(embeds=[embed]))

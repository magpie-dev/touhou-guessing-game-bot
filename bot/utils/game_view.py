from __future__ import annotations
import dataclasses

import miru

import typing
import hikari
import crescent

if typing.TYPE_CHECKING:
    from bot.guessing_game.abstract_game import AbstractGame


class GameView(miru.View):
    def __init__(self, *, game: AbstractGame) -> None:
        self.game: AbstractGame = game
        super().__init__(timeout=120, autodefer=False)

    @classmethod
    async def respond_with_view(
        cls,
        game: AbstractGame,
        miru_ctx: miru.Context | None = None,
        **kwargs: typing.Any,
    ) -> GameView:
        view = cls(game=game)

        if miru_ctx:
            await miru_ctx.respond(**kwargs, components=view.build())
            view.start(await miru_ctx.interaction.fetch_initial_response())
        else:
            msg = await game.ctx.respond(
                **kwargs, ensure_message=True, components=view.build()
            )
            view.start(msg)
        return view

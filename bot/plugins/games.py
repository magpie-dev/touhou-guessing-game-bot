import crescent

from bot.guessing_game.endless import EndlessGame
from bot.guessing_game.game import Game
from bot.utils import Plugin

plugin = Plugin()

group = crescent.Group("guessing-game")


@plugin.include
@group.child
@crescent.command
async def normal(ctx: crescent.Context) -> None:
    await Game(ctx, plugin.app).start()


@plugin.include
@group.child
@crescent.command
async def endless(ctx: crescent.Context) -> None:
    await EndlessGame(ctx, plugin.app).start()

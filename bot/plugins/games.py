import crescent

from bot.guessing_game.game import Game
from bot.utils import Plugin

plugin = Plugin()

group = crescent.Group("guessing-game")


@plugin.include
@group.child
@crescent.command
async def normal(ctx: crescent.Context) -> None:
    await Game(ctx, plugin.app).start()

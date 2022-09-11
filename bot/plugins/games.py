import crescent

from bot.guessing_game.game import Game
from bot.utils import Plugin

from db.database import User

plugin = Plugin()

group = crescent.Group("guessing-game")


@plugin.include
@group.child
@crescent.command
async def normal(ctx: crescent.Context) -> None:

    game = Game(ctx, plugin.app)
    await game.start()



@plugin.include
@crescent.command
async def test(ctx: crescent.Context) -> None:
    user = await User(user_id=1234, guesses={}).create()
    print(user)

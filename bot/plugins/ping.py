import crescent

from bot.utils import Plugin

plugin = Plugin()


@plugin.include
@crescent.command
async def ping(ctx: crescent.Context) -> None:
    await ctx.respond(f"Pong! `{round(plugin.app.heartbeat_latency * 100000)/100}ms`")

from __future__ import annotations

import abc
import asyncio
import typing

import crescent
import hikari

import characters
import db

if typing.TYPE_CHECKING:
    from bot.bot import Bot


class AbstractGame(abc.ABC):
    def __init__(self, ctx: crescent.Context, bot: Bot) -> None:
        self.ctx = ctx
        self.bot = bot

    @property
    @abc.abstractmethod
    def character(self) -> str:
        ...

    @abc.abstractmethod
    async def on_start(self) -> None:
        ...

    @abc.abstractmethod
    async def on_win(self) -> None:
        ...

    async def start(self) -> None:
        self.bot.subscribe(hikari.MessageCreateEvent, self.on_message)
        await self.on_start()

    async def stop(self) -> None:
        self.bot.unsubscribe(hikari.MessageCreateEvent, self.on_message)

    async def on_message(self, event: hikari.MessageCreateEvent) -> None:
        if event.channel_id != self.ctx.channel_id or event.author.is_bot:
            return

        if not event.content:
            return

        correct = characters.is_same_name(event.content, self.character)

        if correct:
            await asyncio.gather(event.message.add_reaction("✅"), self.on_win())
        else:
            await event.message.add_reaction("❌")

        await db.Guess(
            character_id=await characters.get_character_id(name=self.character),
            guessed_by=event.author.id,
            correct=correct,
        ).create()

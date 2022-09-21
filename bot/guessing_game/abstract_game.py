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
        self._timeout_event: asyncio.TimerHandle | None = None
        self.schedule_timeout()

    @property
    @abc.abstractmethod
    def character(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def game_mode(self) -> db.GameMode:
        ...

    @property
    @abc.abstractmethod
    def timeout(self) -> int:
        ...

    @abc.abstractmethod
    async def on_start(self) -> None:
        ...

    @abc.abstractmethod
    async def on_win(self) -> None:
        ...

    @abc.abstractmethod
    async def on_timeout(self) -> None:
        ...

    def timeout_handler(self) -> None:
        asyncio.ensure_future(self.on_timeout())

        async def _timeout_handler_inner() -> None:
            asyncio.ensure_future(
                db.Guess(
                    character_id=await self.get_character_id(), game_mode=self.game_mode
                ).create()
            )

        asyncio.ensure_future(_timeout_handler_inner())

    async def get_character_id(self) -> int:
        return await characters.get_character_id(name=self.character)

    def schedule_timeout(self) -> None:
        if self._timeout_event:
            self._timeout_event.cancel()

        self._timeout_event = asyncio.get_event_loop().call_later(
            self.timeout, self.timeout_handler
        )

    async def start(self) -> None:
        if self.on_message not in self.bot.event_manager.get_listeners(
            hikari.MessageCreateEvent  # type: ignore
        ):
            self.bot.subscribe(hikari.MessageCreateEvent, self.on_message)

        await self.on_start()

    async def stop(self) -> None:
        if self._timeout_event:
            self._timeout_event.cancel()
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
            character_id=await self.get_character_id(),
            guessed_by=event.author.id,
            correct=correct,
            game_mode=self.game_mode,
        ).create()

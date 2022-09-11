import functools
import hashlib
import pathlib
import random
import typing

import async_lru


def all_characters() -> typing.Iterable[str]:
    path = pathlib.Path("resources/images")
    return (file.stem for file in path.glob("*.png"))


ALL_CHARACTERS = list(all_characters())


def random_character() -> str:
    return random.choice(ALL_CHARACTERS)


def is_same_name(a: str, b: str) -> bool:
    a = a.casefold()
    b = b.casefold()

    if a == b:
        return True

    if len(a) == 2 and " ".join(a.split(" ")[::-1]) == b:
        return True

    return False


def get_character_url(name: str, *, hidden: bool) -> str:
    base_url = (
        "https://raw.githubusercontent.com/magpie-dev/"
        "touhou-guessing-game-bot/main/resources"
    )
    if hidden:
        return f"{base_url}/silhouettes/{hash_character_name(name)}.png"
    return f"{base_url}/images/{name.replace(' ', '%20')}.png"


@functools.lru_cache(maxsize=None)
def hash_character_name(name: str) -> str:
    return hashlib.md5(name.encode("utf-8")).hexdigest()


@async_lru.alru_cache(maxsize=None)
async def get_character_id(name: str) -> int:
    import db

    c = await db.Character.fetch(name=name)
    return c.id

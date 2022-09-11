import typing

T = typing.TypeVar("T")

class alru_cache:
    def __init__(self, maxsize: int | None = None) -> None: ...
    def __call__(self, func: T) -> T: ...

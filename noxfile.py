import functools
import typing

import nox


def poetry_session(
    callback: typing.Callable[[nox.Session], None]
) -> typing.Callable[[nox.Session], None]:
    @nox.session(name=callback.__name__)
    def inner(session: nox.Session) -> None:
        session.install("poetry")
        session.run("poetry", "shell")
        session.run("poetry", "install")
        callback(session)

    return inner


def pip_session(*args: str) -> typing.Callable[[nox.Session], None]:
    def inner(callback: typing.Callable[[nox.Session], None]):
        @nox.session
        @functools.wraps(callback)
        def inner(session: nox.Session):
            for arg in args:
                session.install(arg)
            callback(session)

        return inner

    return inner


@pip_session("flake8")
def flake8(session: nox.Session) -> None:
    session.run("flake8", "bot", "characters")


@pip_session("codespell")
def codespell(session: nox.Session) -> None:
    session.run("codespell", "bot", "characters")


@pip_session("isort")
def isort(session: nox.Session) -> None:
    session.run("isort", "--check", "bot", "characters")


@poetry_session
def mypy(session: nox.Session) -> None:
    session.run("mypy", "bot", "characters")

from __future__ import annotations

import functools
import typing

import nox

SCRIPT_PATHS = [
    "bot",
    "characters",
]


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


def pip_session(*args: str, name: str | None = None) -> typing.Callable[[nox.Session], None]:
    def inner(callback: typing.Callable[[nox.Session], None]):
        @nox.session(name=name)
        @functools.wraps(callback)
        def inner(session: nox.Session):
            for arg in args:
                session.install(arg)
            callback(session)

        return inner

    return inner


@pip_session("black", "codespell", "isort", name="apply-lint")
def apply_lint(session: nox.Session) -> None:
    session.run("black", *SCRIPT_PATHS)
    session.run("codespell", "-i", "2", *SCRIPT_PATHS)
    session.run("isort", *SCRIPT_PATHS)


@pip_session("black", "flake8", "codespell", "isort")
def lint(session: nox.Session) -> None:
    session.run("black", "--check", *SCRIPT_PATHS)
    session.run("flake8", *SCRIPT_PATHS)
    session.run("codespell", *SCRIPT_PATHS)
    session.run("isort", "--check", *SCRIPT_PATHS)


@poetry_session
def mypy(session: nox.Session) -> None:
    session.run("mypy", *SCRIPT_PATHS)

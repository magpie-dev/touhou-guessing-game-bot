import typing
import apgorm
from apgorm import types

__all__: typing.Sequence[str] = (
    "User",
    "Guess",
    "Character",
    "Database",
)


class User(apgorm.Model):
    id = types.Numeric().field()
    favorite = types.Int().field()

    primary_key = (id,)


class Guess(apgorm.Model):
    id = types.Serial().field()

    character_id = types.Int().field()
    guessed_by = types.Numeric().nullablefield()
    correct = types.Boolean().nullablefield()

    primary_key = (id,)

class Character(apgorm.Model):
    id = types.Serial().field()
    name = types.VarChar(32).field()

    primary_key = (name,)


class Database(apgorm.Database):
    users = User
    characters = Character
    guesses = Guess

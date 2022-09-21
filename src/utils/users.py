from __future__ import annotations

import hikari


def get_name_or_nickname(user: hikari.User, member: hikari.Member | None) -> str:
    if member:
        return member.nickname or member.username
    return user.username

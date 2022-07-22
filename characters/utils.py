import hashlib


def hash_character_name(name: str) -> str:
    return hashlib.md5(name.encode("utf-8")).hexdigest()

import dataclasses

import dotenv


@dataclasses.dataclass
class Config:
    token: str

    db_host: str
    db_database: str
    db_user: str
    db_pwd: str

    def __post_init__(self) -> None:
        if self.token is None:
            raise ValueError("TOKEN environment variable not found")


CONFIG = Config(
    **{k.lower(): v for k, v in dotenv.dotenv_values().items()}  # type: ignore
)

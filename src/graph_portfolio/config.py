import os

from dataclasses import dataclass

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


@dataclass
class AppConfig:
    ENABLE_PROMETHEUS: bool
    STOOQ_INTERVAL: str
    STOOQ_FETCH_BATCH_SIZE: int
    STOOQ_FETCH_DELAY_SECONDS: int

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            ENABLE_PROMETHEUS=os.getenv("ENABLE_PROMETHEUS", "false")[0].lower()
            in ("t", "1", "y"),
            STOOQ_INTERVAL=os.getenv("STOOQ_DATA_FETCH_INTERVAL", "DAILY"),
            STOOQ_FETCH_BATCH_SIZE=os.getenv("STOOQ_FETCH_BATCH_SIZE", 10),
            STOOQ_FETCH_DELAY_SECONDS=os.getenv("STOOQ_FETCH_DELAY_SECONDS", 2),
        )


CONFIG = AppConfig.from_env()

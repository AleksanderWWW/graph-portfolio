import datetime
from dataclasses import dataclass


@dataclass
class QueryData:
    start: datetime.date
    end: datetime.date
    tickers: list[str]


@dataclass
class Response:
    tickers: list[str]
    execution_time_seconds: int
    annealer_run_time_seconds: int
    is_independent_set: bool
    errors: list[str] | None = None

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class QueryDataDTO:
    start: datetime.date
    end: datetime.date
    tickers: Optional[list[str]] = None
    index: Optional[str] = None


@dataclass
class ResponseDTO:
    tickers: list[str]
    execution_time_seconds: int
    annealer_run_time_seconds: int
    is_independent_set: bool
    errors: Optional[list[str]] = None

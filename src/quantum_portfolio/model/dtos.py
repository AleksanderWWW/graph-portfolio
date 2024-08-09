from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class QueryDataDTO:
    start: datetime.date
    end: datetime.date
    tickers: Optional[list[str]] = None
    index: Optional[str] = None

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError("Start date must be before end date")

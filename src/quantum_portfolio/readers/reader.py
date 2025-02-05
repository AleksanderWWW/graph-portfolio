import datetime
from typing import Protocol

import pandas as pd


class DataReaderFunc(Protocol):
    def __call__(
        self, tickers: list[str], start_date: datetime.date, end_date: datetime.date
    ) -> pd.DataFrame: ...

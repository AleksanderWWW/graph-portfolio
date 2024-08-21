import abc
import datetime as dt

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


class DataReader(abc.ABC):
    @abc.abstractmethod
    def get_data(self, tickers: list, start: dt.date, end: dt.date) -> "pd.DataFrame":
        pass

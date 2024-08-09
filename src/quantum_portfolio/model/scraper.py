import abc
import datetime as dt
from concurrent.futures import ThreadPoolExecutor as Executor
from typing import Optional

import pandas as pd
import pandas_datareader as pdr

from pytickersymbols import PyTickerSymbols

from quantum_portfolio.model.dtos import QueryDataDTO


TICKER_PROVIDER = "yahoo"


class DataReader(abc.ABC):
    @abc.abstractmethod
    def get_data(self, tickers: list, start: dt.date, end: dt.date) -> pd.DataFrame:
        pass


class MockReader(DataReader):
    @property
    def param_ticker_data(self) -> dict[str, list[float]]:
        return {
                "Param-ticker-1": [1, 2, 3, 4, 5],
                "Param-ticker-2": [5, 4, 3, 2, 1],
        }

    @property
    def index_ticker_data(self) -> dict[str, list[float]]:
        return {
            "Index-ticker-1": [1, 2, 3, 4, 5],
            "Index-ticker-2": [5, 4, 3, 2, 1],
        }

    def __init__(self) -> None:
        self._data = pd.DataFrame(
            {
                **self.param_ticker_data,
                **self.index_ticker_data,
            }
        )

    def get_data(self, tickers: list, start: dt.date, end: dt.date) -> pd.DataFrame:
        return self._data.loc[:, tickers]


class Scraper:
    def __init__(self, data_reader: DataReader, query_data: QueryDataDTO) -> None:
        self._reader = data_reader
        self._query_data = query_data

        self._all_dfs: list[pd.DataFrame] = []
        self.data: Optional[pd.DataFrame] = None

    def scrape_data(self, sort: bool = True) -> None:
        if self._query_data.tickers is None and self._query_data.index is None:
            return

        tickers = self._resolve_tickers()

        self.data = self._reader.get_data(tickers, self._query_data.start, self._query_data.end)

        if sort:
            self.data = self.data.reindex(sorted(self.data.columns), axis=1)

    def _resolve_tickers(self) -> list[str]:
        tickers: set[str] = set()

        if self._query_data.tickers is not None:
            for ticker in self._query_data.tickers:
                tickers.add(ticker)

        if self._query_data.index is not None:
            for ticker in pull_tickers(self._query_data.index):
                tickers.add(ticker)

        return list(tickers)


def pull_tickers(index: str) -> list[str]:
    stock_data = PyTickerSymbols()

    indices = stock_data.get_all_indices()

    if index not in indices:
        raise ValueError(f"Index '{index}' not supported. Available choices: {indices}")

    return [item["symbol"] for item in stock_data.get_stocks_by_index(index)]

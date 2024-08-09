import abc
import datetime as dt
from concurrent.futures import ThreadPoolExecutor as Executor

import pandas as pd
import pandas_datareader as pdr

from pytickersymbols import PyTickerSymbols

from src.quantum_portfolio.model.dtos import QueryDataDTO


TICKER_PROVIDER = "yahoo"


class DataReader(abc.ABC):
    @abc.abstractmethod
    def get_data(self, tickers: list, start: dt.date, end: dt.date) -> pd.DataFrame:
        pass


class MockReader(DataReader):
    def __init__(self):
        self._data = pd.DataFrame(
            {
                "AAPL": [1, 2, 3, 4, 5],
                "MSFT": [5, 4, 3, 2, 1]
            }
        )

    def get_data(self, tickers: list, start: dt.date, end: dt.date) -> pd.DataFrame:
        return self._data[tickers]


class Scraper:
    def __init__(self, data_reader: DataReader, query_data: QueryDataDTO) -> None:
        self._reader = data_reader
        self._query_data = query_data

        self._all_dfs: list[pd.DataFrame] = []
        self.data: pd.DataFrame = pd.DataFrame()

    def scrape_data(self) -> None:
        if self._query_data.tickers is None and self._query_data.index is None:
            return

        tickers = self._resolve_tickers()

        self.data = self._reader.get_data(tickers, self._query_data.start, self._query_data.end)

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

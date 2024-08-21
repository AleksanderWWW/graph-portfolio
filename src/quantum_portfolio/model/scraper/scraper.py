from typing import Optional

import pandas as pd

from pytickersymbols import PyTickerSymbols

from quantum_portfolio.model.scraper.dtos import QueryDataDTO
from quantum_portfolio.model.scraper.readers.abstract import DataReader


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

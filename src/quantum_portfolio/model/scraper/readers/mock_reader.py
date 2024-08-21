import datetime as dt

import pandas as pd

from quantum_portfolio.model.scraper.readers.abstract import DataReader


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

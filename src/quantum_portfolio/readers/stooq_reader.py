import datetime
import asyncio
import aiohttp
import os
from enum import Enum
from io import StringIO
from urllib.parse import urlencode, urlunparse

import pandas as pd

from quantum_portfolio.utils import URLComponents


class StooqDataInterval(Enum):
    DAILY = "d"
    WEEKLY = "w"
    MONTHLY = "m"
    QUARTERLY = "q"
    YEARLY = "y"


SCHEME: str = "https"
HOST: str = "stooq.pl"

DATE_FORMAT: str = "%Y%m%d"

INDEX_COLUMN_NAME: str = "Data"
RETURN_COLUMNS_NAME: str = "Zamkniecie"


def read_stooq(
    tickers: list[str], *, start_date: datetime.date, end_date: datetime.date
) -> pd.DataFrame:
     return asyncio.run(read_stooq_data(
        tickers, start_date=start_date, end_date=end_date
        )
    )


async def read_stooq_data(
    tickers: list[str], *, start_date: datetime.date, end_date: datetime.date
) -> pd.DataFrame:
    """Fetch stock data from Stooq asynchronously for multiple tickers."""
    
    query_params = {
        "d1": start_date.strftime(DATE_FORMAT),
        "d2": end_date.strftime(DATE_FORMAT),
        "i": StooqDataInterval[os.getenv("STOOQ_DATA_INTERVAL", "DAILY")].value,
    }

    urls = [
        urlunparse(
            URLComponents(
                scheme="https", 
                netloc=HOST, 
                url="/q/d/l", 
                path="", 
                query=urlencode(query_params | {"s": ticker}),
                fragment="")
        )
        for ticker in tickers
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [read_single_ticker(session, url, ticker) for url, ticker in zip(urls, tickers)]
        results = await asyncio.gather(*tasks)

    return pd.concat(results, axis=1)


async def read_single_ticker(session: aiohttp.ClientSession, url: str, ticker: str) -> pd.DataFrame:
    """Fetch a single ticker asynchronously and parse the data."""
    async with session.get(url) as response:
        text = await response.text()

    data = pd.read_csv(StringIO(text), index_col=INDEX_COLUMN_NAME)
    return data[[RETURN_COLUMNS_NAME]].rename(columns={RETURN_COLUMNS_NAME: ticker})


if __name__ == "__main__":
        data = read_stooq(
        ["ale", "pko"], start_date=datetime.date(2025, 1, 12), end_date=datetime.date(2025, 2, 5)
        )

        print(data)

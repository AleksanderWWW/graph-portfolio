import asyncio
import datetime
from enum import Enum
from functools import lru_cache
from io import StringIO
from typing import Final
from urllib.parse import urlencode, urlunparse

import aiohttp
import pandas as pd

from graph_portfolio.config import CONFIG
from graph_portfolio.exceptions import DataNotFound
from graph_portfolio.utils import URLComponents


class StooqDataInterval(Enum):
    DAILY = "d"
    WEEKLY = "w"
    MONTHLY = "m"
    QUARTERLY = "q"
    YEARLY = "y"


SCHEME: Final[str] = "https"
HOST: Final[str] = "stooq.pl"

DATE_FORMAT: Final[str] = "%Y%m%d"

INDEX_COLUMN_NAME: Final[str] = "Data"
RETURN_COLUMNS_NAME: Final[str] = "Zamkniecie"


@lru_cache
def read_stooq(
    tickers: frozenset[str], *, start_date: datetime.date, end_date: datetime.date
) -> pd.DataFrame:
    return asyncio.run(
        read_stooq_data(list(tickers), start_date=start_date, end_date=end_date)
    )


async def read_stooq_data(
    tickers: list[str], *, start_date: datetime.date, end_date: datetime.date
) -> pd.DataFrame:
    """Fetch stock data from Stooq asynchronously for multiple tickers."""

    query_params = {
        "d1": start_date.strftime(DATE_FORMAT),
        "d2": end_date.strftime(DATE_FORMAT),
        "i": StooqDataInterval[CONFIG.STOOQ_INTERVAL].value,
    }

    urls = [
        urlunparse(
            URLComponents(
                scheme="https",
                netloc=HOST,
                url="/q/d/l",
                path="",
                query=urlencode(query_params | {"s": ticker}),
                fragment="",
            )
        )
        for ticker in tickers
    ]
    batch_size = CONFIG.STOOQ_FETCH_BATCH_SIZE
    delay = CONFIG.STOOQ_FETCH_DELAY_SECONDS

    async with aiohttp.ClientSession() as session:
        results = []

        for i in range(0, len(urls), batch_size):
            batch = [
                read_single_ticker(session, url, ticker)
                for url, ticker in zip(
                    urls[i : i + batch_size], tickers[i : i + batch_size]
                )
            ]
            results.extend(await asyncio.gather(*batch))

            if i + batch_size < len(urls):  # Avoid sleeping after the last batch
                await asyncio.sleep(delay)

    return pd.concat(results, axis=1)


async def read_single_ticker(
    session: aiohttp.ClientSession, url: str, ticker: str
) -> pd.DataFrame:
    """Fetch a single ticker asynchronously and parse the data."""
    async with session.get(url) as response:
        text = await response.text()

    if INDEX_COLUMN_NAME not in text:
        raise DataNotFound(ticker, url)
    data = pd.read_csv(StringIO(text), index_col=INDEX_COLUMN_NAME)
    return data[[RETURN_COLUMNS_NAME]].rename(columns={RETURN_COLUMNS_NAME: ticker})

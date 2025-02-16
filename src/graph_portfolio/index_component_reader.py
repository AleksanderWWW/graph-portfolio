import warnings
from io import StringIO
from typing import Final

import pandas as pd
import requests

from graph_portfolio.exceptions import DataNotFound

URL: Final[str] = "https://www.biznesradar.pl/gielda/indeks:{index}"

TEXT_IN_INVALID_RESPONSE: Final[str] = "Błąd 404"

COLUMN_WITH_TICKER_NAMES: Final[str] = "Profil"


def resolve_tickers(tickers: list[str]) -> frozenset[str]:
    resolved_tickers = []

    for ticker in tickers:
        split = ticker.split(":")
        match split:
            case [ticker_name]:
                resolved_tickers.append(ticker_name)
            case ["index", index, expected_len]:
                resolved_tickers += get_index_components(
                    index, expected_len=int(expected_len)
                )
            case ["index", index]:
                resolved_tickers += get_index_components(index)
            case _:
                raise ValueError(f"Invalid item in the ticker list: {ticker}")

    return frozenset(resolved_tickers)


def get_index_components(index: str, *, expected_len: int | None = None) -> list[str]:
    url = URL.format(index=index.upper())

    response = requests.get(url)

    if TEXT_IN_INVALID_RESPONSE in response.text:
        raise DataNotFound(index, url)

    names = pd.read_html(StringIO(response.text))[0][COLUMN_WITH_TICKER_NAMES]

    names = names.apply(lambda name: str(name).split(" ")[0].lower())

    if expected_len is not None and len(names) != expected_len:
        warnings.warn(
            f"'{index}' component fetch results might be incomplete. Expected {expected_len} items, got: {len(names)}."
        )

    return names.to_list()


if __name__ == "__main__":
    ts = ["index:wig20:30", "xtb"]
    print(resolve_tickers(ts))

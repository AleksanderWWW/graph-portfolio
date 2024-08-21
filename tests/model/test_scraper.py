from unittest.mock import patch

import pandas as pd
import pytest

from quantum_portfolio.model.scraper.scraper import Scraper
from quantum_portfolio.model.scraper.readers.mock_reader import MockReader
from quantum_portfolio.model.scraper.dtos import QueryDataDTO


@pytest.fixture
def mock_reader() -> MockReader:
    return MockReader()


def test_scraper_tickers_not_index(mock_reader) -> None:
    scraper = Scraper(mock_reader, QueryDataDTO(
        start='2021-01-01', end='2021-01-10', tickers=list(mock_reader.param_ticker_data.keys()))
                      )

    scraper.scrape_data()

    expected = pd.DataFrame(mock_reader.param_ticker_data)

    expected = expected.reindex(sorted(expected.columns), axis=1)

    assert scraper.data.equals(expected)


def test_scraper_tickers_and_index(mock_reader) -> None:
    scraper = Scraper(mock_reader, QueryDataDTO(
        start='2021-01-01', end='2021-01-10', tickers=list(mock_reader.param_ticker_data.keys()), index="DOW")
                      )

    with patch(
            "quantum_portfolio.model.scraper.scraper.pull_tickers", return_value=["Index-ticker-1", "Index-ticker-2"]
    ) as mock_pull_tickets:
        scraper.scrape_data()

        expected = pd.DataFrame(
            {
                **mock_reader.param_ticker_data,
                **mock_reader.index_ticker_data,
            }
        )

        expected = expected.reindex(sorted(expected.columns), axis=1)

        assert scraper.data.equals(expected)

        assert mock_pull_tickets.called_once_with("DOW")


@patch("quantum_portfolio.model.scraper.scraper.pull_tickers", return_value=["ticker-1", "ticker-2"])
def test_resolve_tickers(mock_pull_tickets) -> None:
    scraper = Scraper(MockReader(), QueryDataDTO(
        start='2021-01-01', end='2021-01-10', tickers=['AAPL', 'MSFT'], index="DOW",
    ))

    tickets = scraper._resolve_tickers()

    assert sorted(tickets) == sorted(["AAPL", "MSFT", "ticker-1", "ticker-2"])

    assert mock_pull_tickets.called_once_with("DOW")

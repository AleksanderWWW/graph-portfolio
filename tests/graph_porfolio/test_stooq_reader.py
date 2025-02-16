import datetime
from datetime import timedelta
from unittest.mock import Mock, patch

import pytest

from graph_portfolio.stooq_reader import read_stooq


@pytest.mark.unit
@patch("graph_portfolio.stooq_reader.asyncio.run")
def test_read_stooq_is_cached(mock_asyncio_run: Mock):
    start = datetime.date.today() - timedelta(days=365)
    end = datetime.date.today()

    for _ in range(10):
        read_stooq(
            tickers=frozenset(["ticker1", "ticker2", "ticker3"]),
            start_date=start,
            end_date=end,
        )

    assert mock_asyncio_run.call_count == 1

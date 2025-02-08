import numpy as np
import pytest
from pydantic import ValidationError

from graph_portfolio.schema import (
    Date,
    QueryData,
    RequestData,
    Result,
    ResponseData,
)


class TestQueryDataModel:
    def test_invalid_dates(self):
        with pytest.raises(ValueError):
            QueryData(
                start=Date(day=7, month=7, year=2023),
                end=Date(day=6, month=7, year=2023),
                tickers=["pko"],
            )

    def test_no_tickers(self):
        with pytest.raises(ValidationError):
            QueryData(
                start=Date(day=7, month=7, year=2023),
                end=Date(day=8, month=7, year=2023),
                tickers=[],
            )

    @pytest.mark.parametrize("threshold", [-0.4, 0, 1, 1.4, 2.7])
    def test_invalid_corr_threshold(self, threshold):
        with pytest.raises(ValueError):
            QueryData(
                start=Date(day=7, month=7, year=2023),
                end=Date(day=8, month=7, year=2023),
                tickers=["alr"],
                corr_threshold=threshold,
            )

    def test_correct_init(self):
        QueryData(
            start=Date(day=7, month=7, year=2023),
            end=Date(day=8, month=7, year=2024),
            tickers=["alr", "pko", "ale", "kgh", "peo", "pkn"],
        )


def test_path_from_query_to_response():
    query_data = QueryData(
        start=Date(day=7, month=7, year=2023),
        end=Date(day=8, month=7, year=2024),
        tickers=["alr", "pko", "ale", "kgh", "peo", "pkn"],
    )

    request_data = RequestData(data=query_data)

    result = Result(
        tickers=list(
            np.random.choice(request_data.data.tickers, replace=False, size=3)
        ),
        is_independent_set=True,
    )

    response = ResponseData(result=result)

    assert response.result.is_independent_set
    assert len(response.result.tickers) == 3

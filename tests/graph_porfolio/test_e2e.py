from typing import Any

import pytest

from graph_portfolio.api import GraphPortfolioAPI
from graph_portfolio.schema import RequestData


@pytest.mark.e2e
def test_e2e(request_data: dict[str, Any]):
    api = GraphPortfolioAPI()

    request = RequestData.model_validate(request_data)

    query = api.decode_request(request)

    prediction = api.predict(query)

    response = api.encode_response(prediction)

    assert response.result.is_independent_set

    assert len(response.result.tickers) >= 1

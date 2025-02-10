from typing import Any

import litserve as ls
from fastapi import HTTPException

from graph_portfolio.graph import get_max_diversified_portfolio
from graph_portfolio.schema import QueryData, RequestData, ResponseData, Result
from graph_portfolio.stooq_reader import read_stooq
from graph_portfolio.index_component_reader import resolve_tickers
from graph_portfolio.exceptions import DataNotFound


class GraphPortfolioAPI(ls.LitAPI):
    def setup(self, device: str) -> Any:
        return super().setup(device)

    def decode_request(self, request: RequestData) -> QueryData:
        return request.data

    def predict(self, query: QueryData) -> Result:
        try:
            data = read_stooq(
                tickers=resolve_tickers(query.tickers),
                start_date=query.start,
                end_date=query.end,
            )
        except DataNotFound as not_found_exc:
            raise HTTPException(404, detail=not_found_exc.msg)
        except ValueError as invalid_value_exc:
            raise HTTPException(400, detail=str(invalid_value_exc))
        except Exception as generic_exc:
            raise HTTPException(500, detail=str(generic_exc))

        try:
            portfolio_data = get_max_diversified_portfolio(data, query.corr_threshold)
        except Exception as exc:
            raise HTTPException(500, detail=str(exc))

        return Result(
            tickers=portfolio_data.assets,
            is_independent_set=portfolio_data.is_independent_set,
        )

    def encode_response(self, output: Result) -> ResponseData:
        return ResponseData(result=output)


if __name__ == "__main__":
    api = GraphPortfolioAPI()
    server = ls.LitServer(api, track_requests=True)
    server.run(port=8000)

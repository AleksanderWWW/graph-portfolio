from typing import Any

import litserve as ls

from fastapi import HTTPException

from quantum_portfolio.schema import QueryData, Result, RequestData, ResponseData
from quantum_portfolio.stooq_reader import read_stooq, DataNotFound
from quantum_portfolio.graph import get_max_diversified_portfolio


class SimpleLitAPI(ls.LitAPI):
    def setup(self, device: str) -> Any:
        return super().setup(device)
    
    def decode_request(self, request: RequestData) -> QueryData:
        return request.data

    def predict(self, query: QueryData) -> Result:
        try:
            data = read_stooq(
                tickers=query.tickers,
                start_date=query.start,
                end_date=query.end,
            )
        except DataNotFound as not_found_exc:
            raise HTTPException(404, detail=not_found_exc.msg)
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
    api = SimpleLitAPI()
    server = ls.LitServer(api)
    server.run(port=8000)

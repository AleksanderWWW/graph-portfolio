import litserve as ls

from quantum_portfolio.schema import Response, QueryData
from quantum_portfolio.stooq_reader import read_stooq
from quantum_portfolio.graph import get_max_diversified_assets, is_max_independent_set


class SimpleLitAPI(ls.LitAPI):
    def setup(self, device):
        return super().setup(device)
    
    def decode_request(self, request: QueryData) -> QueryData:
        return request

    def predict(self, query: QueryData):
        data = read_stooq(
            tickers=query.tickers,
            start_date=query.start,
            end_date=query.end,
        )
        
        assets, is_max_ind = get_max_diversified_assets(data)
        return Response(
            tickers=list(assets),
            is_independent_set=is_max_ind,
        )

    def encode_response(self, output: Response):
        return {"result": output}


if __name__ == "__main__":
    api = SimpleLitAPI()
    server = ls.LitServer(api)
    server.run(port=8000)

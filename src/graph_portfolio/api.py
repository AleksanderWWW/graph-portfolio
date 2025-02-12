import os
import time
from typing import Any

import litserve as ls
from fastapi import HTTPException

from prometheus_client import Histogram, CollectorRegistry, multiprocess, make_asgi_app

from graph_portfolio.graph import get_max_diversified_portfolio
from graph_portfolio.schema import QueryData, RequestData, ResponseData, Result
from graph_portfolio.stooq_reader import read_stooq
from graph_portfolio.index_component_reader import resolve_tickers
from graph_portfolio.exceptions import DataNotFound
from graph_portfolio.config import CONFIG


# Set the directory for multiprocess mode
os.environ["PROMETHEUS_MULTIPROC_DIR"] = "/tmp/prometheus_multiproc_dir"

# Ensure the directory exists
if not os.path.exists("/tmp/prometheus_multiproc_dir"):
    os.makedirs("/tmp/prometheus_multiproc_dir")

# Use a multiprocess registry
registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)


class PrometheusLogger(ls.Logger):
    def __init__(self):
        super().__init__()
        self.function_duration = Histogram(
            "request_processing_seconds",
            "Time spent processing request",
            ["function_name"],
            registry=registry,
        )

    def process(self, key, value):
        print("processing", key, value)
        self.function_duration.labels(function_name=key).observe(value)


class GraphPortfolioAPI(ls.LitAPI):
    def setup(self, device: str) -> Any:
        return super().setup(device)

    def decode_request(self, request: RequestData) -> QueryData:
        return request.data

    def predict(self, query: QueryData) -> Result:
        start = time.time()
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

        self.log("predict", time.time() - start)
        return Result(
            tickers=portfolio_data.assets,
            is_independent_set=portfolio_data.is_independent_set,
        )

    def encode_response(self, output: Result) -> ResponseData:
        return ResponseData(result=output)


if __name__ == "__main__":
    logger: ls.Logger | None = None

    if CONFIG.ENABLE_PROMETHEUS:
        prometheus_logger = PrometheusLogger()
        prometheus_logger.mount(path="/metrics", app=make_asgi_app(registry=registry))

        logger = prometheus_logger

    api = GraphPortfolioAPI()

    server = ls.LitServer(api, track_requests=True, loggers=logger)
    server.run(port=8000)

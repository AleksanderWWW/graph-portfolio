from pydantic import BaseModel


class Date(BaseModel):
    day: int
    month: int
    year: int


class QueryData(BaseModel):
    start: Date
    end: Date
    tickers: list[str]
    corr_threshold: float = 0.5


class RequestData(BaseModel):
    data: QueryData


class Result(BaseModel):
    tickers: list[str]
    is_independent_set: bool


class ResponseData(BaseModel):
    result: Result

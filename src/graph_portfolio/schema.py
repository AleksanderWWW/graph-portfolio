import datetime
from typing import Self

from pydantic import BaseModel, conlist, model_validator


class Date(BaseModel):
    day: int
    month: int
    year: int


class QueryData(BaseModel):
    start: Date
    end: Date
    tickers: conlist(str, min_length=1)
    corr_threshold: float = 0.5

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        start_date = datetime.date(self.start.year, self.start.month, self.start.day)
        end_date = datetime.date(self.end.year, self.end.month, self.end.day)

        if start_date >= end_date:
            raise ValueError("Start date must be before end date")

        if self.corr_threshold <= 0 or self.corr_threshold >= 1:
            raise ValueError("Correlation threshold must be a float in (0, 1)")

        return self


class RequestData(BaseModel):
    data: QueryData


class Result(BaseModel):
    tickers: list[str]
    is_independent_set: bool


class ResponseData(BaseModel):
    result: Result

import datetime

from typing import Self
from pydantic import BaseModel, Field, ValidationError, model_validator


class QueryData(BaseModel):
    start: datetime.date
    end: datetime.date
    tickers: list[str] = Field(..., min_items=1, description="List of stock tickers")

    @model_validator(mode="after")
    def validate_date_range(self) -> Self:
        """Ensure the end date is after the start date."""
        if self.end < self.start:
            raise ValidationError("End date must be after the start date.")
        return self


class Response(BaseModel):
    tickers: list[str]
    is_independent_set: bool
    errors: list[str] | None = None

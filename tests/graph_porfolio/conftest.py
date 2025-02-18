from typing import Any

import pandas as pd
import pytest


@pytest.fixture(scope="session")
def financial_test_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "A1": [1, 2, 3, 4],
            "A2": [10, 23, 32, 49],
            "B1": [10, 10, 10, 10],
        }
    )


@pytest.fixture(scope="session")
def request_data() -> dict[str, Any]:
    return {
        "data": {
            "start": {
                "day": 7,
                "month": 7,
                "year": 2023,
            },
            "end": {
                "day": 7,
                "month": 7,
                "year": 2024,
            },
            "tickers": ["index:wig20", "index:wig30"],
            "corr_threshold": 0.3,
        }
    }

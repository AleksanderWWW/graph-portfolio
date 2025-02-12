from unittest.mock import patch

import pytest

from graph_portfolio.config import AppConfig


@pytest.mark.unit
@patch.dict(
    "graph_portfolio.config.os.environ",
    values={
        "ENABLE_PROMETHEUS": "true",
        "STOOQ_DATA_FETCH_INTERVAL": "yearly",
        "STOOQ_FETCH_BATCH_SIZE": "20",
        "STOOQ_FETCH_DELAY_SECONDS": "1",
    },
)
def test_app_config():
    config = AppConfig.from_env()

    assert config.ENABLE_PROMETHEUS

    assert config.STOOQ_INTERVAL == "YEARLY"
    assert config.STOOQ_FETCH_BATCH_SIZE == 20
    assert config.STOOQ_FETCH_DELAY_SECONDS == 1

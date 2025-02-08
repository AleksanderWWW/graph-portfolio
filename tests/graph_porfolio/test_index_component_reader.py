from unittest.mock import patch, Mock

import pytest

from graph_portfolio.index_component_reader import resolve_tickers


@pytest.mark.unit
@patch(
    "graph_portfolio.index_component_reader.get_index_components",
    return_value=[
        "ale",
        "alr",
        "bdx",
        "cdr",
    ],
)
def test_resolve_tickers_mocked(mock_get_components: Mock):
    tickers = ["index:wig20:20", "xtb"]

    resolved = resolve_tickers(tickers)

    mock_get_components.assert_called_once_with("wig20", expected_len=20)

    assert resolved == ["ale", "alr", "bdx", "cdr", "xtb"]


@pytest.mark.intergation
def test_resolve_tickers():
    tickers = ["index:wig20", "xtb", "index:wig30"]

    resolved = resolve_tickers(tickers)

    assert len(resolved) == 51

    assert "xtb" in resolved

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

    assert sorted(resolved) == sorted(["ale", "alr", "bdx", "cdr", "xtb"])


@pytest.mark.unit
@patch("graph_portfolio.index_component_reader.get_index_components")
def test_resolve_tickers_mocked_invalid_input(mock_get_components: Mock):
    tickers = ["funkyindex:wig20:20"]

    with pytest.raises(ValueError):
        resolve_tickers(tickers)

    mock_get_components.assert_not_called()


@pytest.mark.unit
@patch("graph_portfolio.index_component_reader.get_index_components")
def test_resolve_tickers_mocked_not_asking_for_index(mock_get_components: Mock):
    tickers = ["xtb", "pko"]

    resolved = resolve_tickers(tickers)

    mock_get_components.assert_not_called()

    assert sorted(resolved) == sorted(["xtb", "pko"])


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
def test_resolve_tickers_mocked_returns_unique_tickers(mock_get_components: Mock):
    tickers = ["index:wig20", "ale", "bdx"]

    resolved = resolve_tickers(tickers)

    assert len(resolved) == 4  # only unique tickers


@pytest.mark.integration
def test_resolve_tickers():
    tickers = ["index:wig20", "test_ticker", "index:wig30"]

    resolved = resolve_tickers(tickers)

    assert len(resolved) == 31

    assert "test_ticker" in resolved

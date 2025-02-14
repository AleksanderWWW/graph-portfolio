import networkx as nx
import pandas as pd
import pytest

from graph_portfolio.graph import (
    build_graph,
    get_corr_matrix,
    get_max_diversified_portfolio,
    is_independent_set,
)


@pytest.mark.unit
def test_is_independent_set():
    graph = nx.Graph()
    graph.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("A", "C"),
        ]
    )

    assert is_independent_set(graph, ["B", "D"])

    graph.add_edges_from([("B", "D")])

    assert not is_independent_set(graph, ["B", "D"])

    assert is_independent_set(graph, ["A"])


@pytest.mark.integration
def test_get_max_diversified_portfolio(financial_test_data: pd.DataFrame):
    result = get_max_diversified_portfolio(financial_test_data, corr_threshold=0.5)

    assert result.is_independent_set

    assert "B1" in result.assets

    assert len(result.assets) == 2


@pytest.mark.integration
def test_build_graph(financial_test_data: pd.DataFrame):
    corr_matrix = get_corr_matrix(financial_test_data)

    graph = build_graph(corr_matrix, corr_threshold=0.5)

    assert is_independent_set(graph, ["B1", "A1"])

    assert is_independent_set(graph, ["B1", "A2"])

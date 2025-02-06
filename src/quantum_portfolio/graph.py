import networkx as nx
import pandas as pd
from networkx.algorithms.approximation import maximum_independent_set


def get_max_diversified_assets(
    data: pd.DataFrame, corr_threshold: float = 0.5
) -> tuple[set[str], bool]:
    corr_matrix = get_corr_matrix(data)
    label_mapping = {i: name for i, name in enumerate(corr_matrix.columns)}

    graph = build_graph(corr_matrix, corr_threshold)

    max_ind = maximum_independent_set(graph)

    assets = set(label_mapping[label] for label in max_ind)
    return assets, is_max_independent_set(graph, assets)


def build_graph(corr_matrix: pd.DataFrame, corr_threshold: float) -> nx.Graph:
    return nx.from_numpy_array(
        ((corr_matrix.values > corr_threshold) & (corr_matrix.values < 1))
    )


def get_corr_matrix(data: pd.DataFrame) -> pd.DataFrame:
    return data.pct_change().corr()


def is_max_independent_set(graph: nx.Graph, chosen_nodes: set[str]) -> bool:
    return len(graph.subgraph(chosen_nodes).edges) == 0

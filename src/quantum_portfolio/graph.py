import networkx as nx
import pandas as pd
from networkx.algorithms.approximation import maximum_independent_set


def get_max_diversified_assets(
    data: pd.DataFrame, corr_threshold: float = 0.5
) -> set[str]:
    corr_matrix = get_corr_matrix(data)
    label_mapping = {i: name for i, name in enumerate(corr_matrix.columns)}

    graph = build_graph(corr_matrix, corr_threshold)

    max_ind = maximum_independent_set(graph)

    return set(label_mapping[label] for label in max_ind)


def build_graph(corr_matrix: pd.DataFrame, corr_threshold: float) -> nx.Graph:
    return nx.from_numpy_array(
        ((corr_matrix.values > corr_threshold) & (corr_matrix.values < 1))
    )


def get_corr_matrix(data: pd.DataFrame) -> pd.DataFrame:
    return data.pct_change().corr()

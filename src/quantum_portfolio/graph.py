import pandas as pd
import networkx as nx


def build_graph(data: pd.DataFrame, corr_threshold: float) -> nx.Graph:
    corr_matrix = data.pct_change().corr()

    label_mapping = {i: name for i, name in enumerate(corr_matrix.columns)}

    graph = nx.from_numpy_array(((corr_matrix.values > corr_threshold) & (corr_matrix.values < 1)))
    nx.set_node_attributes(graph, label_mapping, "label")

    return graph

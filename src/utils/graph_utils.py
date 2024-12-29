from typing import Dict, Set
from pyvis.network import Network  # pip install pyvis


def visualise_graph(adj_dict: Dict[str, Set[str]], file_name: str = "mygraph.html"):
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        layout=True,
    )

    for node in adj_dict.keys():
        net.add_node(node)

    for node, adj_nodes in adj_dict.items():
        for adj_node in adj_nodes:
            net.add_edge(node, adj_node)

    net.toggle_physics(True)
    net.show(file_name, notebook=False)

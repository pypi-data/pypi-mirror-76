from typing import Dict, List

from deduce_uces.mergers.merger import Merger
from deduce_uces.types import MinimalUCE
import networkx as nx

from deduce_uces.utils import find, make_id

##############################################
# WARNING: GraphMerger is experimental.      #
# Do not use until more testing is complete. #
##############################################


def to_adjacency_graph(uces_by_genome: Dict[str, List[MinimalUCE]]) -> nx.DiGraph:
    g = nx.DiGraph()

    for genome, uces in uces_by_genome.items():
        for uce in uces:
            # Add a node for this UCE to the graph
            if not g.has_node(uce.id):
                g.add_node(uce.id, start={genome: uce.start}, end={genome: uce.end})
            else:
                g.nodes[uce.id]["start"][genome] = uce.start
                g.nodes[uce.id]["end"][genome] = uce.end

    for genome, uces in uces_by_genome.items():
        sorted_uces = sorted(uces, key=lambda x: x.start)

        for i in range(len(sorted_uces) - 1):
            # If adjacent in this genome, add or update an edge between the UCEs
            if sorted_uces[i].start == sorted_uces[i + 1].start - 1:
                if not g.has_edge(sorted_uces[i].id, sorted_uces[i + 1].id):
                    g.add_edge(
                        sorted_uces[i].id,
                        sorted_uces[i + 1].id,
                        weight=1,
                        adjacent_in=[genome],
                    )
                else:
                    g.edges[sorted_uces[i].id, sorted_uces[i + 1].id]["weight"] += 1
                    g.edges[sorted_uces[i].id, sorted_uces[i + 1].id][
                        "adjacent_in"
                    ] += [genome]

    return g


def from_adjacency_graph(g: nx.DiGraph) -> Dict[str, List[MinimalUCE]]:
    uces_by_genome = {}

    for node in g.nodes.data():
        for genome in node[1]["start"].keys():
            if not genome in uces_by_genome:
                uces_by_genome[genome] = []

            uces_by_genome[genome].append(
                MinimalUCE(
                    node[0], start=node[1]["start"][genome], end=node[1]["end"][genome]
                )
            )

    return uces_by_genome


def merge_graph(g: nx.DiGraph, min_genomes: int) -> nx.DiGraph:
    edges_to_merge = [edge for edge in g.edges.data("weight") if edge[2] >= min_genomes]

    # The number of new UCEs is equal to the number of existing plus the number of merged
    existing_uces = set(n for n in g.nodes())

    gen_id = make_id(
        len(existing_uces) + len(edges_to_merge),
        start_from=len(existing_uces) + len(edges_to_merge) - 1,
    )

    while len(edges_to_merge) > 0:
        edge_to_merge = edges_to_merge[0]
        edges_to_merge = edges_to_merge[1:]

        node_from = edge_to_merge[0]
        node_to = edge_to_merge[1]
        new_id = gen_id()

        g.add_node(
            new_id, start=g.nodes[node_from]["start"], end=g.nodes[node_to]["end"]
        )

        edges_to_move = [e for e in g.edges(node_to, data=True)]

        for edge in edges_to_move:
            g.remove_edge(edge[0], edge[1])

        g.remove_edge(node_from, node_to)
        g.remove_node(node_from)
        g.remove_node(node_to)

        for edge in edges_to_move:
            g.add_edge(
                new_id,
                edge[1],
                weight=edge[2]["weight"],
                adjacent_in=edge[2]["adjacent_in"],
            )

        def translate(edge):
            if edge == node_from or edge == node_to:
                return new_id
            else:
                return edge

        edges_to_merge = [
            (translate(edge[0]), translate(edge[1]), edge[2]) for edge in edges_to_merge
        ]

    return g


class GraphMerger(Merger):
    def merge(
        self, uces_by_genome: Dict[str, List[MinimalUCE]], min_genomes: int
    ) -> Dict[str, List[MinimalUCE]]:
        g = to_adjacency_graph(uces_by_genome)

        g = merge_graph(g, min_genomes)

        return from_adjacency_graph(g)

"""Inspectable graph data contracts for Lab 4.

The baseline intentionally avoids NetworkX/PyG/DGL. A traffic graph is kept as
plain immutable Python records so every node, edge, feature, and provenance tag
can be inspected before a GNN library is introduced in a later lab.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    feature_names: tuple[str, ...]
    features: tuple[float, ...]

@dataclass(frozen=True)
class GraphEdge:
    src: str
    dst: str
    relation: str
    provenance: tuple[str, ...]
    feature_names: tuple[str, ...] = ()
    features: tuple[float, ...] = ()

@dataclass(frozen=True)
class TrafficGraph:
    design: str
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]
    raw_observable_budget: tuple[str, ...]
    explicit_relations: tuple[str, ...]
    information_loss: tuple[str, ...]

    def nodes_of_type(self, node_type: str) -> tuple[GraphNode, ...]:
        return tuple(n for n in self.nodes if n.node_type == node_type)

    def edges_of_relation(self, relation: str) -> tuple[GraphEdge, ...]:
        return tuple(e for e in self.edges if e.relation == relation)

    @property
    def provenance_codes(self) -> tuple[str, ...]:
        return tuple(sorted({code for e in self.edges for code in e.provenance}))

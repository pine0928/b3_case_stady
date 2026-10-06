"""Lab 4 student starter: explicit graph-construction decisions.

Every edge must document provenance using one or more of:
P protocol-grounded, O order-derived, B burst/cycle-derived,
A association-derived, L learned/adaptive, H designer-typed.
"""
from labs.common.graphs import TrafficGraph

def packet_chain_graph(flow) -> TrafficGraph:
    raise NotImplementedError

def burst_graph(flow, bursts) -> TrafficGraph:
    raise NotImplementedError

def packet_burst_hierarchical_graph(flow, bursts) -> TrafficGraph:
    raise NotImplementedError

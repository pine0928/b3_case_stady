from labs.common.graphs import GraphNode, GraphEdge, TrafficGraph
from labs.lab4_graph import starter

def test_lab4_contracts_are_present():
    assert GraphNode is not None and GraphEdge is not None and TrafficGraph is not None
    assert callable(starter.packet_chain_graph)
    assert callable(starter.burst_graph)
    assert callable(starter.packet_burst_hierarchical_graph)

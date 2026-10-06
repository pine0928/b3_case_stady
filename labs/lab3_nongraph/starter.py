"""Lab 3 starter: non-graph representation builders.

Students implement the same interfaces as the instructor reference in
`reference.py`.  Keep the canonical observable budget unless an extension is
explicitly declared and compared separately.
"""
from labs.common.schema import Flow, Burst


def statistical_vector(flow: Flow):
    """TODO: aggregate only the declared canonical observables."""
    raise NotImplementedError


def packet_sequence(flow: Flow, max_packets: int):
    """TODO: first-N packet rows + zero padding + validity mask."""
    raise NotImplementedError


def burst_sequence(bursts: list[Burst], max_bursts: int):
    """TODO: summarize the frozen Lab 2 bursts without changing boundaries."""
    raise NotImplementedError


def hierarchical_representation(flow: Flow, bursts: list[Burst]):
    """TODO: preserve packet-within-burst membership as a ragged hierarchy."""
    raise NotImplementedError


def pad_hierarchy(rep, max_bursts: int, max_packets_per_burst: int):
    """TODO: make batching loss explicit with masks and dropped-item counts."""
    raise NotImplementedError

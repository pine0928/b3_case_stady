"""Fixed-length vectorizers used to control Lab 5 learning experiments.

These vectorizers are deliberately transparent.  They are not claimed to be
state-of-the-art encoders; their purpose is to expose when a relation is made
explicit before learning.
"""
from __future__ import annotations
import math
import numpy as np

from labs.common.preprocess import direction_only_bursts
from labs.lab3_nongraph.starter import statistical_vector, packet_sequence, burst_sequence, hierarchical_representation, pad_hierarchy
from labs.lab4_graph.starter import packet_chain_graph, packet_burst_hierarchical_graph


def _flat(values) -> list[float]:
    out = []
    for row in values:
        out.extend(float(x) for x in row)
    return out


def vectorize_statistics(flow) -> np.ndarray:
    return np.asarray(statistical_vector(flow).values, dtype=np.float64)


def vectorize_packet_sequence(flow, max_packets: int = 8) -> np.ndarray:
    rep = packet_sequence(flow, max_packets)
    return np.asarray(_flat(rep.values) + [float(x) for x in rep.mask], dtype=np.float64)


def vectorize_burst_sequence(flow, max_bursts: int = 4) -> np.ndarray:
    bursts = direction_only_bursts(flow)
    rep = burst_sequence(bursts, max_bursts)
    return np.asarray(_flat(rep.values) + [float(x) for x in rep.mask], dtype=np.float64)


def vectorize_hierarchy(flow, max_bursts: int = 4, max_packets_per_burst: int = 2) -> np.ndarray:
    bursts = direction_only_bursts(flow)
    ragged = hierarchical_representation(flow, bursts)
    rep = pad_hierarchy(ragged, max_bursts, max_packets_per_burst)
    values = []
    values.extend(_flat(rep.burst_values))
    for burst_rows in rep.packet_values:
        values.extend(_flat(burst_rows))
    values.extend(float(x) for x in rep.burst_mask)
    for pmask in rep.packet_mask:
        values.extend(float(x) for x in pmask)
    return np.asarray(values, dtype=np.float64)


def _node_packet_features(graph):
    return {n.node_id: n for n in graph.nodes if n.node_type == "packet"}


def _edge_relation_summary(graph) -> list[float]:
    """Relation-local summaries from the graph, without adding raw observables.

    The product term is intentionally generic: it lets a linear downstream
    model react to two jointly large neighbouring packets.  The same relation
    could be computed from a sequence; graph construction merely makes the
    neighbourhood explicit.
    """
    packets = _node_packet_features(graph)
    pair_products = []
    pair_absdiff = []
    direction_switch = []
    for e in graph.edges:
        if e.relation != "next_packet" or e.src not in packets or e.dst not in packets:
            continue
        a, b = packets[e.src], packets[e.dst]
        da, la, _ = a.features
        db, lb, _ = b.features
        pair_products.append((la / 700.0) * (lb / 700.0))
        pair_absdiff.append(abs(la - lb) / 700.0)
        direction_switch.append(1.0 if da != db else 0.0)
    if not pair_products:
        return [0.0] * 7
    cross_products = [p * s for p, s in zip(pair_products, direction_switch)]
    return [
        float(np.mean(pair_products)),
        float(np.max(pair_products)),
        float(np.mean(pair_absdiff)),
        float(np.max(pair_absdiff)),
        float(np.mean(direction_switch)),
        float(np.max(cross_products)),
        float(np.mean(cross_products)),
    ]


def vectorize_packet_chain_graph(flow, include_relations: bool = True) -> np.ndarray:
    if not flow.packets:
        raise ValueError("graph vectorization requires at least one packet")
    graph = packet_chain_graph(flow)
    # Node block deliberately matches the same packet observables used by the
    # packet-sequence representation, but discards position after aggregation.
    rows = np.asarray([n.features for n in graph.nodes], dtype=np.float64)
    node_summary = np.concatenate([rows.mean(axis=0), rows.std(axis=0), rows.max(axis=0), rows.min(axis=0)])
    relation = _edge_relation_summary(graph) if include_relations else [0.0] * 7
    return np.asarray(list(node_summary) + relation, dtype=np.float64)


def vectorize_hierarchical_graph(flow, include_relations: bool = True) -> np.ndarray:
    if not flow.packets:
        raise ValueError("graph vectorization requires at least one packet")
    bursts = direction_only_bursts(flow)
    graph = packet_burst_hierarchical_graph(flow, bursts)
    packet_rows = np.asarray([n.features for n in graph.nodes if n.node_type == "packet"], dtype=np.float64)
    burst_rows = np.asarray([n.features for n in graph.nodes if n.node_type == "burst"], dtype=np.float64)
    psummary = np.concatenate([packet_rows.mean(axis=0), packet_rows.std(axis=0), packet_rows.max(axis=0), packet_rows.min(axis=0)])
    bsummary = np.concatenate([burst_rows.mean(axis=0), burst_rows.std(axis=0), burst_rows.max(axis=0), burst_rows.min(axis=0)])
    relation = _edge_relation_summary(graph) if include_relations else [0.0] * 7
    # Membership/topology counts are derived from the frozen burst partition.
    rel_counts = []
    for rel in ("member_of", "next_burst"):
        rel_counts.append(float(sum(e.relation == rel for e in graph.edges)))
    return np.asarray(list(psummary) + list(bsummary) + relation + rel_counts, dtype=np.float64)


def vectorize_sequence_adjacency_summary(flow) -> np.ndarray:
    """Non-graph control that reconstructs the packet-chain graph vector exactly.

    It uses the same canonical packet rows and the same adjacent-pair relation
    summaries as :func:`vectorize_packet_chain_graph`, but it derives adjacency
    directly from sequence position rather than constructing a graph object.

    This control is intentionally *not* a new baseline representation.  It is an
    experimental-audit instrument showing that the current graph relation block
    is a feature-engineering choice over chronological neighbours, not graph-
    unique information.
    """
    rows = np.asarray(
        [(p.direction, p.packet.packet_length, p.iat) for p in flow.packets],
        dtype=np.float64,
    )
    node_summary = np.concatenate(
        [rows.mean(axis=0), rows.std(axis=0), rows.max(axis=0), rows.min(axis=0)]
    )

    pair_products = []
    pair_absdiff = []
    direction_switch = []
    for a, b in zip(flow.packets, flow.packets[1:]):
        da, la = a.direction, a.packet.packet_length
        db, lb = b.direction, b.packet.packet_length
        pair_products.append((la / 700.0) * (lb / 700.0))
        pair_absdiff.append(abs(la - lb) / 700.0)
        direction_switch.append(1.0 if da != db else 0.0)

    if not pair_products:
        relation = [0.0] * 7
    else:
        cross_products = [p * s for p, s in zip(pair_products, direction_switch)]
        relation = [
            float(np.mean(pair_products)),
            float(np.max(pair_products)),
            float(np.mean(pair_absdiff)),
            float(np.max(pair_absdiff)),
            float(np.mean(direction_switch)),
            float(np.max(cross_products)),
            float(np.mean(cross_products)),
        ]
    return np.asarray(list(node_summary) + relation, dtype=np.float64)

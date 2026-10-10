"""Reproducible matched-information experiment runner for Lab 5."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import numpy as np
from sklearn.model_selection import train_test_split

from labs.common.schema import Flow, DirectedPacket, PacketRecord
from .dataset import make_dataset
from .splits import group_holdout_indices
from .models import fit_and_score, make_linear, make_mlp, Metrics
from .protocol import assert_registry_contract, retention_audit
from .vectorizers import (
    vectorize_statistics,
    vectorize_packet_sequence,
    vectorize_burst_sequence,
    vectorize_hierarchy,
    vectorize_packet_chain_graph,
    vectorize_hierarchical_graph,
)

Vectorizer = Callable[[object], np.ndarray]

VECTORIZERS: dict[str, Vectorizer] = {
    "statistics": vectorize_statistics,
    "packet-sequence": vectorize_packet_sequence,
    "burst-sequence": vectorize_burst_sequence,
    "hierarchy": vectorize_hierarchy,
    "packet-chain-graph": vectorize_packet_chain_graph,
    "hierarchical-graph": vectorize_hierarchical_graph,
    "packet-chain-graph-no-relations": lambda flow: vectorize_packet_chain_graph(flow, include_relations=False),
    "hierarchical-graph-no-relations": lambda flow: vectorize_hierarchical_graph(flow, include_relations=False),
}

@dataclass(frozen=True)
class ExperimentResult:
    representation: str
    learner: str
    n_features: int
    metrics: Metrics
    retained_packet_fraction: float = 1.0
    protocol: str = "practical-budget"
    observation_limit: int | None = None


@dataclass(frozen=True)
class _WithFlow:
    label: int
    flow: Flow


def _matrix(items, vectorizer: Vectorizer):
    X = np.stack([vectorizer(x.flow) for x in items])
    y = np.asarray([x.label for x in items], dtype=np.int64)
    return X, y


def _observed_flow(flow: Flow, packet_limit: int | None) -> Flow:
    """Enforce the raw-observable contract at the vectorizer boundary.

    Packet metadata other than length is scrubbed; timestamps are reconstructed
    solely from IAT. A vectorizer cannot recover IPs, ports, flags or protocol.
    """
    if packet_limit is not None and packet_limit < 1:
        raise ValueError("packet_limit must be >= 1")
    packets = flow.packets if packet_limit is None else flow.packets[:packet_limit]
    t = 0.0
    projected = []
    for index, dp in enumerate(packets):
        if index:
            t += float(dp.iat)
        packet = PacketRecord(t, "0.0.0.0", "0.0.0.0", None, None,
                              "REDACTED", dp.packet.packet_length, 0, None)
        projected.append(DirectedPacket(packet, dp.direction, dp.iat))
    return Flow(key=("REDACTED",), packets=projected)


def run_experiment(n_per_class: int = 120, seed: int = 7, *,
                   protocol: str = "practical-budget", packet_limit: int = 8,
                   items=None, groups=None) -> list[ExperimentResult]:
    """Compare practical default caps or a common first-k packet observation window.

    Matched mode shares an identical first-k input packet set across vectorizers.
    Some representations impose further internal caps (e.g., first four bursts),
    so effective retained information can still differ and is reported.
    """
    if protocol not in ("practical-budget", "matched-horizon"):
        raise ValueError(f"unknown experiment protocol: {protocol}")
    if protocol == "matched-horizon" and packet_limit < 1:
        raise ValueError("packet_limit must be >= 1")
    assert_registry_contract(VECTORIZERS)
    external_items = items is not None
    if items is None:
        if groups is not None:
            raise ValueError("groups require explicit items")
        items = make_dataset(n_per_class=n_per_class, seed=seed)
    if len(items) < 2:
        raise ValueError("at least two labeled samples are required")
    indices = np.arange(len(items))
    y_all = np.asarray([x.label for x in items])
    if groups is None:
        if external_items:
            raise ValueError("externally supplied items require groups to prevent leakage")
        train_idx, test_idx = train_test_split(
            indices, test_size=0.30, random_state=seed, stratify=y_all
        )
    else:
        train_idx, test_idx = group_holdout_indices(y_all, groups, seed=seed)
    train = [items[i] for i in train_idx]
    test = [items[i] for i in test_idx]

    limit = packet_limit if protocol == "matched-horizon" else None
    observed = [_observed_flow(x.flow, limit) for x in items]
    retention = [retention_audit(f) for f in observed]
    original_lengths = [len(x.flow.packets) for x in items]
    observed_by_id = {id(item): flow for item, flow in zip(items, observed)}
    results = []
    for name, vectorizer in VECTORIZERS.items():
        if protocol == "matched-horizon":
            # All packet and burst caps are at least k. Padding shape is fixed.
            if name == "packet-sequence":
                vectorizer = lambda f, k=packet_limit: vectorize_packet_sequence(f, max_packets=k)
            elif name == "burst-sequence":
                vectorizer = lambda f, k=packet_limit: vectorize_burst_sequence(f, max_bursts=k)
            elif name == "hierarchy":
                vectorizer = lambda f, k=packet_limit: vectorize_hierarchy(f, max_bursts=k, max_packets_per_burst=k)
        if protocol == "matched-horizon":
            retained_fraction = float(np.mean([min(packet_limit, n) / max(1, n) for n in original_lengths]))
        else:
            retained_fraction = float(np.mean([r[name]["retained_packets"] / max(1, n) for r, n in zip(retention, original_lengths)]))
        Xtr, ytr = _matrix([_WithFlow(x.label, observed_by_id[id(x)]) for x in train], vectorizer)
        Xte, yte = _matrix([_WithFlow(x.label, observed_by_id[id(x)]) for x in test], vectorizer)
        for learner_name, factory in (("linear", make_linear), ("mlp", make_mlp)):
            metrics = fit_and_score(factory(seed), Xtr, ytr, Xte, yte)
            results.append(ExperimentResult(name, learner_name, Xtr.shape[1], metrics, retained_fraction, protocol, limit))
    return results


def run_capture_experiment(manifest_path, *, seed=7, protocol="practical-budget",
                           packet_limit=8, tshark_path="tshark", inactivity_timeout=30.0):
    """Instructor-only labeled PCAP evaluation; never derive labels from traffic."""
    from .manifest import read_capture_manifest, load_labeled_captures
    entries = read_capture_manifest(manifest_path)
    items, groups = load_labeled_captures(entries, tshark_path=tshark_path,
                                           inactivity_timeout=inactivity_timeout)
    return run_experiment(seed=seed, protocol=protocol, packet_limit=packet_limit,
                          items=items, groups=groups)

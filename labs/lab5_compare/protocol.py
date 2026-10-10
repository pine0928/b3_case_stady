"""Matched-information experiment protocol for Lab 5.

The core rule is intentionally strict: compared representations may differ in
how they *organize* the canonical observations, but they may not silently see
extra raw fields.  This module therefore treats the observable budget as part
of the experiment configuration rather than an informal comment.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import FrozenSet

CANONICAL_OBSERVABLES: FrozenSet[str] = frozenset({"direction", "packet_length", "iat"})

@dataclass(frozen=True)
class RepresentationConfig:
    name: str
    observables: FrozenSet[str] = CANONICAL_OBSERVABLES
    uses_burst_partition: bool = False
    uses_explicit_relations: bool = False
    note: str = ""
    horizon: str = "full-flow"


def observable_budget(config: RepresentationConfig) -> set[str]:
    return set(config.observables)


def assert_matched_budget(*configs: RepresentationConfig) -> None:
    """Raise if any representation sees a different raw observable set."""
    if len(configs) < 2:
        return
    expected = configs[0].observables
    mismatched = [c for c in configs[1:] if c.observables != expected]
    if mismatched:
        details = ", ".join(
            f"{c.name}={sorted(c.observables)}" for c in configs
        )
        raise ValueError(f"unmatched observable budgets: {details}")


# Names are exactly the executable vectorizer registry keys.
CANONICAL_CONFIGS = (
    RepresentationConfig("statistics"),
    RepresentationConfig("packet-sequence", horizon="first-8-packets"),
    RepresentationConfig("burst-sequence", uses_burst_partition=True, horizon="first-4-bursts"),
    RepresentationConfig("hierarchy", uses_burst_partition=True, horizon="first-4-bursts-first-2-packets-each"),
    RepresentationConfig("packet-chain-graph", uses_explicit_relations=True),
    RepresentationConfig("hierarchical-graph", uses_burst_partition=True, uses_explicit_relations=True),
    RepresentationConfig("packet-chain-graph-no-relations"),
    RepresentationConfig("hierarchical-graph-no-relations", uses_burst_partition=True),
)


def assert_registry_contract(registry: dict, configs=CANONICAL_CONFIGS) -> None:
    names = [c.name for c in configs]
    if len(names) != len(set(names)) or set(names) != set(registry):
        raise ValueError(f"representation registry mismatch: declared={names}, executed={list(registry)}")
    assert_matched_budget(*configs)
    if any(c.observables != CANONICAL_OBSERVABLES for c in configs):
        raise ValueError("vectorizer raw-observable contract differs from canonical packet fields")


def retention_audit(flow) -> dict[str, dict[str, int]]:
    """Explicit effective observation counts for current default vectorizer settings.

    Counts are not an assertion of equal horizon; unequal horizons are intentional
    metadata that must accompany interpretation of experiment results.
    """
    from labs.common.preprocess import direction_only_bursts
    n = len(flow.packets)
    bursts = direction_only_bursts(flow)
    full = {"total_packets": n, "retained_packets": n}
    first8 = {"total_packets": n, "retained_packets": min(n, 8)}
    burst4 = {"total_packets": n, "retained_packets": sum(len(b.packets) for b in bursts[:4])}
    hierarchy = {"total_packets": n, "retained_packets": sum(min(len(b.packets), 2) for b in bursts[:4])}
    return {
        "statistics": dict(full), "packet-sequence": first8,
        "burst-sequence": burst4, "hierarchy": hierarchy,
        "packet-chain-graph": dict(full), "hierarchical-graph": dict(full),
        "packet-chain-graph-no-relations": dict(full),
        "hierarchical-graph-no-relations": dict(full),
    }

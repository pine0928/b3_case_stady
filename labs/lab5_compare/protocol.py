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


CANONICAL_CONFIGS = (
    RepresentationConfig("statistical-vector"),
    RepresentationConfig("packet-sequence"),
    RepresentationConfig("burst-sequence", uses_burst_partition=True),
    RepresentationConfig("packet-burst-hierarchy", uses_burst_partition=True),
    RepresentationConfig("packet-chain-graph", uses_explicit_relations=True),
    RepresentationConfig(
        "packet-burst-hierarchical-graph",
        uses_burst_partition=True,
        uses_explicit_relations=True,
    ),
)

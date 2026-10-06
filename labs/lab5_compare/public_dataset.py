"""Student-safe synthetic fixture for Lab 5.

This file exposes the controlled relational task without importing hidden
reference preprocessors or graph/non-graph solutions.  It is a teaching
fixture, not a benchmark dataset.
"""
from __future__ import annotations
import random
from dataclasses import dataclass
from labs.common.schema import DirectedPacket, Flow, PacketRecord

BASE_LENGTHS = (60, 80, 100, 120, 140, 160, 620, 700)
DIRECTIONS = (+1, +1, -1, -1, +1, +1, -1, -1)
TIMES = (0.00, 0.02, 0.05, 0.08, 0.12, 0.15, 0.19, 0.23)

@dataclass(frozen=True)
class LabeledFlow:
    flow: Flow
    label: int

def _valid_large_positions(label: int, rng: random.Random) -> tuple[int, int]:
    fw = [i for i, d in enumerate(DIRECTIONS) if d == +1]
    bw = [i for i, d in enumerate(DIRECTIONS) if d == -1]
    candidates = []
    for i in fw:
        for j in bw:
            if (abs(i - j) == 1) == bool(label):
                candidates.append((i, j))
    return rng.choice(candidates)

def make_labeled_flow(label: int, seed: int) -> LabeledFlow:
    if label not in (0, 1):
        raise ValueError("label must be 0 or 1")
    rng = random.Random(seed)
    hi_fw, hi_bw = _valid_large_positions(label, rng)
    low = list(BASE_LENGTHS[:-2]); rng.shuffle(low)
    lengths = [None] * 8
    lengths[hi_fw], lengths[hi_bw] = 620, 700
    for i in range(8):
        if lengths[i] is None:
            lengths[i] = low.pop()
    jitter = rng.choice((-4, -2, 0, 2, 4))
    lengths = [max(40, int(x + jitter)) for x in lengths]
    packets = []
    prev = None
    for ts, direction, length in zip(TIMES, DIRECTIONS, lengths):
        if direction == +1:
            src, dst, sport, dport = "10.0.0.1", "10.0.0.2", 50000, 443
        else:
            src, dst, sport, dport = "10.0.0.2", "10.0.0.1", 443, 50000
        record = PacketRecord(ts, src, dst, sport, dport, "TCP", length, max(0, length - 40), 0x18)
        iat = 0.0 if prev is None else ts - prev
        packets.append(DirectedPacket(record, direction, iat)); prev = ts
    return LabeledFlow(Flow(("TCP", ("10.0.0.1", 50000), ("10.0.0.2", 443)), packets), label)

def make_dataset(n_per_class: int = 120, seed: int = 7) -> list[LabeledFlow]:
    if n_per_class <= 0:
        raise ValueError("n_per_class must be positive")
    items = [make_labeled_flow(label, seed * 100000 + label * 10000 + i)
             for label in (0, 1) for i in range(n_per_class)]
    random.Random(seed).shuffle(items)
    return items

"""Deterministic synthetic dataset for matched-information experiments.

Every sample contains exactly eight packets.  Class labels are determined by a
*local relation*: whether one large FW packet and one large BW packet are
chronological neighbours.  Positive and negative samples use the same length
multiset, direction counts, packet count, and timestamp grid.  Thus coarse
statistics cannot solve the task reliably merely from total volume or class-
specific size distributions.

The fixture is not a benchmark dataset.  It is a controlled microscope for
understanding information/representation/model confounding before real PCAP
experiments are attempted.
"""
from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Iterable

from labs.common.schema import DirectedPacket, Flow, PacketRecord
from labs.common.preprocess import direction_only_bursts

BASE_LENGTHS = (60, 80, 100, 120, 140, 160, 620, 700)
DIRECTIONS = (+1, +1, -1, -1, +1, +1, -1, -1)
TIMES = (0.00, 0.02, 0.05, 0.08, 0.12, 0.15, 0.19, 0.23)

@dataclass(frozen=True)
class LabeledFlow:
    flow: Flow
    label: int


def _valid_large_positions(label: int, rng: random.Random) -> tuple[int, int]:
    fw_positions = [i for i, d in enumerate(DIRECTIONS) if d == +1]
    bw_positions = [i for i, d in enumerate(DIRECTIONS) if d == -1]
    candidates = []
    for i in fw_positions:
        for j in bw_positions:
            adjacent = abs(i - j) == 1
            if adjacent == bool(label):
                candidates.append((i, j))
    return rng.choice(candidates)


def make_labeled_flow(label: int, seed: int) -> LabeledFlow:
    if label not in (0, 1):
        raise ValueError("label must be 0 or 1")
    rng = random.Random(seed)
    hi_fw_pos, hi_bw_pos = _valid_large_positions(label, rng)

    low = list(BASE_LENGTHS[:-2])
    rng.shuffle(low)
    lengths = [None] * 8
    lengths[hi_fw_pos] = 620
    lengths[hi_bw_pos] = 700
    for i in range(8):
        if lengths[i] is None:
            lengths[i] = low.pop()

    # Add a tiny class-independent global offset to avoid exact duplicate rows
    # while preserving the relational nature of the label.
    jitter = rng.choice((-4, -2, 0, 2, 4))
    lengths = [max(40, int(x + jitter)) for x in lengths]

    packets: list[DirectedPacket] = []
    prev = None
    for i, (ts, direction, length) in enumerate(zip(TIMES, DIRECTIONS, lengths)):
        if direction == +1:
            src, dst, sport, dport = "10.0.0.1", "10.0.0.2", 50000, 443
        else:
            src, dst, sport, dport = "10.0.0.2", "10.0.0.1", 443, 50000
        record = PacketRecord(
            timestamp=ts,
            src_ip=src,
            dst_ip=dst,
            src_port=sport,
            dst_port=dport,
            protocol="TCP",
            packet_length=length,
            payload_length=max(0, length - 40),
            tcp_flags=0x18,
        )
        iat = 0.0 if prev is None else ts - prev
        packets.append(DirectedPacket(record, direction, iat))
        prev = ts
    flow = Flow(key=("TCP", ("10.0.0.1", 50000), ("10.0.0.2", 443)), packets=packets)
    return LabeledFlow(flow=flow, label=label)


def make_dataset(n_per_class: int = 120, seed: int = 7) -> list[LabeledFlow]:
    if n_per_class <= 0:
        raise ValueError("n_per_class must be positive")
    items = []
    for label in (0, 1):
        for i in range(n_per_class):
            items.append(make_labeled_flow(label, seed * 100000 + label * 10000 + i))
    rng = random.Random(seed)
    rng.shuffle(items)
    return items


def relation_truth(flow: Flow) -> bool:
    """Ground-truth local relation used by the fixture generator."""
    for a, b in zip(flow.packets, flow.packets[1:]):
        if a.direction != b.direction and a.packet.packet_length >= 600 and b.packet.packet_length >= 600:
            return True
        if a.direction != b.direction and b.packet.packet_length >= 600 and a.packet.packet_length >= 600:
            return True
    return False


def bursts_for(sample: LabeledFlow):
    return direction_only_bursts(sample.flow)

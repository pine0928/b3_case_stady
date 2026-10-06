"""Canonical reference preprocessing for Labs 0-2.

Students receive starter versions with TODO regions. These reference functions
exist for tests, instructor demos, and reproducible expected outputs.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .schema import PacketRecord, DirectedPacket, Flow, Burst


def inter_arrival_times(records: Iterable[PacketRecord]) -> list[float]:
    ordered = sorted(records, key=lambda p: p.timestamp)
    if not ordered:
        return []
    out = [0.0]
    out.extend(max(0.0, b.timestamp - a.timestamp) for a, b in zip(ordered, ordered[1:]))
    return out


def endpoint(packet: PacketRecord, source: bool) -> tuple:
    if source:
        return (packet.src_ip, packet.src_port)
    return (packet.dst_ip, packet.dst_port)


def canonical_flow_key(packet: PacketRecord) -> tuple:
    """Canonical bidirectional key, independent of first observed direction."""
    a = endpoint(packet, True)
    b = endpoint(packet, False)
    lo, hi = sorted((a, b), key=lambda x: (x[0], -1 if x[1] is None else x[1]))
    return (packet.protocol, lo, hi)


def _flow_forward_endpoint(records: list[PacketRecord]) -> tuple:
    """Baseline FW convention: source endpoint of earliest packet in the flow."""
    first = min(records, key=lambda p: p.timestamp)
    return endpoint(first, True)


def build_flows(records: Iterable[PacketRecord]) -> list[Flow]:
    groups: dict[tuple, list[PacketRecord]] = defaultdict(list)
    for record in records:
        groups[canonical_flow_key(record)].append(record)

    flows: list[Flow] = []
    for key in sorted(groups, key=repr):
        ordered = sorted(groups[key], key=lambda p: p.timestamp)
        forward = _flow_forward_endpoint(ordered)
        directed: list[DirectedPacket] = []
        prev_ts = None
        for p in ordered:
            direction = +1 if endpoint(p, True) == forward else -1
            iat = 0.0 if prev_ts is None else max(0.0, p.timestamp - prev_ts)
            directed.append(DirectedPacket(packet=p, direction=direction, iat=iat))
            prev_ts = p.timestamp
        flows.append(Flow(key=key, packets=directed))
    return flows


def direction_only_bursts(flow: Flow) -> list[Burst]:
    bursts: list[Burst] = []
    for dp in flow.packets:
        if not bursts or bursts[-1].direction != dp.direction:
            bursts.append(Burst(direction=dp.direction, packets=[]))
        bursts[-1].packets.append(dp)
    return bursts


def iat_aware_bursts(flow: Flow, max_gap: float) -> list[Burst]:
    """Alternative: split on direction change OR a within-direction IAT gap."""
    if max_gap < 0:
        raise ValueError("max_gap must be non-negative")
    bursts: list[Burst] = []
    for dp in flow.packets:
        split = (
            not bursts
            or bursts[-1].direction != dp.direction
            or (bursts[-1].packets and dp.iat > max_gap)
        )
        if split:
            bursts.append(Burst(direction=dp.direction, packets=[]))
        bursts[-1].packets.append(dp)
    return bursts


def summarize_bursts(bursts: Iterable[Burst]) -> list[dict]:
    rows = []
    for idx, burst in enumerate(bursts):
        packets = burst.packets
        if not packets:
            continue
        start = packets[0].packet.timestamp
        end = packets[-1].packet.timestamp
        rows.append(
            {
                "burst_index": idx,
                "direction": burst.direction,
                "packets": len(packets),
                "bytes": sum(p.packet.packet_length for p in packets),
                "payload_bytes": sum(p.packet.payload_length for p in packets),
                "duration": max(0.0, end - start),
            }
        )
    return rows

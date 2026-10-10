"""Canonical reference preprocessing for Labs 0-2.

Students receive starter versions with TODO regions. These reference functions
exist for tests, instructor demos, and reproducible expected outputs.
"""
from __future__ import annotations

import ipaddress
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


def _endpoint_sort_key(ep: tuple) -> tuple:
    ip, port = ep
    address = ipaddress.ip_address(ip)
    return (address.version, int(address), -1 if port is None else port)


def canonical_flow_key(packet: PacketRecord) -> tuple:
    """Canonical bidirectional 5-tuple; compare numeric IP addresses."""
    a, b = endpoint(packet, True), endpoint(packet, False)
    lo, hi = sorted((a, b), key=_endpoint_sort_key)
    return (packet.protocol, lo, hi)


def build_flows(records: Iterable[PacketRecord], inactivity_timeout: float = 30.0) -> list[Flow]:
    """Materialize canonical Lab-1 idle-timeout flow occurrences.

    Capture order is authoritative; timestamps must be nondecreasing.
    For TCP FIN/RST-aware termination use flow_stream.iter_completed_flows.
    """
    from .flow_baseline import iter_idle_flows
    return list(iter_idle_flows(records, inactivity_timeout))



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

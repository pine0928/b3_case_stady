"""Canonical five-dimensional burst feature row for Lab 3 and Lab 4."""
from __future__ import annotations
from labs.common.schema import Burst

def burst_feature_row(burst: Burst, previous_end: float | None) -> tuple[float, ...]:
    packets = burst.packets
    if not packets:
        return (float(burst.direction), 0.0, 0.0, 0.0, 0.0)
    start = packets[0].packet.timestamp
    end = packets[-1].packet.timestamp
    gap = 0.0 if previous_end is None else max(0.0, start - previous_end)
    return (
        float(burst.direction),
        float(len(packets)),
        float(sum(dp.packet.packet_length for dp in packets)),
        float(max(0.0, end - start)),
        float(gap),
    )


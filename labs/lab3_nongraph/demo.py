"""Instructor demo for the canonical Lab 3 representations."""
from __future__ import annotations

from labs.common.fixtures import tiny_packet_records
from labs.common.preprocess import build_flows, direction_only_bursts
from labs.lab3_nongraph.starter import (
    burst_sequence,
    hierarchical_representation,
    packet_sequence,
    pad_hierarchy,
    statistical_vector,
)


def main() -> None:
    flow = next(f for f in build_flows(tiny_packet_records()) if f.key[0] == "TCP")
    bursts = direction_only_bursts(flow)

    stats = statistical_vector(flow)
    packets = packet_sequence(flow, max_packets=6)
    burst_seq = burst_sequence(bursts, max_bursts=4)
    hierarchy = hierarchical_representation(flow, bursts)
    padded = pad_hierarchy(hierarchy, max_bursts=4, max_packets_per_burst=2)

    print("STATISTICAL VECTOR")
    for name, value in zip(stats.feature_names, stats.values):
        print(f"  {name:24s} {value:.6g}")

    print("\nPACKET SEQUENCE")
    print("  features:", packets.feature_names)
    print("  mask:", packets.mask, "truncated:", packets.truncated)
    for row in packets.values:
        print(" ", row)

    print("\nBURST SEQUENCE")
    print("  features:", burst_seq.feature_names)
    print("  mask:", burst_seq.mask, "truncated:", burst_seq.truncated)
    for row in burst_seq.values:
        print(" ", row)

    print("\nHIERARCHY")
    print("  bursts:", len(hierarchy.bursts), "packets:", hierarchy.packet_count)
    for i, burst in enumerate(hierarchy.bursts):
        print(f"  B{i}: summary={burst.burst_features} packets={burst.packet_features}")
    print("  padded burst mask:", padded.burst_mask)
    print("  padded packet mask:", padded.packet_mask)
    print("  dropped packets:", padded.dropped_packets)


if __name__ == "__main__":
    main()

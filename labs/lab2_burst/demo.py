"""Instructor/reference demo for Lab 2."""
from pathlib import Path
from labs.common.tshark import load_tshark_packet_records
from labs.common.preprocess import build_flows, direction_only_bursts, iat_aware_bursts, summarize_bursts


def main(path: str | None = None, max_gap: float = 0.10) -> None:
    pcap = Path(path) if path else Path(__file__).parents[1] / "data" / "canonical_smoke.pcap"
    flows = build_flows(load_tshark_packet_records(pcap))
    print(f"capture={pcap} flows={len(flows)}")
    for fi, flow in enumerate(flows):
        base = direction_only_bursts(flow)
        alt = iat_aware_bursts(flow, max_gap=max_gap)
        print(f"\nflow[{fi}] key={flow.key}")
        print("direction-only:")
        for row in summarize_bursts(base):
            print(" ", row)
        print(f"iat-aware(max_gap={max_gap}):")
        for row in summarize_bursts(alt):
            print(" ", row)


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)

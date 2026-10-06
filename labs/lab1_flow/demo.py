"""Instructor/reference demo for Lab 1."""
from pathlib import Path
from labs.common.tshark import load_tshark_packet_records
from labs.common.preprocess import build_flows


def main(path: str | None = None, timeout: float = 30.0) -> None:
    pcap = Path(path) if path else Path(__file__).parents[1] / "data" / "canonical_smoke.pcap"
    records = load_tshark_packet_records(pcap)
    flows = build_flows(records)
    print(f"capture={pcap}")
    print(f"flows={len(flows)}")
    for idx, flow in enumerate(flows):
        pattern = " ".join("FW" if p.direction > 0 else "BW" for p in flow.packets)
        print(f"flow[{idx}] key={flow.key} packets={len(flow.packets)} pattern={pattern}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)

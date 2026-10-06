"""Instructor/reference demo for Lab 0 using the course-standard TShark path."""
from pathlib import Path
from labs.common.tshark import load_tshark_packet_records
from labs.common.preprocess import inter_arrival_times


def main(path: str | None = None) -> None:
    pcap = Path(path) if path else Path(__file__).parents[1] / "data" / "canonical_smoke.pcap"
    records = load_tshark_packet_records(pcap)
    iats = inter_arrival_times(records)
    print(f"capture={pcap}")
    print(f"supported_packets={len(records)}")
    for idx, (record, iat) in enumerate(zip(records[:8], iats[:8])):
        print(idx, record, f"IAT={iat:.6f}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)

"""Compare educational and TShark ingestion on the same capture."""
from __future__ import annotations

import argparse
from pathlib import Path

from labs.common.pcap import load_packet_records
from labs.common.tshark import load_tshark_packet_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pcap",
        nargs="?",
        default=str(Path(__file__).parents[1] / "data" / "canonical_smoke.pcap"),
    )
    args = parser.parse_args()

    educational = load_packet_records(args.pcap)
    scalable = load_tshark_packet_records(args.pcap)
    if educational != scalable:
        print("FAIL: ingestion paths produced different PacketRecord sequences")
        for i, (a, b) in enumerate(zip(educational, scalable)):
            if a != b:
                print(f"first mismatch at record {i}:\n  educational={a}\n  tshark={b}")
                break
        if len(educational) != len(scalable):
            print(f"record counts: educational={len(educational)} tshark={len(scalable)}")
        return 1

    print(f"PASS: {len(educational)} PacketRecords are identical")
    print("educational: labs.common.pcap")
    print("scalable:    labs.common.tshark (streaming TShark)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

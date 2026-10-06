"""Smoke-test an instructor/user supplied real capture through Lab 0-2.

This script does not claim semantic correctness for arbitrary captures; it
checks that the baseline parser and aggregation path execute reproducibly.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from labs.common.pcap import load_packet_records
from labs.common.preprocess import build_flows, direction_only_bursts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('pcap', type=Path)
    args = parser.parse_args()

    raw = args.pcap.read_bytes()
    records = load_packet_records(args.pcap)
    flows = build_flows(records)
    burst_count = sum(len(direction_only_bursts(f)) for f in flows)

    print(f'capture={args.pcap}')
    print(f'sha256={hashlib.sha256(raw).hexdigest()}')
    print(f'supported_packets={len(records)}')
    print(f'flows={len(flows)}')
    print(f'direction_only_bursts={burst_count}')
    print('protocols=' + ','.join(sorted({r.protocol for r in records})))


if __name__ == '__main__':
    main()

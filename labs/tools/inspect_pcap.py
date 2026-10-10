"""Show the canonical raw TShark TSV fields without solving Lab 0 parsing.

Run from the repository root: python -m labs.tools.inspect_pcap CAPTURE.pcap
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess

from labs.common.field_spec import FieldSpec
from labs.common.tshark import DEFAULT_FIELD_SPEC


def build_command(capture: Path, executable: str, spec: FieldSpec) -> list[str]:
    command = [executable, "-n", "-r", str(capture), "-Y", spec.display_filter, "-T", "fields"]
    for field in spec.tshark_fields:
        command.extend(["-e", field])
    command.extend(["-E", "separator=\t", "-E", "quote=n", "-E", "occurrence=f"])
    return command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path, help="PCAP or PCAPNG input file")
    args = parser.parse_args(argv)
    if not args.capture.is_file():
        parser.error(f"Capture file not found: {args.capture}")
    executable = shutil.which("tshark")
    if executable is None:
        parser.error("TShark not found on PATH; install Wireshark/TShark first")
    spec = FieldSpec.from_yaml(DEFAULT_FIELD_SPEC)
    print("\t".join(spec.tshark_fields), flush=True)
    return subprocess.call(build_command(args.capture, executable, spec))


if __name__ == "__main__":
    raise SystemExit(main())

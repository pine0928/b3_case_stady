"""Streaming TShark ingestion for the B3 labs.

TShark owns protocol dissection; this module owns the stable PacketRecord
contract.  Field selection is declarative and lives in packet_fields.yaml.
"""
from __future__ import annotations
from pathlib import Path
import shutil
import subprocess
from typing import Iterator

from .field_spec import FieldSpec
from .schema import PacketRecord

DEFAULT_FIELD_SPEC = Path(__file__).with_name("packet_fields.yaml")


def _optional_int(value: str) -> int | None:
    value = value.strip()
    return None if not value else int(value, 0)


def parse_tshark_row(line: str, spec: FieldSpec) -> PacketRecord:
    cols = line.rstrip("\r\n").split("\t")
    if len(cols) != len(spec.fields):
        raise ValueError(f"Expected {len(spec.fields)} TShark fields, got {len(cols)}: {line!r}")
    row = {field.attribute: value for field, value in zip(spec.fields, cols)}
    captured = int(row["captured_frame_length"])
    original = int(row["original_frame_length"])
    if captured < original:
        raise ValueError("snaplen-truncated frame is outside the baseline")
    proto = int(row["protocol"])
    if proto == 6:
        protocol, src_port, dst_port = "TCP", _optional_int(row["tcp_src_port"]), _optional_int(row["tcp_dst_port"])
        payload_length = int(row["tcp_payload_length"] or "0")
        tcp_flags = _optional_int(row["tcp_flags"])
    elif proto == 17:
        protocol, src_port, dst_port = "UDP", _optional_int(row["udp_src_port"]), _optional_int(row["udp_dst_port"])
        udp_length = int(row["udp_length"] or "8")
        payload_length = max(0, udp_length - 8)
        tcp_flags = None
    else:
        raise ValueError(f"Unexpected IP protocol: {proto}")
    return PacketRecord(
        timestamp=float(row["timestamp"]), src_ip=row["src_ip"], dst_ip=row["dst_ip"],
        src_port=src_port, dst_port=dst_port, protocol=protocol,
        packet_length=int(row["ip_length"]), payload_length=payload_length, tcp_flags=tcp_flags,
    )


def iter_tshark_packet_records(path: str | Path, *, spec: FieldSpec | None = None, tshark_path: str = "tshark") -> Iterator[PacketRecord]:
    spec = spec or FieldSpec.from_yaml(DEFAULT_FIELD_SPEC)
    capture = Path(path)
    executable = shutil.which(tshark_path) if Path(tshark_path).name == tshark_path else tshark_path
    if not executable or not Path(executable).exists():
        raise RuntimeError("TShark was not found. Install Wireshark/TShark or pass tshark_path.")
    command = [executable, "-n", "-r", str(capture), "-Y", spec.display_filter, "-T", "fields"]
    for field in spec.tshark_fields:
        command.extend(["-e", field])
    command.extend(["-E", "separator=\t", "-E", "quote=n", "-E", "occurrence=f"])
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    assert proc.stdout is not None
    try:
        for line in proc.stdout:
            if line.strip():
                yield parse_tshark_row(line, spec)
    finally:
        proc.stdout.close()
    stderr = proc.stderr.read() if proc.stderr is not None else ""
    returncode = proc.wait()
    if proc.stderr is not None:
        proc.stderr.close()
    if returncode != 0:
        raise RuntimeError(f"TShark failed with exit code {returncode}: {stderr.strip()}")


def _parse_tshark_row(line: str) -> PacketRecord:
    """Compatibility wrapper for the pre-YAML instructor tests."""
    return parse_tshark_row(line, FieldSpec.from_yaml(DEFAULT_FIELD_SPEC))

def load_tshark_packet_records(path: str | Path, *, tshark_path: str = "tshark") -> list[PacketRecord]:
    """Compatibility materializer; core pipelines should prefer the iterator."""
    return list(iter_tshark_packet_records(path, tshark_path=tshark_path))

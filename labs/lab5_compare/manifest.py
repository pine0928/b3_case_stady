"""Explicitly labeled capture manifest for instructor-only real-PCAP evaluation.

One row represents one capture and one ground-truth label. Mixed-label captures
must be segmented and labeled externally before they can enter this baseline.
"""
from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from labs.common.tshark import iter_tshark_packet_records
from labs.common.preprocess import build_flows
from .dataset import LabeledFlow

REQUIRED_COLUMNS = ("capture_path", "label", "group_id", "provenance")

@dataclass(frozen=True)
class CaptureEntry:
    capture_path: Path
    label: int
    group_id: str
    provenance: str


def read_capture_manifest(path: str | Path) -> list[CaptureEntry]:
    manifest = Path(path).resolve()
    with manifest.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or any(key not in reader.fieldnames for key in REQUIRED_COLUMNS):
            raise ValueError(f"manifest requires columns: {REQUIRED_COLUMNS}")
        entries = []
        for line, row in enumerate(reader, start=2):
            if any(not (row.get(key) or "").strip() for key in REQUIRED_COLUMNS):
                raise ValueError(f"manifest line {line}: missing required value")
            try:
                label = int(row["label"])
            except ValueError as exc:
                raise ValueError(f"manifest line {line}: label must be an integer") from exc
            capture = (manifest.parent / row["capture_path"]).resolve()
            if not capture.is_file():
                raise FileNotFoundError(f"manifest line {line}: {capture}")
            entries.append(CaptureEntry(capture, label, row["group_id"].strip(), row["provenance"].strip()))
    if not entries:
        raise ValueError("manifest is empty")
    return entries


def load_labeled_captures(entries: list[CaptureEntry], *, tshark_path: str = "tshark", inactivity_timeout: float = 30.0):
    """Return (labeled flows, capture/group IDs), preserving capture boundaries."""
    items, groups = [], []
    for entry in entries:
        records = iter_tshark_packet_records(entry.capture_path, tshark_path=tshark_path)
        flows = build_flows(records, inactivity_timeout=inactivity_timeout)
        for flow in flows:
            if flow.packets:
                items.append(LabeledFlow(flow=flow, label=entry.label))
                groups.append(entry.group_id)
    if not items:
        raise ValueError("no usable flows in labeled captures")
    return items, groups

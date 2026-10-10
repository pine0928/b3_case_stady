"""Lab 0 starter: TShark fields -> PacketRecord.

The PCAP dissection is delegated to TShark.  Your job is to understand the
selected protocol fields and map one tab-separated TShark row into the stable
PacketRecord contract used by later labs.
"""
from labs.common.schema import PacketRecord

# This order is the TSV contract.  Compare each name with the same field in
# Wireshark before implementing parse_tshark_row().
# Field names and ordering are declared once in the shared YAML FieldSpec.
# Students still implement the conversion from a TSV row to PacketRecord.
from labs.common.field_spec import FieldSpec
from labs.common.tshark import DEFAULT_FIELD_SPEC

TSHARK_FIELDS = FieldSpec.from_yaml(DEFAULT_FIELD_SPEC).tshark_fields


def parse_tshark_row(line: str) -> PacketRecord:
    """TODO: convert one tab-separated TShark fields row to PacketRecord.

    Requirements are defined in SPECIFICATION.md.  In particular, decide from
    ip.proto whether TCP or UDP fields are meaningful; do not treat empty TCP
    columns in a UDP row (or vice versa) as zero-valued observations.
    """
    raise NotImplementedError


def inter_arrival_times(records: list[PacketRecord]) -> list[float]:
    """TODO: return non-negative IATs after timestamp ordering; first IAT = 0."""
    raise NotImplementedError

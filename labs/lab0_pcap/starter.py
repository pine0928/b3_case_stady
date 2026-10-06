"""Lab 0 starter: TShark fields -> PacketRecord.

The PCAP dissection is delegated to TShark.  Your job is to understand the
selected protocol fields and map one tab-separated TShark row into the stable
PacketRecord contract used by later labs.
"""
from labs.common.schema import PacketRecord

# This order is the TSV contract.  Compare each name with the same field in
# Wireshark before implementing parse_tshark_row().
TSHARK_FIELDS = (
    "frame.time_epoch",
    "ip.src", "ip.dst", "ip.proto", "ip.len",
    "tcp.srcport", "tcp.dstport", "tcp.len", "tcp.flags",
    "udp.srcport", "udp.dstport", "udp.length",
    "frame.cap_len", "frame.len",
)


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

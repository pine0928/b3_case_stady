"""Lab 0 student implementation tests; intentionally RED for untouched starter."""
import pytest
from labs.lab0_pcap.starter import TSHARK_FIELDS, parse_tshark_row, inter_arrival_times
from labs.common.schema import PacketRecord


def row(**values):
    fields = {
        "frame.time_epoch": "1.25", "ip.src": "192.0.2.1",
        "ip.dst": "198.51.100.2", "ip.proto": "6", "ip.len": "60",
        "tcp.srcport": "12345", "tcp.dstport": "443", "tcp.len": "20",
        "tcp.flags": "0x0018", "udp.srcport": "", "udp.dstport": "",
        "udp.length": "", "frame.cap_len": "74", "frame.len": "74",
    }
    fields.update(values)
    return "\t".join(fields[name] for name in TSHARK_FIELDS)


def test_tcp_row_mapping():
    p = parse_tshark_row(row())
    assert isinstance(p, PacketRecord)
    assert (p.timestamp, p.src_ip, p.dst_ip) == (1.25, "192.0.2.1", "198.51.100.2")
    assert (p.protocol, p.src_port, p.dst_port) == ("TCP", 12345, 443)
    assert (p.packet_length, p.payload_length, p.tcp_flags) == (60, 20, 0x18)


def test_udp_row_mapping_with_empty_tcp_columns():
    p = parse_tshark_row(row(**{
        "ip.proto": "17", "tcp.srcport": "", "tcp.dstport": "",
        "tcp.len": "", "tcp.flags": "", "udp.srcport": "53",
        "udp.dstport": "50000", "udp.length": "18",
    }))
    assert (p.protocol, p.src_port, p.dst_port) == ("UDP", 53, 50000)
    assert (p.payload_length, p.tcp_flags) == (10, None)


@pytest.mark.parametrize("bad", [
    "too\tfew", row(**{"ip.proto": "1"}),
    row(**{"frame.cap_len": "60", "frame.len": "74"}),
])
def test_reject_unsupported_rows(bad):
    with pytest.raises(ValueError):
        parse_tshark_row(bad)


def test_iat_sorted_and_empty():
    assert inter_arrival_times([]) == []
    records = [parse_tshark_row(row(**{"frame.time_epoch": str(t)})) for t in (1.05, 1.0, 1.02)]
    assert inter_arrival_times(records) == pytest.approx([0.0, 0.02, 0.03])

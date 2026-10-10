"""Lab 1 behavioral tests: intentionally RED for an untouched student starter."""
import pytest
from labs.common.schema import PacketRecord
from labs.lab1_flow import starter


def packet(t, src="10.0.0.1", dst="10.0.0.2", sport=50000, dport=443, proto="TCP"):
    return PacketRecord(timestamp=t, src_ip=src, dst_ip=dst, src_port=sport,
                        dst_port=dport, protocol=proto, packet_length=60, payload_length=0)


def signature(flows):
    return [(f.key, [(dp.packet.timestamp, dp.direction, dp.iat) for dp in f.packets]) for f in flows]


def trace():
    return [packet(1.0), packet(1.02), packet(1.05, "10.0.0.2", "10.0.0.1", 443, 50000),
            packet(1.07, "10.0.0.2", "10.0.0.1", 443, 50000), packet(1.5)]


def test_bidirectional_key_numeric_ip_and_protocol():
    a = packet(0, "10.0.0.2", "10.0.0.10", 80, 50000)
    b = packet(1, "10.0.0.10", "10.0.0.2", 50000, 80)
    assert starter.canonical_flow_key(a) == starter.canonical_flow_key(b)
    assert starter.canonical_flow_key(a) != starter.canonical_flow_key(packet(0, "10.0.0.2", "10.0.0.10", 80, 50000, "UDP"))
    assert starter.canonical_flow_key(a) == ("TCP", ("10.0.0.2", 80), ("10.0.0.10", 50000))


def test_flow_split_direction_iat_and_restart():
    flows = starter.build_flows(trace(), 0.1)
    assert len(flows) == 2
    assert [len(f.packets) for f in flows] == [4, 1]
    assert [p.direction for p in flows[0].packets] == [1, 1, -1, -1]
    assert [p.iat for p in flows[0].packets] == pytest.approx([0, 0.02, 0.03, 0.02])
    assert flows[1].packets[0].direction == 1
    assert flows[1].packets[0].iat == 0


def test_timeout_strict_boundary_and_empty():
    assert starter.build_flows([], 1.0) == []
    assert len(starter.build_flows([packet(1), packet(2)], 1.0)) == 1
    assert len(starter.build_flows([packet(1), packet(2.001)], 1.0)) == 2


@pytest.mark.parametrize("timeout", [0, -1])
def test_invalid_timeout(timeout):
    with pytest.raises(ValueError):
        starter.build_flows([], timeout)
    with pytest.raises(ValueError):
        list(starter.iter_flows(iter(()), timeout))


def test_streaming_equivalence_and_one_shot_input():
    expected = signature(starter.build_flows(trace(), 0.1))
    assert signature(starter.iter_flows(iter(trace()), 0.1)) == expected


def test_streaming_yields_before_eof():
    consumed = []
    def source():
        for p in [packet(1), packet(3), packet(4)]:
            consumed.append(p.timestamp)
            yield p
    gen = starter.iter_flows(source(), 1.0)
    first = next(gen)
    assert [p.packet.timestamp for p in first.packets] == [1]
    assert consumed == [1, 3], "The first completed Flow must be yielded before reading the entire input"
    assert len(list(gen)) == 1


def test_multiple_keys_and_out_of_order_rejected():
    a = packet(1)
    b = packet(2, "192.0.2.1", "192.0.2.2", 53, 53, "UDP")
    flows = starter.build_flows([a, b], 10)
    assert len(flows) == 2
    with pytest.raises(ValueError):
        starter.build_flows([packet(2), packet(1)], 10)
    with pytest.raises(ValueError):
        list(starter.iter_flows(iter([packet(2), packet(1)]), 10))

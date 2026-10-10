"""Lab 2: API checks pass before implementation; semantic checks require student work."""
from labs.common.schema import DirectedPacket, Flow, PacketRecord
from labs.lab2_burst import starter


def _flow(directions=(1, 1, -1, -1, 1), iats=(0.0, 0.02, 0.03, 0.02, 0.43)):
    packets = []
    for i, (direction, iat) in enumerate(zip(directions, iats)):
        record = PacketRecord(timestamp=float(i), src_ip="10.0.0.1", dst_ip="10.0.0.2",
                              src_port=1000, dst_port=80, protocol="TCP",
                              packet_length=100, payload_length=60)
        packets.append(DirectedPacket(packet=record, direction=direction, iat=iat))
    return Flow(key=("TCP",), packets=packets)


def _assert_partition(flow, bursts):
    assert isinstance(bursts, list)
    assert all(b.packets and b.direction in (-1, 1) for b in bursts)
    assert all(all(p.direction == b.direction for p in b.packets) for b in bursts)
    assert [id(p) for b in bursts for p in b.packets] == [id(p) for p in flow.packets]


def test_lab2_api_is_present():
    assert callable(starter.direction_only_bursts)
    assert callable(starter.alternative_bursts)


def test_direction_only_empty():
    assert starter.direction_only_bursts(_flow((), ())) == []


def test_direction_only_single_packet():
    flow = _flow((1,), (0.0,))
    bursts = starter.direction_only_bursts(flow)
    _assert_partition(flow, bursts)
    assert [len(b.packets) for b in bursts] == [1]


def test_direction_only_maximal_runs():
    flow = _flow()
    bursts = starter.direction_only_bursts(flow)
    _assert_partition(flow, bursts)
    assert [b.direction for b in bursts] == [1, -1, 1]
    assert [len(b.packets) for b in bursts] == [2, 2, 1]


def test_direction_only_does_not_split_long_gap():
    flow = _flow((1, 1, 1), (0.0, 0.01, 99.0))
    bursts = starter.direction_only_bursts(flow)
    _assert_partition(flow, bursts)
    assert [len(b.packets) for b in bursts] == [3]


def test_alternative_preserves_order_and_membership():
    # Students may choose IAT, ACK/payload, or another documented alternative.
    # max_gap is a suggested parameter, NOT a mandated segmentation rule.
    flow = _flow()
    bursts = starter.alternative_bursts(flow, max_gap=0.01)
    _assert_partition(flow, bursts)

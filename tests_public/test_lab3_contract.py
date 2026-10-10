"""Lab 3 public tests: API discovery vs assessed representation behavior."""
import pytest
from labs.common.fixtures import tiny_packet_records
from labs.common.schema import DirectedPacket, Flow, Burst
from labs.lab3_nongraph import starter
from labs.common.representations import StatisticalVector, PaddedSequence, HierarchicalRepresentation, PaddedHierarchy


def _flow():
    packets = tiny_packet_records()[:5]
    iats = (0.0, 0.02, 0.03, 0.02, 0.43)
    directions = (1, 1, -1, -1, 1)
    return Flow(("TCP",), [DirectedPacket(p, d, i) for p,d,i in zip(packets,directions,iats)])


def direction_only_bursts(flow):
    groups=[]
    for packet in flow.packets:
        if not groups or groups[-1].direction != packet.direction:
            groups.append(Burst(packet.direction, []))
        groups[-1].packets.append(packet)
    return groups


def test_api_available():
    assert all(callable(getattr(starter, name)) for name in ("statistical_vector", "packet_sequence", "burst_sequence", "hierarchical_representation", "pad_hierarchy"))


def test_statistical_vector_values_and_order():
    rep = starter.statistical_vector(_flow())
    assert isinstance(rep, StatisticalVector)
    assert rep.feature_names == ("packet_count", "forward_packet_count", "backward_packet_count", "total_bytes", "forward_bytes", "backward_bytes", "mean_packet_length", "std_packet_length", "mean_iat", "std_iat", "flow_duration", "direction_switch_count")
    assert rep.values[:7] == pytest.approx((5,3,2,500,330,170,100))
    assert rep.values[7] == pytest.approx(14.1421356237)
    assert rep.values[8] == pytest.approx(0.1)
    assert rep.values[10:] == pytest.approx((0.5,2))


def test_packet_sequence_padding_and_truncation():
    padded = starter.packet_sequence(_flow(), 7)
    assert isinstance(padded, PaddedSequence)
    assert padded.feature_names == ("direction", "packet_length", "iat")
    assert padded.mask == (1,1,1,1,1,0,0)
    assert padded.values[0] == pytest.approx((1,100,0))
    assert padded.values[-1] == (0,0,0)
    assert (padded.original_length,padded.retained_length,padded.truncated) == (5,5,False)
    short = starter.packet_sequence(_flow(), 3)
    assert short.mask == (1,1,1)
    assert (short.original_length,short.retained_length,short.truncated) == (5,3,True)
    assert [row[0] for row in short.values] == [1,1,-1]


def test_burst_sequence_frozen_boundaries():
    rep = starter.burst_sequence(direction_only_bursts(_flow()), 4)
    assert isinstance(rep,PaddedSequence)
    assert rep.feature_names == ("direction", "packet_count", "byte_count", "duration", "gap_from_previous_burst")
    assert rep.mask == (1,1,1,0)
    assert [row[:3] for row in rep.values[:3]] == [(1,2,220),(-1,2,170),(1,1,110)]
    assert rep.values[-1] == (0,0,0,0,0)
    assert (rep.original_length,rep.retained_length) == (3,3)


def test_hierarchy_partition_and_loss_accounting():
    flow=_flow(); bursts=direction_only_bursts(flow)
    rep=starter.hierarchical_representation(flow,bursts)
    assert isinstance(rep,HierarchicalRepresentation)
    assert rep.packet_count == 5
    assert [len(b.packet_features) for b in rep.bursts] == [2,2,1]
    padded=starter.pad_hierarchy(rep,2,1)
    assert isinstance(padded,PaddedHierarchy)
    assert padded.burst_mask == (1,1)
    assert padded.packet_mask == ((1,),(1,))
    assert (padded.original_bursts,padded.retained_bursts,padded.original_packets,padded.retained_packets,padded.dropped_packets) == (3,2,5,2,3)
    padded2=starter.pad_hierarchy(rep,4,3)
    assert padded2.burst_mask == (1,1,1,0)
    assert padded2.packet_mask == ((1,1,0),(1,1,0),(1,0,0),(0,0,0))
    assert padded2.dropped_packets == 0


def test_hierarchy_rejects_invalid_partition():
    flow=_flow(); bursts=direction_only_bursts(flow)
    bursts[0].packets=bursts[0].packets[:-1]
    with pytest.raises(ValueError): starter.hierarchical_representation(flow,bursts)


def test_nonpositive_limits_rejected():
    flow=_flow(); bursts=direction_only_bursts(flow)
    with pytest.raises(ValueError): starter.packet_sequence(flow,0)
    with pytest.raises(ValueError): starter.burst_sequence(bursts,0)
    rep=starter.hierarchical_representation(flow,bursts)
    with pytest.raises(ValueError): starter.pad_hierarchy(rep,0,2)
    with pytest.raises(ValueError): starter.pad_hierarchy(rep,2,0)

"""Lab 4 public RED/GREEN tests: independent fixture, no instructor references."""
import pytest
from labs.common.fixtures import tiny_packet_records
from labs.common.schema import Burst, DirectedPacket, Flow
from labs.common.graphs import GraphNode, GraphEdge, TrafficGraph
from labs.lab4_graph import starter


def _flow():
    packets=tiny_packet_records()[:5]
    directions=(1,1,-1,-1,1)
    iats=(0.0,0.02,0.03,0.02,0.43)
    return Flow(("TCP",), [DirectedPacket(p,d,i) for p,d,i in zip(packets,directions,iats)])


def _bursts(flow):
    groups=[]
    for dp in flow.packets:
        if not groups or groups[-1].direction != dp.direction:
            groups.append(Burst(dp.direction,[]))
        groups[-1].packets.append(dp)
    return groups


def _edges(graph, relation):
    return [(e.src,e.dst,e.provenance) for e in graph.edges_of_relation(relation)]


def test_api_available():
    assert GraphNode and GraphEdge and TrafficGraph
    assert all(callable(getattr(starter, name)) for name in (
        'packet_chain_graph','burst_graph','packet_burst_hierarchical_graph'))


def test_packet_chain_exact_topology_and_features():
    g=starter.packet_chain_graph(_flow())
    assert isinstance(g,TrafficGraph)
    assert [(n.node_id,n.node_type) for n in g.nodes] == [(f'p{i}','packet') for i in range(1,6)]
    assert _edges(g,'next_packet') == [(f'p{i}',f'p{i+1}',('O','H')) for i in range(1,5)]
    assert g.nodes[0].feature_names == ('direction','packet_length','iat')
    assert g.nodes[0].features == pytest.approx((1,100,0))
    assert g.nodes[2].features == pytest.approx((-1,90,0.03))
    assert g.edges[0].feature_names == ('target_iat',)
    assert [e.features[0] for e in g.edges] == pytest.approx((0.02,0.03,0.02,0.43))
    assert g.raw_observable_budget == ('direction','packet_length','iat')
    assert g.information_loss == ()


def test_burst_graph_topology_and_loss():
    f=_flow(); g=starter.burst_graph(f,_bursts(f))
    assert isinstance(g,TrafficGraph)
    assert [(n.node_id,n.node_type) for n in g.nodes] == [(f'b{i}','burst') for i in range(1,4)]
    assert _edges(g,'next_burst') == [('b1','b2',('B','O','H')),('b2','b3',('B','O','H'))]
    assert g.nodes[0].feature_names == ('direction','packet_count','byte_count','duration','gap_from_previous_burst')
    assert [n.features[:3] for n in g.nodes] == [(1,2,220),(-1,2,170),(1,1,110)]
    assert g.edges[0].features == pytest.approx((1,0.03))
    assert g.edges[1].features == pytest.approx((1,0.43))
    assert g.raw_observable_budget == ('direction','packet_length','iat')
    assert 'within-burst individual packet lengths' in g.information_loss


def test_hierarchy_exact_membership_and_information():
    f=_flow(); g=starter.packet_burst_hierarchical_graph(f,_bursts(f))
    assert isinstance(g,TrafficGraph)
    assert len(g.nodes_of_type('packet')) == 5
    assert len(g.nodes_of_type('burst')) == 3
    assert len(g.edges) == 11
    assert _edges(g,'member_of') == [('p1','b1',('B','H')),('p2','b1',('B','H')),('p3','b2',('B','H')),('p4','b2',('B','H')),('p5','b3',('B','H'))]
    assert len(g.edges_of_relation('next_packet')) == 4
    assert len(g.edges_of_relation('next_burst')) == 2
    assert g.raw_observable_budget == ('direction','packet_length','iat')
    assert g.information_loss == ()


def test_empty_and_single_packet_boundary():
    f=Flow(('TCP',),[])
    assert starter.packet_chain_graph(f).nodes == ()
    assert starter.packet_chain_graph(f).edges == ()
    assert starter.burst_graph(f,[]).edges == ()
    assert starter.packet_burst_hierarchical_graph(f,[]).nodes == ()
    single=Flow(('TCP',),_flow().packets[:1]); bursts=_bursts(single)
    assert len(starter.packet_chain_graph(single).nodes) == 1
    assert starter.packet_chain_graph(single).edges == ()
    assert starter.burst_graph(single,bursts).edges == ()
    assert len(starter.packet_burst_hierarchical_graph(single,bursts).edges_of_relation('member_of')) == 1


def test_invalid_partition_rejected():
    f=_flow(); bursts=_bursts(f)
    bursts[0].packets.pop()
    with pytest.raises(ValueError): starter.burst_graph(f,bursts)
    with pytest.raises(ValueError): starter.packet_burst_hierarchical_graph(f,bursts)

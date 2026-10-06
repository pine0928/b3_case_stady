from labs.common.representations import StatisticalVector, PaddedSequence, HierarchicalRepresentation
from labs.lab3_nongraph import starter

def test_lab3_contracts_are_present():
    assert StatisticalVector is not None
    assert PaddedSequence is not None
    assert HierarchicalRepresentation is not None
    assert callable(starter.statistical_vector)
    assert callable(starter.packet_sequence)
    assert callable(starter.burst_sequence)
    assert callable(starter.hierarchical_representation)
    assert callable(starter.pad_hierarchy)

from labs.lab5_compare.protocol import RepresentationConfig, CANONICAL_OBSERVABLES
from labs.lab5_compare.public_dataset import make_dataset
from labs.lab5_compare.public_harness import split_dataset, evaluate_vectorizer

def test_lab5_public_harness_smoke():
    assert CANONICAL_OBSERVABLES == frozenset({"direction", "packet_length", "iat"})
    data = make_dataset(n_per_class=4, seed=3)
    train, test = split_dataset(data, seed=3)
    assert len(train) + len(test) == 8
    def simple_vectorizer(flow):
        return [float(len(flow.packets)), float(sum(p.packet.packet_length for p in flow.packets))]
    result = evaluate_vectorizer(simple_vectorizer, train, test, learner="linear", seed=3)
    assert 0.0 <= result.accuracy <= 1.0

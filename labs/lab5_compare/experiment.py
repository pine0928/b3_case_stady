"""Reproducible matched-information experiment runner for Lab 5."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import numpy as np
from sklearn.model_selection import train_test_split

from .dataset import make_dataset
from .models import fit_and_score, make_linear, make_mlp, Metrics
from .protocol import CANONICAL_CONFIGS, assert_matched_budget
from .vectorizers import (
    vectorize_statistics,
    vectorize_packet_sequence,
    vectorize_burst_sequence,
    vectorize_hierarchy,
    vectorize_packet_chain_graph,
    vectorize_hierarchical_graph,
)

Vectorizer = Callable[[object], np.ndarray]

VECTORIZERS: dict[str, Vectorizer] = {
    "statistics": vectorize_statistics,
    "packet-sequence": vectorize_packet_sequence,
    "burst-sequence": vectorize_burst_sequence,
    "hierarchy": vectorize_hierarchy,
    "packet-chain-graph": vectorize_packet_chain_graph,
    "hierarchical-graph": vectorize_hierarchical_graph,
    "packet-chain-graph-no-relations": lambda flow: vectorize_packet_chain_graph(flow, include_relations=False),
    "hierarchical-graph-no-relations": lambda flow: vectorize_hierarchical_graph(flow, include_relations=False),
}

@dataclass(frozen=True)
class ExperimentResult:
    representation: str
    learner: str
    n_features: int
    metrics: Metrics


def _matrix(items, vectorizer: Vectorizer):
    X = np.stack([vectorizer(x.flow) for x in items])
    y = np.asarray([x.label for x in items], dtype=np.int64)
    return X, y


def run_experiment(n_per_class: int = 120, seed: int = 7) -> list[ExperimentResult]:
    assert_matched_budget(*CANONICAL_CONFIGS)
    items = make_dataset(n_per_class=n_per_class, seed=seed)
    indices = np.arange(len(items))
    y_all = np.asarray([x.label for x in items])
    train_idx, test_idx = train_test_split(
        indices, test_size=0.30, random_state=seed, stratify=y_all
    )
    train = [items[i] for i in train_idx]
    test = [items[i] for i in test_idx]

    results = []
    for name, vectorizer in VECTORIZERS.items():
        Xtr, ytr = _matrix(train, vectorizer)
        Xte, yte = _matrix(test, vectorizer)
        for learner_name, factory in (("linear", make_linear), ("mlp", make_mlp)):
            metrics = fit_and_score(factory(seed), Xtr, ytr, Xte, yte)
            results.append(ExperimentResult(name, learner_name, Xtr.shape[1], metrics))
    return results

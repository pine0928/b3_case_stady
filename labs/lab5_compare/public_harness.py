"""Student-safe evaluation harness for Lab 5.

The harness accepts a student-supplied vectorizer.  It intentionally does not
contain the instructor reference representations or relation-engineering audit.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable
import numpy as np
from sklearn.model_selection import train_test_split
from .public_dataset import LabeledFlow
from .models import fit_and_score, make_linear, make_mlp, Metrics

@dataclass(frozen=True)
class PublicResult:
    learner: str
    n_features: int
    accuracy: float
    macro_f1: float

def split_dataset(items: list[LabeledFlow], seed: int = 7, test_size: float = 0.30):
    idx = np.arange(len(items)); y = np.asarray([x.label for x in items])
    tr, te = train_test_split(idx, test_size=test_size, random_state=seed, stratify=y)
    return [items[i] for i in tr], [items[i] for i in te]

def _matrix(items: list[LabeledFlow], vectorizer: Callable):
    X = np.stack([np.asarray(vectorizer(x.flow), dtype=np.float64) for x in items])
    y = np.asarray([x.label for x in items], dtype=np.int64)
    return X, y

def evaluate_vectorizer(vectorizer: Callable, train, test, learner: str = "linear", seed: int = 0) -> PublicResult:
    Xtr, ytr = _matrix(train, vectorizer); Xte, yte = _matrix(test, vectorizer)
    factory = make_linear if learner == "linear" else make_mlp if learner == "mlp" else None
    if factory is None:
        raise ValueError("learner must be 'linear' or 'mlp'")
    m: Metrics = fit_and_score(factory(seed), Xtr, ytr, Xte, yte)
    return PublicResult(learner, int(Xtr.shape[1]), m.accuracy, m.macro_f1)

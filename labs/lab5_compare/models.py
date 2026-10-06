"""Small common learners for Lab 5.

We use the *same* learner families across vectorized representations.  This is
intentional: the baseline first asks what changes when representation changes
under a common learner, then asks what changes when the learner changes while
the representation is held fixed.
"""
from __future__ import annotations
from dataclasses import dataclass
import warnings

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score

@dataclass(frozen=True)
class Metrics:
    accuracy: float
    macro_f1: float


def make_linear(seed: int = 0):
    return make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, random_state=seed, solver="lbfgs"),
    )


def make_mlp(seed: int = 0):
    return make_pipeline(
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=(24,),
            activation="relu",
            alpha=1e-3,
            max_iter=1200,
            random_state=seed,
        ),
    )


def fit_and_score(model, X_train, y_train, X_test, y_test) -> Metrics:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return Metrics(
        accuracy=float(accuracy_score(y_test, pred)),
        macro_f1=float(f1_score(y_test, pred, average="macro")),
    )

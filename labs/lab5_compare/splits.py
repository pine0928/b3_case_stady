"""Leakage-aware, class-complete group holdout for labeled captures.

A group is indivisible. A split is accepted only if both partitions contain
all labels. If this is impossible, fail explicitly rather than leak groups or
silently switch to a sample-level split.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import combinations
import numpy as np


def group_holdout_indices(labels, groups, *, test_size=0.30, seed=7):
    if len(labels) != len(groups) or len(labels) < 2:
        raise ValueError('labels and groups must have equal length >= 2')
    if not 0 < test_size < 1:
        raise ValueError('test_size must be between zero and one')
    group_members = defaultdict(list)
    for i, group in enumerate(groups):
        group_members[group].append(i)
    unique_groups = list(group_members)
    if len(unique_groups) < 2:
        raise ValueError('at least two independent groups are required')
    label_groups = defaultdict(set)
    for label, group in zip(labels, groups):
        label_groups[label].add(group)
    insufficient = [str(label) for label, owners in label_groups.items() if len(owners) < 2]
    if insufficient:
        raise ValueError('group-disjoint class-complete split impossible: labels occur in fewer than two groups: ' + ', '.join(insufficient))

    n = len(labels)
    all_labels = set(labels)
    rng = np.random.default_rng(seed)
    shuffled = list(unique_groups)
    rng.shuffle(shuffled)
    candidates = []
    m = len(shuffled)
    if m <= 16:
        # Exhaustive search provides a definitive infeasibility result for small datasets.
        for k in range(1, m):
            for subset in combinations(shuffled, k):
                candidates.append(set(subset))
    else:
        # Bounded randomized search: failure is a search failure, not proof of impossibility.
        for _ in range(4096):
            k = int(rng.integers(1, m))
            candidates.append(set(rng.choice(m, size=k, replace=False).tolist()))
            candidates[-1] = {shuffled[i] for i in candidates[-1]}

    best = None
    best_score = float('inf')
    for test_groups in candidates:
        test_idx = [i for g in test_groups for i in group_members[g]]
        if not test_idx or len(test_idx) == n:
            continue
        test_set = set(test_idx)
        train_idx = [i for i in range(n) if i not in test_set]
        if {labels[i] for i in test_idx} != all_labels or {labels[i] for i in train_idx} != all_labels:
            continue
        score = abs(len(test_idx) / n - test_size)
        if score < best_score:
            best_score = score
            best = (np.asarray(sorted(train_idx), dtype=int), np.asarray(sorted(test_idx), dtype=int))
    if best is None:
        qualifier = 'impossible' if m <= 16 else 'not found after 4096 candidate attempts'
        raise ValueError(f'group-disjoint class-complete split {qualifier}; revise group design or dataset')
    train, test = best
    assert set(groups[i] for i in train).isdisjoint(groups[i] for i in test)
    return train, test

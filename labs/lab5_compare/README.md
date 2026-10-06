# Lab 5 - Matched-Information Graph vs Non-Graph Comparison

## Goal
Introduce small learners only after representation contracts are frozen and test whether an apparent performance difference is attributable to information, representation, or model capacity.

Canonical raw observable budget:
```text
direction, packet_length, IAT
```
Burst boundaries and graph edges are derived structures, not extra raw observations.

## Reading order
At this stage, read this Lab's README and `SPECIFICATION.md`, then revisit the evidence you produced in Labs 3 and 4. You do not need to read later-Lab material yet.

## Implementation Specification
Before coding, read `labs/lab5_compare/SPECIFICATION.md`. It is the authoritative baseline contract for definitions, function/artifact behavior, edge cases, the tiny worked example, and what the public tests do or do not certify.

## What to Read
- `labs/lab5_compare/starter.py`
- `labs/lab5_compare/protocol.py`
- `labs/lab5_compare/public_dataset.py`
- `labs/lab5_compare/public_harness.py`
- `templates/reports/lab5.md`
- your Lab 3/4 representation reports

## What to Do
1. Implement the budget checks in `starter.py`.
2. Vectorize at least one non-graph and one graph/hierarchical representation using the same raw observables.
3. Compare them under a common learner.
4. Hold representation fixed and compare learner capacity.
5. Include at least one representation/edge ablation.
6. Check scaling, seed, split/leakage, input dimension, and parameter count.
7. State what the result can and cannot support.

Minimal harness pattern:
```python
from labs.lab5_compare.public_dataset import make_dataset
from labs.lab5_compare.public_harness import split_dataset, evaluate_vectorizer

data = make_dataset(seed=7)
train, test = split_dataset(data, seed=7)
result = evaluate_vectorizer(my_vectorizer, train, test, learner="linear", seed=7)
print(result)
```

## How to Test
```bash
python -m pytest -q tests_public
```

## What to Submit
- `labs/lab5_compare/starter.py`
- your student-owned vectorizer/experiment code
- `reports/lab5.md` created from `templates/reports/lab5.md`
- compact result tables/figures needed to reproduce the seminar evidence

## What to Present
Show the matched raw-observable budget, primary comparison, relation/representation ablation, model-capacity control, seed/split/leakage checks, and a claim/non-claim conclusion.

## Exit Condition
The public contract passes, at least one matched-information comparison and one falsifying control have run reproducibly, and your report separates information, representation, and model explanations rather than attributing the score directly to "Graph".

## Claim Boundary
**You may claim:** only effects that survive the controls actually run under the documented synthetic/experimental setting.

**You may not claim:** intrinsic graph superiority, general real-world superiority, or causal attribution from a single score comparison.

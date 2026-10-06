# Lab 3 - Non-Graph Representation Design

## Goal
Build four non-graph representations from the same frozen flow/burst objects and state exactly what each representation preserves, makes implicit, aggregates, truncates, or loses.

Canonical raw observable budget unless explicitly extended:

```text
direction, packet_length, IAT
```

## Reading order
At this stage, read this Lab's README and `SPECIFICATION.md`, then revisit the evidence you produced in Lab 2. You do not need to read later-Lab material yet.

## Implementation Specification
Before coding, read `labs/lab3_nongraph/SPECIFICATION.md`. It is the authoritative baseline contract for definitions, function/artifact behavior, edge cases, the tiny worked example, and what the public tests do or do not certify.

## What to Read
- `labs/common/representations.py`
- `labs/lab3_nongraph/starter.py`
- `templates/reports/lab3.md`
- your Lab 2 burst definition

## What to Do
Implement in `starter.py`:
1. statistical vector;
2. directional packet sequence;
3. burst sequence;
4. packet-within-burst hierarchy.

Make padding/truncation explicit. Use masks or retained/dropped counts. Do not fit normalization statistics on validation/test data or padded rows. Hand-check at least one tiny flow against expected values.

## How to Test
```bash
python -m pytest -q tests_public
```

## What to Submit
- `labs/lab3_nongraph/starter.py`
- `reports/lab3.md` created from `templates/reports/lab3.md`

## What to Present
For every representation report: shape/structure, ordering retained, burst boundary explicit/implicit, hierarchy retained/absent, first irreversible information-loss point, truncation/mask policy, and raw observable budget.

## Exit Condition
All four builders satisfy the public contract, your tiny-flow hand calculation agrees with code output, and the report identifies the first irreversible information loss for every representation.

## Claim Boundary
**You may claim:** the four representations expose/compress the same frozen observations in different ways under the documented budget.

**You may not claim:** that a representation is more powerful merely because it is higher-dimensional/hierarchical, or that better task performance follows without a controlled experiment.

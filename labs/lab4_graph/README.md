# Lab 4 - Graph Representation Design

## Goal
Construct graphs from the same observations used in Lab 3, forcing every node and edge to have an explicit semantic meaning and provenance rather than treating graph construction as automatic.

Provenance codes: P protocol-grounded, O order-derived, B burst/cycle-derived, A association-derived, L learned/adaptive, H designer-typed.

## Reading order
At this stage, read this Lab's README and `SPECIFICATION.md`, then revisit the evidence you produced in Lab 3. You do not need to read later-Lab material yet.

## Implementation Specification
Before coding, read `labs/lab4_graph/SPECIFICATION.md`. It is the authoritative baseline contract for definitions, function/artifact behavior, edge cases, the tiny worked example, and what the public tests do or do not certify.

## What to Read
- `labs/common/graphs.py`
- `labs/lab4_graph/starter.py`
- `templates/reports/lab4.md`
- your Lab 3 preservation/loss report

## What to Do
Implement:
```python
packet_chain_graph(flow)
burst_graph(flow, bursts)
packet_burst_hierarchical_graph(flow, bursts)
```
For every edge type document semantics, provenance, raw observables used, what becomes explicit relative to Lab 3, information loss, and a plausible non-graph equivalent. Then perform at least one edge deletion/replacement or node-unit change and explain what becomes implicit or disappears.

## How to Test
```bash
# Before implementation: API check should PASS; behavior tests should FAIL (RED)
python -m pytest -q tests_public/test_lab4_contract.py -k api_available
python -m pytest -q tests_public/test_lab4_contract.py
# After implementation: all Lab 4 tests should PASS (GREEN)
python -m pytest -q tests_public/test_lab4_contract.py
```

## What to Submit
- `labs/lab4_graph/starter.py`
- `reports/lab4.md` created from `templates/reports/lab4.md`

## What to Present
Show the same tiny flow in the three graph designs. Defend why each node is a node and each edge exists. Show one perturbation audit and the corresponding non-graph encoding.

## Exit Condition
All graph builders satisfy the public contract, every edge type has a provenance label, and you can explain both the graph-specific explicit structure and an equivalent sequence/hierarchy encoding where one exists.

## Claim Boundary
**You may claim:** graph construction makes selected relations explicit for message passing under a stated design.

**You may not claim:** that graph edges are new raw observations, that graph structure is uniquely determined by PCAP data, or that a graph is superior before matched-information/model controls are run.

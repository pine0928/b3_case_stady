# Lab 3 Report - Non-Graph Representation Audit

For each representation, record the output shape/structure, retained information, first irreversible loss point, and input budget.

| Representation | Shape / structure | Preserved | Implicit / lost | Truncation / mask |
|---|---|---|---|---|
| Statistical vector | | | | |
| Packet sequence | | | | |
| Burst sequence | | | | |
| Hierarchy | | | | |

## Manual check
- Tiny flow used:
- Hand-derived expected value(s):
- Code output agrees?:

## Claim boundary
- Supported:
- Not supported:

## Observable budget and leakage controls
- Canonical raw observables (no additional fields):
- Frozen Lab 2 burst rule and parameter(s):
- Training-only normalization policy (no validation/test fitting):
- Padding exclusion when fitting statistics:

## Truncation and loss accounting
- Packet sequence: original / retained / dropped packets:
- Burst sequence: original / retained / dropped bursts:
- Hierarchy: original / retained bursts and packets; masks:
- Why zeros from padding are not observations:

## Evidence and tests
- API check output:
- Assessed public test output:
- Numerical hand-check and explanation of first irreversible loss:

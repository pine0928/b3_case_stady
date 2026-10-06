# Lab 2 - Flow to Burst

## Goal
Construct burst abstractions from bidirectional flows and learn that burst boundaries are modeling decisions built from observations, not fields stored in the PCAP.

## Reading order
At this stage, read this Lab's README and `SPECIFICATION.md`, then revisit the evidence you produced in Lab 1. You do not need to read later-Lab material yet.

## Implementation Specification
Before coding, read `labs/lab2_burst/SPECIFICATION.md`. It is the authoritative baseline contract for definitions, function/artifact behavior, edge cases, the tiny worked example, and what the public tests do or do not certify.

## What to Read
- `labs/lab2_burst/starter.py`
- `templates/reports/lab2.md`
- your Lab 1 FlowKey/Flow convention

## What to Do
1. Implement `direction_only_bursts(flow)` as maximal same-direction runs.
2. Implement one documented `alternative_bursts(flow, **params)` rule.
3. Compare canonical and alternative burst count/size/duration on the same flow.
4. Identify at least one burst boundary that changes and explain why.
5. State what packet-level information is lost when you summarize a burst.

## How to Test
```bash
python -m pytest -q tests_public
```

## What to Submit
- `labs/lab2_burst/starter.py`
- `reports/lab2.md` created from `templates/reports/lab2.md`

## What to Present
Show one flow as packets and as bursts. Explain where each boundary came from, how the alternative rule changes the abstraction, and what detail disappears after aggregation.

## Exit Condition
Both burst rules run reproducibly, the canonical rule passes the public contract test, and your report contains a numerical comparison plus an explicit information-loss statement.

## Claim Boundary
**You may claim:** different documented burst rules produce different derived representations from the same flow.

**You may not claim:** that a burst boundary is directly observed in the PCAP, that one burst definition is universally correct, or that aggregation is beneficial before task-level evidence exists.

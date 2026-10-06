# Lab 1 - PacketRecord to FlowKey and Flow

## Goal
Turn ordered packet observations into a canonical bidirectional **FlowKey** and temporally continuous **Flow instances**. Then refactor the same semantics into a streaming generator.

## Before coding
Do not read all streaming material first. Follow this order:

1. Read `labs/tutorials/DUAL_INGESTION.md` to connect Lab 0's `PacketRecord` to the analysis pipeline.
2. Read `SPECIFICATION.md` and complete `GOLDEN_TRACE_WORKSHEET.md` by hand.
3. Complete Part 1A.
4. **Before Part 1B**, read `labs/tutorials/PYTHON_STREAMING_PROCESS_DESIGN.md` and work through `labs/tutorials/python_streaming_companion/README.md` Steps 1-7.
5. After Part 1B, use `labs/tutorials/SCALING_WALL_EXPERIMENT.md` to test why the execution model matters as captures grow.

## Part 1A — Correctness first
1. Implement `canonical_flow_key`.
2. Implement `build_flows(records, inactivity_timeout) -> list[Flow]`.
3. Reproduce the Golden Trace and explain every Flow boundary.
4. Change the idle timeout once and record what changes.

At this point the complete input and output may be materialized. The purpose is to make the Flow semantics explicit before changing the execution model.

## Part 1B — Streaming refactor
Implement:

```python
def iter_flows(records: Iterable[PacketRecord], inactivity_timeout: float) -> Iterator[Flow]:
    ...
```

The semantics must remain the same as Part 1A, but the function must **yield a Flow when it becomes complete** rather than first constructing a list of every Flow. Do not begin by converting `records` to `list(records)`.

The intended pipeline is:

```text
TShark stdout
    ↓
yield PacketRecord
    ↓
active Flow states only
    ↓ timeout / EOF
yield completed Flow
    ↓
downstream analysis
```

For the same finite trace, this should hold conceptually:

```python
build_flows(records, timeout) == list(iter_flows(records, timeout))
```

A generator alone does **not** guarantee bounded memory. The important design question is what state must remain active for future packets and what can be yielded and discarded.

## How to test
```bash
python -m pytest -q tests_public
```

## What to submit
- `labs/lab1_flow/starter.py`
- `reports/lab1.md` created from `templates/reports/lab1.md`

## What to present
Explain FlowKey vs Flow, the FW/BW convention, timeout sensitivity, and why the streaming version can avoid retaining completed Flows. Also explain why `list(iter_flows(...))` deliberately materializes the output again.

## Exit condition
You can reproduce the Golden Trace by hand; Part 1A and Part 1B have the same Flow semantics; and you can identify the state that must remain in memory while streaming.

## Claim boundary
**You may claim:** your documented rules deterministically construct observed Flow instances from supported packet observations.

**You may not claim:** that a 5-tuple uniquely identifies an application interaction, that an observed Flow is necessarily the complete ground-truth TCP connection, that FW always means client-to-server, or that a Python generator by itself guarantees bounded memory.

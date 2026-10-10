# Network Behavior Analysis — Course Repository

This repository contains all Labs for the course from Day 1. Work through them in the order specified by the syllabus and instructor.

Reference solutions are intentionally not included here. As the class moves to the next Lab, the previous Lab's solution may be published in the separate `network-behavior-analysis-solutions` repository.

Use Git locally to track your work. Start with `docs/GIT_WORKFLOW.md`. A personal GitHub repository is not required unless the instructor explicitly asks for one.


## Recommended learning path

Do **not** read every tutorial at the beginning.  Use the tutorials when the
corresponding design question appears in a Lab.  The recommended route is:

| Stage | Main question | Read / run at this point |
| --- | --- | --- |
| Before / during Lab 0 | What can we actually observe in a PCAP, and how do Wireshark, TShark, and Python connect? | `labs/tutorials/SMALL_PCAP_ANALYSIS_FIRST.md` |
| Lab 0 -> Lab 1 | Why do we keep a stable `PacketRecord` boundary while changing the ingestion mechanism? | `labs/tutorials/DUAL_INGESTION.md` |
| Lab 1A | What is a FlowKey, and when does one observed Flow end and another begin? | `labs/lab1_flow/SPECIFICATION.md` + `GOLDEN_TRACE_WORKSHEET.md` |
| Lab 1B | How do we preserve the same Flow semantics while processing incrementally with iterators, generators, pipes, and `yield`? | `labs/tutorials/PYTHON_STREAMING_PROCESS_DESIGN.md`, then its `python_streaming_companion/README.md` Steps 1-7 |
| After Lab 1B / when scaling matters | Why is streaming needed, and what memory problem does it actually solve? | `labs/tutorials/SCALING_WALL_EXPERIMENT.md` |
| Labs 2-5 | How do Flow observations become Burst, non-graph, graph, and matched-information representations? | Read each Lab's `SPECIFICATION.md` and README when you reach that Lab; reuse the previous Lab's evidence rather than reading ahead. |
| Lab 6 | How do we turn the pipeline into a bounded research claim? | Read `labs/lab6_open_project/SPECIFICATION.md` after completing the Lab 5 comparison. |

A useful rule is:

```text
Observe -> encounter a design question -> read the matching tutorial
        -> implement -> test -> explain what changed and why
```

The streaming tutorial is intentionally placed **after Lab 1A**.  First make
the Flow semantics correct; then refactor the same semantics into
`iter_flows(...)` and reason about what state must remain in memory.

## Labs

- `lab0_pcap` — PCAP observation and ingestion
- `lab1_flow` — FlowKey and Flow
- `lab2_burst` — Burst reconstruction
- `lab3_nongraph` — non-graph representations
- `lab4_graph` — graph representations
- `lab5_compare` — matched-information comparison
- `lab6_open_project` — open project

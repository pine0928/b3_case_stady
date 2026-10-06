# Python Streaming Companion — Study Guide

This guide accompanies the seven executable examples in `python_streaming_steps/`. **Read one concept page, run its matching program, write down what you observe, and only then move to the next step.**

The learning loop is:

```text
Question → tiny Python/Unix idea → real PCAP code → Run → Observe → Think
        → What improved? → What still hurts? → next design
```

The target is not memorizing syntax. The target is being able to explain why a design changes when scale, debuggability, reproducibility, and reuse requirements change.

## Route

| Step | Companion page | Executable | New idea | Design pressure |
|---|---|---|---|---|
| 1 | [`01_cli_tsv.md`](01_cli_tsv.md) | `step1_*.py` | CLI, stdout redirection, TSV as an intermediate representation | The file can become enormous and the workflow still requires a separate Python command. |
| 2 | [`02_python_tsv.md`](02_python_tsv.md) | `step2_*.py` | `with`, file objects, iteration, `csv.reader`, delimiter | TShark and Python are still manually coordinated. |
| 3 | [`03_subprocess_run.md`](03_subprocess_run.md) | `step3_*.py` | parent/child process, `subprocess.run`, stdout, stderr, exit status | `capture_output=True` materializes the complete output; that is a bad default for huge packet streams. |
| 4 | [`04_popen_pipe.md`](04_popen_pipe.md) | `step4_*.py` | `Popen`, `PIPE`, process lifetime, EOF, `wait`, stderr | Process control, error handling, and parsing can become tangled. |
| 5 | [`05_csv_pipe.md`](05_csv_pipe.md) | `step5_*.py` | iterables, file-like streams, separation of source from format | Even a streaming input can be defeated if downstream accumulates every row. |
| 6 | [`06_generator.md`](06_generator.md) | `step6_*.py` | iterator protocol, generator, `yield`, `next`, lazy evaluation | A generator only bounds the stage that stays lazy; downstream can still consume unbounded memory. |
| 7 | [`07_layered_adapter.md`](07_layered_adapter.md) | `step7_*.py` | separation of concerns, adapter, stable contract, dependency direction | There is still no universal best implementation: saved TSV, lists, or alternative decoders can be correct under different requirements. |

## Before you start
Use `labs/data/canonical_smoke.pcap`. Small data is intentional: first understand process and data flow; scale comes later. TShark must be installed for Steps 1 and 3–7. Step 2 can be studied with any saved TSV.

## After Step 7
Complete `labs/templates/reports/python_streaming_process_design.md`. You should be able to justify *different* choices for a seven-packet fixture, a 100 GB capture, a reproducibility/debugging case, and a random-access algorithm.

# Python Streaming & Process Design — From a TSV File to a Scalable Packet Pipeline

## Learning goal

This tutorial is about **Python and software design**, not just TShark. We will deliberately build the same idea several times. Each step works; each next step exists because the previous design exposes a new limitation.

By the end, you should be able to explain:

- how a command-line program and a Python program can exchange data;
- how TSV is a useful intermediate representation;
- how `csv.reader()` differs from manually splitting strings;
- when to use `subprocess.run()` and when to use `subprocess.Popen()`;
- what `stdin`, `stdout`, `stderr`, pipes, return codes, and process lifetime mean;
- why iterators and `yield` matter for large captures;
- why process management, row parsing, and `PacketRecord` construction should be separate responsibilities;
- why there is no single best design for every situation.

Use `labs/data/canonical_smoke.pcap` while learning. Do **not** begin with a huge trace.

**Companion study pages:** work through `labs/tutorials/python_streaming_companion/README.md` alongside this tutorial. Each page maps one-to-one to a Step 1–7 executable and follows Question → Micro Example → Code Walkthrough → Run → Observe → Think → Trade-off.

---

## Step 1 — TShark writes a TSV file

First keep the two programs separate:

```text
PCAP -> tshark -> packets.tsv
```

Run the example command printed by:

```bash
python -m labs.tutorials.python_streaming_steps.step1_tshark_to_tsv
```

Then inspect the TSV with a text editor or `head`. A TSV is deliberately boring: one packet per row, fields separated by tabs. That boring boundary is useful because you can inspect it, archive it, compare it, and debug TShark independently of Python.

**Python/Unix idea:** a command-line program can produce a data product without knowing anything about the later Python program.

**What improves:** observability and debugging.

**What remains:** a large capture can create a very large intermediate TSV.

---

## Step 2 — Python reads the saved TSV

Run:

```bash
python -m labs.tutorials.python_streaming_steps.step2_read_tsv path/to/packets.tsv
```

The important code is:

```python
with path.open(newline="", encoding="utf-8") as handle:
    reader = csv.reader(handle, delimiter="\t")
    for row in reader:
        ...
```

Why `csv.reader()` instead of `line.split("\t")`? The latter can be acceptable for a tightly controlled format, but `csv.reader()` makes the tabular contract explicit and gives us one parser abstraction that can consume either a file or a live text stream later.

Notice the `with` statement. The file is a resource with a lifetime. Python closes it even if an exception occurs.

**What improves:** Python can consume the external tool's output using a standard tabular parser.

**What remains:** TShark and Python are still two manual commands.

---

## Step 3 — Python launches TShark with `subprocess.run()`

Run:

```bash
python -m labs.tutorials.python_streaming_steps.step3_run_capture labs/data/canonical_smoke.pcap
```

`subprocess.run()` is a good first process API because its mental model is simple:

```text
start child process -> wait for it -> receive CompletedProcess
```

The example uses `capture_output=True` and `text=True`. `stdout` and `stderr` therefore arrive as Python strings. `check=True` turns a non-zero exit status into an exception.

This is excellent for short commands and small outputs. It is **not** our production design for a huge packet stream, because captured stdout is accumulated before we parse it.

**What improves:** reproducible one-command automation.

**What remains:** output is materialized in memory.

---

## Step 4 — Replace capture-all with `Popen()` and a pipe

Run:

```bash
python -m labs.tutorials.python_streaming_steps.step4_popen_stream labs/data/canonical_smoke.pcap
```

Now the mental model changes:

```text
Python parent                    TShark child
     |                                |
     |------ create process --------->|
     |                                |
     |<====== stdout pipe ============|
     |   read rows while it runs      |
     |                                |
     |<------ exit status ------------|
```

`Popen()` returns while the child process is alive. `stdout=PIPE` creates a stream that Python can read incrementally. We still need to wait for the process and inspect its return code.

`stderr` is a separate channel. Do not silently discard it: diagnostic information belongs there. Also avoid designs that let a child fill an unread pipe indefinitely. The course wrapper keeps error handling explicit; production systems may use additional techniques when stderr volume can be large.

**What improves:** the complete stdout no longer has to exist as one Python string.

**What remains:** process control and row interpretation can easily become tangled in one large function.

---

## Step 5 — Parse the live pipe with `csv.reader()`

Run:

```bash
python -m labs.tutorials.python_streaming_steps.step5_csv_pipe labs/data/canonical_smoke.pcap
```

A useful Python insight is that `csv.reader()` does not require a disk file. It needs an **iterable of text lines**. `proc.stdout` is such an object.

Therefore the same conceptual parser works for:

```text
saved file ----\
               +--> csv.reader(..., delimiter="\t") --> rows
live stdout ---/
```

This is an important abstraction: **file versus pipe is an I/O decision; TSV row interpretation is a data-format decision.**

**What improves:** the parser is no longer tied to an intermediate file.

**What remains:** downstream code may still build a giant list.

---

## Step 6 — Turn rows into a generator with `yield`

Run:

```bash
python -m labs.tutorials.python_streaming_steps.step6_generator labs/data/canonical_smoke.pcap
```

Compare these illustrative sketches (pseudocode, not directly runnable Python):

```text
def load_everything(...):
    records = []
    ...
    records.append(record)
    return records
```

and

```text
def iter_records(...):
    ...
    yield record
```

A generator produces the next item when the consumer asks for it. This enables a pipeline such as:

```text
TShark -> one TSV row -> one PacketRecord -> downstream consumer
```

without requiring an ingestion-stage list of every packet.

But be precise: a generator does **not** guarantee that the whole application uses constant memory. If downstream code calls `list(...)` or stores every packet, memory still grows.

**What improves:** back-to-back incremental processing becomes possible.

**What remains:** we need clean responsibility boundaries and a stable domain interface.

---

## Step 7 — Separate responsibilities and meet at `PacketRecord`

The canonical design is intentionally layered:

```text
build command
     |
manage TShark process / text stream
     |
parse one TSV row
     |
construct one PacketRecord
     |
FlowKey / Flow / Burst / Representation
```

Read `labs/common/tshark.py` after completing Steps 1–6. Identify these responsibilities in the real implementation:

- `_TSHARK_FIELDS`: the external field contract;
- command construction: how TShark is invoked;
- `Popen` and pipe handling: process/resource lifetime;
- `_parse_tshark_row()`: translation from external text to our domain schema;
- `iter_tshark_packet_records()`: lazy public interface;
- `load_tshark_packet_records()`: explicit convenience materialization when a list is genuinely wanted.

The important architecture is:

```text
pcap.py ---------\
                  +--> PacketRecord --> later representations
TShark adapter --/
```

`PacketRecord` prevents TShark-specific details from leaking into Flow, Burst, sequence, or graph code.

---

## Which design is best?

There is no universal winner. Choose according to the job.

| Design | Strongest use | Main cost |
|---|---|---|
| TShark -> saved TSV -> Python | teaching, inspection, debugging, reproducible intermediate data | disk I/O and potentially huge files |
| `subprocess.run(capture_output=True)` | small commands/tests, simple automation | complete output is materialized |
| `Popen` -> `PIPE` -> streaming parser | large sequential processing | process/error/resource management is more subtle |
| Python packet decoder | transparent custom logic, specialized experiments | protocol coverage/maintenance burden |
| high-level wrapper library | rapid development/convenience | another abstraction/dependency; performance and semantics must still be understood |

For this B3 repository, the **canonical large-capture ingestion design** is:

```text
Popen -> stdout PIPE -> csv.reader/row parser -> generator -> PacketRecord
```

The saved-TSV path remains a first-class debugging and teaching technique, not a failed earlier attempt.

---

## Mini exercises

Use `labs/templates/reports/python_streaming_process_design.md` as your worksheet.

1. Inspect a TShark TSV and label each column.
2. Read it with `csv.reader()` and explain `with`, `newline`, and `delimiter`.
3. Run TShark from Python with `subprocess.run()`; inspect `stdout`, `stderr`, and `returncode`/`check=True` behavior.
4. Replace capture-all with `Popen()` and explain parent process, child process, pipe, EOF, and exit status.
5. Feed `proc.stdout` directly to `csv.reader()` and explain why that works.
6. Convert a list-producing function into a generator and demonstrate that `next()` produces one record at a time.
7. Draw the final responsibility boundaries and explain why later Labs should depend on `PacketRecord`, not on TShark rows.
8. Design-choice question: for (a) a seven-packet teaching fixture, (b) a 100 GB research capture, and (c) a suspicious parser bug that must be reproduced tomorrow, choose a path and justify it.

The goal is not to memorize `subprocess` syntax. The goal is to understand **why the design changes as scale, debuggability, and reuse requirements change**.

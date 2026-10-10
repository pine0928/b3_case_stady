# Lab 0 - PCAP observation with Wireshark, TShark, and Python

## Goal
Learn the observation path used throughout the course:

```text
PCAP -> Wireshark (inspect) -> TShark (extract fields) -> Python -> PacketRecord
```

The goal is **not** to implement a PCAP binary parser.  The goal is to identify
which protocol field you are using, extract it reproducibly with TShark, and
map the resulting observations into the stable `PacketRecord` used by Lab 1+

## Implementation Specification
Read `labs/lab0_pcap/SPECIFICATION.md` for the exact TSV field order, parsing failures, and function contracts. The YAML FieldSpec is the source of truth for TShark extraction; the student implements the row mapping independently.

## What to Read
Read `labs/tutorials/SMALL_PCAP_ANALYSIS_FIRST.md` and `labs/lab0_pcap/SPECIFICATION.md`; inspect the fields in Wireshark.

## What to Do
Complete `parse_tshark_row` and `inter_arrival_times` in `labs/lab0_pcap/starter.py` after manually inspecting TCP and UDP packets.

## Before coding
1. Read `labs/tutorials/SMALL_PCAP_ANALYSIS_FIRST.md`.
2. Read `labs/lab0_pcap/SPECIFICATION.md`.
3. Inspect one TCP packet and one UDP packet in Wireshark.  For every TShark field below, locate the corresponding
field in Wireshark.

## Step 1 - inspect the capture
Open `labs/data/canonical_smoke.pcap` in Wireshark.  Identify:
- Ethernet, IPv4, and TCP/UDP layers;
- source/destination IP addresses;
- TCP or UDP source/destination ports;
- IPv4 total length;
- TCP payload length or UDP length;
- TCP flags when applicable.

## Step 2 - extract the same observations with TShark
Start with a small field set so that the protocol meaning stays visible:

```bash
tshark -n -r labs/data/canonical_smoke.pcap \
  -Y "ip && (tcp || udp)" \
  -T fields \
  -e frame.time_epoch -e ip.src -e ip.dst -e ip.proto \
  -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport
```

First explain `-Y`, `-T fields`, and each `-e` field.  Then move to the full
Lab 0 field contract:

```bash
python -m labs.tools.inspect_pcap labs/data/canonical_smoke.pcap
```

The full contract adds IP length, transport payload/length information, TCP
flags, and captured/original frame lengths.  Compare those extra columns with
Wireshark before coding.  Do not memorize a long TShark command as magic syntax.

## Step 3 - Python mapping
Complete:
- `starter.py::parse_tshark_row`
- `starter.py::inter_arrival_times`

`parse_tshark_row` receives one tab-separated line in the exact field order
listed in `starter.py::TSHARK_FIELDS`.  TCP and UDP rows deliberately contain
empty columns for fields that do not apply.

## Step 4 - observation policy
Classify candidate variables as observed, derived, or metadata/label.  Decide
which observations are legitimate model inputs and which may create shortcut
leakage.

## How to Test

Run commands from the **Course repository root**.

**A. Environment and fixture smoke test** (may PASS before you implement anything):

```bash
python -m labs.tools.kickoff_check
python -m pytest -q tests_public/test_lab0_contract.py
```

`kickoff_check` requires TShark and will report its absence. The contract test
checks the bundled fixture and shared decoder, **not your completed code**.

**B. Your Lab 0 implementation** (RED before coding, GREEN when correct):

```bash
python -m pytest -q tests_public/test_lab0_student.py
```

The supplied `starter.py` raises `NotImplementedError`, so the student test
**must FAIL initially**. Implement both TODO functions, rerun the student test,
and inspect any failures. Finally, run `python -m pytest -q tests_public` to
check the whole public suite. A PASS is necessary but does not prove that a
real capture is complete or that chosen features are scientifically valid.

## What to Submit
Submit your completed `labs/lab0_pcap/starter.py` and a final report based on `templates/reports/lab0_report.md`, recording field choices, rejected rows, test results, and observation limitations. The separate `lab0_plan.md` is for pre-lab planning, not final submission.

## What to Present
Demonstrate the mapping from a Wireshark field to its TShark column and PacketRecord attribute, and explain a rejected or unsupported row.

## Exit Condition
You can point to a field in Wireshark, name its TShark field, explain how the
TSV value becomes a `PacketRecord` field, and explain why that field should or
should not be used later as a model input.

## Claim Boundary
**You may claim:** a supported, untruncated IPv4 TCP/UDP observation was mapped to the documented PacketRecord fields. **You may not claim:** the capture contains every packet, or that metadata and labels are valid model features without further analysis.

## Beyond this lab
The same TShark observation boundary can be used for larger captures.  Large-
PCAP streaming, pipes, generators, and memory scaling are advanced topics and
are not required to understand the Lab 0-3 representation pipeline.

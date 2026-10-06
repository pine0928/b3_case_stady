# Running the PCAP Labs — TShark Core Path

The Core course uses one observation path:

```text
PCAP / pcapng
    ↓
Wireshark: inspect protocol structure and field meaning
    ↓
TShark: extract selected fields reproducibly
    ↓
Lab 0 Python: map one TSV row to PacketRecord
    ↓
Lab 1+: FlowKey / Flow / Burst / Analysis
```

## 1. Check the environment

From the repository root:

```bash
python -m labs.tools.kickoff_check
python -m pytest -q tests_public
```

## 2. Inspect the canonical capture

Open `labs/data/canonical_smoke.pcap` in Wireshark first.  Inspect at least one
TCP packet and one UDP packet.

Then print the same observations as raw TShark TSV:

```bash
python -m labs.tools.inspect_pcap labs/data/canonical_smoke.pcap
```

The first line is the field-name contract.  The following lines are the raw
observations.  Empty TCP columns in UDP rows, and empty UDP columns in TCP rows,
mean "not applicable".

## 3. Implement Lab 0

Read:

```text
labs/lab0_pcap/README.md
labs/lab0_pcap/SPECIFICATION.md
labs/lab0_pcap/starter.py
```

Your Lab 0 job is not to parse PCAP bytes.  TShark already performs protocol
dissection.  Your job is to understand the selected protocol fields and map one
TShark TSV row into the course `PacketRecord` representation.

Large-PCAP streaming and memory engineering are advanced topics.  They are not
part of the Core Lab 0–3 path.

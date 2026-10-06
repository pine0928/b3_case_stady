# Hands-on Lab: From PCAP to Traffic Representation

The labs share one canonical data path:

`PCAP -> PacketRecord -> FlowKey/Flow -> Burst -> Representation -> Model`

The starter code deliberately separates infrastructure from semantic choices. Utilities for loading, splitting, evaluation, and visualization may be supplied; aggregation and representation decisions remain student-owned.

## Lab contract
Each lab contains or will contain:
1. `README.md` - learning objectives, design questions, expected outputs.
2. `starter.py` - runnable interfaces with explicit TODO regions.
3. tests under `../tests/` - mechanical correctness checks.
4. a short design sheet - assumptions, preservation/loss, and research extension.

## Progression
- Lab 0: PCAP to packet records
  - Companion: `labs/tutorials/python_streaming_companion/README.md` — Step 1–7 Python/process study pages
- Lab 1: packet to bidirectional FlowKey/Flow
- Lab 2: flow to burst
- Lab 3: non-graph representations
- Lab 4: graph representations
- Lab 5: matched-information graph vs non-graph comparison
- Lab 6: open representation design project

Graph use is never mandatory in Lab 6. The representation must be justified from the task and observations.

## Cross-lab transition gates
The canonical track is a continuous scaffold, not seven independent exercises. Do not advance only because tests pass:
- 0 -> 1: packet schema + field-use policy are stable.
- 1 -> 2: flow/FW-BW/session semantics are reproducible.
- 2 -> 3: canonical burst rule + one sensitivity alternative are documented.
- 3 -> 4: hand-calculated preservation/loss audit passes.
- 4 -> 5: edge semantics/provenance and graph-design perturbation audit are complete.
- 5 -> 6: matched-information + experimental audits are complete; the toy task is not being used as evidence of intrinsic graph superiority.

See `notes/whole_hands_on_chapter_audit.md` for the full LO, responsibility, redundancy, real-PCAP, and Lab 6 scaffolding audit.

## Core architecture note
See `docs/STREAMING_5TUPLE_ARCHITECTURE.md` for the canonical 5-tuple streaming design, state/eviction rule, and the deliberate boundary before Host/Host-Pair research extensions.

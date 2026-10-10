# Lab 4 Report - Graph Design Audit

## Graph designs

| Design | Node unit | Edge types | Provenance | What becomes explicit? | Non-graph equivalent |
|---|---|---|---|---|---|
| Packet chain | | | | | |
| Burst graph | | | | | |
| Packet-burst hierarchy | | | | | |

## Perturbation audit
- Edge deleted/replaced:
- What became implicit or disappeared?
- Node-unit change tried:
- Information gained/lost by the abstraction:

## Claim boundary
- Supported:
- Not supported:

## Matched-information and temporal audit
- Canonical raw fields used (direction, packet_length, IAT):
- Packet/burst order retained and how it is encoded:
- Which features are aggregated or lost, and where:
- Are any labels, future packets, or test-set statistics used? (must be no):
- Non-graph encoding with the same observable budget:

## Verification
- API check command/result:
- RED before implementation / GREEN after implementation:
- Perturbation and its effect on topology versus raw observations:

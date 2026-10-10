# Lab 3 Specification -- Non-Graph Representations

## Purpose and scope
Lab 3 converts the frozen Lab 1/2 objects into four inspectable non-graph representations. No learner is introduced. The canonical raw observable budget is exactly:

```text
direction, packet_length, IAT
```

No IP address, port, protocol ID, TCP flags, payload bytes, or labels may be silently added.

## Canonical definitions
### Packet feature row
`(direction, packet_length, iat)` as floats.

### Burst feature row
`(direction, packet_count, byte_count, duration, gap_from_previous_burst)` where:
- duration = last timestamp - first timestamp inside the burst;
- first burst gap = 0;
- later gap = current burst start - previous burst end.

### Statistical vector (12 features, this exact order)
1. packet_count
2. forward_packet_count
3. backward_packet_count
4. total_bytes
5. forward_bytes
6. backward_bytes
7. mean_packet_length
8. population_std_packet_length
9. mean_iat
10. population_std_iat
11. flow_duration
12. direction_switch_count

Population standard deviation uses denominator `N` (not `N-1`). Empty numeric collections yield zero for baseline aggregate statistics.

## Function contracts
### `statistical_vector(flow) -> StatisticalVector`
Return the 12 features above with matching `feature_names`. It intentionally discards exact local order except direction-switch count.

### `packet_sequence(flow, max_packets) -> PaddedSequence`
- `max_packets > 0`;
- rows are packet feature rows in flow order;
- retain first N (`head/first-N`) if too long;
- zero-pad to exactly `max_packets` rows;
- mask is 1 for retained real rows and 0 for padding;
- record original and retained lengths.

### `burst_sequence(bursts, max_bursts) -> PaddedSequence`
- `max_bursts > 0`;
- use frozen Lab 2 boundaries without recomputing them;
- use the five burst features above;
- retain first N bursts, zero-pad, and provide a mask/length metadata.

### `hierarchical_representation(flow, bursts) -> HierarchicalRepresentation`
- supplied bursts must be an exact ordered partition of `flow.packets`; otherwise raise an error;
- retain ragged packet-within-burst membership;
- packet rows use the canonical packet features;
- burst rows use the canonical burst features;
- do not pad here.

### `pad_hierarchy(rep, max_bursts, max_packets_per_burst) -> PaddedHierarchy`
- both limits > 0;
- head/head truncation: first bursts, then first packets within each retained burst;
- zero padding for missing burst/packet slots;
- separate burst mask and packet mask;
- explicitly record original/retained burst and packet counts so dropped packets are measurable.

## Edge cases and failure modes
- Empty flow: statistical counts/aggregates are zero; packet sequence is all padding; hierarchy has zero bursts.
- Padding zeros are **not** data; masks define validity.
- Do not include padded rows when fitting normalization statistics.
- Normalization parameters must be fit on training data only in later Labs.
- Changing the Lab 2 burst partition inside Lab 3 violates the matched abstraction contract.

## Tiny worked example
Use the canonical five-packet TCP flow:

```text
(direction,length,IAT)
(+1,100,.000)
(+1,120,.020)
(-1, 90,.030)
(-1, 80,.020)
(+1,110,.430)
```

Direction-only bursts are `(p1,p2)|(p3,p4)|(p5)`.

Packet sequence with `max_packets=7` begins with the five rows above and ends with two `(0,0,0)` rows; mask is:

```text
1 1 1 1 1 0 0
```

Burst sequence begins:

```text
B1: (+1, 2, 220, .020, .000)
B2: (-1, 2, 170, .020, .030)
B3: (+1, 1, 110, .000, .430)
```

Statistical vector starts `(5,3,2,500,330,170,...)`, has flow duration `.500`, and direction-switch count `2`.

## Public-test alignment
The public API test checks function discovery and passes before implementation. Public assessed tests check numerical values, feature order, masks, head truncation, exact burst partition, padding/loss accounting, and invalid limits. The untouched starter intentionally fails assessed tests. Public tests are not exhaustive; the report must still explain information loss, observational budget, and train-only normalization.

## Lecture-material boundary
Lecture/seminar material asks which representation is a sensible inductive bias, what information loss may be beneficial, and how early classification changes input budgets. The specification only freezes transformations so later comparisons are reproducible.

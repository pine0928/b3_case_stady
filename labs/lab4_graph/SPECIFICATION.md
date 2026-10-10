# Lab 4 Specification -- Graph Representation Design

## Purpose and scope
Lab 4 re-encodes the same canonical observables from Lab 3 into explicit relations. Graph construction does not create new raw observations. Students implement three baseline designs before perturbing them.

Canonical raw observable budget:

```text
direction, packet_length, IAT
```

Edge provenance codes:
- `P`: protocol-grounded
- `O`: order-derived
- `B`: burst/cycle-derived
- `A`: association-derived
- `L`: learned/adaptive
- `H`: designer-typed

## Canonical definitions
### Packet node
ID `p1`, `p2`, ... in flow order. Features are the canonical packet row `(direction, packet_length, iat)`.

### Burst node
ID `b1`, `b2`, ... in burst order. Features are the Lab 3 burst row `(direction, packet_count, byte_count, duration, gap_from_previous_burst)`.

### Relation names
- `next_packet`: directed chronological adjacency between consecutive packet nodes. Provenance `("O","H")`.
- `member_of`: packet -> containing burst. Provenance `("B","H")`.
- `next_burst`: directed adjacency between consecutive burst nodes. Provenance `("B","O","H")`.

## Function contracts
### `packet_chain_graph(flow) -> TrafficGraph`
- one packet node per packet;
- `n-1` `next_packet` edges for `n` packets;
- edge direction follows time/order;
- raw observable budget exactly the canonical three fields;
- no information loss in the baseline graph object relative to those packet rows.

### `burst_graph(flow, bursts) -> TrafficGraph`
- bursts must correspond to the supplied flow and preserve order;
- one burst node per burst;
- consecutive bursts linked by `next_burst`;
- packet-level individual lengths/IATs are not retained as nodes: explicitly report that loss;
- do not invent edges between non-consecutive bursts in the baseline.

### `packet_burst_hierarchical_graph(flow, bursts) -> TrafficGraph`
- include both packet and burst nodes;
- include `next_packet`, `member_of`, and `next_burst` relations;
- packet-to-burst membership must be exact and exhaustive;
- preserve canonical packet information and burst hierarchy; baseline `information_loss=()`.

Every returned `TrafficGraph` must document `design`, `raw_observable_budget`, `explicit_relations`, and `information_loss` honestly.

## Edge cases and failure modes
- Empty flow -> graph with zero packet nodes/edges; behavior for empty burst list must remain consistent.
- Single packet -> one packet node and no `next_packet` edge.
- Single burst -> one burst node and no `next_burst` edge.
- A graph with packet and burst nodes but no `member_of` edges is **not** an explicit cross-level hierarchy.
- Adding symmetric or long-range edges changes semantics and must be labeled as a design perturbation, not silently substituted for the baseline.
- Provenance describes why an edge exists; it is not a confidence score.

## Tiny worked example
For five packets and three canonical bursts:

```text
packet chain:
p1 -> p2 -> p3 -> p4 -> p5
```

```text
burst chain:
b1 -> b2 -> b3
```

Hierarchical membership:

```text
p1,p2 -> b1
p3,p4 -> b2
p5    -> b3
```

The hierarchical graph therefore has 8 nodes and 11 edges:
- 4 `next_packet`
- 5 `member_of`
- 2 `next_burst`

A useful audit is to delete `p2 -> p3`: packet observations remain, but that chronological adjacency is no longer explicit in topology. Another is to delete all `member_of` edges: packet and burst nodes remain, but the cross-level hierarchy disappears.

## Public-test alignment
The public tests first check API availability, then assess packet-chain and burst topology, node and edge features, provenance, hierarchical membership, observable budgets, information loss, empty/single-packet cases, and invalid burst partitions. Instructor-only tests additionally assess graph design perturbations and richer invariants. A public-test PASS does not establish that a graph outperforms matched-information non-graph baselines.

## Lecture-material boundary
Lecture/seminar material asks whether a relation deserves to be explicit, whether the same relation can be represented by sequence masks/attention, and whether dynamic/learned graphs are justified. The baseline specification gives three reproducible starting designs; open-ended graph novelty begins only after those are understood.

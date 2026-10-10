# Lab 2 Specification -- Flow to Burst

## Purpose and scope
Lab 2 introduces burst segmentation as a derived abstraction. The baseline burst rule is fixed; one alternative rule is deliberately student-designed and must be documented.

## Canonical definitions
A **direction-only burst** is a maximal consecutive run of `DirectedPacket` objects with the same direction in one flow. Every flow packet belongs to exactly one burst; flattening bursts must recover `flow.packets` in the same order.

For direction pattern:

```text
+1 +1 -1 -1 +1
```

the canonical partition is:

```text
(+1,+1) | (-1,-1) | (+1)
```

## Function contracts
### `direction_only_bursts(flow) -> list[Burst]`
- preserve packet order;
- each burst has one direction (`+1` or `-1`);
- start a new burst iff the current packet direction differs from the preceding packet direction;
- no empty bursts;
- concatenating all burst packet lists must exactly equal `flow.packets`.

Empty flow -> `[]`.

### `alternative_bursts(flow, **params) -> list[Burst]`
Implement **one** clearly declared alternative. Allowed examples include:
- direction change OR within-direction IAT gap > `max_gap`;
- payload-aware rule that treats zero-payload/ACK-only packets specially;
- another rule approved in seminar.

The report must name every parameter, state its units/range/default, and explain precisely when a new burst begins. The implementation must still partition the flow without reordering or duplicating packets.

A recommended first alternative is IAT-aware segmentation:

```text
new burst if direction changes OR current_packet.iat > max_gap
```

with `max_gap >= 0`.

## Edge cases and failure modes
- Single-packet flow -> one burst.
- Empty flow -> no bursts.
- A long gap between same-direction packets does **not** split the canonical direction-only baseline.
- An alternative threshold exactly equal to a gap must have a documented `>` versus `>=` convention.
- ACK-only handling changes semantics and must not be silently introduced into the canonical baseline.

## Tiny worked example
For the Lab 1 five-packet TCP flow:

```text
packet:     p1    p2    p3    p4    p5
direction:  +1    +1    -1    -1    +1
IAT:       .000  .020  .030  .020  .430
```

Direction-only result:

```text
B1=(p1,p2), direction=+1
B2=(p3,p4), direction=-1
B3=(p5),    direction=+1
```

If the recommended IAT-aware rule uses `max_gap=0.01`, every non-first packet has a larger gap in this fixture, so the result is five one-packet bursts.

## Public-test alignment
The public tests have separate API and task checks. The API check passes on the
untouched starter; the task checks intentionally fail until implementation.
The task checks verify the direction-only partition (including empty and
single-packet cases, maximal runs, long gaps, and packet identity/order) and
basic partition integrity for the student-designed alternative. The alternative
is **not** required to implement the suggested IAT threshold: its exact
segmentation rule and a changed boundary must be justified in the report.
Instructor tests also verify the IAT-aware *reference example*, not every
permitted student alternative.

## Lecture-material boundary
Lecture/seminar material discusses why bursts can approximate interaction phases and why ACK handling, timeout choice, encrypted protocols, and application multiplexing complicate the notion. The specification defines the baseline partition; it does not declare one burst definition scientifically superior.

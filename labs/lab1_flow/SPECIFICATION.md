# Lab 1 Specification -- PacketRecord to FlowKey and Flow

## Purpose and scope
Lab 1 converts packet observations into researcher-defined 5-tuple identities and temporal Flow instances. The baseline must be reproduced exactly before alternatives are explored.

## Canonical definitions
### Endpoint
An endpoint is `(IP address, transport port)`.

### FlowKey
For one packet, form source endpoint `a=(src_ip,src_port)` and destination endpoint `b=(dst_ip,dst_port)`. Sort the two endpoints deterministically. The canonical bidirectional 5-tuple identity is:

```text
(protocol, lower_endpoint, higher_endpoint)
```

A->B and B->A packets with the same protocol/ports therefore share one **FlowKey**. FlowKey is an identity, not a temporal communication object and not a client/server label.

### Flow
A **Flow** is one temporally continuous observed occurrence of a FlowKey. If no packet with that FlowKey is observed for longer than `inactivity_timeout`, the current Flow ends. A later packet with the same FlowKey starts a **new Flow instance**.

The timeout is an observation/processing boundary. It does not prove that an underlying TCP connection ended.

### FW/BW convention
The source endpoint of the first observed packet in a Flow defines FW (`+1`). Packets from the opposite endpoint are BW (`-1`). FW/BW is therefore relative to that Flow instance; it is not guaranteed client/server direction and is not the canonical endpoint ordering.

### Flow-local IAT
The first packet in each Flow has `iat=0.0`. Later IATs are non-negative differences from the previous observed packet in the same Flow.

## Function contracts
### `canonical_flow_key(packet) -> tuple`
- deterministic and hashable;
- identical for reverse-direction packets of one supported 5-tuple;
- protocol is part of the key;
- must not depend on arrival order.

### `build_flows(records, inactivity_timeout) -> list[Flow]`
- `inactivity_timeout` must be positive;
- process packets in deterministic capture order;
- use `canonical_flow_key` only for identity;
- start a new Flow when no active instance exists for the FlowKey;
- finalize the current instance when `gap > inactivity_timeout`;
- if the same FlowKey appears later, create another Flow rather than resurrecting the old one;
- assign FW/BW from the first observed packet of each Flow;
- compute Flow-local IAT;
- empty input returns `[]`.

### `iter_flows(records, inactivity_timeout) -> Iterator[Flow]`
- accepts an iterable rather than requiring a list;
- must not materialize the complete input with `list(records)`;
- preserves the FlowKey, FW/BW, IAT, and strict `gap > timeout` semantics from Part 1A;
- uses packet timestamps as logical time;
- yields a Flow once the current observation time proves it idle beyond the timeout;
- flushes remaining active Flows at EOF;
- may retain state required by currently active Flows, but should not retain already-completed Flows merely to return them later.

For a finite trace, `list(iter_flows(...))` and `build_flows(...)` must represent the same Flow decomposition. Calling `list(...)` is useful for testing equivalence, but deliberately gives up output-side streaming.

Part 1A establishes these semantics with a materialized list. Part 1B must preserve the same semantics while changing the execution model to a generator.

## Edge cases and failure modes
- Equal timestamps require deterministic capture order; IAT can be zero.
- The first observed packet may be a response because capture started late or packets were missed. FW is therefore a convention.
- NAT, tunnels, multiplexing, QUIC, and reused 5-tuples can make a FlowKey a poor application-level identity.
- A timeout equal to the gap does **not** split under the baseline (`>` not `>=`).
- A PCAP is an observation at one point, not ground-truth knowledge of the complete connection.

## Tiny worked example

```text
p1 1.000 10.0.0.1:50000 -> 10.0.0.2:443 TCP
p2 1.020 10.0.0.1:50000 -> 10.0.0.2:443 TCP
p3 1.050 10.0.0.2:443   -> 10.0.0.1:50000 TCP
p4 1.070 10.0.0.2:443   -> 10.0.0.1:50000 TCP
p5 1.500 10.0.0.1:50000 -> 10.0.0.2:443 TCP
```

All five packets have one FlowKey. With `inactivity_timeout=0.1 s`, packets p1--p4 form Flow 0 and p5 starts Flow 1 because the 0.430 s gap exceeds the timeout. Thus **one FlowKey can produce multiple Flow instances**.

For Flow 0, direction is `FW FW BW BW` and local IAT is `0.000, 0.020, 0.030, 0.020`. Flow 1 starts again with FW and `iat=0.0`.

## Relationship to Burst
Lab 2 introduces Burst inside a Flow. Keep the hierarchy distinct:

```text
FlowKey  --identity-->  one or more Flow instances
Flow     --structure--> one or more Bursts
```

A Burst boundary does not create a new Flow. A Flow timeout does.

## Public-test alignment
The API smoke tests check required entry points. `test_lab1_student.py` checks behavior (and intentionally fails for an untouched starter). The worked example and Golden Trace worksheet are the human-readable behavior contract. The public contract also checks that `iter_flows` is a generator function. Passing an API test alone does not prove semantic correctness or bounded-memory behavior.

## Terminology guardrail
The Core course deliberately does **not** call timeout-separated 5-tuple segments `Session`. In networking literature, session can mean many different protocol/application concepts. Here we use the more precise terms **FlowKey**, **Flow**, and **Burst**.

## Lecture-material boundary
The baseline assumes students understand 5-tuples, packet timestamps, and the distinction between observed packets and complete connections. TCP FIN/RST state machines, retransmission inference, and application sessions are outside the Lab 1 baseline.

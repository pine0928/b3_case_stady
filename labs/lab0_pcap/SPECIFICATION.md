# Lab 0 Specification -- TShark fields to PacketRecord

## Purpose and scope
Lab 0 establishes the observation boundary.  TShark performs PCAP/pcapng
protocol dissection; students do **not** implement binary PCAP, Ethernet, IP,
TCP, or UDP parsers.  Students must understand the selected Wireshark/TShark
fields and map one tab-separated TShark row into `PacketRecord`.

Baseline packets are unfragmented IPv4 TCP/UDP packets selected by:

```text
ip && (tcp || udp) && ip.flags.mf == 0 && ip.frag_offset == 0
```

IPv6, IP reassembly, application parsing, inner VPN traffic, and QUIC stream
semantics are outside the baseline.

## Canonical definitions
The observation unit is one unfragmented IPv4 TCP/UDP packet selected by the YAML FieldSpec. A PacketRecord stores decoded packet metadata, not an application session or a ground-truth label.

## TShark field contract
The TSV columns, in order, are:

1. `frame.time_epoch`
2. `ip.src`
3. `ip.dst`
4. `ip.proto`
5. `ip.len`
6. `tcp.srcport`
7. `tcp.dstport`
8. `tcp.len`
9. `tcp.flags`
10. `udp.srcport`
11. `udp.dstport`
12. `udp.length`
13. `frame.cap_len`
14. `frame.len`

Empty transport columns mean "not applicable", not numeric zero.

## PacketRecord contract
- `timestamp`: `frame.time_epoch` as float.
- `src_ip`, `dst_ip`: `ip.src`, `ip.dst`.
- `protocol`: `"TCP"` for `ip.proto == 6`, `"UDP"` for `ip.proto == 17`.
- `src_port`, `dst_port`: select the TCP or UDP port fields according to protocol.
- `packet_length`: `ip.len` (IPv4 total length), not `frame.len`.
- `payload_length`: `tcp.len` for TCP; `max(0, udp.length - 8)` for UDP.
- `tcp_flags`: parsed TCP flags for TCP; `None` for UDP.

If `frame.cap_len < frame.len`, reject the row as snaplen-truncated rather than
silently treating the capture as complete.

## Function contracts

### `parse_tshark_row(line) -> PacketRecord`
Reject rows with the wrong number of TSV columns, unsupported IP protocol, or
snaplen truncation.  Do not infer flow direction or derive IAT here.

### `inter_arrival_times(records) -> list[float]`
Sort by timestamp ascending.  Empty input returns `[]`; the first IAT is `0.0`;
subsequent IATs are `max(0, t_i - t_{i-1})`.

## Edge cases and failure modes
Reject malformed TSV rows, unsupported protocol numbers, and snaplen-truncated captures. Empty transport-specific columns are expected; an absent required value is not silently converted to zero. Empty record lists produce empty IAT lists.

## Tiny worked example
For timestamps `1.050, 1.000, 1.020`, timestamp ordering gives
`1.000, 1.020, 1.050`, hence `IAT = [0.000, 0.020, 0.030]`.

The canonical capture should yield 7 baseline packets (5 TCP, 2 UDP) when
TShark is installed.  This is an infrastructure/fixture check, not a research
result.

## Scientific boundary
The specification defines what is observed and how it enters `PacketRecord`.
Whether IP addresses, ports, timing, lengths, or other observations should be
used as model inputs remains a scientific design decision documented in the
Lab 0 report.

## Public-test alignment
Public tests exercise the student-facing API and representative valid/invalid rows. Passing them does not establish capture completeness or scientific validity; the exact FieldSpec and worked example remain authoritative.

## Lecture-material boundary
Wireshark/TShark observation, IPv4 header fields, TCP/UDP fields, and timestamp interpretation are prerequisites. Binary PCAP parsing and advanced stream reconstruction are not required in Lab 0.

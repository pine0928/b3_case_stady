# Dual Ingestion Tutorial — Understand First, Scale Second

## 1. Why are there two ingestion paths?

The B3 case study uses one canonical analysis pipeline:

```text
PCAP / pcapng
    |
    +-- educational path: labs/common/pcap.py
    |       small, transparent, dependency-free
    |
    +-- scalable path:    labs/common/tshark.py
            TShark-backed, streaming field extraction
                    |
                    v
               PacketRecord
                    |
             FlowKey / Flow
                    |
                  Burst
                    |
             Representation
                    |
                  Model
```

The two paths are **not competing answers to the same programming exercise**.
They have different jobs.

The educational path makes packet decoding visible. You can follow bytes from a
PCAP record through Ethernet, IPv4, TCP/UDP, and finally into a `PacketRecord`.
That is useful when learning what a packet feature actually means.

The TShark path is the path to prefer when the capture becomes large or the
capture/protocol ecosystem becomes more realistic. Instead of reimplementing a
mature protocol dissector in Python, it asks TShark to decode packets and emits
only the fields needed by this course.

The design principle is:

> **Change the ingestion engine without changing the representation contract.**

Labs 1-6 should not need to know whether a record came from `pcap.py` or
`tshark.py`.

---

## 2. Educational parser walkthrough: `labs/common/pcap.py`

### 2.1 PCAP container first

`iter_decoded_packets()` opens a classic PCAP file and reads:

1. the 4-byte magic number;
2. the rest of the global header;
3. each per-packet PCAP header;
4. the captured Ethernet frame bytes.

The magic number tells the parser the byte order and whether timestamps use
microseconds or nanoseconds. The baseline also checks that the link type is
Ethernet (`DLT_EN10MB = 1`).

This is an important distinction: **PCAP is a container around captured frames**.
It is not itself Ethernet, IP, TCP, or UDP.

### 2.2 Ethernet to IPv4

`_decode_ethernet_ipv4()` begins with the Ethernet header. It reads the
EtherType and accepts IPv4 (`0x0800`), with support for one 802.1Q VLAN tag.
Other link/network-layer cases are outside this deliberately small baseline.

### 2.3 IPv4 fields

The parser then reads the IPv4 header, including:

- version and header length (IHL),
- IPv4 Total Length,
- fragmentation flags/offset,
- protocol number,
- source and destination IPv4 addresses.

The canonical `packet_length` is **IPv4 Total Length**, not the Ethernet frame
length. That definition matters later: a feature is meaningless unless its
measurement boundary is explicit.

The baseline does not reassemble IPv4 fragments. Fragmented packets are skipped
rather than guessed at.

### 2.4 TCP or UDP

For TCP, the parser extracts source/destination ports, TCP header length, flags,
and payload length. For UDP, it extracts ports and derives payload length from
the UDP length field.

The result is a `DecodedPacket`, and `load_packet_records()` maps that object to
the shared `PacketRecord` schema.

### 2.5 Why not use this parser for everything?

Its limitations are intentional. It is small enough to inspect because it does
**not** try to become Wireshark. The canonical baseline covers classic PCAP,
Ethernet, IPv4, TCP/UDP, and one VLAN tag. Real research traces may involve
pcapng, IPv6, tunnels, more link types, more protocols, and many edge cases.
Maintaining all of those dissectors ourselves would distract from the research
question.

---

## 3. TShark walkthrough: `labs/common/tshark.py`

### 3.1 Delegate dissection, keep our own contract

TShark is the command-line form of Wireshark's packet-analysis engine. The B3
wrapper does **not** ask TShark to create our research representation. TShark
only performs packet dissection and field extraction. Our code still decides
how those fields map into `PacketRecord`.

`_TSHARK_FIELDS` makes that boundary explicit. It requests fields such as:

```text
frame.time_epoch   ip.src       ip.dst       ip.proto
ip.len             tcp.srcport  tcp.dstport  tcp.len
tcp.flags          udp.srcport  udp.dstport  udp.length
frame.cap_len      frame.len
```

This list is worth reading as a miniature measurement specification: it says
exactly which observations cross from TShark into our pipeline.

### 3.2 The subprocess command

`iter_tshark_packet_records()` builds a TShark command with several deliberate
choices:

- `-n`: do not perform name resolution;
- `-r <capture>`: read the capture file;
- `-Y ...`: retain the canonical IPv4 TCP/UDP baseline and reject fragments;
- `-T fields`: emit fields rather than verbose packet trees;
- repeated `-e`: request only the fields in `_TSHARK_FIELDS`;
- tab-separated, unquoted output: make the Python-side contract simple.

So the scalable path is conceptually:

```text
large capture
    |
  TShark dissector
    |
selected tab-separated fields, one packet at a time
    |
_parse_tshark_row()
    |
PacketRecord
```

### 3.3 Where the scaling benefit comes from

The wrapper uses `subprocess.Popen()` and iterates over `proc.stdout`. It does
not first collect all TShark output into one giant Python string. Therefore
`iter_tshark_packet_records()` can feed records downstream incrementally.

Be precise about the claim: **streaming avoids materializing the complete
TShark output in memory; it does not make memory usage automatically constant
for the entire later pipeline.** If you call `load_tshark_packet_records()`,
the iterator is deliberately converted to a Python list. Likewise, a later
algorithm that stores every packet will still consume memory proportional to
the data it retains.

For genuinely large traces, prefer the iterator and design downstream
aggregation to consume records incrementally where possible.

### 3.4 Why `frame.cap_len` and `frame.len` are requested

The wrapper checks for snaplen truncation. If captured length is smaller than
the original frame length, part of the packet was not captured. Because packet
length/payload length are representation observables in these labs, silently
accepting truncated data would change the meaning of the features.

---

## 4. The `PacketRecord` contract

Both ingestion paths must terminate at the dataclass in
`labs/common/schema.py`:

```python
@dataclass(frozen=True)
class PacketRecord:
    timestamp: float
    src_ip: str
    dst_ip: str
    src_port: Optional[int]
    dst_port: Optional[int]
    protocol: str
    packet_length: int
    payload_length: int
    tcp_flags: Optional[int] = None
```

Think of this as an **interface between packet acquisition and representation
design**.

| Field | Canonical meaning |
|---|---|
| `timestamp` | capture timestamp in seconds |
| `src_ip`, `dst_ip` | observed IPv4 addresses |
| `src_port`, `dst_port` | TCP/UDP ports when present |
| `protocol` | canonical protocol label such as `TCP` or `UDP` |
| `packet_length` | IPv4 Total Length (L3 bytes) |
| `payload_length` | transport payload bytes under the baseline decoder |
| `tcp_flags` | TCP flag bits; `None` for non-TCP records |

A common schema does **not** imply that every field should become a machine
learning feature. Field-use decisions come later and must distinguish observed
fields, derived fields, metadata/labels, possible shortcut features, and
privacy-sensitive identifiers.

---

## 5. Side-by-side comparison on the canonical smoke PCAP

The repository contains:

```text
labs/data/canonical_smoke.pcap
```

Run the educational path in Lab 0 as usual. If TShark is installed, compare the
two ingestion engines directly:

```bash
python -m labs.tools.compare_ingestion_paths
```

Expected result for the canonical fixture:

```text
PASS: 7 PacketRecords are identical
educational: labs.common.pcap
scalable:    labs.common.tshark (streaming TShark)
```

The important word is **identical**. We are not merely checking that both
programs run. We are testing an invariant:

```text
educational_parser(canonical_smoke.pcap)
              ==
tshark_parser(canonical_smoke.pcap)
```

This is a small example of differential testing: two independent paths are
compared against the same contract.

If TShark is not installed, the scalable wrapper gives an explicit installation
error. The educational parser and the rest of the canonical labs remain usable.

---

## 6. Which path should I use?

| Situation | Educational `pcap.py` | TShark path |
|---|---:|---:|
| Learn how bytes become fields | **Best choice** | harder to inspect internally |
| Tiny canonical fixture | **Good** | good for equivalence testing |
| Large research capture | limited baseline | **preferred ingestion path** |
| pcapng | not supported | **preferred** |
| Broader protocol/link support | deliberately limited | usually much stronger |
| Debug exact course semantics | **very transparent** | inspect field mapping/filters |
| Avoid loading all extracted rows at once | iterator available | **streaming iterator designed for this** |

Do not turn this table into the claim “TShark is always faster.” Performance
depends on capture contents, storage, filters, fields, downstream work, and
hardware. The defensible claim is that the TShark path is **more scalable and
operationally realistic for broad packet dissection**, while our small parser is
**more transparent for learning the baseline mechanics**.

---

## 7. Student exercise — from understanding to a research decision

Record your answers in `reports/dual_ingestion.md` using the provided template.

### Exercise A — Trace one packet

Choose the first packet of `canonical_smoke.pcap`. Starting from `pcap.py`,
explain where each of these values comes from:

1. timestamp;
2. source/destination IP address;
3. source/destination port;
4. protocol;
5. `packet_length`;
6. `payload_length`;
7. TCP flags.

For each item, identify whether it originates in the PCAP record header,
Ethernet, IPv4, or TCP/UDP.

### Exercise B — Match the TShark fields

For the same `PacketRecord` fields, identify the corresponding entry or entries
in `_TSHARK_FIELDS`. Note any field used only for validation rather than stored
in `PacketRecord`.

### Exercise C — Verify the invariant

If TShark is available, run:

```bash
python -m labs.tools.compare_ingestion_paths
```

Record the result. Then explain in 2-4 sentences why equality on seven packets
is useful but **does not prove** equivalence for every possible capture.

If TShark is unavailable on your machine, record that fact rather than faking a
result; inspect `tests/test_tshark_ingestion.py` (instructor demonstration) or
the released public tests as directed in class.

### Exercise D — Make a scaling decision

Consider a hypothetical **10 GB pcapng research trace** containing IPv4/IPv6 and
several application protocols. Choose an ingestion path and justify the choice.
Your answer must discuss at least:

- capture format/protocol coverage;
- transparency versus mature dissection;
- streaming/memory behavior;
- what remains our responsibility after TShark has decoded packets.

### Exercise E — Find the abstraction boundary

Suppose next month we replace TShark with another packet engine. Which parts of
Labs 1-6 should ideally change? Which should not? Explain why `PacketRecord` is
an abstraction boundary rather than merely a convenient dataclass.

---

## 8. Exit check

You are ready to move on when you can explain all four statements without
looking them up:

1. **PCAP is a capture container; Ethernet/IP/TCP/UDP are decoded inside its packet records.**
2. **The educational parser exists to expose that decoding process.**
3. **The TShark path delegates mature dissection and can stream selected observations.**
4. **Both paths must satisfy the same `PacketRecord` contract, so representation design downstream is decoupled from ingestion.**

That separation becomes increasingly important later in the case study: the
research question is not “which library read my PCAP?” but **what information
did my representation preserve, discard, aggregate, or invent?**

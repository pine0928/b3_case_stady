# Dual Ingestion Tutorial — Student Worksheet

Name:  
Date:  
Environment / OS:  
TShark version (or `not installed`):  

## A. Trace one packet through the educational parser

| PacketRecord field | Source layer/header | Byte/header field or code step | My explanation |
|---|---|---|---|
| `timestamp` | | | |
| `src_ip`, `dst_ip` | | | |
| `src_port`, `dst_port` | | | |
| `protocol` | | | |
| `packet_length` | | | |
| `payload_length` | | | |
| `tcp_flags` | | | |

## B. Match the TShark extraction fields

| PacketRecord meaning | TShark field(s) | Stored or validation-only? |
|---|---|---|
| timestamp | | |
| addresses | | |
| protocol | | |
| packet length | | |
| transport ports | | |
| payload length | | |
| TCP flags | | |
| capture truncation check | | |

## C. Differential check

Command used:

```text
python -m labs.tools.compare_ingestion_paths
```

Observed result (or reason it could not be run):

> 

Why is this useful evidence, but not proof of universal equivalence?

> 

## D. 10 GB pcapng decision

Chosen ingestion path:

> 

Justification (format/protocol coverage, transparency vs mature dissection,
streaming/memory, and our remaining responsibilities):

> 

## E. Abstraction boundary

If TShark were replaced by another packet engine, what should change?

> 

What should remain unchanged in Labs 1-6, and why?

> 

## Exit statement

In 3-5 sentences, explain the design principle **understand first, scale second,
same PacketRecord contract** in your own words.

> 

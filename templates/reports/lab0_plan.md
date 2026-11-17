# Lab 0 Pre-lab Plan (optional preparation; not the final report)

## 1. Candidate packet fields

| Field | Observed / Derived / Metadata | Use as model input? | Reason |
|---|---|---|---|
| timestamp | observed | | |
| source/destination IP | # Lab 0 Pre-lab Plan (optional preparation; not the final report)

## 1. Candidate packet fields

| Field | Observed / Derived / Metadata | Use as model input? | Reason |
|---|---|---|---|
| timestamp | observed | | |
| source/destination IP | # Lab 0 Pre-lab Plan (optional preparation; not the final report)

## 1. Candidate packet fields

| Field | Observed / Derived / Metadata | Use as model input? | Reason |
|---|---|---|---|
| timestamp | observed | No | Absolute timestamps may reflect capture time or dataset-specific conditions rather than network behavior.|
| source/destination IP | observed | No | IP addresses may allow the model to memorize endpoints and exploit dataset-specific shortcuts. |
| source/destination port | observed | No | Port numbers may reveal application or service identities and cause shortcut learning.1~Port numbers may reveal application or service identities and cause shortcut learning. |
| protocol | observed | Yes | TCP/UDP is a basic property of packet behavior and may provide useful information. |
| direction | derived | Yes | Direction represents the relationship between packets in a flow and may capture communication patterns. |
| packet length | observed | Yes| Direction represents the relationship between packets in a flow and may capture communication patterns. |
| IAT | derived | Yes | Inter-arrival time captures temporal characteristics of packet sequences. |
| label | metadata | No | Labels are ground-truth information for training or evaluation and must not be used as input features. |

## 2. Initial model-input policy

Before seeing classification results, I would permit protocol, direction, packet length, and inter-arrival time (IAT) as initial model inputs.

I would exclude source/destination IP addresses and port numbers because they may introduce shortcut learning. A model could memorize specific endpoints or services instead of learning general network behavior.

Absolute timestamps would also be excluded because they may contain dataset-specific information. IAT would be used instead to represent relative timing between packets.

Labels would be used only as target information for training and evaluation, not as model inputs.

This is an initial policy and should be reviewed through experiments and further analysis.

## 3. Baseline parser scope

The Lab 0 baseline parser uses TShark to dissect PCAP/pcapng files and converts selected TSV fields into PacketRecord objects.

It supports unfragmented IPv4 TCP and UDP packets.

The parser extracts timestamps, source/destination IP addresses, ports, protocol, packet length, payload length, and TCP flags. It also rejects malformed rows, unsupported IP protocols, and snaplen-truncated packets.

The parser does not implement binary PCAP parsing or Ethernet, IP, TCP, or UDP dissection itself. IPv6, IP reassembly, application-layer parsing, inner VPN traffic, and QUIC stream semantics are outside the baseline scope.

IAT is calculated separately by sorting packets by timestamp and computing the time difference between consecutive packets.

## 4. Question for the next briefing

How should flow direction (forward and backward) be determined consistently when packets are observed in both directions?

Also, how can we ensure that IP addresses and port numbers do not introduce data leakage or shortcut learning during model evaluation?

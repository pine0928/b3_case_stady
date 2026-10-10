# Lab 0 Final Report — PCAP observation and PacketRecord mapping

Student / group: ____________________    Date: ____________________

## 1. Observation and field mapping

Describe one TCP and one UDP packet. For each, map the Wireshark field to its
TShark column and `PacketRecord` attribute. State which columns are empty.

## 2. Implementation and validation

Explain your `parse_tshark_row` and `inter_arrival_times` choices without
pasting all code. Include the command and result of the student public tests.
Explain one malformed/unsupported row and why it must be rejected.

## 3. Observation limitations

Explain snaplen truncation and at least one observation boundary. Distinguish
observed fields, derived features, and labels/metadata; justify which fields
could or should not become model inputs.

## 4. Remaining questions and next Lab

Record any unresolved issue and explain how `PacketRecord` will support Flow
construction in Lab 1.

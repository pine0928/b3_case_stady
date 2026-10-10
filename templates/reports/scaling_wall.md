# Scaling-Wall Experiment Worksheet

## 1. Prediction before running

If the capture becomes larger, predict how time and memory will change.

## 2. Measurement table

| capture | file size | packet count | wall-clock time | peak RSS | retained objects? | notes |
|---|---:|---:|---:|---:|---|---|
| tiny | | | | | | |
| medium | | | | | | |
| larger | | | | | | |

## 3. Code location of materialization

Paste or describe the line where decoded packets/rows are stored.

```python
# example
records.append(packet)
```

## 4. Causal explanation

Explain why memory grows. Do not only write "the PCAP is large".

## 5. State-retention question

When processing packet N, which information from packets 1..N-1 is still needed for your current task?

## 6. Transition to streaming

Explain why streaming becomes a reasonable next design.

# Golden Trace Worksheet — Flow and Burst Reasoning

Use this trace **before** running your program. The goal is to predict the state-machine result by hand and then use the program/tests to check your reasoning.

## Rules for this exercise

- One bidirectional FlowKey is formed from protocol plus the unordered endpoint pair.
- The source endpoint of the first observed packet defines FW; the reverse direction is BW. This is a convention, not a client/server claim.
- A direction change starts a new Burst.
- With `burst_gap_threshold = 1.0 s`, a same-direction packet starts a new Burst only when the gap is **strictly greater** than 1.0 s.
- TCP `idle_timeout = 60 s` for this worksheet.
- One FIN does not immediately end the Flow.

All packets below belong to `10.0.0.1:50000 <-> 10.0.0.2:443 TCP`.

| frame | time (s) | direction | TCP flags | length | your Flow ID | your Burst ID | why did a boundary occur? |
|---:|---:|:---:|:---|---:|:---:|:---:|:---|
| 1 | 0.0 | FW | SYN | 60 | | | |
| 2 | 0.1 | BW | SYN,ACK | 60 | | | |
| 3 | 0.2 | FW | ACK | 52 | | | |
| 4 | 0.3 | FW | — | 100 | | | |
| 5 | 0.5 | FW | — | 200 | | | |
| 6 | 0.6 | BW | — | 300 | | | |
| 7 | 2.0 | BW | — | 400 | | | |
| 8 | 2.1 | FW | FIN,ACK | 52 | | | |
| 9 | 2.2 | BW | ACK | 52 | | | |
| 10 | 2.3 | BW | FIN,ACK | 52 | | | |
| 11 | 2.4 | FW | ACK | 52 | | | |

## First prediction

Before coding, answer:

1. How many Flow instances are present?
2. Which endpoint is FW, and why?
3. How many Bursts are present?
4. Which boundary is caused by the 1.4 s gap?
5. Why does frame 8 not by itself terminate the Flow?
6. Why are SYN/ACK/FIN-only packets still part of the observation?

## Check Case A after making your prediction

Expected Burst groups:

```text
B0: FW [1]
B1: BW [2]
B2: FW [3,4,5]
B3: BW [6]
B4: BW [7]       # same direction, but 1.4 s > 1.0 s
B5: FW [8]
B6: BW [9,10]
B7: FW [11]
```

All frames belong to one Flow instance in this trace. Both directions' FINs are observed; the final ACK remains part of the same observed Flow during the closing grace period.

## Predict these cases before seeing hidden/automated checks

### B — One-sided FIN
What should happen if FW FIN is observed but BW FIN never appears? Explain why `FIN -> delete Flow` is unsafe.

### C — RST
Should the RST packet be included in the Flow before completion?

### D — Idle timeout and same 5-tuple reappearance
If the Flow is evicted after idle timeout and the same FlowKey later appears, is it the old Flow or a new Flow instance?

### E — UDP
What can terminate an observed UDP Flow when there is no FIN/RST?

### F — EOF
What does EOF completion tell you about the capture, and what does it *not* prove about the real connection?

### G — Equal timestamps
If timestamps tie, what observation should preserve packet order?

## Takeaway

Do not start from Python syntax. Start from the semantics:

```text
Trace -> predict state transitions -> implement -> test -> explain discrepancies
```

A passing test is evidence that your implementation follows a specified rule; it is not a substitute for understanding why that rule defines the Flow/Burst representation.

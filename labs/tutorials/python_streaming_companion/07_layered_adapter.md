# Step 7 — Separate infrastructure from domain meaning

**Matching code:** `labs/tutorials/python_streaming_steps/step7_*.py`  
**Python / Unix concepts:** separation of concerns, adapter, stable contract, dependency direction

## 1. Question
How do we stop TShark column positions and subprocess details from leaking into every later Lab?

Before reading further, write a one-sentence answer or prediction.

## 2. Mental model
Separate command construction, process/stream management, TSV parsing, and domain conversion. Expose `PacketRecord` as the stable boundary.

## 3. Micro example
```text
build command
   ↓
process / stream
   ↓
parse TSV row
   ↓
PacketRecord
   ↓
Flow / Burst / Representation
```

Do not merely copy it. Point to the object that owns the data/resource and say when it is created and released.

## 4. Code walkthrough
Open the matching Step 7 program. Read it in this order:

1. imports and external dependencies;
2. objects/resources created;
3. where data enters Python;
4. transformation performed;
5. where data leaves or is yielded;
6. cleanup and error path.

For every unfamiliar Python expression, first explain what *type of object* it produces. This is more useful than reading syntax aloud.

## 5. Run
Open `labs/common/tshark.py` and map each function/constant to one responsibility. Then compare its public interface with `pcap.py`.

## 6. Observe
Pretend TShark is replaced by another extractor. Mark which layers should change and which must not.

Record one concrete observation in the worksheet.

## 7. Think
Answer before moving on:

- What data exists in memory at this point?
- Which component knows the TSV/TShark details?
- What happens if the producer fails halfway through?
- Would the same design still be comfortable at 100 GB? Why?

## 8. Design trade-off
**What improved:** A good adapter localizes external-tool knowledge and protects the research representation pipeline.

**What remains:** There is still no universal best implementation: saved TSV, lists, or alternative decoders can be correct under different requirements.

An earlier design is not automatically wrong. State one situation in which you would deliberately keep it.

## 9. Route
Previous: [Step 6 — Expose records lazily with a generator](06_generator.md)  
Next: Worksheet / whole-path reflection

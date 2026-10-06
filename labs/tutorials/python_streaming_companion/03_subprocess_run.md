# Step 3 — Let Python launch TShark

**Matching code:** `labs/tutorials/python_streaming_steps/step3_*.py`  
**Python / Unix concepts:** parent/child process, `subprocess.run`, stdout, stderr, exit status

## 1. Question
Can one Python command reproduce the whole extraction automatically?

Before reading further, write a one-sentence answer or prediction.

## 2. Mental model
Python becomes the parent process. `run()` starts TShark, waits for it, and returns a `CompletedProcess`.

## 3. Micro example
```python
r = subprocess.run(cmd, capture_output=True, text=True, check=True)
print(r.stdout)
```

Do not merely copy it. Point to the object that owns the data/resource and say when it is created and released.

## 4. Code walkthrough
Open the matching Step 3 program. Read it in this order:

1. imports and external dependencies;
2. objects/resources created;
3. where data enters Python;
4. transformation performed;
5. where data leaves or is yielded;
6. cleanup and error path.

For every unfamiliar Python expression, first explain what *type of object* it produces. This is more useful than reading syntax aloud.

## 5. Run
Run Step 3 on `canonical_smoke.pcap`; then give it a nonexistent capture path.

## 6. Observe
Inspect successful stdout and the failure path. Explain `text=True` and `check=True`.

Record one concrete observation in the worksheet.

## 7. Think
Answer before moving on:

- What data exists in memory at this point?
- Which component knows the TSV/TShark details?
- What happens if the producer fails halfway through?
- Would the same design still be comfortable at 100 GB? Why?

## 8. Design trade-off
**What improved:** Simple automation is often the best design for bounded command output.

**What remains:** `capture_output=True` materializes the complete output; that is a bad default for huge packet streams.

An earlier design is not automatically wrong. State one situation in which you would deliberately keep it.

## 9. Route
Previous: [Step 2 — Read TSV as a Python stream](02_python_tsv.md)  
Next: [Step 4 — Keep the child alive and stream stdout](04_popen_pipe.md)

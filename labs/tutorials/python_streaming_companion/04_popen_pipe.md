# Step 4 — Keep the child alive and stream stdout

**Matching code:** `labs/tutorials/python_streaming_steps/step4_*.py`  
**Python / Unix concepts:** `Popen`, `PIPE`, process lifetime, EOF, `wait`, stderr

## 1. Question
What changes if output is too large to collect before parsing?

Before reading further, write a one-sentence answer or prediction.

## 2. Mental model
`Popen()` returns while TShark is still alive. A pipe connects child stdout to the parent, so Python can consume data incrementally.

## 3. Micro example
```python
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
for line in p.stdout:
    consume(line)
rc = p.wait()
```

Do not merely copy it. Point to the object that owns the data/resource and say when it is created and released.

## 4. Code walkthrough
Open the matching Step 4 program. Read it in this order:

1. imports and external dependencies;
2. objects/resources created;
3. where data enters Python;
4. transformation performed;
5. where data leaves or is yielded;
6. cleanup and error path.

For every unfamiliar Python expression, first explain what *type of object* it produces. This is more useful than reading syntax aloud.

## 5. Run
Run Step 4. Before the loop ends, identify which process is alive and which object represents the pipe.

## 6. Observe
Add a counter and print only every second line. Explain EOF and why the exit code still matters.

Record one concrete observation in the worksheet.

## 7. Think
Answer before moving on:

- What data exists in memory at this point?
- Which component knows the TSV/TShark details?
- What happens if the producer fails halfway through?
- Would the same design still be comfortable at 100 GB? Why?

## 8. Design trade-off
**What improved:** Streaming changes the memory boundary: output need not exist as one giant Python string.

**What remains:** Process control, error handling, and parsing can become tangled.

An earlier design is not automatically wrong. State one situation in which you would deliberately keep it.

## 9. Route
Previous: [Step 3 — Let Python launch TShark](03_subprocess_run.md)  
Next: [Step 5 — Use the same parser on a live pipe](05_csv_pipe.md)

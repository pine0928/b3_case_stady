# Step 5 — Use the same parser on a live pipe

**Matching code:** `labs/tutorials/python_streaming_steps/step5_*.py`  
**Python / Unix concepts:** iterables, file-like streams, separation of source from format

## 1. Question
Do we need a second TSV parser just because rows now come from a pipe?

Before reading further, write a one-sentence answer or prediction.

## 2. Mental model
No. `csv.reader` needs an iterable of text lines. A disk file and `proc.stdout` satisfy the same useful interface.

## 3. Micro example
```python
reader = csv.reader(proc.stdout, delimiter="\t")
for row in reader:
    consume(row)
```

Do not merely copy it. Point to the object that owns the data/resource and say when it is created and released.

## 4. Code walkthrough
Open the matching Step 5 program. Read it in this order:

1. imports and external dependencies;
2. objects/resources created;
3. where data enters Python;
4. transformation performed;
5. where data leaves or is yielded;
6. cleanup and error path.

For every unfamiliar Python expression, first explain what *type of object* it produces. This is more useful than reading syntax aloud.

## 5. Run
Compare Step 2 and Step 5 side by side. Circle the code concerned with TSV syntax and underline the code concerned with I/O source.

## 6. Observe
Write a tiny `io.StringIO("a\tb\n")` example and feed it to `csv.reader`.

Record one concrete observation in the worksheet.

## 7. Think
Answer before moving on:

- What data exists in memory at this point?
- Which component knows the TSV/TShark details?
- What happens if the producer fails halfway through?
- Would the same design still be comfortable at 100 GB? Why?

## 8. Design trade-off
**What improved:** Program to the smallest useful abstraction: iterable text lines, not “disk file”.

**What remains:** Even a streaming input can be defeated if downstream accumulates every row.

An earlier design is not automatically wrong. State one situation in which you would deliberately keep it.

## 9. Route
Previous: [Step 4 — Keep the child alive and stream stdout](04_popen_pipe.md)  
Next: [Step 6 — Expose records lazily with a generator](06_generator.md)

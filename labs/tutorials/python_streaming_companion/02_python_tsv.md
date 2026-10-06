# Step 2 — Read TSV as a Python stream

**Matching code:** `labs/tutorials/python_streaming_steps/step2_*.py`  
**Python / Unix concepts:** `with`, file objects, iteration, `csv.reader`, delimiter

## 1. Question
How should Python consume the inspectable TSV without writing a fragile parser?

Before reading further, write a one-sentence answer or prediction.

## 2. Mental model
A file object is both a managed resource and an iterable source of text lines. `csv.reader` converts that line stream into rows.

## 3. Micro example
```python
with open("packets.tsv", newline="") as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        print(row)
```

Do not merely copy it. Point to the object that owns the data/resource and say when it is created and released.

## 4. Code walkthrough
Open the matching Step 2 program. Read it in this order:

1. imports and external dependencies;
2. objects/resources created;
3. where data enters Python;
4. transformation performed;
5. where data leaves or is yielded;
6. cleanup and error path.

For every unfamiliar Python expression, first explain what *type of object* it produces. This is more useful than reading syntax aloud.

## 5. Run
Run Step 2 on the TSV from Step 1. Put a breakpoint or temporary print inside the loop.

## 6. Observe
Explain when the file opens/closes. Replace `delimiter="\t"` with a comma and observe the result.

Record one concrete observation in the worksheet.

## 7. Think
Answer before moving on:

- What data exists in memory at this point?
- Which component knows the TSV/TShark details?
- What happens if the producer fails halfway through?
- Would the same design still be comfortable at 100 GB? Why?

## 8. Design trade-off
**What improved:** Use a standard parser and make resource lifetime explicit.

**What remains:** TShark and Python are still manually coordinated.

An earlier design is not automatically wrong. State one situation in which you would deliberately keep it.

## 9. Route
Previous: [Step 1 — CLI to an inspectable TSV](01_cli_tsv.md)  
Next: [Step 3 — Let Python launch TShark](03_subprocess_run.md)

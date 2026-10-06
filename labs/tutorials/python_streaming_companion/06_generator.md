# Step 6 — Expose records lazily with a generator

**Matching code:** `labs/tutorials/python_streaming_steps/step6_*.py`  
**Python / Unix concepts:** iterator protocol, generator, `yield`, `next`, lazy evaluation

## 1. Question
How can downstream request records one at a time instead of receiving a complete list?

Before reading further, write a one-sentence answer or prediction.

## 2. Mental model
A generator suspends at `yield` and resumes when the consumer requests another item. It defines when materialization happens.

## 3. Micro example
```python
def records():
    for row in rows:
        yield make_record(row)

g = records()
first = next(g)
```

Do not merely copy it. Point to the object that owns the data/resource and say when it is created and released.

## 4. Code walkthrough
Open the matching Step 6 program. Read it in this order:

1. imports and external dependencies;
2. objects/resources created;
3. where data enters Python;
4. transformation performed;
5. where data leaves or is yielded;
6. cleanup and error path.

For every unfamiliar Python expression, first explain what *type of object* it produces. This is more useful than reading syntax aloud.

## 5. Run
Run the micro example first, then Step 6. Call `next()` once before using a `for` loop.

## 6. Observe
Compare `g = records()` with `list(records())`. State exactly which one materializes all records.

Record one concrete observation in the worksheet.

## 7. Think
Answer before moving on:

- What data exists in memory at this point?
- Which component knows the TSV/TShark details?
- What happens if the producer fails halfway through?
- Would the same design still be comfortable at 100 GB? Why?

## 8. Design trade-off
**What improved:** Lazy interfaces compose naturally with large sequential pipelines.

**What remains:** A generator only bounds the stage that stays lazy; downstream can still consume unbounded memory.

An earlier design is not automatically wrong. State one situation in which you would deliberately keep it.

## 9. Route
Previous: [Step 5 — Use the same parser on a live pipe](05_csv_pipe.md)  
Next: [Step 7 — Separate infrastructure from domain meaning](07_layered_adapter.md)

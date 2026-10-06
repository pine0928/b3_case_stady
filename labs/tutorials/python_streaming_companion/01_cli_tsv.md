# Step 1 — CLI to an inspectable TSV

**Matching code:** `labs/tutorials/python_streaming_steps/step1_*.py`  
**Python / Unix concepts:** CLI, stdout redirection, TSV as an intermediate representation

## 1. Question
Why begin with a file instead of connecting everything immediately?

Before reading further, write a one-sentence answer or prediction.

## 2. Mental model
`tshark` is one process. The shell redirects its standard output to `packets.tsv`. Nothing in TShark needs to know Python exists.

## 3. Micro example
```bash
tshark ... -T fields ... > packets.tsv
head packets.tsv
```

Do not merely copy it. Point to the object that owns the data/resource and say when it is created and released.

## 4. Code walkthrough
Open the matching Step 1 program. Read it in this order:

1. imports and external dependencies;
2. objects/resources created;
3. where data enters Python;
4. transformation performed;
5. where data leaves or is yielded;
6. cleanup and error path.

For every unfamiliar Python expression, first explain what *type of object* it produces. This is more useful than reading syntax aloud.

## 5. Run
Run the Step 1 module, copy the printed command, execute it, then open the first three rows.

## 6. Observe
Count columns; identify one packet per row; deliberately change one `-e` field and observe the schema change.

Record one concrete observation in the worksheet.

## 7. Think
Answer before moving on:

- What data exists in memory at this point?
- Which component knows the TSV/TShark details?
- What happens if the producer fails halfway through?
- Would the same design still be comfortable at 100 GB? Why?

## 8. Design trade-off
**What improved:** A visible intermediate file creates an excellent debugging boundary.

**What remains:** The file can become enormous and the workflow still requires a separate Python command.

An earlier design is not automatically wrong. State one situation in which you would deliberately keep it.

## 9. Route
Previous: Start of route  
Next: [Step 2 — Read TSV as a Python stream](02_python_tsv.md)

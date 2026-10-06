# Lab 6 - Open Representation Design Project

## Goal
Conduct a small end-to-end representation research project from task/PCAP definition to a bounded scientific claim. There is deliberately no canonical winning representation and no requirement to use a graph.

## Reading order
At this stage, read this Lab's README and `SPECIFICATION.md`, then revisit the evidence you produced in Lab 5. You do not need to read later-Lab material yet.

## Implementation Specification
Before coding, read `labs/lab6_open_project/SPECIFICATION.md`. It is the authoritative baseline contract for definitions, function/artifact behavior, edge cases, the tiny worked example, and what the public tests do or do not certify.

## What to Read
- `labs/lab6_open_project/RUBRIC.md`
- all files under `labs/lab6_open_project/templates/`
- your Lab 5 experimental-audit report
- the closest prior representation paper(s) selected for your project

## What to Do
Proceed in this order and freeze each design decision before the next stage where feasible:
1. **Problem and measurement contract** - complete `PROJECT_BRIEF.md` before model training.
2. **Closest prior representation** - complete `PRIOR_ART_AND_CLAIM.md`; identify the smallest meaningful design delta.
3. **Representation design record** - complete `REPRESENTATION_CARD.md`; graph designs must define nodes, all edge types and P/O/B/A/L/H provenance, D0-D4 level, and N1-N7 profile.
4. **Falsification-first plan** - complete `EXPERIMENT_PLAN.md` before the main experiment. Include matched-information baseline, representation ablation, capacity/control comparison, leakage/split checks, and at least one perturbation/failure test.
5. **Implementation and evidence** - reuse Labs 0-5 infrastructure where appropriate; record any intentional delta from frozen contracts.
6. **Claim audit** - complete `FINAL_REPORT.md`; distinguish evidence-supported conclusions from what remains unproven.

## How to Test
Use the relevant Lab 0-5 public tests plus the submission validator:

```bash
python -m pytest -q tests_public
python -m labs.lab6_open_project.validate_submission lab6_submission
```

Passing the validator checks package completeness, not research validity.

## What to Submit
```text
lab6_submission/
├── PROJECT_BRIEF.md
├── PRIOR_ART_AND_CLAIM.md
├── REPRESENTATION_CARD.md
├── EXPERIMENT_PLAN.md
├── FINAL_REPORT.md
├── reproducibility.json
├── src/
└── results/
```
Create `reproducibility.json` from the provided example and record capture provenance/checksum, code revision, split policy, seeds, preprocessing parameters, observable/representation budgets, and environment/package versions.

## What to Present
Final presentation: Research Question -> Measurement/Dataset -> Representation Hypothesis -> Preservation/Loss -> Closest Comparator -> Experimental Design -> Results -> Falsification/Ablation -> What I Can Claim -> What I Cannot Claim -> Next Question.

## Exit Condition
The submission validator passes, the repository revision reproduces the reported evidence, the matched comparator and falsification plan were actually executed (or failures are explicitly documented), and the final claim is bounded by that evidence.

## Claim Boundary
**You may claim:** the smallest conclusion directly supported by your documented measurements, controls, ablations, and failure cases.

**You may not claim:** novelty or superiority beyond the examined prior art/controls, generalization beyond the evaluated setting, or "Graph is better" merely because a graph model scored higher.

A negative result, or a conclusion that a simpler non-graph representation is preferable, is a valid outcome.

# Lab 6 Specification -- Open Representation Design Project

## Purpose and scope
Lab 6 is a capstone research project. Unlike Labs 0--5, there is no canonical "best" representation. The specification fixes the **research-process artifacts and evidence contract**, not the research answer.

## Canonical definitions
A complete project contains:

```text
PROJECT_BRIEF.md
PRIOR_ART_AND_CLAIM.md
REPRESENTATION_CARD.md
EXPERIMENT_PLAN.md
FINAL_REPORT.md
reproducibility.json
src/
results/
```

The five Markdown files must be based on the provided templates. `reproducibility.json` must record enough metadata to identify code revision, environment, data/capture source, split, seeds, preprocessing, raw observable budget, and representation budget.

## Artifact contracts
### `PROJECT_BRIEF.md`
State task, research question, dataset/capture, motivation, success/failure criteria, and a narrow scope feasible before the final deadline.

### `PRIOR_ART_AND_CLAIM.md`
Name the closest prior representation/baseline. Separate what is inherited from what is changed. State the proposed claim in bounded language and identify the evidence needed to support it.

### `REPRESENTATION_CARD.md`
Declare raw observables, aggregation units, preservation/loss, truncation/input budget, and model input. For graph designs also declare node unit, edge semantics, P/O/B/A/L/H provenance, D0--D4 dynamic level, N1--N7 novelty profile, and a plausible non-graph equivalent.

### `EXPERIMENT_PLAN.md`
Written **before** the main result. Include matched-information comparator, representation ablation, model-capacity control, leakage check, and at least one perturbation/failure test. Include the sentence form: "My hypothesis is X. If Y happens, my hypothesis is not supported."

### `FINAL_REPORT.md`
Report method, evidence, negative results, ablations, limitations, `What I can claim`, `What I cannot claim`, and next research question. Do not rewrite the hypothesis after seeing the results without documenting the change.

### `reproducibility.json`
Required top-level keys:
- `capture`
- `code_revision`
- `environment`
- `split`
- `random_seeds`
- `preprocessing`
- `raw_observable_budget`
- `representation_budget`

### `src/` and `results/`
`src/` contains student-owned code needed to reproduce the experiment. `results/` contains compact machine-readable or figure/table outputs referenced by the report. Large PCAP/dataset files should not be committed unless explicitly permitted; document source/checksum instead.

## Edge cases and failure modes
- Negative result is acceptable; unsupported positive claim is not.
- Graph is optional. Choosing a non-graph representation can be the correct design decision.
- Changing dataset, labels, split, observable budget, or main hypothesis after viewing results must be disclosed.
- A mechanical validator PASS means required files/keys exist; it does not certify novelty, correctness, ethics, or scientific validity.
- If real PCAP contains sensitive or non-shareable data, submit metadata/checksum/reproduction instructions rather than the raw capture.

## Tiny worked example
Example bounded project:

```text
RQ: Does explicit burst membership improve early encrypted-traffic classification
    under the same first-20-packet observation budget?
Baseline: first-20 directional packet sequence
Proposal: packet-burst hierarchy built from the same packets
Falsifier: if matched sequence + burst-segment mask matches the hierarchy result,
           graph/hierarchy-specific superiority is not supported.
```

This is a valid project even if the final result shows no improvement.

## Public-test alignment
The public test verifies that required templates/validator exist. `validate_submission.py` checks required files/directories and reproducibility keys. It intentionally does not grade scientific quality. Milestone reviews and the final seminar apply the rubric to reasoning/evidence.

## Lecture-material boundary
Briefings provide examples of good research questions, baselines, falsification, graph novelty taxonomy, and claim boundaries. The specification fixes deliverables and minimum controls while leaving the student's hypothesis, representation, and outcome open.

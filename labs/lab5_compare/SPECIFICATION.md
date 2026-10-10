# Lab 5 Specification -- Matched-Information Comparison

## Purpose and scope
Lab 5 introduces learners only after representation contracts are frozen. Its central contract is fairness: compared representations must not silently receive different raw observations.

## Canonical definitions
Canonical raw observable set:

```text
{"direction", "packet_length", "iat"}
```

A burst partition or graph edge built only from these observations is a **derived structure**, not an additional raw observable.

Three possible explanations for a score difference:
1. **Information advantage** -- one system sees extra raw data/context.
2. **Representation advantage** -- raw budget is matched, but organization/exposure differs.
3. **Model advantage** -- representation is fixed, but learner capacity/optimization differs.

If controls do not separate these, classify the result as **confounded**.

## Function contracts
### `observable_budget(config) -> set[str]`
Return exactly the raw observable names declared by `RepresentationConfig.observables`. No inference from representation name.

### `assert_matched_budget(config_a, config_b, ...)`
- fewer than two configs -> no error;
- all observable sets equal -> return normally;
- any mismatch -> raise `ValueError` whose message identifies mismatched configs/budgets.

### `vectorize_your_representation(flow)`
- return a finite, fixed-length numeric vector for every flow in the chosen experiment;
- document dimension and feature blocks;
- use only pre-declared raw observables;
- derived relation features are allowed but must be labeled and ablated;
- no labels, sample IDs, split IDs, source file names, or endpoint identifiers may leak into features unless explicitly approved as a separate information-budget experiment.

### `explain_advantage_type() -> str`
Return one of the documented interpretation labels (information / representation / model / confounded) with the reasoning written in the report. The string itself is not scientific evidence; it records your conclusion after controls.

## Experimental contracts
- split before fitting scalers/normalizers;
- report train/test sizes and class counts;
- use fixed seeds and report them;
- compare at least one graph/hierarchical and one non-graph representation under a common learner;
- hold representation fixed for at least one learner-capacity comparison;
- run at least one relation/representation ablation;
- report input dimension and, for learned models, parameter count where meaningful;
- check for exact/obvious split leakage in the synthetic setting.

## Edge cases and failure modes
- Equal accuracy does not prove equivalent representations.
- Higher accuracy with more raw fields is an information advantage until controlled.
- "Same model family" does not guarantee matched parameter count when input dimensions differ.
- A relation feature computed from a sequence may exactly reproduce a graph relation summary; this is evidence against claiming graph-exclusive information.
- The provided synthetic dataset is a diagnostic microscope, not a real-world benchmark.

## Tiny worked example
Config A:

```text
packet sequence observables = {direction, packet_length, iat}
```

Config B:

```text
packet-chain graph observables = {direction, packet_length, iat}
```

Budgets match. If B adds `src_port`, the comparison is no longer matched and `assert_matched_budget` must reject it.

Suppose a graph relation block improves linear Macro-F1. Before calling this a graph advantage, compute the same adjacent-packet relation summary directly from the ordered sequence. If the non-graph control reproduces the vector and score, the supported conclusion is "explicit relation engineering helps this learner on this toy task", not "graphs are intrinsically superior".

## Public-test alignment
Public environment tests check the canonical observable set and that the supplied dataset/harness can execute a simple vectorizer. Public student tests check observable-budget handling, mismatched-budget rejection, fixed finite vector dimensions, and the interpretation-label vocabulary. They do not certify fairness of the student's full experiment. Seminar/report review plus instructor tests inspect budget matching, controls, dimensions, seeds, leakage, and interpretation.

## Lecture-material boundary
Lecture/seminar material covers causal interpretation, fairness, confounding, robustness, and why a result can be scientifically useful even when the proposed representation loses. The specification defines minimum experimental controls, not a target accuracy.

## Horizon and retention caveat
Equal raw field names do not ensure equal information exposure: first-k packet truncation and full-flow statistics have different observation horizons. Record packet retention/horizon for each comparison, or match horizons explicitly before attributing an effect to representation.

# Falsification-first experiment plan

## Main hypothesis
State one bounded hypothesis about representation, not just expected accuracy.

## Controls
| ID | Raw observable budget | Representation | Learner/capacity | Purpose |
|---|---|---|---|---|
| C0 | | | | simplest baseline |
| C1 | | | | matched-information comparator |
| C2 | | | | representation ablation |
| C3 | | | | model-capacity control |

## Split/leakage audit
- Group/time split:
- Duplicate/near-duplicate check:
- Train-only preprocessing/scaling:

## Representation ablations
- Remove/replace which structure?
- What explanation does each ablation test?

## Robustness/failure test
- Perturbation or subgroup:
- Why it is relevant:
- Expected failure if the representation relies on a shortcut:

## Reporting
- Primary + secondary metrics:
- Seeds/repetitions:
- Parameter count/input dimension:
- Preprocessing/training/inference cost:
- Input/prefix budget:

"""Run the Lab 5 matched-information comparison."""
from __future__ import annotations
from .experiment import run_experiment


def main():
    results = run_experiment(protocol="practical-budget")
    print("representation                         learner  dim   accuracy  macro-F1")
    print("-" * 79)
    for r in results:
        print(f"{r.representation:38s} {r.learner:7s} {r.n_features:4d}   {r.metrics.accuracy:8.3f}  {r.metrics.macro_f1:8.3f}")
    matched = run_experiment(protocol="matched-horizon", packet_limit=8)
    print("\nMatched-horizon (same first 8 input packets; internal caps adjusted to k):")
    for r in matched:
        print(f"{r.representation:38s} {r.learner:7s} {r.n_features:4d}   {r.metrics.accuracy:8.3f}  {r.metrics.macro_f1:8.3f}")
    print("\nInterpretation rule:")
    print("  1. canonical rows use direction, packet_length, IAT only;")
    print("  1a. matched-horizon uses the same first-k input packets; practical-budget uses representation-specific caps;")
    print("  1b. matching observations does not guarantee equal model capacity or information preservation;")
    print("  2. graph '*-no-relations' rows ablate explicit relational summaries;")
    print("  3. linear -> MLP change holds representation fixed and probes model advantage;")
    print("  4. representation comparisons never prove a causal advantage by themselves.")

if __name__ == "__main__":
    main()

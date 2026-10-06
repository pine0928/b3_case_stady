"""Run the Lab 5 matched-information comparison."""
from __future__ import annotations
from .experiment import run_experiment


def main():
    results = run_experiment()
    print("representation                         learner  dim   accuracy  macro-F1")
    print("-" * 79)
    for r in results:
        print(f"{r.representation:38s} {r.learner:7s} {r.n_features:4d}   {r.metrics.accuracy:8.3f}  {r.metrics.macro_f1:8.3f}")
    print("\nInterpretation rule:")
    print("  1. canonical rows have matched raw observable budgets;")
    print("  2. graph '*-no-relations' rows ablate explicit relational summaries;")
    print("  3. linear -> MLP change holds representation fixed and probes model advantage;")
    print("  4. representation comparisons never prove a causal advantage by themselves.")

if __name__ == "__main__":
    main()

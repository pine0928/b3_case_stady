from pathlib import Path

def test_lab6_required_templates_exist():
    base = Path("labs/lab6_open_project")
    required = [
        "README.md", "SPECIFICATION.md", "RUBRIC.md", "validate_submission.py",
        "templates/PROJECT_BRIEF.md", "templates/PRIOR_ART_AND_CLAIM.md",
        "templates/REPRESENTATION_CARD.md", "templates/EXPERIMENT_PLAN.md",
        "templates/FINAL_REPORT.md", "templates/reproducibility.example.json",
    ]
    for rel in required:
        assert (base / rel).exists(), rel

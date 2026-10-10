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


def test_lab6_validator_rejects_incomplete_submission(tmp_path):
    from labs.lab6_open_project.validate_submission import validate
    assert any("PROJECT_BRIEF.md" in error for error in validate(tmp_path))

def test_lab6_validator_rejects_untouched_template(tmp_path):
    from labs.lab6_open_project.validate_submission import validate
    import json
    base = Path("labs/lab6_open_project/templates")
    for name in ["PROJECT_BRIEF.md", "PRIOR_ART_AND_CLAIM.md", "REPRESENTATION_CARD.md", "EXPERIMENT_PLAN.md", "FINAL_REPORT.md"]:
        (tmp_path / name).write_text((base / name).read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "reproducibility.json").write_text((base / "reproducibility.example.json").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "results").mkdir()
    assert any("unchanged template" in error for error in validate(tmp_path))

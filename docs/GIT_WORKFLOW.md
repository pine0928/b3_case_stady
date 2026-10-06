# Git workflow for students

This document is the canonical Git workflow for this course.

## Repository model

Clone the instructor-managed Course repository once. All Labs are already present. A personal GitHub repository is **not required** unless the instructor explicitly asks for one.

```bash
git clone <COURSE-REPOSITORY-URL> network-behavior-analysis-course
cd network-behavior-analysis-course
git status
```

The Course repository is the starting snapshot. During normal Lab work, Git is primarily used locally to record your own checkpoints.

## Normal work

```bash
git status
git diff

# edit / experiment / test

git status
git diff
git add -A
git status
git commit -m "Describe the work completed"
git log --oneline --decorate -5
```

Always inspect `git status` and `git diff` before committing.

## Course updates

All Labs are available from Day 1, so there is no routine weekly Lab-material merge. If the instructor announces a correction to the Course repository, follow the specific update instructions given for that correction; do not guess a merge/reset command.

## Reference solutions

Reference solutions are published separately as the class progresses. Do not copy them into earlier commits to rewrite your work history. Use them to compare, review, and learn after completing the corresponding Lab.

## Commands not used as routine operations

Students normally do **not** run `git init`; the cloned repository already contains Git history. Do not use `git reset --hard`, force-push, or history rewriting as a routine fix. Ask before using destructive recovery commands.

## Data policy

Do not commit large/raw captures unless explicitly approved. Record provenance, collection/license conditions, checksums, and preprocessing notes in the appropriate data documentation.

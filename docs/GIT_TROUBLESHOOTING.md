# Git troubleshooting

Before attempting recovery, stop and inspect:

```bash
git status
git log --oneline --decorate -8
git diff
git diff --staged
```

Do not use `git reset --hard`, force-push, or delete `.git` unless the instructor explicitly directs you to do so. Preserve evidence first; recovery should be deliberate.

# Git collaboration policy

`main` is the protected, always-green integration branch. Use an open GitHub
Issue, a short-lived matching branch (`proof/<issue>-<summary>` for proof work),
an Issue-first commit/PR title, and a reviewed PR to merge. The documented
repository-bootstrap exception is `chore: repository bootstrap ...` and must
state why no Issue exists.

```bash
git switch main
git pull --ff-only origin main
git switch -c proof/142-posterior-normalization
lake build
lake env lean ESeries/CheckAxioms.lean
python scripts/check_public_release.py
git add <paths>
git diff --cached
git commit
git push -u origin proof/142-posterior-normalization
```

Refresh private topic branches with `git fetch origin` and
`git rebase origin/main`; never rebase or force-push `main`. Resolve conflicts
deliberately and abort an uncertain rebase. Revert published changes instead of
rewriting them. Tags are annotated from a verified `main` revision; no release
or deployment workflow is configured.

The repository must never contain `.lake` output, cache state, generated logs,
secrets, local paths, data, checkpoints, or archives holding them. Main branch
protection must require a review and the stable `ci / required` check.

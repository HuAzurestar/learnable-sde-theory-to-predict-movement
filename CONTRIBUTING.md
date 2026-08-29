# Contributing

## Build and audit

Before opening a pull request, run:

```bash
lake build
lake env lean ESeries/CheckAxioms.lean
python scripts/check_public_release.py
```

For ordinary work, create or triage one public GitHub Issue with one primary
type (`feature`, `bug`, `documentation`, `refactor`, `performance`, `test`,
`build`, `ci`, `maintenance`, or `proof`). Start from protected `main` on a
short-lived `<prefix>/<issue>-<summary>` branch; `proof/<issue>-<summary>` is
reserved for theorem/proof work. Commit and PR titles use
`#<issue> <type>(optional-scope): imperative summary`, and the type must match
the branch prefix. `chore: repository bootstrap ...` is the sole documented
no-Issue exception. Open a focused reviewed PR to `main` with `Refs: #<issue>`
or `Closes: #<issue>` and the actual command results. Do not force-push or
delete `main`; prefer squash merge and delete the merged topic branch.

See `GIT_WORKFLOW.md` for sync, conflict recovery, hotfix, and release rules.

New theorems must not use `sorry`, project-defined axioms, or undocumented
assumptions. If a proof requires a new analytic assumption, state it explicitly
in the theorem signature and update `FORMALIZATION_SCOPE.md`.

## Proof changes

- Prefer Mathlib definitions and lemmas over parallel local abstractions.
- Keep theorem names stable unless the pull request documents the migration.
- Add the declaration to `ESeries/CheckAxioms.lean` when it belongs to the public
  audit surface.
- Explain any new noncomputable choice, classical reasoning, or additional axiom
  dependency in the pull request.
- Do not commit `.lake/`, cache output, generated logs, or editor state.

## Commit messages

Use `#<issue> <type>(optional-scope): imperative summary` with one conceptual
change per commit. Common types are `feat`, `fix`, `refactor`, `test`, `docs`,
`build`, `ci`, `chore`, and `proof`.

Examples:

```text
#142 proof(evidence): formalize posterior weight normalization
#87 fix(e8): add the missing balanced-prior assumption
#203 docs: clarify the PDE formalization boundary
```

Include `Refs: #12`; use `Closes: #12` only when the default-branch merge should
close it. Do not include private work item identifiers, workstation paths, or
generated proof logs.

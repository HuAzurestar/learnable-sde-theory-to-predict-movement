# Contributing

## Build and audit

Before opening a pull request, run:

```bash
lake build
lake env lean ESeries/CheckAxioms.lean
python scripts/check_public_release.py
```

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

Use `<type>(optional-scope): imperative summary` with one conceptual change per
commit. Common types are `feat`, `fix`, `refactor`, `test`, `docs`, `build`, and
`chore`.

Examples:

```text
feat(evidence): formalize posterior weight normalization
fix(e8): add the missing balanced-prior assumption
docs: clarify the PDE formalization boundary
```

Reference public GitHub issues such as `Closes #12`. Do not include private work
item identifiers, workstation paths, or generated proof logs.

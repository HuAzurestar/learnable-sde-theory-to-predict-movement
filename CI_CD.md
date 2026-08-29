# CI/CD guide

This guide describes the repository workflows. A workflow badge or check is
evidence only for the exact GitHub commit and event it names; no outcome for a
remote run is implied here.

## When workflows run

`CI` runs for pushes to `main`, pull requests targeting `main`, and manual
`workflow_dispatch` runs with read-only repository permission.

`Release` may be run manually to reproduce a build. A GitHub Release is
published only when the workflow runs from a `v*` tag ref. Only its publish job
has `contents: write`; a non-tag manual run cannot publish an asset.

## CI jobs

| Job shown in GitHub | What it verifies | Why it exists |
| --- | --- | --- |
| `policy / traceability and public boundary` | On pull requests, checks the traceable title/branch convention; on every trigger, runs the public-release scan. | Preserves review traceability and prevents material outside the public boundary from entering the build. |
| `lean / pinned build and proof audit` | Builds the package through the pinned Lean/Lake setup, then runs `scripts/audit_proofs.py`. The audit rejects `sorry`, `admit`, custom `axiom`, and `opaque` declarations and checks the designated theorem dependency reports. | Ensures the formalization compiles and that its stated proof and axiom boundary is mechanically enforced. |
| `ci / required` | Runs even after an upstream failure and passes only if both `policy` and `lean` finish successfully. | Supplies branch protection with a single, readable required result. |

The proof audit permits only the standard logical assumptions specified by the
repository audit; a `sorryAx` dependency or any other unapproved assumption is
a failure. The precise scope is documented in
[FORMALIZATION_SCOPE.md](FORMALIZATION_SCOPE.md).

## Release outputs

For a `v*` tag, `Release` rebuilds from the pinned source, runs the placeholder
and axiom audit, runs the public-release scan, and packages the formalization
source plus its pinned manifest/toolchain and audit report. The output is first
stored as a short-lived Actions artifact.

The tag-only publish job creates `SHA256SUMS` for the source archive and
`axiom-audit.txt`, then attaches those files and the archive to the GitHub
Release. Verify downloaded files with `sha256sum -c SHA256SUMS` in the release
asset directory.

## Data boundary

This repository publishes Lean source, manifests, and audit evidence, not
trajectory data, raw observations, identifiers, predictions, model weights, or
checkpoints. Such material must not be added to the repository, CI artifacts,
or Release assets.

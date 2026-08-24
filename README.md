# Learnable SDE Theory to Predict Movement

Lean 4 formalization of the finite-measure and algebraic core used by the
soft-evidence and dual-conditioning theory associated with Learnable SDE.

The repository contains complete proofs for its stated scope: there are no
project-defined axioms and no `sorry` placeholders in theorem bodies. Analytic
PDE existence, uniqueness, and Doob h-transform results are outside the current
formalization boundary; see [FORMALIZATION_SCOPE.md](FORMALIZATION_SCOPE.md).

## Toolchain

- Lean 4.33.0, pinned by `lean-toolchain`;
- Mathlib v4.33.0, pinned by `lake-manifest.json`;
- Lake configuration in `lakefile.toml`.

## Build

Install Lean through `elan`, then run:

```bash
lake exe cache get
lake build
```

The cache step is optional but substantially reduces the first build time.

## Axiom audit

```bash
lake env lean ESeries/CheckAxioms.lean
```

The printed dependency lists should contain only Lean's standard logical axioms
such as `propext`, `Classical.choice`, and `Quot.sound`. CI rebuilds the library
and runs this audit from source; generated build logs are intentionally not
versioned.

## Formalized results

| Result | Lean declaration | File |
|---|---|---|
| Soft-evidence posterior mixture identity | `posterior_mixture` | `ESeries/Basic.lean` |
| Likelihood-ratio form of the posterior weight | `weight_likelihood_ratio` | `ESeries/Basic.lean` |
| Total-variation mixture bound | `mixture_tv_bound` | `ESeries/Basic.lean` |
| Logistic weight range, slope, and monotonicity | `weight_mem_Icc`, `weight_slope_bound`, `weight_mono` | `ESeries/Basic.lean` |
| Existence/exclusion complement identity | `prob_compl_identity` | `ESeries/Basic.lean` |
| Weight and TV Lipschitz bounds | `e6_weight_lipschitz`, `e6_tv_lipschitz` | `ESeries/Basic.lean` |
| Evidence-pattern weight ratio | `weight_ratio_eq` | `ESeries/E8.lean` |
| Nested evidence concentration identity | `nested_concentration` | `ESeries/E8.lean` |

## Repository layout

```text
ESeries.lean                 library entry point
ESeries/Basic.lean           soft-evidence and TV results
ESeries/E8.lean              evidence-pattern concentration results
ESeries/CheckAxioms.lean     reproducible axiom audit
lakefile.toml                Lake package definition
lean-toolchain               pinned Lean toolchain
lake-manifest.json           pinned dependency graph
```

## Related software

The executable Python framework is maintained in
[learnable-sde-for-movement-prediction](https://github.com/HuAzurestar/learnable-sde-for-movement-prediction).

## Contributing, citation, and release

See [CONTRIBUTING.md](CONTRIBUTING.md) for proof and commit requirements and
[CITATION.cff](CITATION.cff) for citation metadata. No license has been granted
yet. Until the rights holder adds a `LICENSE` file, the source is available for
inspection but no permission to copy, modify, or redistribute it is implied.
See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).

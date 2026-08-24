# Formalization scope

## Included

The Lean development formalizes finite-dimensional real-algebra and
finite-measure statements needed for:

- posterior mixtures under soft binary evidence;
- likelihood-ratio and logistic-weight identities;
- total-variation bounds induced by mixture weights;
- complement identities for measurable events;
- products of evidence-pattern weights;
- nested evidence concentration under explicit assumptions.

Every public theorem states its assumptions in the Lean signature. The main
library builds without project-defined axioms or theorem-body placeholders.

## Not included

The following analytic statements are documentation-level research assumptions,
not Lean theorems in this repository:

- existence and uniqueness for the relevant parabolic PDEs;
- regularity and positivity conditions for h-functions;
- construction and well-posedness of Doob h-transforms for the target SDEs;
- limiting convergence results that require measure-theoretic or stochastic
  analysis beyond the algebraic carrier proved here.

The repository must not describe those items as machine-checked until their
definitions, assumptions, and proofs are present in the Lean source and CI.

## Important correction

The identity expressing an evidence-pattern weight ratio as a product of
`exp (-|lambda_i|)` is exact only under the nested-deviation and balanced-prior
assumptions stated by `nested_concentration`. The general result is
`weight_ratio_eq`, which retains the prior-odds factors and both mismatch
directions.

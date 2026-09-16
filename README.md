# ZND T–P Manifold

A research codebase for constructing and evaluating a tabulated ZND detonation manifold for stoichiometric hydrogen–air mixtures.

## Current objective

Construct a two-dimensional table of ZND solutions

\[
\mathrm{ZND}(\phi,T_1,P_1) \rightarrow Y_i(x),\;T(x),\;p(x)
\]

with the current baseline fixed at **\(\phi=1\)** and air represented by **O2 + N2**.

### Parameter space

| Parameter | Range | Sampling |
|---|---:|---:|
| Equivalence ratio, φ | 1.0 | fixed |
| Initial temperature, T₁ | 300–1000 K | 100 K |
| Initial pressure, P₁ | 0.1–5.0 atm | 0.1 atm |
| Total tabulated states | — | 400 |

The current SDToolbox sweep completed **399/400** states. The isolated unresolved state is **400 K, 3.9 atm**, where the CJ calculation times out. Timeout handling prevents that state from blocking the rest of the manifold.

## Off-grid validation

The current validation state is:

- **T₁ = 351.5 K**
- **P₁ = 0.84 atm**
- **φ = 1.0**

A direct SDToolbox calculation at the validation state is used as ground truth. Full temperature, pressure, and species profiles are reconstructed from the tabulated manifold and compared with that direct solution.

Two baseline retrieval methods have been evaluated:

1. Nearest-neighbor retrieval
2. Bilinear interpolation in T–P space

See **[Nearest Neighbor vs Bilinear](results/nearest_vs_bilinear.md)** for the quantitative comparison.

## Current result

At the 351.5 K, 0.84 atm validation point, bilinear interpolation substantially reduces profile error relative to nearest-neighbor retrieval. Temperature and reactive-species profiles are reconstructed closely; pressure remains the largest normalized discrepancy.

## Repository organization

```text
znd-manifold/
├── README.md
├── src/                 # ZND manifold and interpolation scripts
├── results/             # Markdown summaries and compact numerical results
└── figures/             # Selected validation figures
```

Large per-state ZND profile caches are intentionally not intended for Git tracking.

## Status

This repository is an active research workspace. Methods, validation coverage, and software structure will evolve as the ZND manifold is developed for eventual fast querying by downstream heat-transfer models.

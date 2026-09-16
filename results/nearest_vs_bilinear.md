# Nearest-Neighbor vs Bilinear Profile Reconstruction

## Purpose

Compare two simple methods for retrieving an off-grid ZND solution from a regular temperature-pressure manifold at fixed stoichiometric hydrogen-air composition (φ = 1).

The direct SDToolbox solution at the same off-grid state is treated as the validation truth for both methods.

## Manifold

- Temperature: 300–1000 K in 100 K increments
- Pressure: 0.1–5.0 atm in 0.1 atm increments
- Requested states: 400
- Successfully generated states: 399
- Numerical hole: 400 K, 3.9 atm (CJ calculation timeout)

The missing state does not affect this validation because the target lies in the 300–400 K, 0.8–0.9 atm cell.

## Validation state

Both methods are now verified at exactly:

- **T₁ = 351.5 K**
- **P₁ = 0.84 atm**
- **φ = 1.0**

Nearest neighbor selects the tabulated state **400 K, 0.8 atm**.

Bilinear interpolation uses the four surrounding states with the following verified weights:

| Corner | T (K) | P (atm) | Weight |
|---|---:|---:|---:|
| (T0, P0) | 300 | 0.8 | 0.291 |
| (T1, P0) | 400 | 0.8 | 0.309 |
| (T0, P1) | 300 | 0.9 | 0.194 |
| (T1, P1) | 400 | 0.9 | 0.206 |

Weight sum = **1.000**.

## Profile NRMSE

| Quantity | Nearest neighbor (%) | Bilinear (%) | Reduction vs nearest (%) |
|---|---:|---:|---:|
| Temperature | 0.8619 | 0.0509 | 94.1 |
| Pressure | 26.9835 | 3.4548 | 87.2 |
| H₂ | 0.9072 | 0.1350 | 85.1 |
| O₂ | 0.8163 | 0.1216 | 85.1 |
| H₂O | 1.4360 | 0.1132 | 92.1 |
| OH | 4.1962 | 0.1530 | 96.4 |
| H | 2.2162 | 0.3094 | 86.0 |
| O | 3.0689 | 0.2349 | 92.3 |
| HO₂ | 1.2338 | 0.1444 | 88.3 |
| H₂O₂ | 1.3267 | 0.3103 | 76.6 |
| N₂ | 0.0000 | 0.0000 | — |

## Bilinear error details

| Quantity | RMSE | MAE | Max absolute error | NRMSE (%) |
|---|---:|---:|---:|---:|
| Temperature (K) | 0.718149 | 0.272389 | 17.5107 | 0.0508568 |
| Pressure (Pa) | 26242.2 | 26213.4 | 43800.2 | 3.45482 |
| H₂ | 3.85053e-05 | 4.13483e-06 | 1.22830e-03 | 0.135000 |
| O₂ | 2.75272e-04 | 2.55869e-05 | 8.50782e-03 | 0.121611 |
| H₂O | 2.45528e-04 | 3.72612e-05 | 7.55260e-03 | 0.113180 |
| OH | 4.17831e-05 | 1.59496e-05 | 9.24476e-04 | 0.153022 |
| H | 9.95573e-06 | 1.69997e-06 | 3.28945e-04 | 0.309370 |
| O | 3.21910e-05 | 9.94647e-06 | 9.54728e-04 | 0.234949 |
| HO₂ | 1.04879e-06 | 7.65492e-08 | 2.91640e-05 | 0.144447 |
| H₂O₂ | 1.63551e-07 | 2.33616e-08 | 4.54458e-06 | 0.310320 |
| N₂ | 0 | 0 | 0 | 0 |

## Interpretation

This is now an apples-to-apples comparison: the same ZND manifold and the same direct SDToolbox truth state are used for both retrieval methods.

Nearest-neighbor retrieval discards three of the four surrounding tabulated states and substitutes a single nearby profile. Bilinear interpolation uses all four surrounding states with location-based weights. At this validation point, bilinear interpolation reduces NRMSE by roughly **76–96%** for the nonzero quantities relative to nearest-neighbor retrieval.

Temperature and the reactive-species profiles are reconstructed particularly closely by bilinear interpolation. Pressure remains the largest normalized discrepancy at **3.45% NRMSE**, even though this is much smaller than the **26.98%** nearest-neighbor pressure error.

Among the species, the largest bilinear NRMSE values are H₂O₂ (**0.310%**) and H (**0.309%**); all non-inert species remain below **0.32% NRMSE** at this validation state.

N₂ has zero profile error because the reduced FFCM2 H₂ mechanism treats N₂ as an inert diluent in this calculation; its mass-fraction profile is unchanged.

## Error metric

For a profile f(x),

```text
RMSE = sqrt(mean((f_reconstructed - f_truth)^2))
```

Temperature and pressure NRMSE are normalized by the range of the direct truth profile. Species NRMSE is normalized by the peak absolute mass fraction in the direct truth profile.

NRMSE is a profile-level aggregate metric; it should not be interpreted as saying every individual point lies within that percentage.

## Next experiment

Repeat the same direct-truth comparison at several additional off-grid T-P states distributed across the manifold. The purpose is to determine whether the strong local bilinear performance observed here persists across the broader operating space before introducing more sophisticated interpolation, compression, or ML-based representations.

# Nearest-Neighbor vs Bilinear Profile Reconstruction

## Purpose

Compare two simple methods for retrieving an off-grid ZND solution from a regular temperature-pressure manifold at fixed stoichiometric hydrogen-air composition (φ = 1).

The direct SDToolbox solution is treated as the validation truth.

## Manifold

- Temperature: 300–1000 K in 100 K increments
- Pressure: 0.1–5.0 atm in 0.1 atm increments
- Requested states: 400
- Successfully generated states: 399
- Numerical hole: 400 K, 3.9 atm (CJ calculation timeout)

## Validation state

The nearest-neighbor run used:

- T₁ = 351.5 K
- P₁ = 0.84 atm
- φ = 1.0

Nearest neighbor therefore selects the tabulated state **400 K, 0.8 atm**.

> **Verification note:** The bilinear error values currently available are numerically identical to an earlier 351.5 K, 0.85 atm run. Before treating the table below as a strict same-state comparison, verify that the bilinear run was executed at P₁ = 0.84 atm. For 0.84 atm, the expected four bilinear weights are 0.291, 0.309, 0.194, and 0.206 for (300 K, 0.8 atm), (400 K, 0.8 atm), (300 K, 0.9 atm), and (400 K, 0.9 atm), respectively.

## Profile NRMSE

| Quantity | Nearest neighbor (%) | Bilinear currently reported (%) |
|---|---:|---:|
| Temperature | 0.8619 | 0.0535 |
| Pressure | 26.9835 | 3.4542 |
| H₂ | 0.9072 | 0.1375 |
| O₂ | 0.8163 | 0.1264 |
| H₂O | 1.4360 | 0.1161 |
| OH | 4.1962 | 0.1610 |
| H | 2.2162 | 0.3016 |
| O | 3.0689 | 0.2525 |
| HO₂ | 1.2338 | 0.1595 |
| H₂O₂ | 1.3267 | 0.3181 |
| N₂ | 0.0000 | 0.0000 |

## Interpretation

Nearest-neighbor retrieval discards three of the four surrounding tabulated states and substitutes a single nearby ZND profile. This produces particularly large pressure error and larger errors in sensitive radical species such as OH and O.

Bilinear interpolation instead combines the four surrounding T-P states according to their relative location around the requested state. The currently reported bilinear result reconstructs temperature and reactive-species profiles closely, with pressure remaining the largest normalized discrepancy.

N₂ has zero profile error because the reduced FFCM2 H₂ mechanism treats N₂ as an inert diluent in this calculation; its mass-fraction profile is unchanged.

## Error metric

For a profile f(x),

```
RMSE = sqrt(mean((f_interp - f_truth)^2))
```

Temperature and pressure NRMSE are normalized by the range of the direct truth profile. Species NRMSE is normalized by the peak absolute mass fraction in the direct truth profile.

NRMSE is a profile-level aggregate metric; it should not be interpreted as saying every individual point lies within that percentage.

## Next check

Run bilinear interpolation at exactly **351.5 K, 0.84 atm** and confirm the interpolation weights before using the two columns as an apples-to-apples quantitative comparison.

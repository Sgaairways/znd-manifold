# Nearest-Neighbor vs Bilinear Profile Reconstruction

## Purpose

Compare two simple methods for retrieving an off-grid ZND solution from a regular temperature-pressure manifold at fixed stoichiometric hydrogen-air composition (φ = 1).

The direct SDToolbox solution at the same off-grid state is treated as the validation truth for both methods. The comparison therefore holds the manifold, requested state, direct truth solution, and profile discretization fixed while changing only the reconstruction method.

## Manifold

- Temperature: 300–1000 K in 100 K increments
- Pressure: 0.1–5.0 atm in 0.1 atm increments
- Equivalence ratio: φ = 1.0
- Requested states: 400
- Successfully generated states: 399
- Numerical hole: 400 K, 3.9 atm (CJ calculation timeout)

The missing state does not affect this validation because the target lies in the 300–400 K, 0.8–0.9 atm cell. Bilinear interpolation is performed only when all four corners of the requested T-P cell are available.

## Validation state

Both methods are verified at exactly:

- **T₁ = 351.5 K**
- **P₁ = 0.84 atm**
- **φ = 1.0**
- Common profile grid: **1200 points**
- Species array: **9 × 1200**

Both runs reuse the same independent direct-truth file:

```text
znd_tp_profiles/truth_target_T0351.50_P00.840.npz
```

The SDToolbox-generated arrays also pass the current JAX compatibility check on CPU: temperature `(1200,)`, pressure `(1200,)`, and species `(9, 1200)` arrays can be moved into JAX successfully.

## Reconstruction methods

### Nearest neighbor

The target is bracketed by 300 and 400 K and by 0.80 and 0.90 atm. Nearest-neighbor retrieval selects:

- **T = 400 K**
- **P = 0.80 atm**
- Temperature distance from target: **48.5 K**
- Pressure distance from target: **0.0400 atm**

This method uses that single tabulated ZND profile as the reconstruction at the requested off-grid state.

### Bilinear interpolation

Bilinear interpolation uses all four surrounding states with the following verified weights:

| Corner | T (K) | P (atm) | Weight |
|---|---:|---:|---:|
| (T0, P0) | 300 | 0.8 | 0.291 |
| (T1, P0) | 400 | 0.8 | 0.309 |
| (T0, P1) | 300 | 0.9 | 0.194 |
| (T1, P1) | 400 | 0.9 | 0.206 |

Weight sum = **1.000**.

## Profile NRMSE comparison

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

## Nearest-neighbor error details

| Quantity | RMSE | MAE | Max absolute error | NRMSE (%) |
|---|---:|---:|---:|---:|
| Temperature (K) | 12.1708 | 3.77751 | 189.215 | 0.861894 |
| Pressure (Pa) | 204963 | 204723 | 339253 | 26.9835 |
| H₂ | 2.58766e-04 | 1.88105e-04 | 5.72949e-03 | 0.907237 |
| O₂ | 1.84776e-03 | 1.06082e-03 | 4.82586e-02 | 0.816316 |
| H₂O | 3.11512e-03 | 2.74250e-03 | 4.27511e-02 | 1.43596 |
| OH | 1.14579e-03 | 1.11208e-03 | 7.16824e-03 | 4.19620 |
| H | 7.13191e-05 | 5.56225e-05 | 6.80424e-04 | 2.21621 |
| O | 4.20478e-04 | 3.54893e-04 | 3.67266e-03 | 3.06890 |
| HO₂ | 8.95845e-06 | 6.42913e-07 | 2.41055e-04 | 1.23382 |
| H₂O₂ | 6.99203e-07 | 2.26174e-07 | 1.83453e-05 | 1.32666 |
| N₂ | 0 | 0 | 0 | 0 |

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

This is an apples-to-apples comparison: the same ZND manifold, requested state, direct SDToolbox truth solution, and profile grid are used for both methods.

Nearest-neighbor retrieval discards three of the four surrounding tabulated states and substitutes a single nearby profile. Bilinear interpolation instead combines all four surrounding states according to their relative location in the T-P cell.

At this validation point, bilinear interpolation reduces NRMSE by approximately **76–96%** for all quantities with nonzero error relative to nearest-neighbor retrieval.

Temperature and reactive-species profiles are reconstructed particularly closely by bilinear interpolation. Temperature NRMSE decreases from **0.862% to 0.051%**. Pressure remains the largest normalized bilinear discrepancy at **3.45% NRMSE**, but this is substantially below the **26.98%** pressure NRMSE from nearest-neighbor retrieval.

The largest nearest-neighbor species NRMSE values occur for OH (**4.20%**) and O (**3.07%**). With bilinear interpolation, the largest species NRMSE values are H₂O₂ (**0.310%**) and H (**0.309%**), and all non-inert species remain below **0.32% NRMSE** at this validation state.

N₂ has zero profile error because the reduced FFCM2 H₂ mechanism treats N₂ as an inert diluent in this calculation; its mass-fraction profile is unchanged.

The present comparison demonstrates the reconstruction error difference between the two retrieval methods at this state. It does **not** by itself establish that the remaining error is caused by reaction-front misalignment; profile alignment can be investigated separately if later validation shows localized errors around induction or reaction regions.

## Error metric

For a profile `f(x)`,

```text
RMSE = sqrt(mean((f_reconstructed - f_truth)^2))
```

Temperature and pressure NRMSE are normalized by the range of the direct truth profile. Species NRMSE is normalized by the peak absolute mass fraction in the direct truth profile.

NRMSE is a profile-level aggregate metric and should not be interpreted as saying every individual point lies within that percentage.

## Saved outputs

### Nearest neighbor

```text
znd_nearest_neighbor_selection.csv
znd_nearest_neighbor_error_summary.csv
znd_nearest_neighbor_validation.npz
znd_tp_nearest_neighbor_plots/
```

### Bilinear

The bilinear run produces the corresponding interpolation weights, profile error summary, validation arrays, and profile plots for the same target state.

Both methods reuse the common cached manifold under:

```text
znd_tp_profiles/
```

## Completed follow-up: multi-point off-grid validation

The proposed broader validation has now been completed. Bilinear interpolation was evaluated at **9 additional off-grid T-P states** distributed across the manifold using three temperatures (351.5, 651.5, and 951.5 K) and three pressures (0.84, 2.54, and 4.64 atm).

At each state, the reconstructed temperature, pressure, and species profiles were compared against an independently calculated SDToolbox ZND solution.

Across the nine validation cases:

- Mean temperature NRMSE: **0.114%**
- Mean pressure NRMSE: **1.670%**
- Mean H2 NRMSE: **0.146%**
- Mean OH NRMSE: **0.159%**
- Mean NRMSE for every species remained below **0.41%**
- Maximum pressure NRMSE: **3.455%**
- The largest profile errors generally occurred in the lower-temperature validation cases.

These results extend the original single-state comparison and indicate that the strong bilinear reconstruction performance persists across the tested off-grid operating conditions. The nine-point study is documented in [the multi-point validation report](../validation/bilinear_multipoint_validation.md).

## Next experiment

Move the validated manifold lookup and bilinear profile reconstruction into a **JAX-oriented framework**. The immediate goal is to reproduce the existing interpolation results in JAX while preserving the current SDToolbox-generated manifold and direct-truth validation baseline.

This provides a foundation for fast and vectorized ZND profile queries for eventual coupling to the downstream **RDE heat-transfer solver**. Once the JAX baseline is verified, later work can investigate profile compression, differentiable optimization, and ML-based representations without losing the simple bilinear benchmark.

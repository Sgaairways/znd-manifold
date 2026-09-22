# Bilinear Interpolation: 9-Point Off-Grid Validation

## Purpose

This validation evaluates whether a precomputed ZND manifold can accurately reconstruct full detonation profiles at operating conditions that are not explicitly tabulated.

The current manifold uses stoichiometric hydrogen-air (\(\phi=1\)) over a regular temperature-pressure grid. Each tabulated ZND state contains the spatial profiles

\[
T(x), \qquad p(x), \qquad Y_i(x).
\]

For an off-grid \((T_1,P_1)\) query, bilinear interpolation combines the four surrounding tabulated ZND solutions to reconstruct the requested profiles. The interpolated result is then compared with an independently calculated SDToolbox ZND solution at exactly the same operating condition.

The long-term application is fast profile lookup for a downstream RDE heat-transfer model, where these thermochemical profiles can provide information needed to construct the thermal boundary conditions without recalculating a full ZND solution for every query.

---

## Validation Design

Nine off-grid states were selected across three temperatures and three pressures:

| Case | Temperature (K) | Pressure (atm) |
|---:|---:|---:|
| 1 | 351.5 | 0.84 |
| 2 | 351.5 | 2.54 |
| 3 | 351.5 | 4.64 |
| 4 | 651.5 | 0.84 |
| 5 | 651.5 | 2.54 |
| 6 | 651.5 | 4.64 |
| 7 | 951.5 | 0.84 |
| 8 | 951.5 | 2.54 |
| 9 | 951.5 | 4.64 |

For each state, the interpolated and direct SDToolbox profiles were compared for temperature, pressure, and all species in the reduced FFCM2 hydrogen mechanism.

---

## Aggregate NRMSE Results

| Quantity | Mean NRMSE (%) | Median NRMSE (%) | Maximum NRMSE (%) | Worst-case \(T_1\) (K) | Worst-case \(P_1\) (atm) |
|---|---:|---:|---:|---:|---:|
| Temperature | **0.114** | 0.048 | 0.690 | 351.5 | 4.64 |
| Pressure | **1.670** | 1.040 | **3.455** | 351.5 | 0.84 |
| H2 | **0.146** | 0.077 | 0.839 | 351.5 | 4.64 |
| O2 | **0.140** | 0.071 | 0.812 | 351.5 | 4.64 |
| H2O | **0.137** | 0.068 | 0.805 | 351.5 | 4.64 |
| OH | **0.159** | 0.079 | 0.860 | 351.5 | 4.64 |
| H | **0.410** | 0.153 | 2.144 | 351.5 | 4.64 |
| O | **0.291** | 0.151 | 1.507 | 351.5 | 4.64 |
| HO2 | **0.395** | 0.098 | 2.530 | 351.5 | 4.64 |
| H2O2 | **0.266** | 0.165 | 1.293 | 351.5 | 4.64 |
| N2 | **0.000** | 0.000 | 0.000 | — | — |

---

## Case-by-Case NRMSE (%)

| Case | T | P | H2 | O2 | H2O | OH | H | O | HO2 | H2O2 | N2 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.051 | 3.455 | 0.135 | 0.122 | 0.113 | 0.153 | 0.309 | 0.235 | 0.144 | 0.310 | 0.000 |
| 2 | 0.146 | 3.377 | 0.124 | 0.126 | 0.125 | 0.187 | 0.719 | 0.335 | 0.480 | 0.350 | 0.000 |
| 3 | 0.690 | 3.433 | 0.839 | 0.812 | 0.805 | 0.860 | 2.144 | 1.507 | 2.530 | 1.293 | 0.000 |
| 4 | 0.048 | 1.087 | 0.092 | 0.087 | 0.080 | 0.102 | 0.186 | 0.176 | 0.170 | 0.224 | 0.000 |
| 5 | 0.003 | 1.040 | 0.012 | 0.010 | 0.009 | 0.015 | 0.041 | 0.053 | 0.027 | 0.025 | 0.000 |
| 6 | 0.015 | 1.022 | 0.024 | 0.022 | 0.022 | 0.018 | 0.072 | 0.076 | 0.076 | 0.013 | 0.000 |
| 7 | 0.056 | 0.569 | 0.077 | 0.071 | 0.068 | 0.079 | 0.153 | 0.151 | 0.098 | 0.165 | 0.000 |
| 8 | 0.009 | 0.528 | 0.006 | 0.004 | 0.004 | 0.009 | 0.032 | 0.037 | 0.018 | 0.008 | 0.000 |
| 9 | 0.006 | 0.516 | 0.004 | 0.003 | 0.003 | 0.006 | 0.030 | 0.049 | 0.012 | 0.006 | 0.000 |

---

## Observations

- **Temperature reconstruction is highly accurate.** Mean temperature NRMSE across the nine off-grid states is 0.114%, with a maximum of 0.690%.
- **Pressure is the largest systematic source of interpolation error.** Mean pressure NRMSE is 1.670%, and the maximum is 3.455%.
- **Major species are reconstructed accurately.** H2, O2, H2O, and OH all have mean NRMSE below 0.16%.
- **Minor/radical species are more sensitive.** H, O, HO2, and H2O2 show larger relative errors than the major species, although their mean NRMSE values remain below 0.41% across these validation states.
- **The most challenging tested region is at low temperature.** Most profile-wise maximum errors occur at 351.5 K and 4.64 atm.
- **Accuracy improves substantially at higher temperature for the tested states.** Cases at 951.5 K show particularly small errors.
- N2 has zero interpolation error for these tests. In the reduced hydrogen mechanism used here, N2 acts as the diluent and its profile is unchanged.

These observations describe the nine tested off-grid conditions and should not be interpreted as exhaustive validation of every location in the full manifold.

---

## Representative Profiles

For presentation and qualitative comparison, four profiles provide a compact representation of the reconstruction quality:

- \(p(x)\): directly relevant to the downstream flow/thermal state and the largest source of NRMSE in this validation.
- \(T(x)\): directly relevant to the heat-transfer application.
- \(Y_{H_2}(x)\): representative major reactant profile.
- \(Y_{OH}(x)\): chemically sensitive radical profile.

Case 1 (351.5 K, 0.84 atm) is useful for direct comparison with the earlier nearest-neighbor baseline at the same operating condition. Case 3 (351.5 K, 4.64 atm) is useful as a more challenging bilinear validation case.

---

## Takeaway

The nine-point validation indicates that a precomputed ZND manifold combined with bilinear interpolation can accurately reconstruct off-grid temperature, pressure, and species profiles over the tested \(T_1-P_1\) conditions.

This establishes bilinear interpolation as a simple baseline profile-reconstruction method for the next stage of the project: integrating fast ZND profile lookup into a JAX-oriented framework for eventual coupling to the downstream RDE heat-transfer and design-optimization workflow.

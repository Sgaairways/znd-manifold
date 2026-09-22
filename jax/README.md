# JAX ZND Manifold Lookup

## Purpose

This directory documents the JAX-oriented implementation of the validated ZND manifold lookup. The goal is to preserve the existing SDToolbox-generated detonation manifold and direct-truth validation baseline while moving the runtime profile reconstruction into JAX.

The intended application is fast retrieval of thermochemical profiles for a downstream rotating detonation engine (RDE) heat-transfer model:

[
(T_1,P_1,phi) ightarrow 	ext{ZND profile lookup} ightarrow T(x),p(x),Y_i(x) ightarrow 	ext{thermal boundary conditions} ightarrow 	ext{heat-transfer solver}.
]

At the current stage, (phi=1) and the manifold is parameterized by initial temperature and pressure.

## What changed — and what did not

The physics/database did **not** change. SDToolbox remains the offline high-fidelity source used to generate the cached ZND solutions. The existing physical-distance (x) representation, common-grid resampling, bilinear weights, direct SDToolbox truth cases, and NRMSE definitions were retained.

The change is the interpolation backend:

- Previous baseline: SciPy `RegularGridInterpolator`.
- Current implementation: JAX-jitted bilinear weighted reconstruction using `jax.numpy`.
- JAX 64-bit mode is enabled to support a clean numerical comparison with the established NumPy/SciPy baseline.

For an off-grid query ((T,P)), the same four surrounding manifold states are used. With

[
a=rac{T-T_0}{T_1-T_0}, qquad
b=rac{P-P_0}{P_1-P_0},
]

the four weights are

[
w_{00}=(1-a)(1-b),quad
w_{10}=a(1-b),quad
w_{01}=(1-a)b,quad
w_{11}=ab.
]

Each temperature, pressure, and species profile is reconstructed from the corresponding four corner profiles.

## Validation strategy

The JAX port was checked at two levels.

### 1. JAX vs. SciPy regression

The first requirement was that changing the software backend must not change the established bilinear reconstruction.

Across the nine off-grid validation states, the maximum observed JAX-SciPy discrepancies were:

| Quantity | Maximum absolute JAX-SciPy difference |
|---|---:|
| Pressure | `1.86e-9 Pa` |
| Temperature | `9.09e-13 K` |
| H2O | `5.55e-17` mass fraction |
| O2 | `2.78e-17` mass fraction |
| H2 | `6.94e-18` mass fraction |
| OH | `6.94e-18` mass fraction |
| O | `6.94e-18` mass fraction |
| H | `8.67e-19` mass fraction |
| HO2 | `2.17e-19` mass fraction |
| H2O2 | `1.36e-20` mass fraction |
| N2 | `0` |

These differences are numerical roundoff. The JAX implementation therefore reproduces the established SciPy bilinear calculation to numerical precision.

### 2. JAX vs. direct SDToolbox truth

The same nine previously established off-grid validation states were reused:

| Temperature [K] | Pressure [atm] |
|---:|---:|
| 351.5 | 0.84 |
| 351.5 | 2.54 |
| 351.5 | 4.64 |
| 651.5 | 0.84 |
| 651.5 | 2.54 |
| 651.5 | 4.64 |
| 951.5 | 0.84 |
| 951.5 | 2.54 |
| 951.5 | 4.64 |

The aggregate JAX-vs-SDToolbox profile errors exactly reproduce the prior bilinear validation baseline:

| Profile | Mean NRMSE [%] | Median [%] | Maximum [%] |
|---|---:|---:|---:|
| Temperature | **0.1137** | 0.0479 | 0.6897 |
| Pressure | **1.6697** | 1.0404 | 3.4548 |
| H2 | **0.1457** | 0.0766 | 0.8388 |
| O2 | **0.1396** | 0.0707 | 0.8124 |
| H2O | **0.1366** | 0.0678 | 0.8055 |
| OH | **0.1587** | 0.0789 | 0.8596 |
| H | **0.4097** | 0.1535 | 2.1439 |
| O | **0.2911** | 0.1509 | 1.5070 |
| HO2 | **0.3952** | 0.0979 | 2.5299 |
| H2O2 | **0.2662** | 0.1654 | 1.2931 |
| N2 | **0.0000** | 0.0000 | 0.0000 |

Thus, moving the interpolation kernel to JAX produced no measurable loss of reconstruction accuracy.

## Performance benchmark

A warmed interpolation-only CPU benchmark was also performed. This benchmark measures the species-profile interpolation kernel after JIT compilation; it excludes disk I/O, manifold generation, corner-profile loading, and physical-(x) resampling.

Across the nine validation states:

- JAX species-profile lookup: approximately **7.2–8.1 microseconds/query**
- SciPy species-profile lookup: approximately **47.9–52.6 microseconds/query**
- Mean JAX time: approximately **7.50 microseconds/query**
- Mean SciPy time: approximately **49.09 microseconds/query**
- Observed warmed-kernel speedup: approximately **6.5x**

The first JAX call incurred a one-time JIT compilation cost (about 180 ms in the benchmark run). Therefore, the 6.5x value should be interpreted specifically as a **warmed interpolation-kernel speedup**, not as a 6.5x speedup of the complete SDToolbox/manifold workflow.

## Current result

The current result can be summarized as:

> The validated full-profile bilinear ZND reconstruction was ported from SciPy to JAX. Across nine off-grid validation states, JAX reproduced the SciPy predictions to numerical precision and retained the same direct-SDToolbox validation accuracy. For the tested warmed species-profile interpolation kernel on CPU, JAX was approximately 6.5x faster than SciPy.

This establishes JAX as a viable runtime framework without changing the underlying ZND physics or validated interpolation baseline.

## Why JAX matters for the RDE application

The end goal is not merely to accelerate one interpolation call. The manifold is intended to provide rapid thermochemical-state information to a downstream RDE thermal model. A design, transient calculation, or optimization workflow may require many profile queries.

The desired architecture is:

```text
SDToolbox (offline)
    → precomputed ZND manifold
    → JAX profile lookup
    → T(x), p(x), Y_i(x)
    → thermal boundary conditions
    → heat-transfer / cooling model
    → design optimization
```

JAX provides a path toward JIT compilation, vectorized/batched profile queries, accelerator-compatible array operations, and eventually differentiable model components.

## Next step

The next experiment is to move beyond one-query-at-a-time lookup:

1. Pack the cached manifold into a JAX-friendly in-memory tensor representation.
2. Move cell identification/profile retrieval into the runtime lookup rather than loading four NPZ files for each query.
3. Use `jax.vmap` to evaluate batches of (T-P) operating conditions.
4. Verify batched results against the validated single-query implementation.
5. Benchmark throughput for tens, hundreds, and thousands of profile queries.
6. Preserve the current SciPy bilinear and direct-SDToolbox results as regression baselines.

Only after this equivalence and performance baseline is established should profile compression, learned/ML representations, or more sophisticated differentiable surrogates be introduced.

## Associated result files

The JAX validation currently produces:

- `jax_vs_scipy_regression.csv` — numerical equivalence between JAX and SciPy.
- `jax_vs_sdtoolbox_validation.csv` — case-by-case JAX profile errors against direct SDToolbox truth.
- `jax_aggregate_nrmse.csv` — aggregate nine-point NRMSE statistics.

These files separate two questions that should remain distinct: **Did the JAX port reproduce the established interpolation?** and **Does the interpolation remain accurate relative to the direct ZND calculation?**

# PSO impedance fitting note

## Fit objective

Particle swarm optimization is being tested as a numerical optimizer for a multi-resonator model of the measured longitudinal impedance. The optimizer itself is not a Concept in the current database; this note is about whether the fitted RF parameters remain physically interpretable.

Each resonator contributes a center frequency, amplitude, and quality factor. Bounds are seeded from visible HOM peaks, but the fit should also reproduce the broadband baseline of the beam impedance. A low residual alone is insufficient if two resonators collapse onto the same line or if the fitted damping is outside the measured range.

## Weighting and validation

The objective is weighted over the bunch frequency spectrum rather than uniformly over every frequency bin. This keeps the fit sensitive to impedance that the beam can actually sample while preserving a separate diagnostic for narrow peaks.

After fitting, I will reconstruct the wake field and compare it with the original time-domain trace. The resulting HOM impedance table must be stable against reasonable changes in frequency window, particle count, and initial swarm seed before it is used in a coupled-bunch estimate.

## Decision rule

Accept a candidate only when the residual, parameter bounds, reconstructed wake, and repeatability checks all pass. Otherwise retain the raw coupling impedance data and mark the resonator decomposition as model-dependent.

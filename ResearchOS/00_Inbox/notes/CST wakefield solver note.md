# CST wakefield solver setup note

## Purpose

This run uses the CST Wakefield Solver to compare two bellows transitions under the same beam definition. The first quantity of interest is the longitudinal wake near the bunch; the second is the late-time ringing that may indicate a weakly damped cavity mode.

## Setup choices

The source is a Gaussian bunch with a 3 mm rms length. Both models use identical mesh refinement, open boundaries, wake length, and symmetry settings. The transverse wake is evaluated with the same source offset so that the kick factor remains comparable.

I will record the loss factor from the time-domain result and transform the wake only after checking that the tail has decayed sufficiently. A short wake length can broaden or hide a narrow peak, while an abrupt numerical tail can contaminate the impedance spectrum.

## Cross-checks

An eigenmode analysis will be run for the largest peaks to separate physical resonances from numerical artifacts. Port definitions will also be checked with an S-parameter run. Agreement in frequency is useful, but the boundary conditions and excitation in the two solvers are not identical, so amplitudes should not be compared without a normalization review.

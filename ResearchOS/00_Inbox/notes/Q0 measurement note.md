# Q0 measurement note

## Measurement plan

The vertical test will estimate Q0 from the decay time and stored energy. In the database, Q0 is treated as a measurement-specific form of the broader quality factor concept rather than as a separate Concept until the workflow stabilizes.

The pickup and input coupler introduce external loading, so the observed QL cannot be reported as the intrinsic value. I will obtain Qext for both ports, verify the coupling state, and propagate those terms when converting the loaded decay constant to Q0.

## RF checks

A low-power S-parameter sweep should locate the resonance and expose cable-delay or calibration errors before the decay measurement. The fitted bandwidth, phase rotation, and ring-down result should agree within their stated uncertainty.

R/Q comes from the cavity field model, whereas Q0 is dominated by surface loss. Their product enters the shunt impedance convention used in the performance table, so the report must state the convention instead of presenting a bare resistance value.

## Recording

- Save the raw complex trace and the time-domain decay, not only fitted values.
- Record temperature, field level, calibration plane, QL, and both Qext estimates.
- Treat systematic disagreement between sweep and ring-down methods as an unresolved measurement issue.

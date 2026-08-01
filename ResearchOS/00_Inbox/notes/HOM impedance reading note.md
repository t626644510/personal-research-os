# HOM impedance reading note

## Reading context

The cavity review reports several narrow HOM impedance peaks above the operating mode. The strongest line is not automatically the most dangerous one: its overlap with the bunch spectrum and the fill pattern matters as much as the peak amplitude.

The paper quotes R/Q from an eigenmode calculation and uses Qext from the damping model. I need to confirm whether the plotted impedance uses the loaded quality factor after the HOM coupler is attached, because using the undamped value would overstate the steady-state voltage.

## Working interpretation

The time-domain wake field decays slowly when a higher order mode has a high quality factor. In the frequency domain this becomes a narrow longitudinal impedance peak. A peak close to a beam harmonic deserves a coupled-bunch instability check even when its integrated loss is modest.

For comparison across geometry revisions, I will keep the coupling impedance convention, bunch length, frequency resolution, and port loading fixed. The next pass should tabulate resonant frequency, R/Q, Qext, and the resulting peak impedance rather than compare screenshots.

## Follow-up

- Recalculate the bunch spectrum for the proposed train pattern.
- Check whether the dangerous mode propagates through the beam pipe or remains trapped.
- Review the HOM coupler load model before accepting the damping margin.

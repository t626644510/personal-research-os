---
type: project_verification_matrix
id: project_1500mhz_tm020_harmonic_cavity_verification_matrix
status: draft
created: 2026-08-18
updated: 2026-08-18
---

# 1500 MHz TM020 Harmonic Cavity Verification Matrix

## Purpose and Scope

This matrix separates what the selected paper reports from what the current
1500 MHz harmonic-cavity project must verify. It is a planning artifact, not an
engineering design approval, a requirements specification, or a promotion
record. The paper is a benchmark/reference for selecting verification questions;
its numbers and examples are not current-project validation.

Primary links:

- Project page: [[02_Project/1500 MHz TM020 Harmonic Cavity]]
- Source record: [[00_Inbox/reading/ipac2019-weprb066/source_record]]
- Frozen reading note: [[00_Inbox/reading/ipac2019-weprb066/reading_note]]
- KA-03 gate record: [[99_Meta/KA03_Promotion_Trial_Validation]]

## Provenance Legend

- `[paper/paraphrase]`: directly supported by the selected paper as paraphrased
  in the frozen reading note.
- `[synthesis-inference/unverified]`: a bounded interpretation for planning,
  not a paper sentence and not a frozen project decision.
- `[external-llm/unverified]`: retained only when the reading note labels an
  external explanation as unverified; it is not an acceptance basis.
- `[requires-verification]`: a current-project input, method, or decision is
  still required.

## Verification Matrix

| Topic | Paper evidence or example | What can be benchmarked | Current-project input required | Verification method/artifact | Acceptance criterion or decision needed | Current status | Provenance / locator |
|---|---|---|---|---|---|---|---|
| 500/1500 harmonic relation | The paper gives about 500.12 MHz main RF and 1500.36 MHz third-harmonic RF. | Frequency ratio and the paper's third-harmonic example can be reproduced. | Exact main RF, harmonic number, operating-frequency tolerance, and machine timing requirements. | Frequency specification, analytic ratio check, and recorded RF measurement or design review. | Human-approved harmonic relation and frequency tolerance for this project. | Open; paper example only. | `[paper/paraphrase]` reading note 3.1, 6 |
| TM010/TM020 eigenmode comparison | The paper discusses TM020 for both its main and harmonic cavities; it does not provide a matched current-project comparison. | Reproduce paper-labelled eigenmode frequencies and field-pattern checks when geometry is available. | Current cavity geometry, boundary conditions, materials, beam aperture, and mode-selection criteria. | Eigenmode sweep with field plots, mode labels, and comparison record. | Human-approved mode, frequency, field pattern, and separation from competing modes. | Open; TM020 is only a project candidate. | `[paper/paraphrase]` reading note 3.7, 4.1, 8.1, 8.3 |
| RF parameters: frequency, R/Q, Q0, shunt impedance, geometry factor, surface fields | The paper reports frequency 1500.36 MHz, unloaded Q0 = 36,000, R/Q = 68 ohm, single-cavity shunt impedance 2.45 Mohm, and specified geometry dimensions. Geometry factor and peak surface electric/magnetic fields are current-project verification targets and are not reported by the selected reading-note evidence. | Recalculate paper-reported values from a faithful model and preserve the paper's R/Q convention; verify geometry factor and peak surface electric/magnetic fields for the current project separately. | Final geometry, material and conductivity model, port/loading definition, field normalization, and post-processing convention. | Eigenmode solve plus reproducible RF post-processing and a parameter ledger. | Project-defined acceptance limits and an explicit convention for each reported quantity; no threshold is assumed from the paper. | Open; benchmark/reference only. | `[paper/paraphrase]` reading note 3.3, 7.1, 8.3 |
| Tuner sensitivity, sign, range, and travel | Two copper rods are each 95 mm in diameter and move +/-50 mm for about +/-0.5 MHz; two plungers are each 30 mm in diameter and move +/-25 mm for about +/-0.5 MHz. | Compare geometry-specific frequency shifts and travel ranges against the paper examples. | Cavity geometry, tuner coordinates, mechanical envelope, required frequency range, and allowed stress or contact conditions. | Parameterized electromagnetic model paired with a mechanical travel record and measured calibration if built. | Human-approved sign, sensitivity, range, repeatability, and travel for the selected cavity; no generic value is transferred. | Open; paper examples are design-specific. | `[paper/paraphrase]` reading note 3.4, 8.3 |
| Active/passive operation and ports | The paper describes a normally passive harmonic mode and an optional active-operation case using a rotatable coaxial loop coupler. | Distinguish passive operation from the optional active port arrangement. | Operating mode, required RF drive, port functions, coupler orientation, beam loading, and integration constraints. | RF architecture record, port-boundary EM model, circuit or system analysis, and review decision. | Human-approved operating mode and port architecture; coupler is not itself a cavity mode. | Open. | `[paper/paraphrase]` reading note 3.4, 4.2, 7.2, 8.3 |
| Qext, QL, all ports, and absorbers | The paper reports Q0 for the harmonic example and an approximate loaded-Q range of 10–1000 only for selected parasitic modes shown in Figures 4 and 7; this is not the harmonic working-mode QL or an all-port Q budget. | Reproduce the distinction between intrinsic, external, and loaded Q for a defined model. | Every port, coupler, absorber, termination, operating state, and required bandwidth or fill behaviour. | Multiport EM extraction of Qext and QL, S-parameter analysis, and cold-test or RF measurement plan. | Human-approved Q budget and loading definitions after all ports and absorbers are specified. | Open; Q0 is not QL. | `[paper/paraphrase]` reading note 3.3, 3.6, Figures 4 and 7, 7.2, 8.3 |
| Beam-induced voltage, detuning, and fill-gap transient | The selected source does not establish current-project beam-induced-voltage, detuning, or fill-gap results. | Only a defined paper case can be used as a qualitative reference; no current threshold is available. | Beam current, bunch pattern, fill gap, harmonic voltage and phase, detuning, RF control, cavity count, and impedance model. | Self-consistent beam-cavity transient or longitudinal simulation with recorded assumptions and input data. | Machine-defined voltage, phase, transient, and stability criteria approved before analysis. | Unresolved; missing project inputs. | `[requires-verification]` reading note 7.3, 8.2 |
| HOM spectrum, impedance, and coupled-bunch effects | The paper gives selected-mode loaded-Q information and ferrite-damping context, not a complete current-project HOM impedance budget. | Compare a complete model's mode list and damping bookkeeping with the limited paper examples. | Full cavity and assembly geometry, ports and absorbers, fill pattern, beam spectrum, impedance budget, and coupled-bunch model. | Eigenmode and wakefield analysis, impedance extraction, S-parameter checks, and beam-dynamics assessment. | Human-approved impedance and growth-rate limits; no generic threshold is imported from the paper. | Open. | `[paper/paraphrase]` reading note 3.6; `[requires-verification]` 8.3 |
| Thermal, mechanical, vacuum, manufacturing, and cold test | The source supplies paper-specific dimensions and mentions ferrite damping; it does not validate current materials, cooling, vacuum, fabrication, or test acceptance. | Use the paper geometry and damping description as a reference for test questions only. | Materials, power deposition, cooling, stress, alignment, vacuum limits, fabrication tolerances, seals, and test facility. | CAD and tolerance record, thermal and structural analysis, vacuum/manufacturing review, and cold-test plan/results. | Project-specific thermal, mechanical, vacuum, manufacturing, and test criteria approved by the responsible reviewers. | Open; requirements are not set. | `[paper/paraphrase]` reading note 3.3, 3.6; `[requires-verification]` 6, 8.3 |
| Bunch lengthening and lifetime claims | The paper presents a bunch-lengthening application and a factor-of-four lifetime result for its stated 3 GeV and 300 mA case. | Reproduce the paper's stated case only if all of its beam and machine assumptions are available. | Beam energy, current, bunch charge, fill pattern, RF voltages and phases, optics, impedance, radiation and IBS inputs, cavity count, and lifetime model. | Self-consistent longitudinal, Touschek, and lifetime analysis with a traceable input set and sensitivity study. | Human-approved project-specific bunch-lengthening and lifetime criteria; the paper's factor is not a transferable requirement. | Open; paper claim is not current validation. | `[paper/paraphrase]` reading note 5.2, 5.3; `[requires-verification]` 7.4, 8.1, 8.2 |

## Current Project Input Register

The following inputs are not yet frozen and must be supplied or explicitly
marked not applicable before a quantitative verification run:

- Main-RF frequency, harmonic frequency, allowed frequency error, voltage,
  phase, and RF-control assumptions.
- Beam energy, current, bunch charge, number of bunches, fill pattern, fill gap,
  bunch length, optics, and lifetime-analysis assumptions.
- Required harmonic voltage and phase, number of cavities, active or passive
  operating mode, port functions, coupler arrangement, and absorber plan.
- Final cavity geometry, aperture, materials, conductivity, tuner envelope,
  manufacturing tolerances, cooling, vacuum, alignment, and test constraints.
- HOM impedance budget, coupled-bunch criteria, beam-loading model, detuning
  range, and acceptance thresholds.

## Stop Conditions

No stable engineering design, proposal lifecycle transition, or Concept
promotion may be inferred from this matrix. Quantitative thresholds, current
machine applicability, and transfer of paper values require explicit human
review and the missing project inputs above. A paper benchmark is not a
validation result, and an unresolved row must remain unresolved rather than
being filled with a plausible number.

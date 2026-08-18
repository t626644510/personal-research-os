---
type: project
id: project_1500mhz_tm020_harmonic_cavity
status: active
created: 2026-08-11
updated: 2026-08-18
---

# 1500 MHz TM020 Harmonic Cavity

## Goal

Establish an evidence-backed design basis for the planned approximately 1500 MHz TM020-mode harmonic cavity while keeping engineering choices open until they are explicitly reviewed and decided.

## Scope and Non-goals

The scope is the harmonic-cavity candidate for the current storage-ring project. The known main RF system is an approximately 500 MHz normal-conducting system; selecting or redesigning its cavity mode is outside this project page's scope. This page does not authorize cavity implementation, RW-05, Concept proposals, or KA-01.

## Known Inputs

- The project has an approximately 500 MHz normal-conducting main RF system.
- A roughly 1500 MHz harmonic RF system is planned.
- TM020 is a candidate only for the harmonic cavity in this project.
- The current source record is [[00_Inbox/reading/ipac2019-weprb066/source_record]].
- The current synthesis artifact is [[00_Inbox/reading/ipac2019-weprb066/reading_note]]; it was frozen by RW-04 from explicitly accepted RW-03 content and has state `human_reviewed`.
- The [[00_Inbox/reading/ipac2019-weprb066/reading_note.draft]] remains available as RW-03 history with state `draft`.

## Working Assumptions

- Approximately 1500 MHz is a planning value; the exact operating frequency remains to be confirmed.
- The cited paper is an evidence input, not a project requirement or an adopted cavity design.
- Any transfer from the paper to this project must be checked against project-specific beam, RF, thermal, mechanical, and integration constraints.

## Decisions

No engineering design decision is frozen. Active versus passive operation, target voltage, cavity count, geometry, tuning, coupling, and HOM treatment all remain undecided.

## Open Questions

- Will the harmonic cavity operate actively or passively?
- What harmonic voltage and phase are required for the intended beam distribution?
- How many cavities are appropriate?
- What geometry satisfies RF, aperture, thermal, mechanical, and integration constraints?
- What frequency-tuning range and mechanism are required?
- Is an RF input coupler required, and what external coupling should any ports provide?
- What HOM damping and coupled-bunch stability margins are required?
- Which machine and fill-pattern parameters must be fixed before beam-loading and lifetime studies are credible?

## Papers and Reading Notes

- [[00_Inbox/reading/ipac2019-weprb066/source_record]]
- [[00_Inbox/reading/ipac2019-weprb066/reading_note]]
- [[00_Inbox/reading/ipac2019-weprb066/reading_note.draft]] (RW-03 history)

## Existing Concepts

- [[01_Concept/Cavity mode]]
- [[01_Concept/R over Q]]
- [[01_Concept/Q factor]]
- [[01_Concept/Shunt impedance]]
- [[01_Concept/External Q]]
- [[01_Concept/Loaded Q]]
- [[01_Concept/HOM coupler]]
- [[01_Concept/Coupled-bunch instability]]
- [[01_Concept/Longitudinal impedance]]

## Concept Gaps

TM020 mode; Harmonic cavity; Passive harmonic cavity; Beam loading; Frequency tuner; Coupling tuner; Detuning; Bunch lengthening; Fill gap; Touschek lifetime; Robinson instability; Haïssinski equation.

## Experiments

No experiment or simulation campaign has been started from this page. Candidate studies must be defined only after their inputs, conventions, and acceptance criteria are reviewed.

## Next Actions

1. Complete the final audit and publication of the RW-04 frozen `reading_note.md`; preserve the draft as RW-03 history.
2. Confirm the machine, fill-pattern, and RF requirements that bound the harmonic-cavity problem.
3. Define a verification sequence before freezing any cavity design decision.

## Decision Log

- 2026-08-11: Project foundation created. No engineering design decision was made.

## History

- 2026-08-11: Initial project page created for the RW-03 synthesis trial and minimal Obsidian foundation.
- 2026-08-18: RW-03 synthesis content human accepted and selected-text presentation correction applied; RW-04 was explicitly authorized and the frozen note was created; no engineering decision, RW-05, Concept proposal, or KA-01 work was started.

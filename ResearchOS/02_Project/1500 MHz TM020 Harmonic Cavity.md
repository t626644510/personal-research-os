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

The scope is the harmonic-cavity candidate for the current storage-ring project. The known main RF system is an approximately 500 MHz normal-conducting system; selecting or redesigning its cavity mode is outside this project page's scope.

This page does not freeze an engineering cavity design or authorize automatic promotion. KA-01 is complete; KA-03 First Promotion Trial Stage 2 is complete after the owner-authorized human gate and manual promotion. KA-04 remains unstarted and unauthorized.

## Known Inputs

- The project has an approximately 500 MHz normal-conducting main RF system.
- A roughly 1500 MHz harmonic RF system is planned.
- TM020 is a candidate only for the harmonic cavity in this project.
- The current source record is [[00_Inbox/reading/ipac2019-weprb066/source_record]].
- The current synthesis artifact is [[00_Inbox/reading/ipac2019-weprb066/reading_note]]; it was frozen by RW-04 from explicitly accepted RW-03 content and has state `human_reviewed`.
- The [[00_Inbox/reading/ipac2019-weprb066/reading_note.draft]] remains available as RW-03 history with state `draft`.
- RW-04 and RW-05 are complete; KA-01 is complete; KA-02 human evaluation is complete.
- KA-03 First Promotion Trial Stage 2 is complete: P01 and P03 were accepted
  and manually promoted; P02 was superseded by P01; P04 and P05 were deferred.

## Working Assumptions

- Approximately 1500 MHz is a planning value; the exact operating frequency remains to be confirmed.
- The cited paper is an evidence input, not a project requirement or an adopted cavity design.
- The cited paper is a benchmark/reference for verification planning, not current-project validation.
- Any transfer from the paper to this project must be checked against project-specific beam, RF, thermal, mechanical, and integration constraints.

## Decisions

No engineering design decision is frozen. Active versus passive operation, target voltage, cavity count, geometry, tuning, coupling, and HOM treatment all remain undecided.

## KA-03 Status

KA-03 First Promotion Trial Stage 2 is complete under the explicit human gate
recorded by reviewer `owner-01` on 2026-08-18. P01 `Harmonic cavity` and P03
`Tuner` are accepted and manually promoted; P02 is superseded by P01; P04 is
deferred pending reference `[11]`; and P05 is deferred pending a later
systematic beam-physics study. The independent audit passed on 2026-08-18:
candidate/stable byte fidelity, lifecycle and promotion records, 27 Concepts,
49 tests, and source/run immutability all passed. KA-03 is accepted and
complete and ready for the agreed Major Phase A publication point. No
engineering design decision is frozen by this page.

The mandatory human gate is recorded in
[[99_Meta/KA03_Promotion_Trial_Validation]].

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

## Verification Matrix

- [[02_Project/1500 MHz TM020 Harmonic Cavity Verification Matrix]]

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
- [[01_Concept/Harmonic cavity]]
- [[01_Concept/Tuner]]

## Concept Gaps

TM020 mode; Passive harmonic cavity as an operating-mode topic; Beam loading; Coupling tuner; Detuning; Bunch lengthening; Fill gap; Touschek lifetime; Robinson instability; Haïssinski equation.

## Experiments

No experiment or simulation campaign has been started from this page. Candidate studies must be defined only after their inputs, conventions, and acceptance criteria are reviewed.

## Next Actions

1. Complete the agreed Major Phase A publication closeout for the audited
   KA-03 package.
2. Plan future KA-04 work only under separate explicit authorization; keep
   KA-04 unstarted and unauthorized.
3. Continue P04 reference `[11]` review and the P05 later systematic
   beam-physics study; do not acquire new sources in this phase.
4. Keep current operating mode, target voltage, cavity count, geometry, tuner,
   coupler, HOM, and project-applicability decisions open until separately
   reviewed.

## Decision Log

- 2026-08-11: Project foundation created. No engineering design decision was made.
- 2026-08-18: KA-02 human evaluation closed. KA-03 First Promotion Trial Stage 1
  was authorized and prepared for human scientific review; no engineering or
  lifecycle decision was made.
- 2026-08-18: owner-01 passed the KA-03 mandatory human gate and authorized P01
  and P03 acceptance and manual promotion, P02 supersession by P01, and P04/P05
  deferral. No engineering design decision was frozen.

## History

- 2026-08-11: Initial project page created for the RW-03 synthesis trial and minimal Obsidian foundation.
- 2026-08-18: RW-03 synthesis content human accepted and selected-text presentation correction applied; RW-04 was explicitly authorized and the frozen note was created; no engineering decision, RW-05, Concept proposal, or KA-01 work was started.
- 2026-08-18: RW-04/RW-05/KA-01 completed and KA-02 closed. KA-03 First Promotion
  Trial Stage 1 was authorized and prepared; human scientific review and any
  promotion remain pending.
- 2026-08-18: KA-03 Stage 2 completed the authorized lifecycle transitions and
  manual promotion of `Harmonic cavity` and `Tuner`; at that closeout boundary,
  the independent audit was pending and was subsequently passed.
- 2026-08-18: KA-03 Stage 2 independent audit passed; KA-03 is accepted and
  complete and ready for the agreed Major Phase A publication point.

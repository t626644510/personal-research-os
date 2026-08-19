# Proposal ka01-20260818t065446z-67f9fb66-p01-create

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p01-create`
- Run ID: `ka01-20260818t065446z-67f9fb66`
- Type: create
- State: accepted
- Human owner: owner-01
- Prompt path: `ResearchOS/99_Meta/prompts/concept_proposal_v0.1.md`
- Prompt version: `v0.1`
- Repository baseline commit: `fb0538ce9ddf22a8e3c151a05820f03fc5dc7892`
- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Source SHA-256: `67f9fb66faa227d27947e75fb5bd7c4ecfedd222bd09ad4ae2648673c2629627`
- Prepared by: manually triggered Codex implementation conversation
- Prepared at: `2026-08-18T06:54:46.411Z`
- Source locator: `3.1 Double-RF context and frequencies`; `3.3 Harmonic-cavity parameters`; `3.4 Frequency tuners and couplers are different functions`; `3.5 Six harmonic cavities and the lifetime claim`
- Target stable id: harmonic_cavity
- Target stable path: `ResearchOS/01_Concept/Harmonic cavity.md`
- Supersedes: `ka01-20260818t065446z-67f9fb66-p02-create`

## Summary

This proposal records the accepted and manually promoted `Harmonic cavity`
Concept candidate from direct paper-supported content and a bounded reusable
definition. KA-02 evaluated this unit as `retain_for_revision`; owner-01
accepted the complete revised candidate and authorized its separate manual
promotion in KA-03 Stage 2.

## Proposed Changes

- `id`: retain the proposed `harmonic_cavity`; no canonical, alias, or semantic
  registry match was found.
- `aliases`: propose the Chinese alias `谐波腔`; do not add `Passive harmonic
  cavity` or `被动谐波腔` as automatic aliases.
- `category`: propose `accelerator physics` and `RF engineering` as review
  categories; field-level evidence is E06.
- `level`: `working`; `confidence.textbook`: `medium`; and
  `confidence.personal`: `low`, all accepted by owner-01.
- `origin`: `paper` and `manual`; `paper` covers source-specific facts, while
  `manual` covers the bounded synthesis accepted by owner-01. `created` and
  `updated`: `2026-08-18`.
- `Hover Summary`, `Definition`, `My Understanding`, `Engineering View`,
  `Application`, `Formula`, `Decision Log`, and `Sources`: use Chinese-first
  final text accepted by owner-01, with E01-E04 supporting the paper-specific
  portions.
- `Definition`: distinguish a reusable integer-harmonic RF-cavity definition
  from the selected paper's third-harmonic example.
- `Engineering View`: distinguish passive and possible active operation,
  describe P02 absorption as the accepted scope decision, and keep the paper's
  Q0, R/Q, shunt impedance, dimensions, and six-cavity configuration
  explicitly paper-specific.
- `Formula`: add only the bounded harmonic-frequency relation with defined
  symbols; no full bunch-lengthening model is proposed.
- `Definition`, `Formula`, and passive/active operating-mode interpretation:
  bounded synthesis from the paper case and the human-approved KA-02 scope
  decision, not a paper quotation or a complete bunch-lengthening model; this
  bounded synthesis and the `manual` origin were accepted by owner-01.
- `Related Concepts`: retain only minimal resolvable provisional links mapped
  by E05; this does not change stable Concept files.
- `My Understanding`, `Decision Log`, and body approval were accepted by
  owner-01; project-specific applicability remains explicitly limited.
- Evidence-kind boundary: E01-E04 are faithful paraphrases; E05-E07 are
  explicitly inferences for provisional related-concept, category, and bounded
  synthesis mapping; no exact quote is used as factual support.

## Evidence

### E01

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.1 Double-RF context and frequencies`
- Kind: paraphrase
- Source-grounded paraphrase: The paper describes a roughly 500.12 MHz main RF
  system together with a 1500.36 MHz third-harmonic system for bunch
  lengthening.
- Supports candidate field/section: `Definition`, `Application`, `Hover Summary`
- Uncertainty: The broader definition and transfer beyond this paper remain
  unresolved.

### E02

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.3 Harmonic-cavity parameters`
- Kind: paraphrase
- Source-grounded paraphrase: The paper reports a 1500.36 MHz harmonic cavity,
  unloaded Q, Q0 = 36,000, paper-reported R/Q = 68 ohm, shunt impedance of
  2.45 Mohm, and a 90 mm effective length.
- Supports candidate field/section: `Definition`, `Engineering View`,
  `Sources`
- Uncertainty: These are paper-specific parameters. The R/Q value is reported
  under a convention that cannot be generalized unconditionally, and no value
  is generalized to the current machine.

### E03

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.4 Frequency tuners and couplers are different functions`
- Kind: paraphrase
- Source-grounded paraphrase: The paper distinguishes harmonic-cavity
  frequency tuning from input-coupler and possible active-loop details, and
  describes passive and active operating questions.
- Supports candidate field/section: `Engineering View`, `Unresolved or
  Disputed`
- Uncertainty: Operating boundaries, ports, and current-project applicability
  remain unresolved.

### E04

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.5 Six harmonic cavities and the lifetime claim`
- Kind: paraphrase
- Source-grounded paraphrase: The paper describes six harmonic cavities with a
  combined shunt impedance of 14.7 Mohm and a paper-specific lifetime factor
  claim whose verification remains open.
- Supports candidate field/section: `Engineering View`, `Application`
- Uncertainty: The lifetime claim is not a general project conclusion.

### E05

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.3 Harmonic-cavity parameters`
- Kind: inference
- Reasoning: The source terms cavity mode, shunt impedance, R/Q, and Q are
  mapped to existing canonical names only as provisional review links. This is
  a navigation inference, not a claim that the paper defines those Concepts.
- Supports candidate field/section: `Related Concepts`
- Uncertainty: A human must confirm the usefulness and direction of each link.

### E06

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.1 Double-RF context and frequencies`; `3.3 Harmonic-cavity parameters`
- Kind: inference
- Reasoning: The proposed `accelerator physics` and `RF engineering`
  categories are inferred from the selected source's accelerator RF cavity and
  double-RF/harmonic-cavity context. This is not a paper quotation or a source
  assertion that these are the canonical categories.
- Supports candidate field/section: `category`
- Uncertainty: The category assignment remains provisional and requires human
  review.

### E07

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.1 Double-RF context and frequencies`; `3.4 Frequency tuners and
  couplers are different functions`; KA-02 `retain_for_revision` scope decision
- Kind: inference
- Reasoning: The reusable integer-harmonic definition, `f_h = n f_0`, and the
  interpretation of passive and active operation as operating modes are bounded
  synthesis from the paper case and the human-approved KA-02 scope decision.
  This is not a paper quotation and is not a complete bunch-lengthening model.
- Supports candidate field/section: `Definition`, `Formula`, `My Understanding`,
  `Engineering View`
- Uncertainty: owner-01 accepted this bounded synthesis and the `manual` origin;
  project-specific applicability remains subject to future verification.

## Unresolved or Disputed

- Current-machine applicability, passive versus active boundary, port
  configuration, cavity count, geometry, and lifetime interpretation remain
  unresolved; unsupported machine-specific conclusions are not promoted.
- Paper-specific numerical values must not be promoted as current-machine facts.
- The Chinese-first body and `谐波腔` alias were accepted for this promotion;
  future localization or alias changes require a separate human decision.

## Review Record

- Human review: accepted by owner-01 on 2026-08-18; the complete revised
  candidate and all listed human-owned fields were accepted.
- KA-02 evaluation input: `retain_for_revision`; owner-01 accepted P02's
  passive-operation absorption as an operating-mode scope decision, not an
  automatic alias.
- Scientific acceptance: accepted by owner-01 on 2026-08-18.

## Promotion Record

- Promoted: yes
- Promotion approval: owner-01 explicitly authorized manual promotion on
  2026-08-18.
- Stable path: `ResearchOS/01_Concept/Harmonic cavity.md`
- Promotion timestamp: `2026-08-18T14:40:54.940Z`

## Lifecycle Log

- 2026-08-18T07:20:42.967Z - Created as a proposed candidate by KA-01 post-audit correction; pending human review.
- 2026-08-18 - Candidate revised under the human-approved KA-02 direction; state remained proposed and scientific acceptance and promotion remain pending.
- 2026-08-18T14:40:54.940Z - owner-01 transitioned this proposal from proposed to accepted after accepting the complete revised candidate and explicitly authorized manual promotion to `ResearchOS/01_Concept/Harmonic cavity.md`.

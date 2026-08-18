# Proposal ka01-20260818t065446z-67f9fb66-p01-create

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p01-create`
- Run ID: `ka01-20260818t065446z-67f9fb66`
- Type: create
- State: proposed
- Human owner: unassigned
- Prompt path: `ResearchOS/99_Meta/prompts/concept_proposal_v0.1.md`
- Prompt version: `v0.1`
- Repository baseline commit: `fb0538ce9ddf22a8e3c151a05820f03fc5dc7892`
- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Source SHA-256: `67f9fb66faa227d27947e75fb5bd7c4ecfedd222bd09ad4ae2648673c2629627`
- Prepared by: manually triggered Codex implementation conversation
- Prepared at: `2026-08-18T06:54:46.411Z`
- Source locator: `3.1 Double-RF context and frequencies`; `3.3 Harmonic-cavity parameters`; `3.4 Frequency tuners and couplers are different functions`; `3.5 Six harmonic cavities and the lifetime claim`
- Target stable id: not applicable
- Target stable path: not applicable
- Supersedes: none

## Summary

Propose a limited `Harmonic cavity` Concept candidate from direct paper-supported
content. The candidate is review material only; it is not stable knowledge and
does not imply approval or promotion.

## Proposed Changes

- `id`: propose `harmonic_cavity`; no canonical, alias, or semantic registry
  match was found.
- `aliases`: `[]`; no source-supported alternate name is required.
- `category`: propose `accelerator physics` and `RF engineering` as review
  categories; field-level evidence is E06.
- `level`, `confidence.textbook`, and `confidence.personal`: remain
  `TODO(HUMAN)`; no human judgment is inferred.
- `origin`: `paper`; `created` and `updated`: `2026-08-18`.
- `Hover Summary`, `Definition`, `Engineering View`, `Application`, and
  `Sources`: field-level evidence is E01-E04.
- `Related Concepts`: provisional review links are mapped by E05; this does
  not change stable Concept files.
- `My Understanding` and `Decision Log`: remain `TODO(HUMAN)`.
- `Formula`: remains `UNRESOLVED`; no equation or symbol definition is
  invented.
- Evidence-kind boundary: E01-E04 are faithful paraphrases; E05 and E06 are
  explicitly inferences for provisional related-concept and category mapping;
  no exact quote is used as factual support.

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

## Unresolved or Disputed

- A formal reusable definition, level, and both confidence values require human
  review.
- The formula, current-machine applicability, passive versus active boundary,
  port configuration, and lifetime interpretation are `UNRESOLVED`.
- Paper-specific numerical values must not be promoted as current-machine facts.
- Chinese-first body localization and Chinese aliases remain `TODO(HUMAN)`
  before any promotion; no aliases are proposed in this run.

## Review Record

- Human review: pending; no human owner is assigned.
- Scientific acceptance: not recorded.

## Promotion Record

- Promoted: no
- Promotion approval: not recorded; separate explicit human authorization is
  required.
- Stable path: not applicable

## Lifecycle Log

- 2026-08-18T07:20:42.967Z - Created as a proposed candidate by KA-01 post-audit correction; pending human review.

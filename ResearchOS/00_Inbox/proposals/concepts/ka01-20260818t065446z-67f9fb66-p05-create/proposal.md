# Proposal ka01-20260818t065446z-67f9fb66-p05-create

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p05-create`
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
- Source locator: `3.1 Double-RF context and frequencies`; `3.5 Six harmonic cavities and the lifetime claim`; `5.2 rw-entry-0004 — Bunch-lengthening references`
- Target stable id: not applicable
- Target stable path: not applicable
- Supersedes: none

## Summary

Propose a limited `Bunch lengthening` Concept candidate from the paper's direct
design objective and bounded proportionality claim. The candidate is review
material only; it is not stable knowledge and does not imply approval or
promotion.

## Proposed Changes

- `id`: propose `bunch_lengthening`; no canonical, alias, or semantic registry
  match was found.
- `aliases`: `[]`; no source-supported alternate name is required.
- `category`: propose `accelerator physics` and `RF engineering` as review
  categories; field-level evidence is E05.
- `level`, `confidence.textbook`, and `confidence.personal`: remain
  `TODO(HUMAN)`; no human judgment is inferred.
- `origin`: `paper`; `created` and `updated`: `2026-08-18`.
- `Hover Summary`, `Definition`, `Engineering View`, `Application`, and
  `Sources`: field-level evidence is E01-E03.
- `Related Concepts`: the provisional review link is mapped by E04; this does
  not change stable Concept files.
- `My Understanding` and `Decision Log`: remain `TODO(HUMAN)`.
- `Formula`: remains `UNRESOLVED`; the paper's proportionality statement is
  not converted into an equation.
- Evidence-kind boundary: E01-E03 are faithful paraphrases; E04 and E05 are
  explicitly inferences for provisional related-concept and category mapping;
  no exact quote is used as factual support.

## Evidence

### E01

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.1 Double-RF context and frequencies`
- Kind: paraphrase
- Source-grounded paraphrase: The paper describes a third-harmonic RF system
  used with the main RF system in a bunch-lengthening design.
- Supports candidate field/section: `Definition`, `Application`, `Hover Summary`
- Uncertainty: The exact efficiency definition and operating conditions are not
  established by this statement alone.

### E02

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.5 Six harmonic cavities and the lifetime claim`
- Kind: paraphrase
- Source-grounded paraphrase: The paper reports six harmonic cavities and
  describes their use in the bunch-lengthening design, alongside a
  paper-specific lifetime factor claim.
- Supports candidate field/section: `Engineering View`, `Application`
- Uncertainty: The lifetime claim has explicit verification limits and is not a
  general conclusion.

### E03

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `5.2 rw-entry-0004 — Bunch-lengthening references`
- Kind: paraphrase
- Source-grounded paraphrase: The reading note records the paper's statement
  that bunch-lengthening efficiency is proportional to cavity shunt impedance,
  while preserving the efficiency meaning and conditions as unresolved.
- Supports candidate field/section: `Definition`, `Engineering View`,
  `Unresolved or Disputed`
- Uncertainty: No formula, model, or current-machine conclusion is supplied.

### E04

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `5.2 rw-entry-0004 — Bunch-lengthening references`
- Kind: inference
- Reasoning: The source's shunt-impedance term is mapped to the existing
  canonical `Shunt impedance` name only as a provisional review link. This is
  not a source-defined relation and does not alter the stable Concept.
- Supports candidate field/section: `Related Concepts`
- Uncertainty: A human must confirm whether the relation is useful.

### E05

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.1 Double-RF context and frequencies`; `5.2 rw-entry-0004 — Bunch-lengthening references`
- Kind: inference
- Reasoning: The proposed `accelerator physics` and `RF engineering`
  categories are inferred from the selected source's accelerator RF cavity,
  double-RF, and bunch-lengthening context. This is not a paper quotation or a
  source assertion that these are the canonical categories.
- Supports candidate field/section: `category`
- Uncertainty: The category assignment remains provisional and requires human
  review.

## Unresolved or Disputed

- The exact efficiency definition, formula, model, level, confidence, and
  current-machine applicability are `TODO(HUMAN)` or `UNRESOLVED`.
- Detuning, fill pattern, beam distribution, and lifetime interpretation are
  not silently converted from synthesis or verification material into paper
  facts.
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

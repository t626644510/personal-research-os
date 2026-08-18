# Proposal ka01-20260818t065446z-67f9fb66-p03-create

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p03-create`
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
- Source locator: `3.4 Frequency tuners and couplers are different functions`
- Target stable id: not applicable
- Target stable path: not applicable
- Supersedes: none

## Summary

Propose a limited `Frequency tuner` Concept candidate from the paper's direct
description of copper-rod and plunger tuning. The candidate is review material
only; it is not stable knowledge and does not imply approval or promotion.

## Proposed Changes

- `id`: propose `frequency_tuner`; no canonical, alias, or semantic registry
  match was found.
- `aliases`: `[]`; no source-supported alternate name is required.
- `category`: propose `RF engineering` as a review category; field-level
  evidence is E03.
- `level`, `confidence.textbook`, and `confidence.personal`: remain
  `TODO(HUMAN)`; no human judgment is inferred.
- `origin`: `paper`; `created` and `updated`: `2026-08-18`.
- `Hover Summary`, `Definition`, `Engineering View`, `Application`, and
  `Sources`: field-level evidence is E01.
- `Related Concepts`: the provisional review link is mapped by E02; this does
  not change stable Concept files.
- `My Understanding` and `Decision Log`: remain `TODO(HUMAN)`.
- `Formula`: remains `UNRESOLVED`; no tuning equation is invented.
- Evidence-kind boundary: E01 is a faithful paraphrase; E02 and E03 are
  explicitly inferences for provisional related-concept and category mapping;
  no exact quote is used as factual support.

## Evidence

### E01

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.4 Frequency tuners and couplers are different functions`
- Kind: paraphrase
- Source-grounded paraphrase: The source describes two copper rods, each 95 mm
  in diameter; each moves ±50 mm, with about ±0.5 MHz range. It also describes
  two plungers, each 30 mm in diameter; each moves ±25 mm, with about ±0.5 MHz
  range.
- Supports candidate field/section: `Definition`, `Engineering View`,
  `Application`, `Hover Summary`
- Uncertainty: The mechanisms and ranges are design-specific; a general
  reusable definition and current-machine applicability remain unresolved.

### E02

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.4 Frequency tuners and couplers are different functions`
- Kind: inference
- Reasoning: The source's cavity-tuning language is mapped to the existing
  canonical `Cavity mode` name only as a provisional review link. This is not a
  source-defined relation and does not alter the stable Concept.
- Supports candidate field/section: `Related Concepts`
- Uncertainty: A human must confirm whether this relation is useful.

### E03

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.4 Frequency tuners and couplers are different functions`
- Kind: inference
- Reasoning: The proposed `RF engineering` category is inferred from the
  selected source's accelerator RF cavity and tuner context. This is not a
  paper quotation or a source assertion that this is the canonical category.
- Supports candidate field/section: `category`
- Uncertainty: The category assignment remains provisional and requires human
  review.

## Unresolved or Disputed

- The general mechanism, level, confidence, formula, failure modes, and
  current-machine applicability are `TODO(HUMAN)` or `UNRESOLVED`.
- The numerical dimensions and ranges must remain attributed to the selected
  paper's design.
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

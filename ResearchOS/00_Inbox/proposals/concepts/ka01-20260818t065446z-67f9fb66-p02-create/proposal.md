# Proposal ka01-20260818t065446z-67f9fb66-p02-create

- Proposal ID: `ka01-20260818t065446z-67f9fb66-p02-create`
- Run ID: `ka01-20260818t065446z-67f9fb66`
- Type: create
- State: superseded
- Human owner: owner-01
- Prompt path: `ResearchOS/99_Meta/prompts/concept_proposal_v0.1.md`
- Prompt version: `v0.1`
- Repository baseline commit: `fb0538ce9ddf22a8e3c151a05820f03fc5dc7892`
- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Source SHA-256: `67f9fb66faa227d27947e75fb5bd7c4ecfedd222bd09ad4ae2648673c2629627`
- Prepared by: manually triggered Codex implementation conversation
- Prepared at: `2026-08-18T06:54:46.411Z`
- Source locator: `3.4 Frequency tuners and couplers are different functions`; `4.2 rw-entry-0002 — Coupling tuner and passive-cavity couplers`
- Target stable id: not applicable
- Target stable path: not applicable
- Supersedes: none
- Superseded by: `ka01-20260818t065446z-67f9fb66-p01-create`

## Summary

This retained proposal records a limited `Passive harmonic cavity` candidate
from direct paper-supported operating-mode content. It was superseded by P01;
the passive operation scope is retained as an operating-mode subsection inside
`Harmonic cavity`, not as a separate stable Concept.

## Proposed Changes

- `id`: propose `passive_harmonic_cavity`; no canonical, alias, or semantic
  registry match was found.
- `aliases`: `[]`; no source-supported alternate name is required.
- `category`: propose `accelerator physics` and `RF engineering` as review
  categories; field-level evidence is E04.
- `level`, `confidence.textbook`, and `confidence.personal`: remain
  `TODO(HUMAN)`; no human judgment is inferred.
- `origin`: `paper`; `created` and `updated`: `2026-08-18`.
- `Hover Summary`, `Definition`, `Engineering View`, `Application`, and
  `Sources`: field-level evidence is E01-E02.
- `Related Concepts`: provisional review links are mapped by E03; this does
  not change stable Concept files.
- `My Understanding` and `Decision Log`: remain `TODO(HUMAN)`.
- `Formula`: remains `UNRESOLVED`; no equation or symbol definition is
  invented.
- Evidence-kind boundary: E01-E02 are faithful paraphrases; E03 and E04 are
  explicitly inferences for provisional related-concept and category mapping;
  no exact quote is used as factual support.

## Evidence

### E01

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.4 Frequency tuners and couplers are different functions`
- Kind: paraphrase
- Source-grounded paraphrase: The paper describes normal harmonic-cavity
  operation without an RF power supply actively driving the cavity and
  distinguishes this from a possible active-operation case using a rotatable
  coaxial loop coupler.
- Supports candidate field/section: `Definition`, `Engineering View`,
  `Application`, `Hover Summary`
- Uncertainty: This is a source-specific operating description; general
  passive-cavity scope and port behavior remain unresolved.

### E02

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `4.2 rw-entry-0002 — Coupling tuner and passive-cavity couplers`
- Kind: paraphrase
- Source-grounded paraphrase: The paper-supported part of the human question
  distinguishes passive harmonic-cavity operation from open questions about
  couplers, ports, and an active mode.
- Supports candidate field/section: `Engineering View`, `Unresolved or
  Disputed`
- Uncertainty: The unresolved questions are not converted into paper facts.

### E03

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.4 Frequency tuners and couplers are different functions`
- Kind: inference
- Reasoning: The source's cavity, Q, and shunt-impedance terms are mapped to
  existing canonical names only as provisional review links. This does not
  assert a source-defined relation or alter stable Concepts.
- Supports candidate field/section: `Related Concepts`
- Uncertainty: A human must confirm the usefulness of each link.

### E04

- Source Vault path: `00_Inbox/reading/ipac2019-weprb066/reading_note.md`
- Locator: `3.4 Frequency tuners and couplers are different functions`; `4.2 rw-entry-0002 — Coupling tuner and passive-cavity couplers`
- Kind: inference
- Reasoning: The proposed `accelerator physics` and `RF engineering`
  categories are inferred only from the selected source's accelerator RF
  cavity, double-RF/harmonic-cavity, and passive-operation context. This is not
  a paper quotation or a source assertion that these are the canonical
  categories.
- Supports candidate field/section: `category`
- Uncertainty: The category assignment remains provisional and requires human
  review.

## Unresolved or Disputed

- General definition, level, confidence, formula, ports, loading, and passive
  versus active boundary are `TODO(HUMAN)` or `UNRESOLVED`.
- No statement here determines the current machine's RF implementation.
- Chinese-first body localization and Chinese aliases remain `TODO(HUMAN)`
  before any promotion; no aliases are proposed in this run.

## Review Record

- Human review: superseded by owner-01 on 2026-08-18.
- Supersession decision: proposal
  `ka01-20260818t065446z-67f9fb66-p01-create` replaces this candidate because
  it incorporates the accepted passive-operation scope inside `Harmonic cavity`
  without creating a separate passive-cavity Concept or alias.
- Scientific acceptance: superseded; no stable Concept was promoted from P02.

## Promotion Record

- Promoted: no
- Promotion approval: not applicable after supersession.
- Stable path: not applicable

## Lifecycle Log

- 2026-08-18T07:20:42.967Z - Created as a proposed candidate by KA-01 post-audit correction; pending human review.
- 2026-08-18T14:40:54.940Z - owner-01 transitioned this proposal from proposed to superseded by `ka01-20260818t065446z-67f9fb66-p01-create`; the accepted merge rationale is passive operation as an internal operating mode, with this artifact retained permanently.

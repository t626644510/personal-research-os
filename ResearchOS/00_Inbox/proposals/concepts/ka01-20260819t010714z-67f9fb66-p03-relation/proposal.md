# Proposal ka01-20260819t010714z-67f9fb66-p03-relation

- Proposal ID: ka01-20260819t010714z-67f9fb66-p03-relation
- Run ID: ka01-20260819t010714z-67f9fb66
- Type: relation
- State: deferred
- Human owner: owner-01
- Prompt path: ResearchOS/99_Meta/prompts/concept_proposal_v0.1.md
- Prompt version: v0.1
- Repository baseline commit: 2ef697927ee5d6e739b5cbb48c5745622312961d
- Source Vault path: 00_Inbox/reading/ipac2019-weprb066/reading_note.md
- Source SHA-256: 67f9fb66faa227d27947e75fb5bd7c4ecfedd222bd09ad4ae2648673c2629627
- Prepared by: Codex manually triggered implementation conversation
- Prepared at: 2026-08-19T01:07:14Z
- Source locator: `3.4 Frequency tuners and couplers are different functions`
- Target stable id: `tuner`
- Target stable path: `ResearchOS/01_Concept/Tuner.md`
- Supersedes: none

## Summary

This is a relation-only proposal for the KA-04 Stage 1 trial. It targets the
existing stable Concept `tuner` and changes only its Related Concepts
wikilink list. The proposal is deferred by human decision and remains
unpromoted.

## Proposed Changes

- Target section: `Related Concepts`.
- Navigation direction under review: `Tuner` → `Harmonic cavity`.
- Current Related Concepts state:
  - [[Cavity mode]]
- Additions:
  - [[Harmonic cavity]]
- Removals: none.
- Proposed Related Concepts state:
  - [[Cavity mode]]
  - [[Harmonic cavity]]
- No YAML field, H1, explanatory prose outside Related Concepts, source
  metadata, formula, or History content is changed.
- The candidate is a complete copy of the current stable target with only the
  proposed wikilink bullet added inside Related Concepts.

## Evidence

### E01 — Source-supported relation context

- Source Vault path: 00_Inbox/reading/ipac2019-weprb066/reading_note.md
- Locator: `3.4 Frequency tuners and couplers are different functions`
- Kind: paraphrase
- Evidence: The paper describes the harmonic-cavity frequency tuner as a separate function from couplers, with two 30 mm plungers moving ±25 mm for about ±0.5 MHz; this directly places frequency-tuner functionality in the harmonic-cavity engineering context.
- Supports candidate field/section: `Related Concepts` addition [[Harmonic cavity]].
- Boundary: This is a faithful paraphrase of the selected reading note's
  paper-supported content, not a quotation and not a general claim about every
  paper or every cavity.

### E02 — Durable navigation rationale

- Source Vault path: 00_Inbox/reading/ipac2019-weprb066/reading_note.md
- Locator: `3.4 Frequency tuners and couplers are different functions`
- Kind: inference
- Evidence: A reverse-direction link from the reusable Tuner Concept to the existing Harmonic cavity Concept improves navigation from a tuning mechanism to a demonstrated RF-cavity application. It is proposed separately with its own evidence and rationale, not generated as automatic reciprocity from r02.
- Supports candidate field/section: `Related Concepts` addition [[Harmonic cavity]].
- Boundary: This inference proposes a useful cross-Concept navigation path only;
  it does not introduce a typed relation, universal engineering law, or
  automatic reciprocal link.

## Unresolved or Disputed

- The link is an application/navigation relation only. It does not make Harmonic cavity the only tuner application, include Coupling tuner, or promote the paper's geometry-specific tuning data into a universal law.
- The relation was reviewed and deferred by `owner-01`; any future
  reconsideration requires a new explicit human request.
- The source-specific numerical/design details do not become stable Concept
  changes through this relation proposal.
- The forward direction was independently accepted and promoted as P02, but
  that decision does not imply this reverse link.

## Review Record

- Review status: deferred by human decision.
- Reviewer: owner-01.
- Human decision: deferred.
- Rationale: The relation is a weak generic-to-example edge with reciprocal and
  application-list growth risk.
- Review scope: exact target, one link addition, evidence locators, durability,
  and over-linking risk.

## Promotion Record

- Promoted: no.
- Promotion status: not authorized and not performed.
- Stable Concept path: not applicable.
- Promotion decision: deferred; no promotion authorization was granted.

## Lifecycle Log

- 2026-08-19 - Created as a relation proposal by the manually
  triggered Codex implementation conversation; initial state is `proposed`.
- 2026-08-19T01:58:16Z - owner-01 deferred this relation after human review;
  it is not rejected, but remains unpromoted because of reciprocal and
  application-list growth risk. Return to `proposed` requires a later explicit
  human request.

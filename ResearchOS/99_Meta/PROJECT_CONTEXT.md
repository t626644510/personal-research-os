# Personal Research OS Project Context

Status: KA-00 governance accepted; KA-01 eligibility gate open; KA-01 not authorized and not started\
Pre-KA-00 implementation baseline: `d622b92c78d3fcaf327db93e599e6a77fe112f1c`\
Current governance version: identified by this document's Git history\
Future KA-01 run baseline: `git rev-parse HEAD` at run start\
Active business stage: **Stage 01: Knowledge Agent Integration**

## Completed capabilities

- The versioned Vault scaffold, stable Concept Schema v0.1, deterministic
  Concept validator/indexer, and Git workflow exist.
- The stable Concept Database and generated `concept_index.json` support
  canonical names, stable ids, aliases, categories, related wikilinks, and
  offline lookup.
- P01 provides deterministic local mention resolution.
- Commit `9af4145` established the accepted P01.5 local HTML UI prototype
  baseline. Its human reading and UX evaluation questions remain open.
- Commit `d622b92` added Chinese localization, Chinese alias display
  conventions, localized reading samples, and tests.

## Immutable architecture decisions

These decisions remain fixed unless a separate architecture change is
explicitly approved:

- `ResearchOS/01_Concept/` contains human-approved stable knowledge only.
- `ResearchOS/99_Meta/Concept_Schema_v0.1.md` is unchanged and remains the
  stable Concept contract.
- `concept_index.json` is derived from stable Concept Markdown and is never a
  proposal workspace or a hand-edited knowledge source.
- Hover lookup remains local, offline, deterministic, and free of AI calls.
- Codex is a manually triggered knowledge-production assistant. No
  repository-hosted AI client, Agent runtime, or model/API call is planned now.
- Proposal artifacts remain under `ResearchOS/00_Inbox/proposals/` as audit
  records. Their content can affect stable knowledge only through a separately
  approved promotion action.
- A KA-01 source must be exactly one Markdown file inside
  `ResearchOS/00_Inbox/`, outside its `proposals/` subtree, after traversal and
  symlink resolution. Its stored identity is a Vault-relative POSIX path plus
  a SHA-256 fingerprint.
- Every valid one-source KA-01 execution has exactly one persistent run
  assessment at
  `ResearchOS/00_Inbox/proposals/runs/<run_id>/assessment.md`.
- Concept relations remain Obsidian wikilinks; no graph database or typed-edge
  architecture is introduced.

## Current open questions

- The human evaluation questions in `P01.5_UI_Validation.md`, including
  highlight density, summary length, Concept granularity, reading efficiency,
  alias matching, and keyboard behavior, are unresolved.
- A one-source trial must test proposal classification, duplicate control,
  provenance quality, uncertainty handling, and human review cost.
- The project has not decided whether any later extraction automation or
  repository runtime would be justified.

## Active stage and next gate

KA-00 governance is accepted. KA-01's eligibility gate is open, but KA-01 is
not authorized and not started. The next executable gate requires a separate
explicit human instruction approving `prompts/concept_proposal_v0.1.md` and
exactly one eligible source. Only that separately approved conversation may
process one human-selected Markdown file inside `ResearchOS/00_Inbox/` and
outside `ResearchOS/00_Inbox/proposals/`. It may create one run assessment and
Concept proposal artifacts only under `ResearchOS/00_Inbox/proposals/`, then
must stop for human review.

## Explicit non-goals

- No AI client, Agent runtime, API call, RAG, embeddings, vector database,
  crawler, watcher, scheduled scan, or automatic promotion.
- No extraction code, multi-source batch, network requirement, or new
  dependency.
- No change to Concept Schema v0.1, stable Concepts, or the generated index
  during KA-00.
- No invented personal confidence, personal understanding, Decision Log
  entry, citation, formula, or experimental conclusion.

## Role boundary

The audit/planning conversation does not modify code. When the human directly
requests it, that conversation may update only the explicitly designated
context, roadmap, governance, and prompt Markdown files.

The explicitly authorized Markdown files above are the only working-tree
artifacts it may change. It never modifies stable Concepts, generated indexes,
source material, proposal scientific content, or dependencies. It never
modifies Git state, including the index/staging area, branch or tag refs,
commits, or remotes. It does not promote candidates or execute a
research-source run.

Implementation artifacts remain the responsibility of a separate
implementation prompt that the human has explicitly approved.

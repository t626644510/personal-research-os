# Personal Research OS Project Context

Status: KA-00 governance accepted; RW-00 governance accepted and complete on 2026-08-04;\
RW-01 eligibility gate open; RW-01 not authorized and not started;\
KA-01 eligibility gate open; KA-01 not authorized and not started\
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

## Accepted Reading Workspace design direction

- Reading Workspace is planned as an upstream source-preparation layer for
  KA-01. It does not replace the Knowledge Proposal Protocol, proposal review,
  or human-approved promotion.
- Stable Concept files and the generated `concept_index.json` are read-only
  consumers for the Reading UI. Hover resolution remains deterministic,
  local, and offline.
- Human annotations are human-owned and must never be silently rewritten.
- A minimal `author_type` distinction remains visible even when confidence
  and verification metadata are present. Confidence is a filtering and review
  aid, not proof.
- Pasted LLM answers default to unverified auxiliary material. LLM synthesis
  may prepare a reading-note draft only.
- Only a human may assign `human_reviewed` to a reading note. A changed note
  must be reviewed again before another handoff.
- A Reading Workspace handoff may pass only one human-selected, reviewed
  `reading_note.md` to a KA-01 run. KA-01 does not follow its links to session
  data, PDFs, other papers, or LLM transcripts.
- Only that final, selected KA source receives the existing KA-01 SHA-256
  fingerprint, computed when the run begins. RW does not require a PDF hash or
  a second provenance hash.
- Provenance laundering, circular LLM reuse, copyright, privacy, subjective
  confidence, noisy highlighting, and review burden are recorded risks, but
  they are not acceptance blockers for the RW-01 prototype.
- Initial LLM interaction remains manual: prepare and copy a question, then
  paste the external answer into the local session. No model call is embedded
  in the first UI.

## Current open questions

- The human evaluation questions in `P01.5_UI_Validation.md`, including
  highlight density, summary length, Concept granularity, reading efficiency,
  alias matching, and keyboard behavior, are unresolved.
- RW-01 must evaluate reading readability, annotation friction, confidence
  controls, question/answer traceability, and whether the workflow is useful
  enough to justify later PDF overlays or an Obsidian plugin.
- A one-source trial must test proposal classification, duplicate control,
  provenance quality, uncertainty handling, and human review cost.
- The project has not decided whether any later extraction automation or
  repository runtime would be justified.

## Active stage and next gate

RW-00 governance and the P0 UI contract were human accepted and completed on
2026-08-04. The RW-01 eligibility gate is open, but RW-01 is not authorized
and not started. The next executable action requires a separate explicit
human-approved RW-01 implementation prompt. Acceptance of RW-00 does not
authorize RW-01, RW-02, reading artifacts, model calls, or KA-01. Integrated
AI runtime, automatic acquisition, and a full Obsidian plugin remain outside
the first prototype. Stage 02 Information Acquisition remains a separate
future concern.

No Reading Workspace implementation and no KA-01 execution have occurred
during RW-00. No reading session, source, reading-note, run-assessment, or
proposal artifact has been created by this phase.

KA-00 governance remains accepted. KA-01's eligibility gate remains open, but
KA-01 is not authorized and not started. The human has expressed intent to run
KA-01 after an eligible reviewed source exists; intent alone is not execution
authority. A protocol-valid run still requires a separate explicit human
instruction naming exactly one eligible `SOURCE_PATH` and approving the
prompt version used at execution time. For a Reading Workspace handoff, that
source is the one human-selected, reviewed `reading_note.md`. Only the
separately approved KA-01 conversation may create one run assessment and
Concept proposal artifacts under `ResearchOS/00_Inbox/proposals/`, then it
must stop for human review.

## Explicit non-goals

- No AI client, Agent runtime, API call, RAG, embeddings, vector database,
  crawler, watcher, scheduled scan, or automatic promotion.
- No extraction code, multi-source batch, network requirement, or new
  dependency.
- No integrated AI runtime, automatic literature acquisition, coordinate-aware
  PDF overlay, OCR, automatic PDF-to-Markdown conversion, or full Obsidian
  plugin in the first Reading Workspace prototype.
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

RW-00 changes governance and specification Markdown only. It does not
implement the Reading Workspace, create reading content, execute KA-01, or
alter any KA-00 historical fact.

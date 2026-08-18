# Personal Research OS Project Context

Status: KA-00 governance accepted; RW-00 governance accepted and complete on 2026-08-04;\
RW-01 and RW-01.1 accepted and complete at commit `8afa9aa`;\
RW-02.2 human UI accepted on 2026-08-11; RW-02 accepted and complete;\
HTML prototype frozen; commit `792c802` is the published RW-02 baseline;\
RW-03 synthesis content human accepted on 2026-08-18; selected-text presentation correction applied; RW-03 accepted and complete and published at commit `7c5dc4f`; `reading_note.draft.md` remains `state: draft` as RW-03 history; final `reading_note.md` is `state: human_reviewed`; RW-04 freeze was explicitly authorized and implemented, pending final audit and publication; RW-05, Concept proposal, and KA-01 remain unauthorized and unstarted\
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
- Every RW-03 synthesis requires one human-selected `SOURCE_PATH` and one
  human-selected `SESSION_PATH`. One `EXTERNAL_SUMMARY_PATH` is optional only
  when the human explicitly selects it for that run.
- An optional external summary remains unverified, session-external,
  non-authoritative, and not `human_reviewed`. The two answer-input channels
  are canonical `llm_answer` entries already inside `SESSION_PATH` and the
  separately selected external summary. The current session has no
  `llm_answer`; it has two `human_question` and three `human_note` entries.
  The summary is not split into canonical session entries or promoted to
  paper, source, human, or reviewed content. Future deduplication may merge
  repeated wording only while retaining every origin label.
- Only a human may assign `human_reviewed` to a reading note. A changed note
  must be reviewed again before another handoff.
- A Reading Workspace handoff may pass only one human-selected, reviewed
  `reading_note.md` to a KA-01 run. KA-01 does not follow its links to session
  data, PDFs, other papers, or LLM transcripts.
- Only that final, selected KA source receives the existing KA-01 SHA-256
  fingerprint, computed when the run begins. RW does not require a PDF hash or
  a source, session, external-summary, or second provenance fingerprint.
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
- Realistic human reading on 2026-08-11 identified five RW-02.2 usability
  corrections: section-level bilingual alignment, Chinese note/question
  capture, visible annotated-block markers, an independent figure/table rail,
  and draggable widths for a full-width 4K layout. The repository owner
  accepted the resulting RW-02.2 UI on 2026-08-11 with the overall conclusion
  “通过，未报告其他问题”.
- A one-source trial must test proposal classification, duplicate control,
  provenance quality, uncertainty handling, and human review cost.
- The project has not decided whether any later extraction automation or
  repository runtime would be justified.

## Active stage and next gate

RW-00 governance and the P0 UI contract were human accepted and completed on
2026-08-04. RW-01 and RW-01.1 were human accepted and completed at commit
`8afa9aa`. RW-02.2 human UI was accepted on 2026-08-11.
Current automated verification passed 25 Concept checks, 32 focused Reading UI
tests, and 49 full-suite tests. The 974,523-byte offline HTML contains 18
bilingual section pairs, 7 images, 2 rendered tables, 3 accessible resizers,
and 131 unique annotatable source blocks. RW-02 is accepted and complete; the
HTML prototype is frozen; commit `792c802` is the published RW-02 baseline.
RW-03 was separately authorized on 2026-08-11. RW-03 synthesis content human
accepted on 2026-08-18; selected-text presentation correction applied; RW-03
accepted and complete and published at commit `7c5dc4f`. The draft remains
`state: draft` as RW-03 history, and final `reading_note.md` is
`state: human_reviewed`. RW-04 freeze was explicitly authorized and
implemented, pending final audit and publication. The final note is eligible
for a future handoff but has not been selected for any KA-01 run. RW-05,
Concept proposal, and KA-01 remain unauthorized and unstarted. The frozen prototype itself still
does not embed model calls or permit a KA-01 run. Integrated
AI runtime and automatic acquisition remain outside this prototype. Stage 02
Information Acquisition remains a separate future concern.

RW-02.1 remains a historical narrow presentation correction, not an
architecture redesign.
The English `source.reading.md` transcription remains the only authoritative
reading source and the local PDF remains the visual authority. Figures 1–7 are
local raster crops embedded into the offline page; the optional Chinese
`source.zh-CN.reading.md` is machine/LLM-assisted, unverified, derived display
aid only. It does not duplicate figures or become a second source authority.
RW-02.1 originally allowed entry creation only from English; that historical
fact is preserved. RW-02.2 supersedes only that usability boundary: English
selection permits `source_excerpt`, `human_note`, and `human_question`, while
Chinese reference selection permits `human_note` and `human_question` only,
never `source_excerpt`. New entries may record `selected_text_origin` and
`selected_block_id`; legacy entries remain byte-for-byte compatible when
those optional fields are absent.

RW-02.2 pairs the real source's 18 ordered H1/H2/H3 boundaries into bilingual
section rows, derives block-level annotation markers from canonical entries,
moves Figures 1–7 and Tables 1–2 into one independently scrolling authoritative
English rail, and provides three accessible resizers for the full-width desktop
layout. These presentation values remain outside session payloads, recovery,
session ids, entries, preferences, and Markdown export.

The ignored `_local/reading_session.md` is a byte-identical copy of the real
active session with two human questions and three human notes. The separately
copied `_local/external_llm_conversation_summary.md` remains external LLM
material, unverified, session-external, not paper-source authority, and not
`human_reviewed`; it has not entered the session.

The HTML prototype is frozen following human acceptance; commit `792c802` is
the published RW-02 baseline. The following remains a historical statement
about the RW-02.2 publication boundary: RW-02.2 did not create or start RW-03
reading-note closure, Obsidian Home, or the 1500 MHz TM020 Harmonic Cavity
project page. RW-03 was subsequently authorized on 2026-08-11. Its synthesis
content was human accepted on 2026-08-18 and the selected-text presentation
correction was applied; RW-03 is accepted and complete and published at commit
`7c5dc4f`. The draft remains `state: draft` as history, and final
`reading_note.md` is `state: human_reviewed`. RW-04 freeze is explicitly
authorized and implemented, pending final audit and publication; RW-05,
Concept proposal, and KA-01 remain unauthorized and unstarted.

No Reading Workspace implementation and no KA-01 execution have occurred
during RW-00. No reading session, source, reading-note, run-assessment, or
proposal artifact has been created by this phase.

KA-00 governance remains accepted. KA-01's eligibility gate remains open, but
KA-01 is not authorized and not started. The human has expressed intent to run
KA-01 after an eligible reviewed source exists; intent alone is not execution
authority. A protocol-valid run still requires a separate explicit human
instruction naming exactly one eligible `SOURCE_PATH` and approving the
prompt version used at execution time. For a Reading Workspace handoff, that
source is the one human-selected, reviewed `reading_note.md`. The final note is
eligible for a future handoff but has not been selected for any KA-01 run. Only the
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

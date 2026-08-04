# Reading Workspace Protocol v0.1

Version: v0.1\
Status: RW-00 governance human accepted on 2026-08-04; RW-01 eligibility gate open, not authorized or started\
Applies to: reading and source preparation upstream of KA-01

This protocol defines the smallest implementation-neutral contract for a local
Reading Workspace. It governs ownership, session entries, reading-note review,
and the one-file bridge into KA-01. It does not implement the workspace.

## 1. Purpose and boundaries

Reading and annotation occur upstream of KA-01. The workflow helps a human:

1. read one technical source locally;
2. capture source excerpts, personal notes, and questions;
3. record answers obtained from a manually triggered external LLM;
4. optionally ask an LLM to prepare a reading-note draft;
5. review and freeze one Markdown reading note; and
6. select that one reviewed note as a possible future KA-01 source.

The Reading Workspace does not define or require an AI runtime, model API,
RAG, embeddings, a vector database, a crawler, automatic acquisition,
automatic Concept generation, or automatic Concept promotion. The first
workflow uses copy/paste for LLM interaction.

`ResearchOS/01_Concept/` and
`ResearchOS/99_Meta/concept_index.json` are read-only during reading.
Concept names, aliases, and hover data may be consumed for deterministic local
display, but the Reading Workspace may not edit stable Concepts, regenerate or
hand-edit the index, create Concept proposals, or imply promotion approval.

## 2. Proposed artifact layout

The following layout is proposed for later RW implementation; RW-00 does not
create it:

```text
ResearchOS/00_Inbox/reading/<paper_id>/
├── source_record.md
├── reading_session.md
├── reading_note.draft.md
├── reading_note.md
└── _local/
    └── source.pdf
```

Responsibilities:

| Artifact | Responsibility |
| --- | --- |
| `source_record.md` | Human-visible source identity, bibliographic details when available, and local source locators |
| `reading_session.md` | Complete, portable export of session entries and their metadata |
| `reading_note.draft.md` | Optional LLM-produced or implementation-assisted synthesis draft |
| `reading_note.md` | The one reading note explicitly reviewed and selected by a human |
| `_local/source.pdf` | Proposed local-only PDF location for visual cross-checking |

The `<paper_id>` naming policy and exact Markdown serialization may be chosen
during RW-01, provided the contract in this document remains lossless and
readable. No directory or artifact is created merely because this layout is
documented.

`_local/source.pdf` should not be committed by default. RW-00 does not edit
`.gitignore`; the human remains responsible for checking Git status before
any future commit.

Making the repository private later does not erase material already published
in Git history, and repository privacy does not itself grant a right to
redistribute a publisher PDF. This is a non-blocking operational warning, not
an RW-01 acceptance blocker.

## 3. Content ownership and review metadata

The Reading Workspace keeps a minimal origin distinction:

| Content kind | Meaning and ownership |
| --- | --- |
| Source material | Quoted or paraphrased paper content; it remains attributable to the source |
| Human note | Human-owned interpretation or annotation; it is never silently rewritten |
| Human question | A question authored by the human |
| LLM answer | Auxiliary model output; unverified by default and never treated as source text |
| Synthesis draft | LLM-produced reading-note draft; never automatically reviewed |
| Reviewed reading note | A note explicitly reviewed and selected by a human |

Every session entry has one `author_type`, derived from `entry_type` by the
invariant mapping in section 4. The derived value identifies who or what
produced the content. It is not independently assignable or editable, and it
must not be replaced by a confidence score.

Every session entry also records one lightweight confidence value:

```yaml
confidence:
  - not_assessed
  - low
  - medium
  - high
```

Every session entry records one verification value:

```yaml
verification:
  - not_applicable
  - unverified
  - human_checked
  - rejected
```

Confidence and verification are the only editable review metadata. They
support filtering, display, and review. They are not scientific proof, do not
establish provenance by themselves, and do not replace the human review
required for stable Concept promotion.

Sensible editable-metadata defaults are:

- source excerpt: `confidence: not_assessed`,
  `verification: not_applicable`;
- human note or question: `confidence: not_assessed`,
  `verification: not_applicable`;
- pasted LLM answer: `confidence: not_assessed`,
  `verification: unverified`.

Verification for source and human-owned entries may be
`not_applicable` until a human deliberately chooses another value. An LLM
answer remains auxiliary even after `human_checked`; that value records a
human check, not a conversion into source material.

## 4. Reading session entry contract

A reading session uses a flat list of entries. Each entry contains:

| Field | Contract |
| --- | --- |
| `entry_id` | Stable identifier unique within the session |
| `entry_type` | One permitted entry type from the list below |
| `created_at` | ISO 8601 timestamp with `Z` or an explicit numeric timezone offset |
| `author_type` | `source`, `human`, or `llm`, derived from and required to match `entry_type`; not independently editable |
| `source_locator` | Page, heading, section, paragraph, table, figure, or a clear `not_available` / `not_applicable` value |
| `selected_text` | Exact selected source text when present; otherwise an explicit empty or not-applicable value |
| `content` | The entry body shown and exported by the UI |
| `confidence` | `not_assessed`, `low`, `medium`, or `high` |
| `verification` | `not_applicable`, `unverified`, `human_checked`, or `rejected` |

Permitted entry types are:

- `source_excerpt`;
- `human_note`;
- `human_question`;
- `llm_answer`.

The `author_type` invariant is:

| Entry type | `author_type` |
| --- | --- |
| `source_excerpt` | `source` |
| `human_note` | `human` |
| `human_question` | `human` |
| `llm_answer` | `llm` |

`entry_type` is the source of truth and its mapped `author_type` is read-only.
The invariant applies on creation, persistence, import, export, and display.
Mismatched imported data is invalid; import must stop and visibly report the
mismatch rather than silently normalize it or offer origin reassignment.

`selected_text` preserves reading context for an excerpt, note, or question
created from a selection. For a `source_excerpt`, `content` may repeat the
selected passage so the entry remains independently readable. For an entry
without a selection, the export uses one documented empty or not-applicable
representation rather than inventing source context.

An `llm_answer` also allows:

- `model_label`: optional human-entered label for the external model;
- `question_entry_id`: required link to one `human_question` entry in the
  same session.

No API identifier, provider-specific metadata, token count, cost field, model
request id, or nested provenance graph is required. Entry ids and the
question-answer link are sufficient for the first prototype.

Import and export must preserve every entry, field value, entry id, and
question link without silent normalization or loss. The source-text embedding
or local-file reassociation strategy may be selected during RW-01, but
re-importing `reading_session.md` must not lose or rewrite session entries.

Before final Markdown export, RW-01 must make every session mutation
recoverable in an offline local draft. The UI must show a clear saved, unsaved,
or recovery state; refreshing or reopening it must offer recovery of the
latest local session draft; and clearing recovered data must require an
explicit human action. The persistence mechanism must not transmit source
text, annotations, or LLM answers. Its technology remains an implementation
choice: this protocol does not mandate `localStorage`, IndexedDB, a server, or
a framework. Markdown export/import remains the portable, Git-reviewable
session artifact. "Local session draft" describes recovery working state, not
a reading-session artifact state.

## 5. State model

States apply to artifacts, not to individual session entries. Applicability is
split by artifact type.

Reading session states:

| State | Meaning |
| --- | --- |
| `active` | Reading session content is being captured or revised |
| `superseded` | A retained reading session has been replaced by a later one |

Reading-note states:

| State | Meaning |
| --- | --- |
| `draft` | A reading-note candidate exists but has not been human reviewed |
| `human_reviewed` | A human explicitly reviewed and froze the selected reading note |
| `superseded` | A retained reading note has been replaced by a later one |

An LLM or implementation agent may create only `active` reading-session
content and `draft` reading notes. It may not assign `human_reviewed`,
impersonate a reviewer, or select the KA-01 source on the human's behalf.

Only a human may assign `human_reviewed` to one reading note and select it for
handoff. Human review freezes the meaning of that version; it does not assert
scientific truth or promote any Concept.

If a human-reviewed reading note changes later, the changed content loses its
frozen meaning and must return to `draft` until it is explicitly reviewed
again. The previous reviewed version may be retained as `superseded`, but a
superseded note is not eligible for a new handoff unless a human reviews and
selects the intended version again.

## 6. KA-01 bridge

The Reading Workspace preserves the existing KA-01 one-file boundary:

- The human selects exactly one reviewed `reading_note.md` and supplies its
  exact `SOURCE_PATH` when separately authorizing a KA-01 run.
- KA-01 reads only that Markdown file. It does not follow links to
  `source_record.md`, `reading_session.md`, `source.pdf`, other papers,
  LLM transcripts, or any second input.
- The selected reading note must therefore contain the evidence, attribution,
  uncertainty, and page/section locators needed for proposal review.
- When the KA-01 run actually begins, the existing Knowledge Proposal Protocol
  computes one SHA-256 over the exact raw bytes of the selected Markdown file.
- No PDF hash, session hash, source-record hash, double hash, or second
  provenance fingerprint is required by RW.
- KA-01 classification, proposal artifacts, human review, and promotion rules
  remain unchanged.
- RW-00 does not modify
  `ResearchOS/99_Meta/Knowledge_Proposal_Protocol_v0.1.md`.

Intent to run KA-01 later is not execution authority. A valid run still
requires a separate human instruction providing the exact eligible
`SOURCE_PATH` and approving the execution prompt version used at that time.

## 7. Non-blocking risk register

| Risk | Design note |
| --- | --- |
| Origin confusion | LLM content may be mistaken for source content; keep `author_type` visible |
| Provenance laundering | Repeated LLM synthesis can obscure where a statement originated |
| Circular LLM reuse | A later answer may unknowingly restate earlier model output |
| Subjective confidence | Confidence reflects a judgment aid, not objective correctness |
| Public Git history | Committed documents may expose copyrighted material or private research context even if the repository becomes private later |
| Redistribution rights | Publisher PDFs may have restrictions independent of repository visibility |
| Research privacy | Human notes may contain unpublished machine parameters or other sensitive context |
| Highlight noise | Canonical names or aliases may produce dense or false-positive highlighting |
| Review burden | Large excerpts and LLM transcripts may make human verification costly |

These are design and operational notes. They must remain visible during
evaluation, but they do not block RW-01 or require provenance graphs, extra
hashes, a PDF pipeline, or an integrated AI runtime in the first prototype.

## 8. RW-00 stop condition

RW-00 ends with this governance protocol and the separate UI specification.
It creates no reading artifacts, source files, sessions, PDFs, scientific
content, proposal artifacts, UI implementation, or KA-01 run. Human audit and
explicit acceptance are required before RW-01 implementation is authorized.

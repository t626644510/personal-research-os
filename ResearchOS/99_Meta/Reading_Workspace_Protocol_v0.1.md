# Reading Workspace Protocol v0.1

Version: v0.1\
Status: RW-00 governance human accepted on 2026-08-04; RW-01 and RW-01.1 accepted and complete at commit 8afa9aa; configurable 34/42/50rem session-panel correction received final visual confirmation; 25 Concepts passed validation; focused Reading UI suite: 16 tests passed; full suite: 33 tests passed; RW-02.2 human UI accepted on 2026-08-11; RW-02 accepted and complete; HTML prototype frozen; commit 792c802 is the published RW-02 baseline; RW-03 synthesis content human accepted on 2026-08-18; selected-text presentation correction applied; RW-03 accepted and complete and published at commit 7c5dc4f; `reading_note.draft.md` remains `state: draft` as RW-03 history; final `reading_note.md` is `state: human_reviewed`; RW-04 freeze explicitly authorized and implemented, pending final audit and publication; RW-05, Concept proposal, and KA-01 remain unauthorized and unstarted\
Applies to: reading and source preparation upstream of KA-01

This protocol defines the smallest implementation-neutral contract for a local
Reading Workspace. It governs ownership, session entries, reading-note review,
and the one-file bridge into KA-01. It does not implement the workspace.

Realistic human reading on 2026-08-11 identified five RW-02.2 usability
corrections. The repository owner accepted the RW-02.2 human UI on 2026-08-11
with the overall conclusion “通过，未报告其他问题”. RW-02 is accepted and
complete; the HTML prototype is frozen;
commit `792c802` is the published RW-02 baseline.
RW-02.1 remains a historical narrow presentation correction, not an
architecture redesign. RW-03 was separately authorized on 2026-08-11.
RW-03 synthesis content human accepted on 2026-08-18; selected-text
presentation correction applied; RW-03 accepted and complete and published at
commit `7c5dc4f`. `reading_note.draft.md` remains `state: draft` as RW-03
history; final `reading_note.md` is `state: human_reviewed`. RW-04 freeze was
explicitly authorized and implemented, pending final audit and publication;
RW-05, Concept proposal, and KA-01 remain unauthorized and unstarted.

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

## 2. Artifact layout v0.1

The Reading Workspace currently uses this per-paper artifact layout:

```text
ResearchOS/00_Inbox/reading/<paper_id>/
├── source_record.md
├── reading_note.draft.md
├── reading_note.md                 # optional; only after RW-04 human review/freeze
└── _local/
    ├── source.pdf
    ├── source.reading.md
    ├── source.zh-CN.reading.md
    ├── reading_session.md
    ├── external_llm_conversation_summary.md
    ├── reading-workspace.html
    └── assets/figures/
```

Responsibilities:

| Artifact | Responsibility |
| --- | --- |
| `source_record.md` | Git-visible source identity and provenance record |
| `reading_note.draft.md` | RW-03 synthesis artifact and retained history; content human accepted on 2026-08-18, while the file remains `state: draft` |
| `reading_note.md` | RW-04 frozen final note; `state: human_reviewed`, pending final audit and publication |
| `_local/source.reading.md` | Authoritative paper-text input for this workflow |
| `_local/source.zh-CN.reading.md` | Unverified, non-authoritative reference translation |
| `_local/reading_session.md` | Authoritative exported human session |
| `_local/external_llm_conversation_summary.md` | Optional human-selected, unverified external input; session-external and non-authoritative |
| `_local/source.pdf` | Visual authority |
| `_local/reading-workspace.html` and `_local/assets/figures/` | Ignored local presentation artifacts |

This is the actual v0.1 layout, not a future proposal. The current bundle's
session is `_local/reading_session.md`; there is no paper-root
`reading_session.md`. The entire `_local/` subtree is ignored by default and
must not be committed. `reading_note.md` was created by the separately
authorized RW-04 human review and freeze; it remains pending final audit and
publication.

### 2.1 RW-02.1 presentation boundary

For the RW-02 realistic source, `source.reading.md` is the only authoritative
reading transcription and `_local/source.pdf` remains the visual authority.
Figures 1–7 may be prepared as local PNG crops and safely embedded as data
URIs in the offline HTML. Only relative local PNG/JPEG/WebP targets are
eligible; remote, absolute, traversal, symlink-escaping, SVG, missing, and
unsupported targets must remain safe visible placeholders. No remote image,
script, stylesheet, font, API, or other resource is permitted.

An optional `source.zh-CN.reading.md` is a machine/LLM-assisted, unverified
derived display aid. It may translate the complete body and captions while
preserving the English page markers, equations, numerics, units, proper names,
modes, and original bibliography, but it is never a second authority and does
not duplicate figures. `英文原文`, `中英并列`, and `中文参考` are presentation-only
modes. Concept resolution may appear in both panes with namespaced block and
section metadata; panes do not synchronize selection or overlays. RW-02.1
originally allowed only English selection to populate `selected_text` or
create a session entry. That historical fact is retained; section 2.2 defines
the superseding RW-02.2 rule. Translation mode, translation path, derived
assets, and pane state must not enter `rw-session-v0.1`, `session_id`, recovery
data, or canonical entries.

These corrections historically supported human evaluation of figure
legibility, bilingual usefulness and trust, pane width, and the English-only
selection safeguard. They did not claim that any human checklist item was
complete. The derived translation, figure crops, HTML, PDF, and human export
remain ignored `_local/` artifacts.

Making the repository private later does not erase material already published
in Git history, and repository privacy does not itself grant a right to
redistribute a publisher PDF. This is a non-blocking operational warning, not
an RW-01 acceptance blocker.

### 2.2 RW-02.2 usability correction boundary

The 2026-08-11 realistic reading found five usability problems: bilingual
sections did not remain horizontally aligned, Chinese reference text could not
receive human notes or questions, annotated source blocks were not visible,
figures and tables competed with the body scroll, and fixed columns underused
a 4K display. RW-02.2 addresses only those findings.

- English and Chinese Markdown are split at every ordered H1/H2/H3 boundary.
  Paired sections share one row and one body scroll. A count mismatch preserves
  all unpaired content and displays a warning rather than silently mispairing.
- English authoritative selections may create `source_excerpt`, `human_note`,
  or `human_question`. Chinese reference selections may create only
  `human_note` or `human_question`; a Chinese `source_excerpt` is invalid.
- New source-associated entries may carry the optional fields
  `selected_text_origin` and `selected_block_id` defined in section 4. Chinese
  entries use the paired English section's canonical `source_locator` and show
  `中文参考译文 / 机器或 LLM 辅助 / 未核验`.
- Block markers are derived only from canonical `source_excerpt`,
  `human_note`, and `human_question` entries. They are never serialized into a
  session, recovery payload, or Markdown export. Ambiguous or absent matches
  remain visibly unresolved rather than being guessed.
- Figures 1–7 and Tables 1–2 are extracted once, in English source order, into
  an independently scrolling authoritative figure/table rail. Source positions
  retain lightweight links. Table cells are escaped before the minimal GFM
  pipe-table renderer handles them; all existing local-image safety rules stay
  in force.
- The full-width desktop layout exposes English, Chinese, figure/table, and
  session columns with three accessible separators. Pointer and keyboard
  resizing, clamps, custom state, and reset are presentation-only. Layout
  storage must remain outside `rw-session-v0.1`, `session_id`, canonical
  recovery, entries, preferences, and Markdown export; narrow screens hide the
  separators and restore a non-overflowing stack.

The ignored `_local/reading_session.md` is a byte-identical legacy
`rw-session-v0.1` export with two human questions and three human notes. The
separate `_local/external_llm_conversation_summary.md` remains external LLM
material, unverified, session-external, non-authoritative, and not
`human_reviewed`; it is not part of that session.

Current RW-02.2 automated verification passed 25 Concept checks, 32 focused
Reading UI tests, and 49 full-suite tests. The 974,523-byte offline HTML has 18
bilingual section pairs, 7 images, 2 rendered tables, 3 accessible resizers,
and 131 unique annotatable source blocks. These engineering metrics remain
separate from the repository owner's human acceptance record. RW-02 is
accepted and complete; the HTML prototype is frozen;
commit `792c802` is the published RW-02 baseline. The statement that RW-03,
Obsidian Home, and the 1500 MHz TM020 Harmonic Cavity project page required
separate authorization describes the historical RW-02 publication boundary.
RW-03 was subsequently authorized on 2026-08-11. Its synthesis content was
human accepted on 2026-08-18 and the selected-text presentation correction was
applied; RW-03 is accepted and complete and published at commit `7c5dc4f`. The
draft file remains `state: draft` as history, and final `reading_note.md` is
`state: human_reviewed`. RW-04 freeze was explicitly authorized and
implemented, pending final audit and publication; RW-05, Concept proposal, and
KA-01 remain unauthorized and unstarted.

## 3. Content ownership and review metadata

The Reading Workspace keeps a minimal origin distinction:

| Content kind | Meaning and ownership |
| --- | --- |
| Source material | Quoted or paraphrased paper content; it remains attributable to the source |
| Human note | Human-owned interpretation or annotation; it is never silently rewritten |
| Human question | A question authored by the human |
| LLM answer | Auxiliary model output; unverified by default and never treated as source text |
| External summary | Optional, explicitly human-selected RW-03 input; unverified, session-external, non-authoritative, and never `human_reviewed` |
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
| `selected_text_origin` | Optional source association: `authoritative_source` or `reference_translation` |
| `selected_block_id` | Optional id of the actual selected body, caption, figure, or table block |
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

The optional source-association fields obey these compatibility rules:

- new English entries use `selected_text_origin: authoritative_source`;
- new Chinese `human_note` and `human_question` entries use
  `selected_text_origin: reference_translation`;
- `source_excerpt` is legal only with `authoritative_source`;
- `reference_translation` is legal only for `human_note`, `human_question`,
  and an `llm_answer` linked to a reference-translation question;
- a new `llm_answer` inherits the linked question's origin, whether
  `authoritative_source` or `reference_translation`;
- a reference-translation note or question uses the paired English section's
  canonical locator while `selected_block_id` identifies the selected Chinese
  block; and
- a legacy entry without `selected_text_origin` is interpreted semantically as
  authoritative source material, but import and re-export must preserve the
  field's absence rather than adding it. A missing legacy `selected_block_id`
  likewise remains absent.

These optional fields do not change `rw-session-v0.1`, `session_id`,
`source_label`, preferences, or the `entry_type` to `author_type` invariant.
Invalid field/type/link combinations must be rejected, not normalized.

`selected_text` preserves reading context for an excerpt, note, or question
created from a selection. For a `source_excerpt`, `content` may repeat the
selected passage so the entry remains independently readable. For an entry
without a selection, the export uses one documented empty or not-applicable
representation rather than inventing source context.

RW synthesis must also preserve this selected-text presentation invariant:

- every `human_question` and `human_note` with non-empty `selected_text`
  displays that exact session field next to the human content;
- synthesis reads the displayed selection from `selected_text`; it must never
  reconstruct a quotation from `source_locator`, surrounding source text, or
  an LLM paraphrase;
- an `authoritative_source` selection may be displayed as `[paper/quote]`;
- a `reference_translation` selection must be visibly marked
  `中文参考译文 / 机器或 LLM 辅助 / 未核验 / 非权威` and must never receive
  `[paper/quote]`;
- a legacy entry without `selected_text_origin` retains the compatibility
  semantics above and the absent field remains absent;
- when `selected_text` is empty or absent, synthesis displays
  `未记录框选内容` and never invents context.

This is a reading-note display rule only. It does not embed the complete source
in `reading_session.md`, add or normalize an entry field, or change
`rw-session-v0.1`.

An `llm_answer` also allows:

- `model_label`: optional human-entered label for the external model;
- `question_entry_id`: required link to one `human_question` entry in the
  same session.

Multiple `llm_answer` entries may link to the same `human_question` through
that field. The serialized session remains flat; any question-answer grouping
is a derived presentation and must not nest, mutate, or reorder canonical
entries.

No API identifier, provider-specific metadata, token count, cost field, model
request id, or nested provenance graph is required. Entry ids and the
question-answer link are sufficient for the first prototype.

Import and export must preserve every entry, field value, absent optional
field, entry id, entry order, and question link without silent normalization
or loss. The complete
source is not embedded in `reading_session.md` by default. Re-importing the
session must not lose or rewrite entries, and future synthesis must use an
exact human-selected source path rather than treating excerpts as the entire
source.

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

Without an explicit human freeze decision, an LLM or implementation agent may
create only `active` reading-session content and `draft` reading notes; it may
not infer or assign `human_reviewed`.

Only a human makes the semantic review and freeze decision. An implementation
agent may mechanically materialize `state: human_reviewed` only when all three
conditions hold:

1. The human explicitly accepted the content.
2. The human uniquely identified the note/version to freeze.
3. The human explicitly authorized the freeze.

Mechanical materialization is not independent review, delegated judgment,
reviewer impersonation, automatic promotion, or KA-01 source selection. A
`human_reviewed` reading note is merely eligible for a future handoff; selecting
it for a KA-01 run still requires a separate explicit instruction.

RW-04 satisfies this rule: the accepted content is the RW-03 draft; the
uniquely identified version is that draft as committed at full commit
`7c5dc4f9b815719677e5fcced3831309b8bc0e06`; and the explicit freeze
authorization is the repository owner's 2026-08-18 RW-04 instruction. The
implementation agent mechanically materialized the state only after those
human decisions; it did not make the semantic review or select a KA-01 source.

If a human-reviewed reading note changes later, the changed content loses its
frozen meaning and must return to `draft` until it is explicitly reviewed
again. The previous reviewed version may be retained as `superseded`, but a
superseded note is not eligible for a new handoff unless a human reviews and
selects the intended version again.

## 6. RW-03 synthesis handoff

RW-03 was separately authorized on 2026-08-11. RW-03 synthesis content human
accepted on 2026-08-18; selected-text presentation correction applied; RW-03
accepted and complete and published at commit `7c5dc4f`. `reading_note.draft.md`
remains `state: draft` as history; final `reading_note.md` is
`state: human_reviewed`. RW-04 freeze was explicitly authorized and
implemented, pending final audit and publication; RW-05, Concept proposal, and
KA-01 remain unauthorized and unstarted. A valid synthesis trial requires the human
to select both mandatory inputs:

- one exact `SOURCE_PATH` for the original technical source; and
- one exact `SESSION_PATH` for the exported `reading_session.md`.

The human may also select one exact `EXTERNAL_SUMMARY_PATH` for a specific run.
This third input is optional and may be read only when the human explicitly
selects it. It remains external LLM material: unverified, session-external,
non-authoritative, and not `human_reviewed`.

RW-03 reads answers through two distinct channels: canonical `llm_answer`
entries already contained in `SESSION_PATH`, and the optional external summary
outside the session. The current session contains no `llm_answer`; it contains
two `human_question` and three `human_note` entries. Independently, the
authoritative `SOURCE_PATH` grounds paper-supported synthesis. A channel must
not borrow another source's provenance label, and a paragraph must not collapse
unlike origins behind a single label. The external summary is never split into
or imported as canonical session entries and is never promoted to paper/source
evidence, human-authored content, reviewed content, or a stable knowledge
artifact. Future synthesis may deduplicate repeated wording across the two
answer channels only if it retains every origin label and does not obscure
which channel supports each claim.

The manually triggered LLM synthesis step may output only
`reading_note.draft.md`. It may not overwrite any input, create a reviewed
note, claim human review, create a Concept proposal, or begin KA-01. This
handoff does not require the full source to be embedded in the session and
does not add a source hash, session hash, external-summary hash, provenance
SHA, or any other fingerprint.

The mandatory two-file input, with the optional explicitly selected external
summary, is upstream preparation only. It does not change the KA-01 one-file
handoff described below. RW-04 freeze is implemented from explicit human
authority and remains pending final audit and publication; the final note has
not been selected for any KA-01 run.

## 7. KA-01 bridge

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
- No PDF hash, session hash, external-summary hash, source-record hash, double
  hash, or second provenance fingerprint is required by RW.
- KA-01 classification, proposal artifacts, human review, and promotion rules
  remain unchanged.
- RW-00 does not modify
  `ResearchOS/99_Meta/Knowledge_Proposal_Protocol_v0.1.md`.

Intent to run KA-01 later is not execution authority. A valid run still
requires a separate human instruction providing the exact eligible
`SOURCE_PATH` and approving the execution prompt version used at that time.

## 8. Non-blocking risk register

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

## 9. RW-00 stop condition

RW-00 ended with this governance protocol and the separate UI specification.
It created no reading artifacts, source files, sessions, PDFs, scientific
content, proposal artifacts, UI implementation, or KA-01 run. RW-01 was
subsequently human accepted and completed at commit 8afa9aa. RW-01.1 was also
human accepted and completed at that commit; the configurable 34/42/50rem
session-panel correction received final visual confirmation. The validation
record shows 25 Concepts passed, the focused Reading UI suite with 16 tests
passed, and the full suite with 33 tests passed. RW-02 source preparation
and RW-02.1 presentation history remain recorded above. RW-02.2 human UI was
accepted on 2026-08-11. Current RW-02.2 automated verification passed 25
Concept checks, 32 focused Reading UI tests, and 49 full-suite tests; the
generated HTML metrics are recorded above. RW-02 is accepted and complete; the
HTML prototype is frozen;
commit `792c802` is the published RW-02 baseline. RW-03 was subsequently
authorized on 2026-08-11. RW-03 synthesis content human accepted on 2026-08-18;
selected-text presentation correction applied; RW-03 accepted and complete and
published at commit `7c5dc4f`. The draft remains `state: draft` as history; final
`reading_note.md` is `state: human_reviewed`. RW-04 freeze was explicitly
authorized and implemented, pending final audit and publication; RW-05,
Concept proposal, and KA-01 remain unauthorized and unstarted.

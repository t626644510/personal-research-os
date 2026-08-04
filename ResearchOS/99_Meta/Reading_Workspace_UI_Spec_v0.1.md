# Reading Workspace UI Spec v0.1

Version: v0.1\
Status: RW-00 P0 specification human accepted on 2026-08-04; RW-01 and RW-01.1 human accepted and complete (2026-08-04); configurable 34/42/50rem session-panel correction received final visual confirmation; 25 Concepts passed validation; focused Reading UI suite: 16 tests passed; full suite: 33 tests passed; RW-02, RW-03, and KA-01 remain not authorized and not started\
Target phase: RW-01 Offline Reading UI Prototype and RW-01.1 session-layout increment

This specification defines the smallest usable offline Reading Workspace UI.
It describes behavior and data boundaries, not a framework, package choice, or
implementation.

## 1. Prototype goal and boundaries

RW-01 should let one human read one realistic accelerator/RF Markdown source,
see known Concepts in context, capture a structured reading session, and
export and reopen that session locally.

The prototype is a read-only consumer of:

- one human-selected UTF-8 Markdown reading source;
- the current local
  `ResearchOS/99_Meta/concept_index.json`; and
- stable Concept hover data already represented by that index.

It must not edit a stable Concept, regenerate or hand-edit
`concept_index.json`, create a Concept proposal, call a model, or make a
network request. Implementation technology is deferred to RW-01.

## 2. P0 requirements

The P0 UI must:

1. work fully offline and make no API or network call;
2. read the current local `concept_index.json` without changing its contract;
3. accept exactly one UTF-8 Markdown reading source at a time;
4. render readable headings, paragraphs, lists, links, inline code, and fenced
   code;
5. highlight recognized canonical Concept names and aliases in eligible prose;
6. show the existing compact hover/focus card for a highlighted Concept;
7. allow the human to select source text and create a session entry;
8. support `source_excerpt`, `human_note`, and `human_question` creation
   from the reading surface;
9. allow a pasted `llm_answer` to be linked to its
   `human_question`;
10. display `author_type` as a visible, read-only origin badge and expose only
    `confidence` and `verification` as editable controls;
11. display session entries in a side panel;
12. make every session mutation recoverable in an offline local draft before
    final Markdown export;
13. show a clear saved, unsaved, or recovery state;
14. offer recovery of the latest local session draft after refresh or reopen,
    and clear recovered data only through an explicit human action;
15. export the complete structured session as one human-readable Markdown
    file;
16. reopen/import that exported Markdown without losing entries, ids,
    metadata, selected text, locators, or question-answer links;
17. never edit stable Concepts or `concept_index.json`; and
18. load no remote script, stylesheet, font, image, analytics, telemetry, or
    other network resource.

Rendered Markdown is treated as untrusted data. Raw content must not execute as
HTML or script. Link labels and targets may be rendered for reading or copying,
but the prototype must not automatically fetch them or preview remote content.

## 3. Reading surface

The main surface displays the selected Markdown as readable rendered content,
not as an escaped plain-text snapshot. It must preserve the reading order and
make headings and paragraph/section boundaries available to highlight-density
controls and source locators.

Selecting text opens a small entry action with:

- `source_excerpt`;
- `human_note`; and
- `human_question`.

The selected passage populates `selected_text`. The UI proposes the most
specific available heading or section locator and lets the human enter or
correct a page/section locator manually. It must not invent a page number.

Entry defaults follow
`Reading_Workspace_Protocol_v0.1.md`:

| Entry type | Derived `author_type` | Default `confidence` | Default `verification` |
| --- | --- | --- | --- |
| `source_excerpt` | `source` | `not_assessed` | `not_applicable` |
| `human_note` | `human` | `not_assessed` | `not_applicable` |
| `human_question` | `human` | `not_assessed` | `not_applicable` |
| `llm_answer` | `llm` | `not_assessed` | `unverified` |

`author_type` is an invariant derived from `entry_type`, not an editable
field. The UI displays it as a read-only origin badge. Only confidence and
verification are editable controls, initialized to the defaults above, and
their human-made changes are preserved in the export. The UI must not offer
origin correction or reassignment, and confidence must never hide or replace
origin.

## 4. Concept highlighting and hover behavior

Highlighting reuses the current index identities and P01/P01.5 behavior:

- canonical Concept names and aliases resolve to the existing canonical index
  entry;
- matching remains deterministic, local, and case-insensitive where the
  current resolver is case-insensitive;
- longest-term matching wins at an overlapping text position;
- alias-to-canonical behavior remains unchanged; and
- the compact hover/focus card continues to show the existing local Concept
  name, summary, optional category, and related-Concept data.

RW-01 adds presentation controls, not a new Concept index contract.

The UI must provide:

- a global toggle for all Concept highlights;
- density modes for all occurrences, first occurrence per paragraph, and first
  occurrence per section;
- a session-local action to temporarily mute one Concept or matched alias;
- a visible way to restore muted highlights; and
- keyboard focus behavior for highlighted terms and their compact cards.

Highlight matching must skip:

- YAML/frontmatter;
- fenced code;
- inline code; and
- Markdown link targets.

Visible prose used as link text may still be eligible for highlighting, but
its destination must not be altered. Highlighting must not mutate the reading
source, stable Concept files, or the index.

A mute is temporary session UI state, not a change to an alias or Concept. The
export may preserve the UI preference for convenience, but importing it must
not reinterpret the preference as a knowledge change.

## 5. Session side panel and persistence

The side panel lists entries in a stable, readable order and shows at least:

- entry type and id;
- source locator and selected-text context;
- content;
- author type as a read-only origin badge;
- confidence;
- verification;
- creation time; and
- for an LLM answer, its linked question and optional model label.

RW-01.1 presents the same canonical flat entries through these derived tabs:

- Excerpts for `source_excerpt`;
- Notes for `human_note`;
- Q&A grouped by each `human_question.entry_id` and linked
  `llm_answer.question_entry_id`; and
- All as the chronological audit view.

Filtering and grouping must not mutate or reorder the canonical entries array
and must not change `rw-session-v0.1`. In Q&A, the question and its linked
answers appear side by side at ordinary desktop widths and stack on narrow
screens. Questions without answers are explicit. Multiple answers may remain
linked to one question, and every displayed question or answer retains its
origin badge, confidence, verification, and applicable edit/delete controls.

Session-panel width is a presentation-only control with Compact (`34rem`),
Balanced (`42rem`, default), and Wide (`50rem`) presets. The desktop grid keeps
the reading pane flexible, applies the preset through a CSS custom property,
and caps the panel near half the viewport; the existing narrow-screen Q&A
stacking behavior remains authoritative. The selected preset may use a
dedicated browser-local key, but it must not enter session preferences,
recovery data, session IDs, canonical entries, `sessionPayload()`, or
`rw-session-v0.1`. Missing or invalid stored values fall back to Balanced, and
storage failure must not prevent the current-page width change.

The panel supports reviewing and editing human-owned session content without
silently rewriting it. Deleting or replacing an entry, if RW-01 includes that
action, must be explicit; no cleanup or synthesis step may silently collapse
entries.

Before final Markdown export, every session mutation must be recoverable from
an offline local draft. The UI must expose a clear saved, unsaved, or recovery
state. Refreshing or reopening the prototype must offer recovery of the latest
local session draft, and clearing recovered data must require an explicit
human action.

Local persistence must not transmit source text, annotations, or LLM answers.
The implementation technology remains open: this specification does not
mandate `localStorage`, IndexedDB, a server, or a framework. Local recovery is
working-state protection; it does not replace the Markdown export/import,
which remains the portable, human-readable, and Git-reviewable session
artifact. A local recovery draft is not a `draft` reading-session state.

One Markdown export must contain every field required by
`Reading_Workspace_Protocol_v0.1.md`. The exact serialization may be chosen
in RW-01, but it must be:

- UTF-8;
- human-readable;
- deterministic enough to inspect in a Git diff;
- parseable by the same prototype; and
- lossless for every entry and question-answer relationship.

No sidecar file may be required to preserve session entries. The session
export does not embed the complete reading source by default; it preserves the
source label, excerpts, locators, and flat session entries. Re-importing the
session must preserve all entries exactly. A later synthesis step obtains the
complete source from an exact path selected separately by the human.

## 6. Manual LLM workflow

For a selected passage and a `human_question`, the UI may format a copyable
question packet containing:

- the selected passage;
- its available page/section locator; and
- the human's question.

The human manually copies that packet into an external LLM. The UI must not
send it, open an API request, select a provider, or run a repository-hosted
model.

The human may paste the answer back into the session, select the related
`human_question`, and optionally enter a `model_label`. The resulting entry
is:

- `entry_type: llm_answer`;
- `author_type: llm`;
- linked by `question_entry_id`; and
- `verification: unverified` by default.

Only a human action may later change the answer's confidence or verification.
Changing verification does not turn the answer into source material.

## 7. PDF boundary

Full coordinate-aware PDF overlay is deferred beyond RW-01. The first usable
prototype may provide:

- a Markdown or full-text reading surface;
- page or section locators entered manually; and
- optionally, a local PDF displayed separately for visual cross-checking.

RW-01 does not require PDF text-layer reconstruction, OCR, automatic
PDF-to-Markdown conversion, coordinate synchronization, an Obsidian plugin, or
a PDF hash. A separately displayed local PDF must not be uploaded or fetched
over the network.

## 8. Reading-note boundary

The RW-01 prototype implements the annotation and external-LLM-answer capture
primitives, but it does not need to synthesize
`reading_note.draft.md` or produce the final `reading_note.md`.

Its responsibility is to export enough structured session data—including
source excerpts and locators, human notes and questions, LLM-answer origins,
confidence, verification, and question-answer links—for a later manually
triggered reading-note synthesis prompt.

Any later LLM synthesis may produce only a `draft`. Only a human may review,
freeze, and select one `reading_note.md` for a separately authorized KA-01
handoff.

If RW-03 is separately authorized, the human must select one exact original
source `SOURCE_PATH` and one exact exported-session `SESSION_PATH`. The
manually triggered LLM synthesis reads both and writes only
`reading_note.draft.md`. It does not require the complete source to be embedded
in `reading_session.md`, does not add another SHA, and does not change KA-01:
KA-01 still reads only one human-reviewed, human-selected `reading_note.md`.

## 9. RW-01 P0 acceptance criteria

RW-01 is usable when a human can:

1. open one realistic accelerator/RF UTF-8 Markdown paper source;
2. see known Concept canonical names and aliases highlighted, with the compact
   local hover/focus card;
3. create a source excerpt, a personal note, and a human question;
4. paste one external LLM answer, link it to the question, and see it marked
   `llm` and `unverified`;
5. manually change a confidence or verification value and see the new value
   persist;
6. pass the required local-recovery and Markdown round-trip test below; and
7. confirm that the workflow made no network request and changed no stable
   Concept or `concept_index.json` content.

The required acceptance test is:

1. create entries, including a linked human question and LLM answer;
2. reload or reopen the UI;
3. recover the latest local session draft;
4. export the recovered session as Markdown;
5. import that Markdown again; and
6. confirm that no entry or question-answer link was lost.

Acceptance evidence should use local files and a network-observation method
appropriate to the chosen implementation. It does not require CST, a model
call, PDF OCR, a Concept scan, or a KA-01 run.

## 10. RW-02 human UX validation questions

After RW-01 implements the capture primitives, RW-02 should use one
human-selected realistic technical paper to record:

1. Is highlight density acceptable in realistic accelerator/RF reading?
2. Are headings, paragraphs, lists, links, and code readable enough for
   sustained use?
3. How much friction does selecting text and creating an entry add?
4. Are confidence controls useful, or do they create false precision and UI
   burden?
5. Is the question-to-answer link clear enough to trace external LLM material?
6. Do per-paragraph/per-section highlighting and session-local mute controls
   adequately reduce noise?
7. Is the Markdown-first workflow useful enough before building PDF overlays
   or a full Obsidian plugin?

These questions are RW-02 human evaluation gates. RW-02 validates the RW-01
primitives; it does not build a second capture implementation. They are not
reasons to expand RW-01 with an integrated AI runtime, automatic acquisition,
or a PDF reconstruction pipeline.

## 11. RW-01/RW-01.1 authorization boundary

RW-00 defined this specification only and did not itself authorize
implementation. RW-01 and RW-01.1 were human accepted and completed on
2026-08-04. The configurable 34/42/50rem session-panel correction received
final visual confirmation; 25 Concepts passed validation, the focused Reading
UI suite had 16 tests passed, and the full suite had 33 tests passed. RW-02,
RW-03, and KA-01 remain not authorized and not started. No KA-01 execution is
implied by implementing or accepting the Reading Workspace UI.

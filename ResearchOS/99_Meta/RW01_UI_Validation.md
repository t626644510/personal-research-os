# RW-01 Offline Reading UI Prototype Validation

Status: RW-01 and RW-01.1 human accepted and complete (2026-08-04). The
configurable 34/42/50rem session-panel correction received final visual
confirmation. 25 Concepts passed validation; focused Reading UI suite: 16
tests passed; full suite: 33 tests passed. RW-02, RW-03, and KA-01 remain not
authorized and not started.

Implementation baseline: `53c81375211d496dd66fc781f590898191b22c6d`

## Implemented scope

- `tools/reading_ui.py` accepts one UTF-8 Markdown source plus optional
  `--index`, `--output`, and `--open` arguments, then generates one
  self-contained local HTML file.
- The generator reads the accepted `concept_index.json` contract and reuses
  `hover_resolver.resolve_mentions()` for canonical names, aliases, case
  handling, ASCII boundaries, longest-term selection, and non-overlapping
  matches.
- The isolated bounded renderer supports headings, paragraphs, flat ordered
  and unordered lists, links, inline code, and fenced code blocks. It assigns
  deterministic block and section metadata and proposes the nearest heading
  as a source locator.
- Raw HTML is escaped. Frontmatter, fenced code, inline code, and Markdown link
  targets are excluded from Concept matching; visible link labels remain
  eligible. Unsafe link schemes are neutralized.
- `tools/reading_ui.js` implements density controls, Concept/term mute and
  restore, selection capture, the four accepted entry types, read-only
  `author_type`, editable confidence/verification, explicit edit/delete
  actions, manual question packets, pasted external LLM answers, and visible
  session metadata.
- RW-01.1 adds derived Excerpts, Notes, Q&A, and All views to the session
  panel. Q&A groups flat entries by `question_entry_id`, supports multiple
  answers, and marks unanswered questions without changing the canonical
  entries array or session format.
- Every session mutation attempts synchronous browser-local recovery under a
  source-specific key. Reload/reopen offers recovery, clearing requires human
  confirmation, import over non-empty work requires confirmation, and storage
  failures remain visible.
- Markdown export identifies `rw-session-v0.1` and carries one readable fenced
  JSON payload. Import validates root/field types, enums, unique IDs,
  `entry_type`/`author_type`, and question links before replacing state.
- `tools/reading_ui.css` provides a Chinese-primary desktop reading/panel
  layout, narrow-screen stacking, keyboard focus, compact cards, dialogs, and
  visible save/error/recovery states.

The generated page inlines the audited CSS and JavaScript source assets. It
contains no remote script, stylesheet, font, image, analytics, telemetry,
model client, or network request code and requires no local server.

## Architecture and reuse decision

The accepted chain remains unchanged:

```text
Concept Markdown -> concept_index.json -> hover_resolver.py
                                      -> hover_ui.py (existing P01.5 demo)
                                      -> reading_ui.py (new RW-01 consumer)
```

`hover_resolver.py`, `hover_ui.py`, the index contract, Concept Schema, stable
Concepts, and existing tests were not modified. RW-01 adds presentation and
session behavior without duplicating Concept matching rules.

RW-01.1 keeps `rw-session-v0.1` as the only session serialization. Tabs and
question-answer groups are transient projections over the existing flat,
ordered entries; tab state and nested presentation objects are not persisted
or exported.

## Dependency decision

No package was installed, vendored, or added. Python 3.9 standard-library
code implements only the accepted Markdown subset; the page uses vanilla
browser JavaScript and CSS. This keeps RW-01 offline and avoids turning the
bounded renderer into a general Markdown engine.

Three regression tests execute the isolated pure JavaScript view/codec model
with the already available Node executable. This is test-only, uses no npm
package, is skipped when Node is unavailable, and does not make Node part of
the generated UI runtime.

## Audit correction: session Markdown fence boundary

Audit found that the original non-greedy session-envelope expression treated
the first literal triple backticks anywhere inside the JSON payload as the
closing Markdown fence. A human note containing a fenced Python example, or an
LLM answer containing triple backticks, therefore caused import to receive
truncated JSON.

The parser now recognizes the closing JSON fence only when it occupies a
complete line, with optional horizontal whitespace and either LF or CRLF line
endings. Literal backticks, Chinese text, and marker-like text inside JSON
string values remain part of the payload. Parsing and full validation still
complete before session state is replaced, so malformed imports remain atomic.

`test_session_envelope_preserves_embedded_triple_backticks` exercises the
production envelope pattern with an ordered four-entry payload. It includes a
fenced Python block in a `human_note`, literal triple backticks in an
`llm_answer`, Chinese and marker-like text, distinct metadata values, the
`question_entry_id` link, and non-default preferences. The test decodes the
complete captured JSON and compares it exactly with the original payload; it
also rejects a closing fence line containing trailing non-whitespace text.

## RW-01.1 session layout and source handoff

The session panel now provides Excerpts, Notes, Q&A, and All tabs. Filtering
returns an ordered copy or ordered subset and never mutates `state.entries`.
The Q&A projection first records questions in canonical order, then links every
answer through `question_entry_id`; multiple answers keep their canonical
relative order and unanswered questions retain an explicit empty-answer
state. Reused entry cards keep origin, confidence, verification, timestamps,
content, context, and applicable edit/delete controls visible. CSS places each
question beside its answer column on desktop and stacks the columns on narrow
screens.

The future RW-03 synthesis contract now requires one exact human-selected
`SOURCE_PATH` and one exact human-selected `SESSION_PATH`. A separately
authorized, manually triggered LLM step would read both and output only
`reading_note.draft.md`. The session does not embed the complete source by
default. No synthesis runtime, new hash, or KA-01 change is implemented;
KA-01 retains its one reviewed-Markdown input and single existing SHA.

Regression evidence:

- `test_session_tabs_preserve_canonical_entries_and_order` executes every tab
  projection and compares the canonical array before and after.
- `test_question_answer_groups_use_question_entry_id` uses interleaved
  questions and answers, including two answers for one question and one
  unanswered question, and verifies grouping by ID rather than proximity.
- `test_rw_session_v01_export_import_remains_backward_compatible` parses a
  legacy flat session envelope, exports it with the current codec, reparses it,
  and compares the complete payload exactly.

## Preliminary human evaluation correction

Preliminary human evaluation first found that the original ordinary desktop
session-column maximum of `28rem` was too narrow for side-by-side Q&A cards.
Increasing the fixed maximum to `34rem` was still insufficient, so the fixed
choice has been replaced by Compact (`34rem`), Balanced (`42rem`, default), and
Wide (`50rem`) toolbar presets.

The selected preset sets the `--session-panel-width` CSS custom property
immediately. The desktop grid keeps a flexible reading column and caps the
session column near `52vw`. The existing `68rem` Q&A stacking breakpoint and
all narrower responsive behavior are unchanged.

The width is a presentation-only browser preference stored under a dedicated
localStorage key. Missing or invalid values normalize to Balanced. The current
page is updated before persistence is attempted, so a storage failure cannot
undo the visible change. Width never enters session preferences, recovery
data, session IDs, canonical entries, `sessionPayload()`, or
`rw-session-v0.1` export/import.

Regression evidence adds:

- `test_session_panel_width_presets_normalize_deterministically`, covering all
  three presets and invalid-value fallback;
- `test_generated_html_has_accessible_panel_width_selector`, covering the
  labeled selector, default, options, CSS variable, viewport cap, and separate
  storage key; and
- the legacy session round-trip test now compares UTF-8 export bytes and
  confirms that no session-panel/layout field appears in exported data.

No other functional or UX issue was reported. Final governance acceptance was
received on 2026-08-04, including final visual confirmation of the configurable
34/42/50rem session-panel correction.

## Automated verification

Required commands:

```powershell
py -3.9 ResearchOS/99_Meta/tools/concept_tools.py validate
py -3.9 -m unittest discover -s tests -v
git diff --check
```

Focused development check:

```powershell
py -3.9 -m unittest discover -s tests -p test_reading_ui.py -v
```

Verification result:

- Concept validation: 25 Concepts passed.
- Focused RW-01/RW-01.1 suite: 16 tests passed.
- Full suite: 33 tests passed.
- `git diff --check`: passed.

## Local-browser smoke test

Disposable input:

`ResearchOS/00_Inbox/notes/HOM impedance reading note.md`

Disposable output (outside the repository):

`C:\Users\lau\.codex\visualizations\2026\08\04\019fcab3-0c89-7f81-ac79-ae195e17c523\personal-research-os-reading-workspace.html`

Required interaction sequence:

1. inspect rendered headings, paragraphs, and compact Concept cards;
2. change highlight density;
3. mute and restore a Concept or matched term;
4. select text and create an excerpt, note, and question;
5. open and copy the manual external-LLM question packet;
6. paste and link a disposable answer without contacting a model;
7. switch among Excerpts, Notes, Q&A, and All without changing canonical
   chronology;
8. switch Compact, Balanced, and Wide session-panel presets and confirm the
   default, viewport cap, immediate change, and browser-local restoration;
9. confirm desktop side-by-side and narrow-screen stacked Q&A, multiple
   answers, unanswered state, metadata, and controls;
10. change confidence or verification;
11. reload/reopen and recover the local draft;
12. export Markdown and import it again; and
13. confirm every entry and question-answer relationship survives and no
    remote request occurs.

Result: the controlled in-app browser refused the local `file:` URL under its
URL security policy before the page loaded. That policy explicitly prohibited
routing around the refusal through another browser surface or an indirect
transport, so no browser interaction result is claimed. The disposable page
was regenerated successfully after RW-01.1. Static inspection confirms four
tab controls, the Q&A grouping/unanswered-state implementation, all three
width presets with Balanced selected, the CSS variable, the viewport cap, the
separate presentation storage key, and no remote script or stylesheet. The
automated suite verifies generation,
self-containment, safe rendering, Concept resolution, session invariants,
derived-view behavior, recovery/error surfaces, and Markdown import/export.
The human acceptance recorded on 2026-08-04 includes final visual confirmation
of the configurable 34/42/50rem session-panel correction. The controlled
in-app browser refusal remains an environmental limitation of this validation
record, not an implementation or acceptance blocker.

## Known limitations

- Markdown support is intentionally limited to the accepted P0 subset. Nested
  lists, tables, images, emphasis, blockquotes, footnotes, task lists, and
  extension syntax are not fully rendered.
- Raw HTML is displayed as escaped text and never executed.
- PDF text extraction, OCR, coordinate overlays, and PDF-to-Markdown conversion
  are not implemented.
- Browser `file:` local-storage and clipboard behavior can vary by browser and
  security policy. Failures are surfaced; the portable recovery boundary is
  still the exported Markdown session.
- The page is a generated snapshot. Source or index changes require generating
  it again.
- Tooltip placement is CSS-only and may be imperfect near narrow viewport
  edges.

## Deferred boundary

RW-02 may perform realistic human UX validation with a selected technical
paper. RW-01/RW-01.1 does not record RW-02 evaluation conclusions, run RW-03
synthesis, create `reading_note.draft.md`, mark any note `human_reviewed`, call
a model, or start KA-01.

No stable Concept, Concept Schema, `concept_index.json`, Inbox source, reading
note, proposal, run assessment, dependency, or KA artifact is changed or
created by this implementation.

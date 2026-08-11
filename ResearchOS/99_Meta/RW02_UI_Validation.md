# RW-02 Realistic Human UX Validation

**Status:** RW-02.2 human UI accepted on 2026-08-11. RW-02 is accepted and
complete; the HTML prototype is frozen;
the commit containing this status record is the published RW-02 baseline.

**Preparation baseline:** `8afa9aa61f5080d73715f1bb694bc29c5ba71335`
**Authorization:** The repository owner completed the authorized RW-02.2 human
UI acceptance on 2026-08-11. RW-03 and KA-01 remain unauthorized and not
started.

## Selected source

- **Title:** Utilizing the High Shunt Impedance TM020-Mode Cavity in the
  Double RF Systems for the Storage Ring of the Thailand New Light Source
- **Authors:** N. Juntong, T. Phimsen, N. Chulakham, S. Malichan
- **DOI:** `10.18429/JACoW-IPAC2019-WEPRB066`
- **Official PDF:**
  <https://proceedings.jacow.org/ipac2019/papers/weprb066.pdf>
- **License:** Creative Commons Attribution 3.0 International (CC BY 3.0).
  Attribution to the author(s), title, publisher, and DOI is required.
- **Git-visible record:**
  `ResearchOS/00_Inbox/reading/ipac2019-weprb066/source_record.md`
- **Authoritative local PDF:**
  `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.pdf`
- **Derived reading Markdown:**
  `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.reading.md`
- **Generated workspace:**
  `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/reading-workspace.html`

This is the only RW-02 reading source. References listed by the paper remain
follow-up references and are not ingested into this session.

## Preparation method and limitations

- The PDF was downloaded only from the official JACoW PDF URL above.
- PDF metadata was inspected locally with Poppler; the file is four pages,
  unencrypted, and 837,078 bytes.
- Pages were rendered locally with Poppler for visual inspection.
- Text was extracted with the already available bundled `pdfplumber` runtime;
  no production dependency was installed.
- `source.reading.md` is a one-time, page-marked transcription that retains the
  paper's title, authors, abstract, headings, equations, tables, figure
  captions, conclusion, references, DOI, publisher, and license attribution.
- The PDF remains the visual authority. Text-layer spacing and ligature
  artifacts were checked against the rendered pages; table equation layout,
  figure graphics, and any ambiguous symbol or value require direct PDF review.
- This is source preparation for one human evaluation, not a PDF conversion
  pipeline.

## Final preparation audit corrections

- **Source fidelity, PDF page 2:** the transcription preserves the source
  wording, “This helps prolonging the electron beam lifetime.”
- **Source fidelity, PDF page 3:** the continuation preserves the source
  conjunction and capitalization: “so the TM020-mode type cavity was studied
  for using as the harmonic cavity.” The page marker remains in place.
- **Path convention:** `source_record.md` now distinguishes Vault-relative
  paths such as `00_Inbox/reading/ipac2019-weprb066/...` from repository-relative
  paths such as `ResearchOS/00_Inbox/reading/ipac2019-weprb066/...`; file
  locations were not changed.
- **Future human export location (ignored and not created):**
  `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/reading_session.md`
  (Vault-relative: `00_Inbox/reading/ipac2019-weprb066/_local/reading_session.md`).

## Historical RW-02.1 implementation/preparation record

This is the implementation/preparation evidence that existed before the
2026-08-11 realistic reading. It remains historical/pre-acceptance evidence,
not the later acceptance record. At that historical point, RW-02 remained
incomplete and unaccepted.

RW-02.1 is a narrow presentation correction, not an architecture redesign.
The English `source.reading.md` transcription remains the sole authoritative
reading source and the local PDF remains the visual authority. The regenerated
workspace is 929,900 bytes and displays Figures 1–7 from local PNG crops as
seven embedded raster images. The page has no remote script, stylesheet, fetch,
XHR, WebSocket, or beacon dependency. Remote, absolute, traversal,
symlink-escaping, unsupported, and missing image targets remain visible only as
safe placeholders. The Chinese `source.zh-CN.reading.md` file is a
machine/LLM-assisted, unverified derived reference translation for display
only. It does not duplicate figures, enter the `rw-session-v0.1` payload,
change `session_id`, or become a second source authority.

When the optional translation is supplied, the page offers `英文原文`,
`中英并列` (default), and `中文参考` presentation modes. Single-language mode
uses the full reference-surfaces width; bilingual mode retains the two-column
desktop and stacked narrow layout. Concept hover and highlight controls apply
to both panes with namespaced block/section metadata. RW-02.1 originally
allowed only English-pane selection to populate `selected_text` or create a
session entry; the Chinese pane had a non-mutating selection-clear path. That
historical behavior is preserved in this record and superseded only by the
RW-02.2 Chinese note/question rule below. The derived translation, figure
crops, generated HTML, and human export remain under ignored `_local/`.

Historical automated preparation evidence: `py -3.9
ResearchOS/99_Meta/tools/concept_tools.py validate` passed all 25 Concept
files, and `py -3.9 -m unittest discover -s tests -v` passed 37 tests. The
required `git diff --check` completed successfully.

## 2026-08-11 realistic human reading record

The human read the prepared source in the RW-02.1 workspace on 2026-08-11 and
created a real active `rw-session-v0.1` export. This was the historical,
pre-acceptance usability evaluation. It produced five findings:

1. English and Chinese content needed section-level horizontal alignment.
2. Chinese reference text needed to support personal notes and questions while
   remaining ineligible for authoritative source excerpts.
3. Source blocks with annotations needed an obvious visual marker and count.
4. Figures and tables needed their own independently scrolling rail.
5. Desktop columns needed accessible drag resizing to use a 4K display.

The real session contains two `human_question` entries and three `human_note`
entries, with no `source_excerpt` or `llm_answer`. Its five English
`selected_text` values each have one unique normalized match in the English
source. The session does not contain the separate external LLM summary.

## RW-02.2 implementation and acceptance record

RW-02.2 human UI was accepted by the repository owner on 2026-08-11. RW-02 is
accepted and complete; the HTML prototype is frozen;
the commit containing this status record is the published RW-02 baseline. It retains the English
transcription as the authoritative reading
source and the local PDF as visual authority. Both real Markdown inputs contain
18 ordered H1/H2/H3 boundaries. Bilingual mode pairs them into section rows
with one body scroll; unpaired content remains visible with an alignment
warning.

English selections support `source_excerpt`, `human_note`, and
`human_question`. Chinese reference selections support only `human_note` and
`human_question`, show `中文参考译文 / 机器或 LLM 辅助 / 未核验`, use the
paired English canonical locator, and carry `reference_translation` origin.
The optional `selected_text_origin` and `selected_block_id` fields do not
change `rw-session-v0.1`, `session_id`, `source_label`, preferences, or the
`entry_type`/`author_type` invariant. Legacy absence remains absent on
round-trip.

Block-level annotation markers are derived from canonical source excerpts,
notes, and questions and are excluded from session, recovery, and export data.
Legacy matching prefers origin, canonical locator, and normalized selected text
after block id; ambiguous or missing matches remain unresolved. Hidden hover
tooltip text is excluded.

Figures 1–7 and Tables 1–2 are extracted once from the English source, in
order, into an independently scrolling rail with authoritative English
captions/titles. The body contains jump placeholders instead of duplicates.
The project-only GFM pipe-table renderer escapes all cells and retains every
existing local-image and remote-resource safety boundary.

The full-width desktop workspace exposes English, Chinese, figure/table, and
session columns with three accessible resizers. Pointer, keyboard, clamp,
Custom, and reset behavior is presentation-only and uses fault-tolerant local
storage outside canonical session and recovery data. Narrow layouts hide the
resizers and stack without page-level horizontal overflow.

RW-02.2 automated engineering verification completed on 2026-08-11:

- 25 Concept records passed `concept_tools.py validate`;
- the focused Reading UI suite passed 32 tests;
- the full suite passed 49 tests;
- Python compilation, JavaScript syntax checking, and `git diff --check`
  passed; and
- the generated offline HTML is 974,523 bytes with 18 bilingual section pairs,
  7 images, 2 rendered tables, 3 accessible resizers, and 131 unique
  annotatable source blocks.

These metrics are RW-02.2 engineering evidence, not the historical RW-02.1
metrics above. The separate final human acceptance record appears below.

## Local artifact boundary

The narrow `.gitignore` rule `ResearchOS/00_Inbox/reading/**/_local/` matches
all local artifacts below, while leaving `source_record.md` Git-visible:

- `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.pdf`
- `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.reading.md`
- `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.zh-CN.reading.md`
- `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/assets/figures/figure-01.png` through `figure-07.png`
- `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/reading-workspace.html`
- Byte-identical real session copy:
  `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/reading_session.md`
- Corrected external-summary copy:
  `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/external_llm_conversation_summary.md`

The protected originals under `read data/` remain outside the bundle and must
remain unchanged, untracked, and unstaged. The session copy is byte-identical.
Only the copied external summary is corrected; it remains unverified,
session-external, non-authoritative, and outside `reading_session.md`.

## Launch command

From the repository root:

```powershell
py -3.9 ResearchOS/99_Meta/tools/reading_ui.py `
  "ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.reading.md" `
  --reference-translation `
  "ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.zh-CN.reading.md" `
  --output "ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/reading-workspace.html"
```

The generated page must remain offline and self-contained. No server, plugin,
API, model call, or additional renderer is part of RW-02 preparation.

## Human interaction checklist

The repository owner's overall acceptance statement is the basis for closing
this checklist. The check marks record that overall acceptance coverage; they
do not invent item-specific evaluator comments beyond that statement.

- [x] At 3840×2160 and 1920×1080, confirm all 18 bilingual section rows align
      and the body scroll remains unified.
- [x] Create a Chinese personal note and question; confirm the reference badge,
      paired-English canonical locator, origin field, and answer inheritance.
- [x] Confirm Chinese source-excerpt creation is unavailable and rejected on
      import if forged.
- [x] Import `reading_session.md`; confirm exactly five unique English blocks
      are marked and all five entries remain lossless.
- [x] Delete and recover/import entries; confirm markers recalculate and an
      unresolved match is reported without a false marker.
- [x] Confirm Figure 1–7 and Table 1–2 each appear once, in source order, in the
      independently scrolling rail and remain selectable with Concept Hover.
- [x] Exercise all three resizers by pointer and keyboard, minimum clamps,
      Custom state, double-click reset, and Balanced restoration.
- [x] Simulate presentation-localStorage failure; confirm current-page resizing
      remains and no layout value enters session, recovery, or export payloads.
- [x] At 760px, confirm resizers hide, panes stack, and there is no page-level
      horizontal overflow.
- [x] Confirm the page is self-contained and offline with no remote request or
      absolute local path disclosure.
- [x] Confirm the external LLM summary remains outside the session and is not
      presented as paper authority or `human_reviewed`.

The 50–60rem intermediate viewport was not separately documented in detailed
manual testing. This is a non-blocking limitation under the owner's overall UI
acceptance and does not reopen CSS work or require another human HTML review.

## Human evaluation record

- **Initial realistic reading date:** 2026-08-11
- **Initial result:** Five RW-02.2 usability findings recorded above; not an
  acceptance result.
- **Session evidence:** Two human questions and three human notes; no source
  excerpts or LLM answers.
- **External-summary evidence:** Separate session-external material; not
  imported into the session.

- **Final evaluator:** repository owner
- **Final audit date:** 2026-08-11
- **18-pair bilingual alignment judgment:** Covered by the overall acceptance;
  no separate evaluator comment was reported.
- **Chinese provenance and capture judgment:** Covered by the overall
  acceptance; no separate evaluator comment was reported.
- **Five legacy block markers judgment:** Covered by the overall acceptance;
  no separate evaluator comment was reported.
- **Figure/table rail judgment:** Covered by the overall acceptance; no
  separate evaluator comment was reported.
- **Resizer and responsive-layout judgment:** Covered by the overall
  acceptance; the 50–60rem limitation above is non-blocking.
- **Recovery/import/export boundary judgment:** Covered by the overall
  acceptance; no separate evaluator comment was reported.
- **Offline and source-authority judgment:** Covered by the overall acceptance;
  no separate evaluator comment was reported.
- **Final human conclusion:** 通过，未报告其他问题

## Deferred boundary

This record closes the final checklist from the repository owner's overall
human UI acceptance statement. It does not add Concepts, call an LLM or API,
synthesize `reading_note.draft.md`, create `reading_note.md`, start RW-03,
create or start Obsidian Home or the 1500 MHz TM020 Harmonic Cavity project
page, or start KA-01. RW-02 is accepted and complete; the HTML prototype is frozen;
the commit containing this status record is the published RW-02 baseline.
RW-03 and KA-01 remain unauthorized and not started. Any future
RW-03, Obsidian, or KA-01 work still
requires separate authorization.

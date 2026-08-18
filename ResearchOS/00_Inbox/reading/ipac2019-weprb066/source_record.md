# RW-02 Source Record: IPAC2019-WEPRB066

## Paper identity

- `paper_id`: `ipac2019-weprb066`
- **Title:** Utilizing the High Shunt Impedance TM020-Mode Cavity in the
  Double RF Systems for the Storage Ring of the Thailand New Light Source
- **Authors:** N. Juntong, T. Phimsen, N. Chulakham, S. Malichan
- **Complete citation:** N. Juntong, T. Phimsen, N. Chulakham, and S. Malichan,
  “Utilizing the High Shunt Impedance TM020-Mode Cavity in the Double RF
  Systems for the Storage Ring of the Thailand New Light Source,” in *Proc.
  IPAC'19*, Melbourne, Australia, 2019, paper WEPRB066, pp. 2972-2975, JACoW
  Publishing.
- **DOI:** [10.18429/JACoW-IPAC2019-WEPRB066](https://doi.org/10.18429/JACoW-IPAC2019-WEPRB066)
- **Official proceedings landing:** <https://proceedings.jacow.org/ipac2019/>
- **Official PDF:** <https://proceedings.jacow.org/ipac2019/papers/weprb066.pdf>
- **License:** Creative Commons Attribution 3.0 International (CC BY 3.0).
  Any distribution must maintain attribution to the author(s), title of the
  work, publisher, and DOI. Copyright © 2019.

## Selection reason

This is a short realistic accelerator/RF paper covering a 500.12 MHz
normal-conducting main RF system and a 1500.36 MHz third-harmonic TM020 cavity,
including CST verification, tuners, couplers, shunt impedance, Q, R/Q, and
parasitic-mode damping.

This paper is the only RW-02 reading source. The references listed inside the
paper are follow-up references only; they are not ingested into this session.

## Path conventions

The bundle uses two explicit path forms. Vault-relative paths omit the
repository's `ResearchOS/` prefix; repository-relative paths are the exact paths
used from the repository root.

| Artifact | Vault-relative | Repository-relative |
| --- | --- | --- |
| Git-visible source record | `00_Inbox/reading/ipac2019-weprb066/source_record.md` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/source_record.md` |
| Authoritative local PDF | `00_Inbox/reading/ipac2019-weprb066/_local/source.pdf` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.pdf` |
| Derived reading Markdown | `00_Inbox/reading/ipac2019-weprb066/_local/source.reading.md` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.reading.md` |
| Derived figure crops 1–7 (ignored) | `00_Inbox/reading/ipac2019-weprb066/_local/assets/figures/figure-01.png` through `figure-07.png` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/assets/figures/figure-01.png` through `figure-07.png` |
| Derived Chinese reference translation (ignored) | `00_Inbox/reading/ipac2019-weprb066/_local/source.zh-CN.reading.md` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/source.zh-CN.reading.md` |
| Generated Reading Workspace | `00_Inbox/reading/ipac2019-weprb066/_local/reading-workspace.html` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/reading-workspace.html` |
| Byte-identical real session copy (ignored) | `00_Inbox/reading/ipac2019-weprb066/_local/reading_session.md` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/reading_session.md` |
| Corrected external LLM summary copy (ignored) | `00_Inbox/reading/ipac2019-weprb066/_local/external_llm_conversation_summary.md` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/_local/external_llm_conversation_summary.md` |
| RW-03 reading-note draft | `00_Inbox/reading/ipac2019-weprb066/reading_note.draft.md` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/reading_note.draft.md` |
| RW-04 frozen reading note | `00_Inbox/reading/ipac2019-weprb066/reading_note.md` | `ResearchOS/00_Inbox/reading/ipac2019-weprb066/reading_note.md` |

The PDF is the authoritative local source for visual verification. The
`source.reading.md` file is a one-time, page-marked derived transcription for
the existing offline Reading Workspace; it is not a replacement for the PDF,
not a new source authority, and not a general PDF conversion pipeline.

## Interpretation limitation

The paper itself uses TM020 for both its 500.12 MHz main-cavity design and its
1500.36 MHz harmonic-cavity design. That paper fact is not a user-project mode
decision. The user project establishes only an approximately 500 MHz
normal-conducting main cavity; the TM020 candidate selection applies to the
approximately 1500 MHz harmonic cavity. The user's 500 MHz main-cavity mode is
not determined by this record. Paper geometry, numerical conclusions, and
design choices must not be transferred without separate technical
justification and visual/source review.

## Status and provenance boundary

**Status:** RW-02.2 human UI accepted on 2026-08-11. RW-02 is accepted and
complete; the HTML prototype is frozen; commit `792c802` is the published
RW-02 baseline. RW-03 synthesis content human accepted on 2026-08-18;
selected-text presentation correction applied; RW-03 accepted and complete and
published at commit `7c5dc4f`. `reading_note.draft.md` remains `state: draft` as
RW-03 history. RW-04 freeze was explicitly authorized by the repository owner
on 2026-08-18 and is implemented from the accepted committed draft; final
`reading_note.md` is `state: human_reviewed` and remains pending final audit
and publication. The final note is eligible for a future handoff but has not
been selected for any KA-01 run. RW-05, Concept proposal, and KA-01 remain
unauthorized and unstarted.

The local source bundle is prepared for human comparison of the Markdown
reading view against the original PDF. RW-02.1 remains a historical narrow
presentation correction, not an architecture redesign: the English
transcription is the sole authoritative reading source, local raster figure
crops are embedded for self-contained display, and the Chinese file is an
unverified machine/LLM-assisted derived reference translation. RW-02.1
originally allowed only English selection to create entries; that history is
preserved.

A realistic human reading on 2026-08-11 found five RW-02.2 usability issues:
section-level bilingual alignment, Chinese note/question capture, visible
annotated-block markers, an independent figure/table rail, and draggable 4K
column widths. RW-02.2 supersedes only the old selection boundary: English may
create source excerpts, notes, and questions; Chinese reference text may create
notes and questions but never a source excerpt, and remains visibly unverified
and non-authoritative.

The ignored `reading_session.md` copy is byte-identical to the active
`rw-session-v0.1` export and contains two human questions and three human notes,
with no source excerpts or LLM answers. The corrected
`external_llm_conversation_summary.md` is separate external LLM material:
unverified, session-external, not paper-source authority, not
`human_reviewed`, and not imported into the session. The complete raw external
conversation is unavailable, so its question evolution and Candidate Personal
Notes cannot be independently verified.

For RW-03, the authoritative `source.reading.md` and byte-identical
`reading_session.md` are the mandatory `SOURCE_PATH` and `SESSION_PATH`. The
repository owner explicitly selected `external_llm_conversation_summary.md` as
the optional `EXTERNAL_SUMMARY_PATH` for this run. That selection does not
change its status: it remains unverified, session-external, non-authoritative,
and not `human_reviewed`. Answer inputs have two separate provenance channels:
canonical `llm_answer` entries inside the session and the optional external
summary outside it. This session has no `llm_answer`; it has two
`human_question` and three `human_note` entries. Paper-supported synthesis is
grounded independently in the authoritative source. The draft does not split
the summary into session entries or promote external content. Future
deduplication may merge repeated phrasing only while retaining the origin
labels.

The five legacy session entries are semantically authoritative-source
selections under the compatibility rule for absent `selected_text_origin`.
Their exact session `selected_text` values were verified against the
authoritative English reading source and are displayed beside the two human
questions and three human notes in the RW-03 draft and frozen note.

No SHA-256, source fingerprint, session fingerprint, or second provenance
fingerprint is recorded for RW-02. Current RW-02.2 automated verification
passed 25 Concept checks, 32 focused Reading UI tests, and 49 full-suite tests.
The 974,523-byte offline HTML contains 18 bilingual section pairs, 7 images, 2
rendered tables, 3 accessible resizers, and 131 unique annotatable source
blocks. The repository owner accepted the RW-02.2 human UI on 2026-08-11 with
the overall conclusion “通过，未报告其他问题”. RW-02 is accepted and complete;
the HTML prototype is frozen; commit `792c802` is the published RW-02 baseline.
RW-03 was separately authorized on 2026-08-11. RW-03 synthesis content human
accepted on 2026-08-18; selected-text presentation correction applied; RW-03
accepted and complete and published at commit `7c5dc4f`. The draft remains
`state: draft` as history, and the final `reading_note.md` is
`human_reviewed`. No source, session, or external-summary SHA/fingerprint was
added; RW-04 added no SHA or fingerprint to the final note. RW-04 freeze was
explicitly authorized and implemented, pending final audit and publication;
RW-05, Concept proposal, and KA-01 remain unauthorized and unstarted.

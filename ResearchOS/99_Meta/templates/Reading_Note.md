---
type: reading_note
schema_version: reading-note-v0.1
paper_id: ""
state: draft
title: ""
authors: []
doi: ""
source_path: "" # Required authoritative paper source.
session_path: "" # Required authoritative human reading session.
external_summary_path: "" # Optional; leave empty when no human-selected external summary is used.
synthesis_method: manually_triggered_llm
created: ""
updated: ""
---

# Reading Note Title

## 1 Draft Status and Provenance Legend

<!-- State draft status and define provenance labels. -->

## 2 Why This Paper Matters

<!-- Keep paper evidence, human input, external material, and synthesis inference distinct. -->

## 3 Paper-Supported Findings

<!-- Add source-grounded findings with precise locators. -->

## 4 Human Questions

<!--
Cover every human question from the authoritative session.

Selected-text display invariant for sections 4 and 5:
- For every human_question or human_note with non-empty selected_text, place the
  exact session field next to the human content; never reconstruct it from
  source_locator or an LLM paraphrase.
- Present entry_id, source_locator, then "**框选原文（session 原样）**", the
  origin-appropriate marker, a Markdown blockquote of selected_text, and only
  then the original human question or note.
- authoritative_source selections may use [paper/quote].
- reference_translation selections must instead show
  "中文参考译文 / 机器或 LLM 辅助 / 未核验 / 非权威" and must never use
  [paper/quote].
- Preserve the existing compatibility semantics for legacy entries without
  selected_text_origin; do not backfill the absent field.
- If selected_text is empty or absent, display "未记录框选内容" and never invent
  context.
- This presentation rule neither embeds the complete source in the session nor
  changes rw-session-v0.1.
-->

## 5 Human Notes and Follow-ups

<!-- Cover every human note, preserve its origin, and apply the sections 4-5 selected-text display invariant above. -->

## 6 Engineering Implications

<!-- Separate implications from paper claims and mark verification needs. -->

## 7 Equations and Convention Risks

<!-- Define conventions and identify factor, sign, or normalization risks. -->

## 8 Conflicts, Uncertainties, and Required Verification

<!-- Record conflicts and required verification without guessing. -->

## 9 Existing Concepts

<!-- Link only canonical Concept notes. -->

## 10 Concept Gaps

<!-- List non-canonical concept gaps as plain text. -->

## 11 Session Coverage

<!-- Account for every authoritative session entry. -->

## 12 Human Review Checklist

<!-- Record the checks required before promotion from draft. -->

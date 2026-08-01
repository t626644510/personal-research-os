# Concept Schema v0.1

Status: stable baseline

Effective date: 2026-08-01

This schema defines the contract for every Markdown file stored under `01_Concept/`. The contract is intentionally small so that Obsidian, Git, and the Python indexer remain the only required infrastructure in phase 1.

## File identity

- Store one concept per Markdown file at `01_Concept/<Concept Name>.md`.
- The filename (without `.md`) and the H1 title must be identical; this is the canonical concept name.
- `id` is the stable machine identifier. Use lowercase `snake_case`, keep it unique, and do not change it when only the display name changes.
- Put alternate spellings, abbreviations, translations, and legacy names in `aliases`.

## Required YAML metadata

Use this order when creating a note:

```yaml
---
id: concept_id
aliases:
  - Alternate name
category:
  - domain
level: familiar
confidence:
  textbook: medium
  personal: low
origin:
  - manual
created: 2026-08-01
updated: 2026-08-01
---
```

Field rules:

| Field | Type | Rule |
| --- | --- | --- |
| `id` | string | Unique lowercase `snake_case`; pattern `[a-z][a-z0-9_]*` |
| `aliases` | list of strings | May be empty as `[]`; values must be unique within the note |
| `category` | list of strings | At least one research domain |
| `level` | string | One of `seed`, `familiar`, `working`, `expert` |
| `confidence` | map | Must contain `textbook` and `personal`; each is `low`, `medium`, or `high` |
| `origin` | list of strings | At least one provenance label such as `paper`, `textbook`, `simulation`, `experiment`, or `manual` |
| `created` | date string | ISO date in `YYYY-MM-DD` form |
| `updated` | date string | ISO date in `YYYY-MM-DD` form and not earlier than `created` |

Additional top-level fields are reserved for later schema versions and are ignored by the v0.1 index. The dependency-free parser accepts the subset used here: plain or quoted scalar values, two-space-indented lists, and one-level maps. If the schema later needs anchors, multiline YAML scalars, or deeper nesting, replace the small parser with a reviewed YAML library rather than extending it ad hoc.

## Required body

The H2 sections below must each occur exactly once, in this order, and contain content:

```markdown
# Concept Name

## Hover Summary

A self-contained summary for the hover card.

## Definition

The formal definition from a textbook or source.

## My Understanding

The owner's current mental model.

## Engineering View

Practical interpretation, constraints, and failure modes.

## Formula

Key equations and symbol definitions, or an explicit “Not applicable”.

## Application

How the concept is used in current research.

## Related Concepts

Obsidian wikilinks such as `[[Wakefield]]`.

## Sources

Traceable papers, books, documentation, data, or experiments.

## Decision Log

Dated research decisions and their rationale.

## History

Dated note changes.
```

`Hover Summary` is one paragraph of no more than 280 characters. It must make sense without opening the full note. Obsidian wikilinks in `Related Concepts` are the phase-1 relationship model.

## Index contract

`99_Meta/concept_index.json` is generated data. Its canonical name keys come from H1 titles. The original `path`, `aliases`, and normalized `hover_summary` fields remain stable; P01 adds `id`, `category`, and `related_concepts`. Related values are canonical Concept names resolved from wikilinks, including links written with aliases. Do not hand-edit the index. Run:

```powershell
python ResearchOS/99_Meta/tools/concept_tools.py scan
```

The scan is atomic: validation, collision checks, and related-link resolution complete before the existing index is replaced. An unresolved or self-referential related Concept prevents replacement.

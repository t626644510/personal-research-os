"""Resolve Concept mentions from Markdown using the local hover index."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


VAULT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX_PATH = VAULT_ROOT / "99_Meta" / "concept_index.json"
ASCII_WORD_CHARACTER = re.compile(r"[A-Za-z0-9_]")


class HoverIndexError(ValueError):
    """Raised when concept_index.json cannot be used safely."""


@dataclass(frozen=True)
class _TermMatcher:
    canonical_name: str
    term: str
    pattern: re.Pattern[str]
    entry: Mapping[str, Any]


@dataclass(frozen=True)
class _Candidate:
    start: int
    end: int
    matcher: _TermMatcher


def _validate_string_list(entry: Mapping[str, Any], field: str) -> None:
    value = entry.get(field, [])
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise HoverIndexError(f"index field '{field}' must be a list of strings")


def _validate_index(index: Any) -> Mapping[str, Mapping[str, Any]]:
    if not isinstance(index, dict):
        raise HoverIndexError("concept index root must be a JSON object")

    for canonical_name, entry in index.items():
        if not isinstance(canonical_name, str) or not canonical_name.strip():
            raise HoverIndexError("concept index names must be non-empty strings")
        if not isinstance(entry, dict):
            raise HoverIndexError(f"index entry '{canonical_name}' must be an object")
        if not isinstance(entry.get("path"), str) or not entry["path"]:
            raise HoverIndexError(f"index entry '{canonical_name}' has no valid path")
        if not isinstance(entry.get("hover_summary"), str):
            raise HoverIndexError(
                f"index entry '{canonical_name}' has no valid hover_summary"
            )
        _validate_string_list(entry, "aliases")
        _validate_string_list(entry, "category")
        _validate_string_list(entry, "related_concepts")

        concept_id = entry.get("id")
        if concept_id is not None and not isinstance(concept_id, str):
            raise HoverIndexError(f"index entry '{canonical_name}' has an invalid id")
    return index


def load_concept_index(
    index_path: str | Path = DEFAULT_INDEX_PATH,
) -> Mapping[str, Mapping[str, Any]]:
    """Load and validate a generated Concept index.

    Entries generated before P01 remain valid: the new ``id``, ``category``, and
    ``related_concepts`` fields are optional when an older index is consumed.
    """

    path = Path(index_path)
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise HoverIndexError(f"invalid JSON in {path}: {exc}") from exc
    return _validate_index(data)


def _normalized_term(term: str) -> str:
    return " ".join(term.split()).casefold()


def _compile_term(term: str) -> re.Pattern[str]:
    parts = [re.escape(part) for part in term.split()]
    body = r"\s+".join(parts)
    prefix = (
        r"(?<![A-Za-z0-9_])" if ASCII_WORD_CHARACTER.fullmatch(term[0]) else ""
    )
    suffix = (
        r"(?![A-Za-z0-9_])" if ASCII_WORD_CHARACTER.fullmatch(term[-1]) else ""
    )
    return re.compile(f"{prefix}{body}{suffix}", re.IGNORECASE)


def _build_matchers(
    index: Mapping[str, Mapping[str, Any]],
) -> list[_TermMatcher]:
    matchers: list[_TermMatcher] = []
    owners: dict[str, str] = {}

    for canonical_name in sorted(index, key=str.casefold):
        entry = index[canonical_name]
        terms = [canonical_name, *entry.get("aliases", [])]
        for term in terms:
            stripped = term.strip()
            normalized = _normalized_term(stripped)
            if not normalized:
                continue
            previous_owner = owners.get(normalized)
            if previous_owner is not None:
                if previous_owner != canonical_name:
                    raise HoverIndexError(
                        f"term '{stripped}' is shared by '{previous_owner}' and "
                        f"'{canonical_name}'"
                    )
                continue
            owners[normalized] = canonical_name
            matchers.append(
                _TermMatcher(
                    canonical_name=canonical_name,
                    term=stripped,
                    pattern=_compile_term(stripped),
                    entry=entry,
                )
            )
    return matchers


def resolve_mentions(
    markdown_text: str,
    concept_index: Mapping[str, Mapping[str, Any]] | None = None,
    *,
    index_path: str | Path = DEFAULT_INDEX_PATH,
) -> list[dict[str, Any]]:
    """Return left-to-right, longest-first, non-overlapping Concept matches."""

    if not isinstance(markdown_text, str):
        raise TypeError("markdown_text must be a string")
    if concept_index is None:
        index = load_concept_index(index_path)
    else:
        index = _validate_index(concept_index)

    candidates: list[_Candidate] = []
    for matcher in _build_matchers(index):
        for match in matcher.pattern.finditer(markdown_text):
            candidates.append(_Candidate(match.start(), match.end(), matcher))

    candidates.sort(
        key=lambda candidate: (
            candidate.start,
            -(candidate.end - candidate.start),
            candidate.matcher.canonical_name.casefold(),
            candidate.matcher.term.casefold(),
        )
    )

    results: list[dict[str, Any]] = []
    cursor = 0
    for candidate in candidates:
        if candidate.start < cursor:
            continue
        matcher = candidate.matcher
        entry = matcher.entry
        results.append(
            {
                "concept": matcher.canonical_name,
                "matched_term": matcher.term,
                "matched_text": markdown_text[candidate.start : candidate.end],
                "start": candidate.start,
                "end": candidate.end,
                "id": entry.get("id"),
                "path": entry["path"],
                "aliases": list(entry.get("aliases", [])),
                "category": list(entry.get("category", [])),
                "hover_summary": entry["hover_summary"],
                "related_concepts": list(entry.get("related_concepts", [])),
            }
        )
        cursor = candidate.end
    return results


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve Concept mentions from Markdown without network access."
    )
    parser.add_argument("text", nargs="?", help="Markdown text to resolve")
    parser.add_argument("--file", type=Path, help="read Markdown from a UTF-8 file")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.text is not None and args.file is not None:
        parser.error("provide text or --file, not both")

    try:
        if args.file is not None:
            markdown_text = args.file.read_text(encoding="utf-8-sig")
        elif args.text is not None:
            markdown_text = args.text
        elif not sys.stdin.isatty():
            markdown_text = sys.stdin.read()
        else:
            parser.error("provide text, --file, or piped stdin")
        matches = resolve_mentions(markdown_text, index_path=args.index)
    except (OSError, HoverIndexError) as exc:
        print(exc, file=sys.stderr)
        return 1

    print(json.dumps(matches, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

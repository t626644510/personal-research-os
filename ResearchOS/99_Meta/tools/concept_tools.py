"""Validate Concept notes and build the phase-1 hover index.

This module deliberately uses only the Python standard library. It supports the
small YAML subset defined by Concept Schema v0.1; use a reviewed YAML library if
future schema versions require general YAML features.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Sequence


VAULT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONCEPT_DIR = VAULT_ROOT / "01_Concept"
DEFAULT_INDEX_PATH = VAULT_ROOT / "99_Meta" / "concept_index.json"

REQUIRED_METADATA = (
    "id",
    "aliases",
    "category",
    "level",
    "confidence",
    "origin",
    "created",
    "updated",
)
REQUIRED_SECTIONS = (
    "Hover Summary",
    "Definition",
    "My Understanding",
    "Engineering View",
    "Formula",
    "Application",
    "Related Concepts",
    "Sources",
    "Decision Log",
    "History",
)
ALLOWED_LEVELS = {"seed", "familiar", "working", "expert"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}

ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
KEY_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
H1_PATTERN = re.compile(r"^# (.+?)\s*$", re.MULTILINE)
H2_PATTERN = re.compile(r"^## (.+?)\s*$", re.MULTILINE)


class ConceptFormatError(ValueError):
    """Raised when a Concept cannot be parsed or validated."""


@dataclass(frozen=True)
class ParsedConcept:
    path: Path
    name: str
    metadata: dict[str, Any]
    sections: dict[str, str]
    section_order: tuple[str, ...]


def _parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip()
    if value == "[]":
        return []
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ConceptFormatError(f"invalid quoted string: {value}") from exc
        if not isinstance(decoded, str):
            raise ConceptFormatError(f"expected a string, got: {value}")
        return decoded
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def _parse_frontmatter(lines: Sequence[str]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    active_key: str | None = None

    for line_number, raw_line in enumerate(lines, start=2):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line[: len(raw_line) - len(raw_line.lstrip())]:
            raise ConceptFormatError(
                f"frontmatter line {line_number}: use spaces, not tabs"
            )

        indentation = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if indentation == 0:
            if ":" not in stripped:
                raise ConceptFormatError(
                    f"frontmatter line {line_number}: expected 'key: value'"
                )
            key, raw_value = stripped.split(":", 1)
            key = key.strip()
            if not KEY_PATTERN.fullmatch(key):
                raise ConceptFormatError(
                    f"frontmatter line {line_number}: invalid key '{key}'"
                )
            if key in metadata:
                raise ConceptFormatError(
                    f"frontmatter line {line_number}: duplicate key '{key}'"
                )
            value = raw_value.strip()
            metadata[key] = _parse_scalar(value) if value else None
            active_key = key if not value else None
            continue

        if indentation != 2 or active_key is None:
            raise ConceptFormatError(
                f"frontmatter line {line_number}: only two-space lists or maps are supported"
            )

        if stripped.startswith("- "):
            if metadata[active_key] is None:
                metadata[active_key] = []
            if not isinstance(metadata[active_key], list):
                raise ConceptFormatError(
                    f"frontmatter line {line_number}: mixed list and map for '{active_key}'"
                )
            item = _parse_scalar(stripped[2:])
            if not isinstance(item, str) or not item:
                raise ConceptFormatError(
                    f"frontmatter line {line_number}: list entries must be non-empty strings"
                )
            metadata[active_key].append(item)
            continue

        if ":" not in stripped:
            raise ConceptFormatError(
                f"frontmatter line {line_number}: expected nested 'key: value'"
            )
        nested_key, raw_value = stripped.split(":", 1)
        nested_key = nested_key.strip()
        if not KEY_PATTERN.fullmatch(nested_key):
            raise ConceptFormatError(
                f"frontmatter line {line_number}: invalid nested key '{nested_key}'"
            )
        if metadata[active_key] is None:
            metadata[active_key] = {}
        if not isinstance(metadata[active_key], dict):
            raise ConceptFormatError(
                f"frontmatter line {line_number}: mixed list and map for '{active_key}'"
            )
        if nested_key in metadata[active_key]:
            raise ConceptFormatError(
                f"frontmatter line {line_number}: duplicate nested key '{nested_key}'"
            )
        nested_value = _parse_scalar(raw_value)
        if not isinstance(nested_value, str) or not nested_value:
            raise ConceptFormatError(
                f"frontmatter line {line_number}: nested values must be non-empty strings"
            )
        metadata[active_key][nested_key] = nested_value

    return metadata


def _parse_concept(path: Path) -> ParsedConcept:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ConceptFormatError("file is not valid UTF-8") from exc

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ConceptFormatError("file must start with YAML frontmatter delimiter '---'")

    try:
        frontmatter_end = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as exc:
        raise ConceptFormatError("YAML frontmatter is missing its closing '---'") from exc

    metadata = _parse_frontmatter(lines[1:frontmatter_end])
    body = "\n".join(lines[frontmatter_end + 1 :]).strip()

    h1_matches = list(H1_PATTERN.finditer(body))
    if len(h1_matches) != 1:
        raise ConceptFormatError("body must contain exactly one H1 title")
    name = h1_matches[0].group(1).strip()

    heading_matches = list(H2_PATTERN.finditer(body))
    section_order = tuple(match.group(1).strip() for match in heading_matches)
    if len(section_order) != len(set(section_order)):
        duplicate = next(
            heading for heading in section_order if section_order.count(heading) > 1
        )
        raise ConceptFormatError(f"duplicate H2 section '{duplicate}'")

    sections: dict[str, str] = {}
    for index, match in enumerate(heading_matches):
        content_end = (
            heading_matches[index + 1].start()
            if index + 1 < len(heading_matches)
            else len(body)
        )
        sections[match.group(1).strip()] = body[match.end() : content_end].strip()

    return ParsedConcept(path, name, metadata, sections, section_order)


def _validate_string_list(
    metadata: dict[str, Any], field: str, *, allow_empty: bool
) -> list[str]:
    errors: list[str] = []
    value = metadata.get(field)
    if not isinstance(value, list):
        return [f"metadata '{field}' must be a list"]
    if not allow_empty and not value:
        errors.append(f"metadata '{field}' must contain at least one value")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"metadata '{field}' entries must be non-empty strings")
    normalized = [item.strip().casefold() for item in value if isinstance(item, str)]
    if len(normalized) != len(set(normalized)):
        errors.append(f"metadata '{field}' contains duplicate values")
    return errors


def _parse_iso_date(value: Any, field: str, errors: list[str]) -> date | None:
    if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
        errors.append(f"metadata '{field}' must use YYYY-MM-DD")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"metadata '{field}' is not a valid calendar date")
        return None


def _validation_errors(concept: ParsedConcept) -> list[str]:
    errors: list[str] = []
    metadata = concept.metadata

    for field in REQUIRED_METADATA:
        if field not in metadata:
            errors.append(f"missing metadata '{field}'")

    concept_id = metadata.get("id")
    if not isinstance(concept_id, str) or not ID_PATTERN.fullmatch(concept_id):
        errors.append("metadata 'id' must match [a-z][a-z0-9_]*")

    errors.extend(_validate_string_list(metadata, "aliases", allow_empty=True))
    errors.extend(_validate_string_list(metadata, "category", allow_empty=False))
    errors.extend(_validate_string_list(metadata, "origin", allow_empty=False))

    level = metadata.get("level")
    if level not in ALLOWED_LEVELS:
        allowed = ", ".join(sorted(ALLOWED_LEVELS))
        errors.append(f"metadata 'level' must be one of: {allowed}")

    confidence = metadata.get("confidence")
    if not isinstance(confidence, dict):
        errors.append("metadata 'confidence' must be a map")
    else:
        for confidence_kind in ("textbook", "personal"):
            confidence_value = confidence.get(confidence_kind)
            if confidence_value not in ALLOWED_CONFIDENCE:
                allowed = ", ".join(sorted(ALLOWED_CONFIDENCE))
                errors.append(
                    f"metadata 'confidence.{confidence_kind}' must be one of: {allowed}"
                )

    created = _parse_iso_date(metadata.get("created"), "created", errors)
    updated = _parse_iso_date(metadata.get("updated"), "updated", errors)
    if created is not None and updated is not None and updated < created:
        errors.append("metadata 'updated' cannot be earlier than 'created'")

    if concept.path.stem != concept.name:
        errors.append(
            f"filename '{concept.path.stem}' must match H1 title '{concept.name}'"
        )

    missing_sections = [
        section for section in REQUIRED_SECTIONS if section not in concept.sections
    ]
    for section in missing_sections:
        errors.append(f"missing section '## {section}'")

    if not missing_sections:
        positions = [concept.section_order.index(section) for section in REQUIRED_SECTIONS]
        if positions != sorted(positions):
            errors.append("required H2 sections are not in the schema order")

    for section in REQUIRED_SECTIONS:
        if section in concept.sections and not concept.sections[section].strip():
            errors.append(f"section '## {section}' must not be empty")

    hover_summary = concept.sections.get("Hover Summary", "").strip()
    normalized_summary = " ".join(hover_summary.split())
    if "\n\n" in hover_summary:
        errors.append("section '## Hover Summary' must be one paragraph")
    if len(normalized_summary) > 280:
        errors.append("section '## Hover Summary' must not exceed 280 characters")

    return errors


def validate_concept(path: str | Path) -> list[str]:
    """Return validation errors for one Concept Markdown file."""

    concept_path = Path(path)
    if not concept_path.is_file():
        return ["path is not a file"]
    if concept_path.suffix.lower() != ".md":
        return ["Concept path must end in .md"]
    try:
        concept = _parse_concept(concept_path)
    except (OSError, ConceptFormatError) as exc:
        return [str(exc)]
    return _validation_errors(concept)


def _normalized_term(value: str) -> str:
    return " ".join(value.split()).casefold()


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return str(path)


def scan_concepts(
    concept_dir: str | Path = DEFAULT_CONCEPT_DIR,
    output_path: str | Path = DEFAULT_INDEX_PATH,
) -> dict[str, dict[str, Any]]:
    """Validate all Concept notes and atomically regenerate concept_index.json."""

    concept_root = Path(concept_dir).resolve()
    index_path = Path(output_path).resolve()
    if not concept_root.is_dir():
        raise ConceptFormatError(f"Concept directory does not exist: {concept_root}")

    concept_paths = sorted(
        concept_root.rglob("*.md"), key=lambda path: path.as_posix().casefold()
    )
    concepts: list[ParsedConcept] = []
    errors: list[str] = []

    for path in concept_paths:
        try:
            concept = _parse_concept(path)
        except (OSError, ConceptFormatError) as exc:
            errors.append(f"{_display_path(path)}: {exc}")
            continue
        for error in _validation_errors(concept):
            errors.append(f"{_display_path(path)}: {error}")
        concepts.append(concept)

    ids: dict[str, Path] = {}
    terms: dict[str, tuple[str, Path]] = {}
    for concept in concepts:
        concept_id = concept.metadata.get("id")
        if isinstance(concept_id, str):
            previous_path = ids.get(concept_id)
            if previous_path is not None:
                errors.append(
                    f"{_display_path(concept.path)}: duplicate id '{concept_id}' also used by "
                    f"{_display_path(previous_path)}"
                )
            else:
                ids[concept_id] = concept.path

        aliases = concept.metadata.get("aliases", [])
        candidates = [concept.name]
        if isinstance(aliases, list):
            candidates.extend(alias for alias in aliases if isinstance(alias, str))
        local_terms: set[str] = set()
        for candidate in candidates:
            normalized = _normalized_term(candidate)
            if not normalized or normalized in local_terms:
                continue
            local_terms.add(normalized)
            previous = terms.get(normalized)
            if previous is not None and previous[1] != concept.path:
                errors.append(
                    f"{_display_path(concept.path)}: name or alias '{candidate}' conflicts with "
                    f"'{previous[0]}' in {_display_path(previous[1])}"
                )
            else:
                terms[normalized] = (candidate, concept.path)

    if errors:
        raise ConceptFormatError("Concept scan failed:\n- " + "\n- ".join(errors))

    vault_root = concept_root.parent
    index: dict[str, dict[str, Any]] = {}
    for concept in sorted(concepts, key=lambda item: item.name.casefold()):
        relative_path = concept.path.resolve().relative_to(vault_root).as_posix()
        index[concept.name] = {
            "path": relative_path,
            "aliases": concept.metadata["aliases"],
            "hover_summary": " ".join(concept.sections["Hover Summary"].split()),
        }

    serialized = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = index_path.with_name(f"{index_path.name}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
        temporary_path.replace(index_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return index


def _command_validate(paths: Sequence[Path], concept_dir: Path) -> int:
    targets = list(paths)
    if not targets:
        targets = sorted(
            concept_dir.resolve().rglob("*.md"),
            key=lambda path: path.as_posix().casefold(),
        )
    if not targets:
        print(f"No Concept Markdown files found in {concept_dir}", file=sys.stderr)
        return 1

    failed = False
    for path in targets:
        errors = validate_concept(path)
        display_path = _display_path(path)
        if errors:
            failed = True
            print(f"[ERROR] {display_path}", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"[OK] {display_path}")
    return 1 if failed else 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Concept notes and build concept_index.json."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate one or all Concept notes"
    )
    validate_parser.add_argument("paths", nargs="*", type=Path)
    validate_parser.add_argument(
        "--concept-dir", type=Path, default=DEFAULT_CONCEPT_DIR
    )

    scan_parser = subparsers.add_parser(
        "scan", help="validate all Concepts and regenerate the JSON index"
    )
    scan_parser.add_argument(
        "--concept-dir", type=Path, default=DEFAULT_CONCEPT_DIR
    )
    scan_parser.add_argument("--output", type=Path, default=DEFAULT_INDEX_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "validate":
        return _command_validate(args.paths, args.concept_dir)
    try:
        index = scan_concepts(args.concept_dir, args.output)
    except (OSError, ConceptFormatError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"Wrote {len(index)} concepts to {_display_path(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

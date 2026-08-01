"""Generate a self-contained offline HTML preview for Concept hover cards."""

from __future__ import annotations

import argparse
import html
import sys
import tempfile
import webbrowser
from pathlib import Path
from typing import Any, Mapping, Sequence

from hover_resolver import (
    DEFAULT_INDEX_PATH,
    HoverIndexError,
    load_concept_index,
    resolve_mentions,
)


DEFAULT_OUTPUT_PATH = (
    Path(tempfile.gettempdir()) / "personal-research-os-hover-demo.html"
)

STYLES = """
:root {
  color-scheme: light;
  --background: #f4f1e8;
  --paper: #fffdf7;
  --ink: #242821;
  --muted: #62695e;
  --accent: #176b59;
  --highlight: #dff3c9;
  --border: #d8d3c5;
  --shadow: 0 14px 34px rgba(36, 40, 33, 0.18);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--background);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
}

.viewer-header {
  padding: 1rem max(1rem, calc((100vw - 58rem) / 2));
  border-bottom: 1px solid var(--border);
  background: rgba(255, 253, 247, 0.96);
}

.viewer-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
}

.viewer-meta {
  margin: 0.25rem 0 0;
  color: var(--muted);
  font-size: 0.82rem;
}

.note-shell {
  width: min(58rem, calc(100% - 2rem));
  min-height: calc(100vh - 7rem);
  margin: 1.5rem auto;
  padding: clamp(1.25rem, 4vw, 3.5rem);
  border: 1px solid var(--border);
  border-radius: 0.8rem;
  background: var(--paper);
  box-shadow: 0 10px 30px rgba(36, 40, 33, 0.07);
}

.markdown-source {
  margin: 0;
  font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
  font-size: 0.98rem;
  line-height: 1.75;
  overflow-wrap: anywhere;
  white-space: pre-wrap;
}

.concept-hit {
  position: relative;
  border-radius: 0.2rem;
  outline: none;
  cursor: help;
}

.concept-text {
  padding: 0.04rem 0.12rem;
  border-bottom: 2px solid var(--accent);
  border-radius: 0.2rem;
  background: var(--highlight);
  font-weight: 650;
}

.concept-hit:focus-visible .concept-text {
  outline: 3px solid rgba(23, 107, 89, 0.28);
  outline-offset: 2px;
}

.hover-card {
  position: absolute;
  z-index: 20;
  top: calc(100% + 0.55rem);
  left: 0;
  width: min(24rem, calc(100vw - 3rem));
  padding: 0.9rem 1rem;
  border: 1px solid #b9c8bc;
  border-radius: 0.65rem;
  background: #fbfff7;
  box-shadow: var(--shadow);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  font-size: 0.88rem;
  line-height: 1.45;
  opacity: 0;
  pointer-events: none;
  transform: translateY(-0.25rem);
  transition: opacity 90ms ease, transform 90ms ease, visibility 90ms;
  visibility: hidden;
  white-space: normal;
}

.concept-hit:hover .hover-card,
.concept-hit:focus .hover-card {
  opacity: 1;
  transform: translateY(0);
  visibility: visible;
}

.card-title,
.card-summary,
.card-meta {
  display: block;
}

.card-title {
  margin-bottom: 0.38rem;
  color: #0c5545;
  font-size: 1rem;
  font-weight: 760;
}

.card-summary { color: #252c25; }

.card-meta {
  margin-top: 0.48rem;
  color: var(--muted);
  font-size: 0.78rem;
}

.card-label {
  color: #3e483e;
  font-weight: 700;
}

@media (max-width: 40rem) {
  .note-shell {
    width: 100%;
    margin: 0;
    border-right: 0;
    border-left: 0;
    border-radius: 0;
  }
}
""".strip()


def _text(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _hover_card(match: Mapping[str, Any], card_number: int) -> str:
    categories = match.get("category", [])
    related = match.get("related_concepts", [])
    metadata: list[str] = []
    if categories:
        metadata.append(
            '<span class="card-meta"><span class="card-label">Category:</span> '
            + ", ".join(_text(item) for item in categories)
            + "</span>"
        )
    if related:
        metadata.append(
            '<span class="card-meta"><span class="card-label">Related:</span> '
            + ", ".join(_text(item) for item in related)
            + "</span>"
        )

    card_id = f"hover-card-{card_number}"
    return (
        f'<span class="concept-hit" tabindex="0" aria-describedby="{card_id}">'
        f'<span class="concept-text">{_text(match["matched_text"])}</span>'
        f'<span class="hover-card" id="{card_id}" role="tooltip">'
        f'<span class="card-title">{_text(match["concept"])}</span>'
        f'<span class="card-summary">{_text(match["hover_summary"])}</span>'
        + "".join(metadata)
        + "</span></span>"
    )


def _annotate_source(
    markdown_text: str, matches: Sequence[Mapping[str, Any]]
) -> str:
    fragments: list[str] = []
    cursor = 0
    for card_number, match in enumerate(matches, start=1):
        start = match.get("start")
        end = match.get("end")
        if (
            not isinstance(start, int)
            or not isinstance(end, int)
            or start < cursor
            or end <= start
            or end > len(markdown_text)
        ):
            raise ValueError("hover matches must contain ordered, non-overlapping offsets")
        fragments.append(html.escape(markdown_text[cursor:start], quote=False))
        fragments.append(_hover_card(match, card_number))
        cursor = end
    fragments.append(html.escape(markdown_text[cursor:], quote=False))
    return "".join(fragments)


def render_hover_html(
    markdown_text: str,
    matches: Sequence[Mapping[str, Any]],
    *,
    title: str = "Hover Encyclopedia Demo",
) -> str:
    """Render resolved matches into a self-contained, dependency-free page."""

    annotated_source = _annotate_source(markdown_text, matches)
    unique_concepts = len({str(match["concept"]) for match in matches})
    status = f"{len(matches)} mentions · {unique_concepts} concepts · local index only"
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{_text(title)} · Hover Encyclopedia</title>\n"
        f"<style>\n{STYLES}\n</style>\n"
        "</head>\n<body>\n"
        '<header class="viewer-header">'
        f'<p class="viewer-title">{_text(title)}</p>'
        f'<p class="viewer-meta">{_text(status)}</p>'
        "</header>\n"
        '<main class="note-shell">'
        f'<article class="markdown-source" aria-label="Markdown note">{annotated_source}</article>'
        "</main>\n"
        "</body>\n</html>\n"
    )


def generate_hover_demo(
    markdown_path: str | Path,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    *,
    index_path: str | Path = DEFAULT_INDEX_PATH,
) -> tuple[Path, list[dict[str, Any]]]:
    """Generate an offline HTML snapshot and return its path and matches."""

    source_path = Path(markdown_path)
    destination = Path(output_path)
    markdown_text = source_path.read_text(encoding="utf-8-sig")
    concept_index = load_concept_index(index_path)
    matches = resolve_mentions(markdown_text, concept_index)
    rendered = render_hover_html(markdown_text, matches, title=source_path.stem)

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(rendered)
    return destination, matches


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a self-contained offline Concept hover demo."
    )
    parser.add_argument("markdown_file", type=Path, help="UTF-8 Markdown note")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument(
        "--open", action="store_true", help="open the generated file in a browser"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        output_path, matches = generate_hover_demo(
            args.markdown_file, args.output, index_path=args.index
        )
    except (OSError, HoverIndexError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    resolved_output = output_path.resolve()
    print(f"Wrote {len(matches)} hover matches to {resolved_output}")
    if args.open and not webbrowser.open(resolved_output.as_uri()):
        print(
            "The browser could not be opened automatically; open the HTML file manually.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

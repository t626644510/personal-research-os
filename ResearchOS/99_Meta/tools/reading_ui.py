"""Generate a self-contained offline Reading Workspace for one Markdown source.

The renderer intentionally supports only the small offline subset needed by
RW-02.2: headings, paragraphs, flat ordered and unordered lists, links, inline
code, fenced code blocks, safe local raster images, and minimal pipe tables.
Unsupported Markdown remains visible as escaped text. Raw HTML is never
executed. An optional derived translation is a separate presentation pane and
never enters the session payload.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
import tempfile
import webbrowser
from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from pathlib import PureWindowsPath
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

from hover_resolver import (
    DEFAULT_INDEX_PATH,
    HoverIndexError,
    load_concept_index,
    resolve_mentions,
)


TOOLS_DIR = Path(__file__).resolve().parent
VAULT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    Path(tempfile.gettempdir()) / "personal-research-os-reading-workspace.html"
)
JAVASCRIPT_PATH = TOOLS_DIR / "reading_ui.js"
STYLESHEET_PATH = TOOLS_DIR / "reading_ui.css"
SESSION_FORMAT = "rw-session-v0.1"

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
STRUCTURAL_HEADING_PATTERN = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
FENCE_PATTERN = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([^`]*)$")
UNORDERED_LIST_PATTERN = re.compile(r"^\s{0,3}[-+*]\s+(.+)$")
ORDERED_LIST_PATTERN = re.compile(r"^\s{0,3}(\d+)[.)]\s+(.+)$")
PIPE_TABLE_ROW_PATTERN = re.compile(r"^\s*\|.*\|\s*$")
PIPE_TABLE_DELIMITER_PATTERN = re.compile(r"^:?-{3,}:?$")
FIGURE_LABEL_PATTERN = re.compile(r"\bFigure\s+([1-7])\b", re.IGNORECASE)
TABLE_LABEL_PATTERN = re.compile(r"\bTable\s+([1-2])\b", re.IGNORECASE)
IMAGE_PATTERN = re.compile(
    r"!\[([^\]\n]*)\]\(\s*(<[^>\n]+>|[^\s)\n]+)"
    r"(?:\s+(\"[^\"]*\"|'[^']*'))?\s*\)"
)
LINK_PATTERN = re.compile(
    r"\[([^\]\n]+)\]\(\s*(<[^>\n]+>|[^\s)\n]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"
)
CJK_PATTERN = re.compile(r"[\u3400-\u9fff]")
ALLOWED_LINK_SCHEMES = {"", "file", "http", "https", "mailto"}
ALLOWED_IMAGE_MIME_TYPES = {
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


@dataclass(frozen=True)
class _MarkdownSection:
    markdown_text: str
    level: int
    locator: str


@dataclass(frozen=True)
class _PipeTable:
    headers: tuple[str, ...]
    alignments: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]
    end_position: int


def _escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _normalized_term(term: str) -> str:
    return " ".join(term.split()).casefold()


def _display_concept_name(
    canonical_name: str, concept_index: Mapping[str, Mapping[str, Any]]
) -> str:
    aliases = concept_index.get(canonical_name, {}).get("aliases", [])
    chinese_alias = next(
        (
            alias
            for alias in aliases
            if isinstance(alias, str) and CJK_PATTERN.search(alias)
        ),
        None,
    )
    if chinese_alias and chinese_alias != canonical_name:
        return f"{chinese_alias}（{canonical_name}）"
    return canonical_name


def _plain_inline_label(value: str) -> str:
    value = LINK_PATTERN.sub(lambda match: match.group(1), value)
    value = re.sub(r"(`+)(.*?)\1", lambda match: match.group(2), value)
    return value.strip().strip("#").strip() or "文档开头"


def _safe_link_target(target: str) -> str | None:
    candidate = target[1:-1] if target.startswith("<") and target.endswith(">") else target
    candidate = html.unescape(candidate.strip())
    if not candidate or candidate.startswith(("//", "\\\\")):
        return None
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in candidate):
        return None
    try:
        scheme = urlsplit(candidate).scheme.casefold()
    except ValueError:
        return None
    if scheme not in ALLOWED_LINK_SCHEMES:
        return None
    return candidate


def _image_parts(match: re.Match[str]) -> tuple[str, str, str]:
    alt = match.group(1)
    target = match.group(2)
    title = match.group(3) or ""
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if title[:1] in {"\"", "'"} and title[-1:] == title[:1]:
        title = title[1:-1]
    return alt, target, title


def _safe_image_data_uri(
    source_directory: Path | None,
    target: str,
) -> tuple[str | None, str]:
    """Return a local raster data URI or a safe, path-free placeholder reason."""

    if source_directory is None:
        return None, "图片路径不可用"
    candidate = html.unescape(target.strip())
    if not candidate:
        return None, "图片路径不安全"
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in candidate):
        return None, "图片路径不安全"
    if candidate.startswith(("/", "\\", "//", "\\\\")):
        return None, "图片路径不安全"
    try:
        parsed = urlsplit(candidate)
        windows_candidate = PureWindowsPath(candidate)
    except ValueError:
        return None, "图片路径不安全"
    if (
        parsed.scheme
        or parsed.netloc
        or parsed.query
        or parsed.fragment
        or windows_candidate.drive
        or windows_candidate.root
    ):
        return None, "图片路径不安全"

    base_directory = source_directory.resolve()
    resolved = (base_directory / Path(candidate)).resolve(strict=False)
    try:
        resolved.relative_to(base_directory)
    except ValueError:
        return None, "图片路径不安全"

    mime_type = ALLOWED_IMAGE_MIME_TYPES.get(resolved.suffix.casefold())
    if mime_type is None:
        return None, "图片格式不受支持"
    if not resolved.is_file():
        return None, "图片缺失"
    try:
        encoded = base64.b64encode(resolved.read_bytes()).decode("ascii")
    except OSError:
        return None, "图片无法读取"
    return f"data:{mime_type};base64,{encoded}", ""


def _safe_json_for_script(value: Mapping[str, Any]) -> str:
    serialized = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return (
        serialized.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _source_label(source_path: Path) -> str:
    resolved = source_path.resolve()
    try:
        return resolved.relative_to(VAULT_ROOT.resolve()).as_posix()
    except ValueError:
        return source_path.name


def _document_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        match = HEADING_PATTERN.match(line)
        if match and len(match.group(1)) == 1:
            return _plain_inline_label(match.group(2))
    return fallback


def _split_markdown_sections(markdown_text: str) -> list[_MarkdownSection]:
    """Split on H1-H3 boundaries without treating fenced content as headings."""

    normalized = markdown_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    boundaries: list[tuple[int, int, str]] = []
    position = 0

    if lines and lines[0].strip() == "---":
        closing = next(
            (
                index
                for index in range(1, len(lines))
                if lines[index].strip() in {"---", "..."}
            ),
            None,
        )
        if closing is not None:
            position = closing + 1

    fence_marker = ""
    fence_length = 0
    while position < len(lines):
        line = lines[position]
        if fence_marker:
            if re.match(
                rf"^\s{{0,3}}{re.escape(fence_marker)}{{{fence_length},}}\s*$",
                line,
            ):
                fence_marker = ""
                fence_length = 0
            position += 1
            continue

        fence_match = FENCE_PATTERN.match(line)
        if fence_match:
            fence_marker = fence_match.group(1)[0]
            fence_length = len(fence_match.group(1))
            position += 1
            continue

        heading_match = STRUCTURAL_HEADING_PATTERN.match(line)
        if heading_match:
            heading_text = heading_match.group(2).rstrip("#").rstrip()
            boundaries.append(
                (
                    position,
                    len(heading_match.group(1)),
                    _plain_inline_label(heading_text),
                )
            )
        position += 1

    if not boundaries:
        return [
            _MarkdownSection(
                markdown_text=normalized,
                level=0,
                locator="文档开头",
            )
        ]

    sections: list[_MarkdownSection] = []
    for index, (boundary, level, locator) in enumerate(boundaries):
        start = 0 if index == 0 else boundary
        end = boundaries[index + 1][0] if index + 1 < len(boundaries) else len(lines)
        sections.append(
            _MarkdownSection(
                markdown_text="\n".join(lines[start:end]),
                level=level,
                locator=locator,
            )
        )
    return sections


def _split_pipe_table_row(line: str) -> tuple[str, ...]:
    candidate = line.strip()
    if candidate.startswith("|"):
        candidate = candidate[1:]
    if candidate.endswith("|") and not candidate.endswith(r"\|"):
        candidate = candidate[:-1]

    cells: list[str] = []
    current: list[str] = []
    position = 0
    while position < len(candidate):
        character = candidate[position]
        if character == "\\" and position + 1 < len(candidate):
            following = candidate[position + 1]
            if following == "|":
                current.append("|")
                position += 2
                continue
        if character == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
        position += 1
    cells.append("".join(current).strip())
    return tuple(cells)


def _parse_pipe_table(lines: Sequence[str], start: int) -> _PipeTable | None:
    if start + 1 >= len(lines) or not PIPE_TABLE_ROW_PATTERN.match(lines[start]):
        return None
    if not PIPE_TABLE_ROW_PATTERN.match(lines[start + 1]):
        return None

    headers = _split_pipe_table_row(lines[start])
    delimiters = _split_pipe_table_row(lines[start + 1])
    if not headers or len(headers) != len(delimiters):
        return None
    if any(
        not PIPE_TABLE_DELIMITER_PATTERN.fullmatch(cell.strip())
        for cell in delimiters
    ):
        return None

    alignments: list[str] = []
    for delimiter in delimiters:
        stripped = delimiter.strip()
        if stripped.startswith(":") and stripped.endswith(":"):
            alignments.append("center")
        elif stripped.endswith(":"):
            alignments.append("right")
        elif stripped.startswith(":"):
            alignments.append("left")
        else:
            alignments.append("")

    rows: list[tuple[str, ...]] = []
    position = start + 2
    while position < len(lines) and PIPE_TABLE_ROW_PATTERN.match(lines[position]):
        row = _split_pipe_table_row(lines[position])
        if len(row) != len(headers):
            return None
        rows.append(row)
        position += 1
    return _PipeTable(
        headers=headers,
        alignments=tuple(alignments),
        rows=tuple(rows),
        end_position=position,
    )


def _next_nonblank(lines: Sequence[str], start: int) -> int:
    position = start
    while position < len(lines) and not lines[position].strip():
        position += 1
    return position


def _paragraph_at(lines: Sequence[str], start: int) -> tuple[list[str], int]:
    paragraph: list[str] = []
    position = start
    while position < len(lines) and lines[position].strip():
        paragraph.append(lines[position].strip())
        position += 1
    return paragraph, position


def _media_caption_reference(value: str) -> tuple[str, int] | None:
    candidate = value.strip()
    if not candidate.startswith("**"):
        return None
    figure_match = FIGURE_LABEL_PATTERN.search(candidate)
    if figure_match:
        return "figure", int(figure_match.group(1))
    table_match = TABLE_LABEL_PATTERN.search(candidate)
    if table_match:
        return "table", int(table_match.group(1))
    return None


def _caption_text(lines: Sequence[str]) -> str:
    caption = " ".join(line.strip() for line in lines).strip()
    return re.sub(r"^\*\*(.+?)\*\*", lambda match: match.group(1), caption, count=1)


class _MarkdownRenderer:
    def __init__(
        self,
        concept_index: Mapping[str, Mapping[str, Any]],
        *,
        source_directory: Path | None = None,
        namespace: str = "",
        source_origin: str = "authoritative_source",
        media_mode: str = "inline",
    ) -> None:
        self.concept_index = concept_index
        self.source_directory = source_directory
        self.namespace = namespace
        self.source_origin = source_origin
        self.media_mode = media_mode
        self.block_number = 0
        self.media_block_number = 0
        self.section_number = 0
        self.hit_number = 0
        self.current_section_id = f"{namespace}section-000"
        self.current_locator = "文档开头"
        self.concepts_seen: set[str] = set()
        self.media_items: list[str] = []

    def _next_block(self) -> str:
        self.block_number += 1
        return f"{self.namespace}block-{self.block_number:04d}"

    def _next_media_block(self) -> str:
        self.media_block_number += 1
        return f"figure-block-{self.media_block_number:04d}"

    def _next_section(self, locator: str) -> str:
        self.section_number += 1
        self.current_section_id = f"{self.namespace}section-{self.section_number:03d}"
        self.current_locator = locator
        return self.current_section_id

    def _source_attributes(self, block_id: str, kind: str) -> str:
        return (
            f' data-source-block="true" data-block-id="{_escape(block_id)}"'
            f' data-section-id="{_escape(self.current_section_id)}"'
            f' data-source-kind="{_escape(kind)}"'
            f' data-locator="{_escape(self.current_locator)}"'
            f' data-source-origin="{_escape(self.source_origin)}"'
        )

    def _concept_hit(
        self,
        match: Mapping[str, Any],
        block_id: str,
    ) -> str:
        self.hit_number += 1
        concept = str(match["concept"])
        self.concepts_seen.add(concept)
        card_id = f"rw-{self.namespace}concept-card-{self.hit_number:05d}"
        term_key = _normalized_term(str(match["matched_term"]))
        title = _display_concept_name(concept, self.concept_index)
        categories = [str(item) for item in match.get("category", [])]
        related = [
            _display_concept_name(str(item), self.concept_index)
            for item in match.get("related_concepts", [])
        ]
        metadata: list[str] = []
        if categories:
            metadata.append(
                '<span class="card-meta"><span class="card-label">分类：</span>'
                + "、".join(_escape(item) for item in categories)
                + "</span>"
            )
        if related:
            metadata.append(
                '<span class="card-meta"><span class="card-label">相关概念：</span>'
                + "、".join(_escape(item) for item in related)
                + "</span>"
            )
        return (
            '<span class="concept-hit" tabindex="0"'
            f' data-concept="{_escape(concept)}"'
            f' data-term-key="{_escape(term_key)}"'
            f' data-term-label="{_escape(match["matched_term"])}"'
            f' data-block-id="{_escape(block_id)}"'
            f' data-section-id="{_escape(self.current_section_id)}"'
            f' aria-describedby="{card_id}">'
            f'<span class="concept-text">{_escape(match["matched_text"])}</span>'
            f'<span class="hover-card" id="{card_id}" role="tooltip">'
            f'<span class="card-title">{_escape(title)}</span>'
            f'<span class="card-summary">{_escape(match["hover_summary"])}</span>'
            + "".join(metadata)
            + '<span class="card-actions">'
            + '<button type="button" data-action="mute-concept">静音此概念</button>'
            + '<button type="button" data-action="mute-term">仅静音此词</button>'
            + "</span></span></span>"
        )

    def _render_plain(self, value: str, block_id: str) -> str:
        matches = resolve_mentions(value, self.concept_index)
        fragments: list[str] = []
        cursor = 0
        for match in matches:
            start = int(match["start"])
            end = int(match["end"])
            fragments.append(html.escape(value[cursor:start], quote=False))
            fragments.append(self._concept_hit(match, block_id))
            cursor = end
        fragments.append(html.escape(value[cursor:], quote=False))
        return "".join(fragments)

    def _render_link(self, label: str, target: str, block_id: str) -> str:
        rendered_label = self._render_inline(label, block_id, allow_links=False)
        safe_target = _safe_link_target(target)
        if safe_target is None:
            return (
                '<span class="unsafe-link" title="已阻止不安全链接">'
                f"{rendered_label}</span>"
            )
        return (
            f'<a href="{_escape(safe_target)}" target="_blank" '
            f'rel="noopener noreferrer">{rendered_label}</a>'
        )

    def _render_image(
        self,
        match: re.Match[str],
        block_id: str,
        *,
        as_figure: bool,
    ) -> str:
        alt, target, title = _image_parts(match)
        safe_alt = alt.strip() or "未标注图片"
        data_uri, failure_reason = _safe_image_data_uri(
            self.source_directory,
            target,
        )
        source_attributes = (
            self._source_attributes(block_id, "image") if as_figure else ""
        )
        if data_uri is None:
            label = f"{safe_alt}：{failure_reason}"
            placeholder = (
                f'<div class="source-image-placeholder" role="img" '
                f'aria-label="{_escape(label)}">'
                f"图片不可用：{_escape(failure_reason)}</div>"
            )
            if as_figure:
                return f'<figure class="source-figure source-image-fallback"{source_attributes}>{placeholder}</figure>'
            return f'<span class="source-image-inline-fallback"{source_attributes}>{placeholder}</span>'

        title_attribute = f' title="{_escape(title)}"' if title else ""
        image = (
            f'<img class="source-image" src="{data_uri}" '
            f'alt="{_escape(safe_alt)}"{title_attribute} loading="lazy">'
        )
        if as_figure:
            return f'<figure class="source-figure"{source_attributes}>{image}</figure>'
        return f'<span class="source-image-inline"{source_attributes}>{image}</span>'

    def _media_placeholder(self, media_kind: str, number: int) -> str:
        target_id = f"{media_kind}-{number}"
        label = f"Figure {number}" if media_kind == "figure" else f"Table {number}"
        return (
            f'<p class="figure-jump-placeholder" data-media-placeholder="{target_id}">'
            f'<a href="#{target_id}" data-figure-jump="{target_id}">'
            f"转到图表栏：{label}</a></p>"
        )

    def _render_authoritative_figure(
        self,
        image_match: re.Match[str],
        caption: str,
        number: int,
    ) -> str:
        block_id = self._next_media_block()
        image = self._render_image(image_match, block_id, as_figure=False)
        rendered_caption = self._render_inline(caption, block_id)
        return (
            f'<figure class="figures-item source-figure" id="figure-{number}" '
            f'data-figure-item="figure-{number}"'
            f'{self._source_attributes(block_id, "figure")}>'
            f"{image}<figcaption>{rendered_caption}</figcaption></figure>"
        )

    def _render_table_markup(self, table: _PipeTable, block_id: str) -> str:
        header_cells: list[str] = []
        for index, value in enumerate(table.headers):
            alignment = table.alignments[index]
            class_attribute = f' class="align-{alignment}"' if alignment else ""
            header_cells.append(
                f"<th{class_attribute}>{self._render_inline(value, block_id)}</th>"
            )

        body_rows: list[str] = []
        for row in table.rows:
            cells: list[str] = []
            for index, value in enumerate(row):
                alignment = table.alignments[index]
                class_attribute = f' class="align-{alignment}"' if alignment else ""
                cells.append(
                    f"<td{class_attribute}>{self._render_inline(value, block_id)}</td>"
                )
            body_rows.append("<tr>" + "".join(cells) + "</tr>")

        body = "<tbody>" + "".join(body_rows) + "</tbody>" if body_rows else ""
        return (
            '<div class="source-table-scroll"><table class="source-table">'
            "<thead><tr>"
            + "".join(header_cells)
            + "</tr></thead>"
            + body
            + "</table></div>"
        )

    def _render_authoritative_table(
        self,
        table: _PipeTable,
        caption: str,
        number: int,
    ) -> str:
        block_id = self._next_media_block()
        rendered_caption = self._render_inline(caption, block_id)
        table_markup = self._render_table_markup(table, block_id)
        return (
            f'<figure class="figures-item source-table-figure" id="table-{number}" '
            f'data-figure-item="table-{number}"'
            f'{self._source_attributes(block_id, "table")}>'
            f"<figcaption>{rendered_caption}</figcaption>{table_markup}</figure>"
        )

    def _render_inline_table(self, table: _PipeTable) -> str:
        block_id = self._next_block()
        return (
            f'<div class="source-table-block"'
            f'{self._source_attributes(block_id, "table")}>'
            f"{self._render_table_markup(table, block_id)}</div>"
        )

    def _render_inline(
        self,
        value: str,
        block_id: str,
        *,
        allow_links: bool = True,
    ) -> str:
        fragments: list[str] = []
        cursor = 0
        length = len(value)
        while cursor < length:
            code_position = value.find("`", cursor)
            image_match = IMAGE_PATTERN.search(value, cursor)
            link_match = LINK_PATTERN.search(value, cursor) if allow_links else None
            image_position = image_match.start() if image_match else -1
            link_position = link_match.start() if link_match else -1
            positions = [
                position
                for position in (code_position, image_position, link_position)
                if position >= 0
            ]
            if not positions:
                fragments.append(self._render_plain(value[cursor:], block_id))
                break

            next_position = min(positions)
            if next_position > cursor:
                fragments.append(self._render_plain(value[cursor:next_position], block_id))

            if code_position == next_position:
                run_match = re.match(r"`+", value[code_position:])
                assert run_match is not None
                delimiter = run_match.group(0)
                content_start = code_position + len(delimiter)
                content_end = value.find(delimiter, content_start)
                if content_end < 0:
                    fragments.append(self._render_plain(value[code_position:], block_id))
                    break
                code_text = value[content_start:content_end]
                fragments.append(f"<code>{html.escape(code_text, quote=False)}</code>")
                cursor = content_end + len(delimiter)
                continue

            if image_position == next_position:
                assert image_match is not None
                fragments.append(self._render_image(image_match, block_id, as_figure=False))
                cursor = image_match.end()
                continue

            assert link_match is not None
            fragments.append(
                self._render_link(link_match.group(1), link_match.group(2), block_id)
            )
            cursor = link_match.end()
        return "".join(fragments)

    def _render_frontmatter(self, lines: Sequence[str]) -> str:
        block_id = self._next_block()
        content = "\n".join(lines)
        return (
            f'<pre class="frontmatter"{self._source_attributes(block_id, "frontmatter")}>'
            f"{html.escape(content, quote=False)}</pre>"
        )

    def _render_fence(
        self,
        fence_lines: Sequence[str],
        info: str,
    ) -> str:
        block_id = self._next_block()
        language = info.strip().split(maxsplit=1)[0] if info.strip() else ""
        language_class = (
            f' class="language-{_escape(language)}"'
            if re.fullmatch(r"[A-Za-z0-9_-]+", language)
            else ""
        )
        code_text = "\n".join(fence_lines)
        return (
            f'<pre class="fenced-code"{self._source_attributes(block_id, "fenced-code")}>'
            f"<code{language_class}>{html.escape(code_text, quote=False)}</code></pre>"
        )

    def render(
        self,
        markdown_text: str,
        *,
        canonical_locator: str | None = None,
    ) -> str:
        lines = markdown_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        rendered: list[str] = []
        position = 0
        if canonical_locator is not None:
            self.current_locator = canonical_locator

        if lines and lines[0].strip() == "---":
            closing = next(
                (
                    index
                    for index in range(1, len(lines))
                    if lines[index].strip() in {"---", "..."}
                ),
                None,
            )
            if closing is not None:
                rendered.append(self._render_frontmatter(lines[: closing + 1]))
                position = closing + 1

        while position < len(lines):
            line = lines[position]
            if not line.strip():
                position += 1
                continue

            fence_match = FENCE_PATTERN.match(line)
            if fence_match:
                delimiter = fence_match.group(1)
                marker = delimiter[0]
                minimum_length = len(delimiter)
                position += 1
                code_lines: list[str] = []
                while position < len(lines):
                    closing = re.match(rf"^\s{{0,3}}{re.escape(marker)}{{{minimum_length},}}\s*$", lines[position])
                    if closing:
                        position += 1
                        break
                    code_lines.append(lines[position])
                    position += 1
                rendered.append(self._render_fence(code_lines, fence_match.group(2)))
                continue

            heading_match = HEADING_PATTERN.match(line)
            if heading_match:
                level = len(heading_match.group(1))
                heading_text = heading_match.group(2).rstrip("#").rstrip()
                locator = _plain_inline_label(heading_text)
                if level <= 3:
                    self._next_section(canonical_locator or locator)
                block_id = self._next_block()
                rendered.append(
                    f"<h{level}{self._source_attributes(block_id, 'heading')}>"
                    f"{self._render_inline(heading_text, block_id)}</h{level}>"
                )
                position += 1
                continue

            image_match = IMAGE_PATTERN.fullmatch(line.strip())
            if image_match:
                alt, _, _ = _image_parts(image_match)
                figure_match = FIGURE_LABEL_PATTERN.search(alt)
                if self.media_mode == "authoritative" and figure_match:
                    number = int(figure_match.group(1))
                    caption_start = _next_nonblank(lines, position + 1)
                    caption_lines, caption_end = _paragraph_at(lines, caption_start)
                    caption_reference = _media_caption_reference(
                        caption_lines[0] if caption_lines else ""
                    )
                    if caption_reference == ("figure", number):
                        caption = _caption_text(caption_lines)
                        self.media_items.append(
                            self._render_authoritative_figure(
                                image_match,
                                caption,
                                number,
                            )
                        )
                        rendered.append(self._media_placeholder("figure", number))
                        position = caption_end
                        continue
                block_id = self._next_block()
                rendered.append(self._render_image(image_match, block_id, as_figure=True))
                position += 1
                continue

            caption_reference = _media_caption_reference(line)
            if caption_reference:
                media_kind, number = caption_reference
                caption_lines, caption_end = _paragraph_at(lines, position)
                caption = _caption_text(caption_lines)
                if media_kind == "figure" and self.media_mode == "reference_translation":
                    rendered.append(self._media_placeholder(media_kind, number))
                    position = caption_end
                    continue
                if media_kind == "table":
                    table_start = _next_nonblank(lines, caption_end)
                    table = _parse_pipe_table(lines, table_start)
                    if table is not None and self.media_mode in {
                        "authoritative",
                        "reference_translation",
                    }:
                        if self.media_mode == "authoritative":
                            self.media_items.append(
                                self._render_authoritative_table(
                                    table,
                                    caption,
                                    number,
                                )
                            )
                        rendered.append(self._media_placeholder(media_kind, number))
                        position = table.end_position
                        continue

            table = _parse_pipe_table(lines, position)
            if table is not None:
                rendered.append(self._render_inline_table(table))
                position = table.end_position
                continue

            unordered_match = UNORDERED_LIST_PATTERN.match(line)
            ordered_match = ORDERED_LIST_PATTERN.match(line)
            if unordered_match or ordered_match:
                ordered = ordered_match is not None
                tag = "ol" if ordered else "ul"
                start_attribute = (
                    f' start="{_escape(ordered_match.group(1))}"'
                    if ordered_match is not None and ordered_match.group(1) != "1"
                    else ""
                )
                items: list[str] = []
                while position < len(lines):
                    item_match = (
                        ORDERED_LIST_PATTERN.match(lines[position])
                        if ordered
                        else UNORDERED_LIST_PATTERN.match(lines[position])
                    )
                    if item_match is None:
                        break
                    item_text = item_match.group(2) if ordered else item_match.group(1)
                    block_id = self._next_block()
                    items.append(
                        f'<li{self._source_attributes(block_id, "list-item")}>'
                        f"{self._render_inline(item_text, block_id)}</li>"
                    )
                    position += 1
                rendered.append(
                    f'<{tag} class="source-list" data-section-id="{_escape(self.current_section_id)}"'
                    f"{start_attribute}>" + "".join(items) + f"</{tag}>"
                )
                continue

            paragraph_lines = [line.strip()]
            position += 1
            while position < len(lines) and lines[position].strip():
                candidate = lines[position]
                if (
                    HEADING_PATTERN.match(candidate)
                    or FENCE_PATTERN.match(candidate)
                    or UNORDERED_LIST_PATTERN.match(candidate)
                    or ORDERED_LIST_PATTERN.match(candidate)
                    or IMAGE_PATTERN.fullmatch(candidate.strip())
                    or PIPE_TABLE_ROW_PATTERN.match(candidate)
                ):
                    break
                paragraph_lines.append(candidate.strip())
                position += 1
            paragraph_text = " ".join(paragraph_lines)
            block_id = self._next_block()
            rendered.append(
                f'<p{self._source_attributes(block_id, "paragraph")}>'
                f"{self._render_inline(paragraph_text, block_id)}</p>"
            )

        return "\n".join(rendered)


def render_reading_html(
    markdown_text: str,
    concept_index: Mapping[str, Mapping[str, Any]],
    *,
    source_label: str,
    title: str,
    javascript: str,
    stylesheet: str,
    source_directory: Path | None = None,
    reference_translation_text: str | None = None,
    reference_translation_directory: Path | None = None,
) -> str:
    """Render one source into a self-contained Reading Workspace page."""

    source_sections = _split_markdown_sections(markdown_text)
    translation_sections = (
        _split_markdown_sections(reference_translation_text)
        if reference_translation_text is not None
        else []
    )
    renderer = _MarkdownRenderer(
        concept_index,
        source_directory=source_directory,
        source_origin="authoritative_source",
        media_mode="authoritative",
    )
    translation_renderer: _MarkdownRenderer | None = None
    if reference_translation_text is not None:
        translation_renderer = _MarkdownRenderer(
            concept_index,
            source_directory=reference_translation_directory,
            namespace="translation-",
            source_origin="reference_translation",
            media_mode="reference_translation",
        )

    reference_rows: list[str] = []
    for index, (source_section, translation_section) in enumerate(
        zip_longest(source_sections, translation_sections),
        start=1,
    ):
        row_classes = ["reference-section-row"]
        if source_section is None or (
            translation_renderer is not None and translation_section is None
        ):
            row_classes.append("is-unpaired")

        if source_section is None:
            rendered_source_section = (
                '<p class="unmatched-section-note">此中文小节没有可安全配对的英文小节。</p>'
            )
            source_locator = "not_available"
        else:
            source_locator = source_section.locator
            rendered_source_section = renderer.render(
                source_section.markdown_text,
                canonical_locator=source_locator,
            )

        english_cell = (
            '<section class="reference-section-cell english-reference-pane" '
            'data-reference-pane="english" data-source-origin="authoritative_source" '
            f'data-canonical-locator="{_escape(source_locator)}" '
            f'aria-label="英文原文小节 {index}">'
            f'<article class="reading-surface">{rendered_source_section}</article>'
            "</section>"
        )

        translation_cell = ""
        if translation_renderer is not None:
            if translation_section is None:
                rendered_translation_section = (
                    '<p class="unmatched-section-note">此英文小节没有对应的中文参考译文。</p>'
                )
            else:
                canonical_locator = (
                    source_section.locator
                    if source_section is not None
                    else "not_available"
                )
                rendered_translation_section = translation_renderer.render(
                    translation_section.markdown_text,
                    canonical_locator=canonical_locator,
                )
            translation_cell = (
                '<section class="reference-section-cell translation-reference-pane" '
                'data-reference-pane="translation" data-source-origin="reference_translation" '
                f'data-canonical-locator="{_escape(source_locator)}" '
                f'aria-label="中文参考译文小节 {index}">'
                '<article class="reading-surface translation-reading-surface">'
                f"{rendered_translation_section}</article></section>"
            )

        reference_rows.append(
            f'<div class="{" ".join(row_classes)}" data-reference-section-row="{index}">'
            f"{english_cell}{translation_cell}</div>"
        )

    alignment_warning = ""
    if translation_renderer is not None:
        source_levels = [section.level for section in source_sections]
        translation_levels = [section.level for section in translation_sections]
        if (
            len(source_sections) != len(translation_sections)
            or source_levels != translation_levels
        ):
            alignment_warning = (
                '<p class="reference-alignment-warning" id="reference-alignment-warning" '
                'role="status">小节对齐警告：'
                f"英文 {len(source_sections)} 节，中文 {len(translation_sections)} 节；"
                "未配对小节已保留，未静默丢弃正文。</p>"
            )
    bootstrap = {
        "format_version": SESSION_FORMAT,
        "source_label": source_label,
        "session_id": f"{SESSION_FORMAT}:{source_label}",
        "author_by_entry_type": {
            "source_excerpt": "source",
            "human_note": "human",
            "human_question": "human",
            "llm_answer": "llm",
        },
        "defaults": {
            "source_excerpt": {
                "confidence": "not_assessed",
                "verification": "not_applicable",
            },
            "human_note": {
                "confidence": "not_assessed",
                "verification": "not_applicable",
            },
            "human_question": {
                "confidence": "not_assessed",
                "verification": "not_applicable",
            },
            "llm_answer": {
                "confidence": "not_assessed",
                "verification": "unverified",
            },
        },
        "initial_preferences": {
            "density": "all",
            "highlights_enabled": True,
            "muted_concepts": [],
            "muted_terms": [],
        },
    }
    if translation_renderer is None:
        hit_status = (
            f"{renderer.hit_number} 处命中 · {len(renderer.concepts_seen)} 个概念 · "
            "仅使用本地索引"
        )
    else:
        hit_status = (
            f"英文 {renderer.hit_number} 处 / 中文 {translation_renderer.hit_number} 处命中 · "
            "仅使用本地索引"
        )
    bootstrap_json = _safe_json_for_script(bootstrap)
    reference_mode = "english" if translation_renderer is None else "bilingual"
    if translation_renderer is None:
        reference_controls = ""
        language_resizer = """<div class="workspace-resizer language-resizer" id="language-resizer" data-resizer="language" role="separator" tabindex="0" aria-orientation="vertical" aria-label="调整英文与中文栏宽度" aria-controls="reading-surface" aria-valuemin="20" aria-valuemax="80" aria-valuenow="50" hidden></div>"""
    else:
        reference_controls = """<section class="reference-controls" aria-label="参考译文显示控制">
      <label>阅读模式
        <select id="reference-mode" aria-label="阅读模式">
          <option value="english">英文原文</option>
          <option value="bilingual" selected>中英并列</option>
          <option value="translation">中文参考</option>
        </select>
      </label>
      <p class="translation-boundary"><strong>中文参考译文 / 机器或 LLM 辅助 / 未核验</strong> · 英文转录与 PDF 为权威；中文选区只可创建个人笔记或问题。</p>
    </section>"""
        language_resizer = """<div class="workspace-resizer language-resizer" id="language-resizer" data-resizer="language" role="separator" tabindex="0" aria-orientation="vertical" aria-label="调整英文与中文栏宽度" aria-controls="reading-surface" aria-valuemin="20" aria-valuemax="80" aria-valuenow="50"></div>"""
    reading_markup = f"""<div class="reference-surfaces reference-mode-{reference_mode}" data-reference-surfaces data-reference-mode="{reference_mode}">
      {alignment_warning}
      {language_resizer}
      <div class="reference-section-rows" id="reading-surface">
        {''.join(reference_rows)}
      </div>
    </div>"""
    figures_markup = "".join(renderer.media_items) or (
        '<p class="empty-state">当前权威来源没有可提取的图表。</p>'
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{_escape(title)} · 离线阅读工作区</title>
<style>
{stylesheet}
</style>
</head>
<body>
<header class="workspace-header">
  <div>
    <p class="eyebrow">Personal Research OS · RW-02.2</p>
    <h1>{_escape(title)}</h1>
    <p class="source-meta">{_escape(source_label)} · {hit_status}</p>
  </div>
  <div class="save-state" id="save-state" data-state="idle" aria-live="polite">尚无本地草稿</div>
</header>
<nav class="workspace-controls" aria-label="阅读工作区控制">
  <label>高亮密度
    <select id="density-control">
      <option value="all">全部出现</option>
      <option value="paragraph">每段首次</option>
      <option value="section">每节首次</option>
    </select>
  </label>
  <label>会话栏宽度
    <select id="session-panel-width" aria-label="会话栏宽度">
      <option value="compact">紧凑 / Compact · 34rem</option>
      <option value="balanced" selected>平衡 / Balanced · 42rem</option>
      <option value="wide">宽屏 / Wide · 50rem</option>
      <option value="custom" disabled>自定义 / Custom</option>
    </select>
  </label>
  <label class="checkbox-control"><input id="highlight-toggle" type="checkbox" checked> 显示概念高亮</label>
  <button type="button" id="restore-muted">恢复静音项</button>
  <button type="button" id="reset-layout">重置栏宽</button>
  <button type="button" id="export-session">导出会话 Markdown</button>
  <label class="file-control">导入会话 Markdown<input id="import-session" type="file" accept=".md,text/markdown,text/plain"></label>
</nav>
<main class="workspace-shell">
  <section class="reader-pane" aria-label="技术资料阅读区">
    <section class="recovery-banner" id="recovery-banner" hidden aria-live="polite">
      <div><strong>发现可恢复的本地草稿</strong><p id="recovery-summary"></p></div>
      <div class="button-row"><button type="button" id="recover-draft">恢复草稿</button><button type="button" id="discard-draft" class="danger">清除草稿</button></div>
    </section>
    <div class="message-surface" id="message-surface" role="status" aria-live="polite"></div>
    <p class="annotation-location-status" id="annotation-location-status" role="status" aria-live="polite" hidden></p>
    <section class="selection-tools" id="selection-tools" hidden>
      <div><span class="selection-label">已选择：</span><span id="selection-preview"></span></div>
      <p class="selection-origin-note" id="selection-origin-note"></p>
      <div class="button-row">
        <button type="button" id="selection-source-excerpt" data-create-entry="source_excerpt">保存摘录</button>
        <button type="button" data-create-entry="human_note">添加个人笔记</button>
        <button type="button" data-create-entry="human_question">提出问题</button>
      </div>
    </section>
    {reference_controls}
    {reading_markup}
    <p class="subset-note">RW-02.2 渲染标题、段落、扁平列表、链接、行内代码、围栏代码块、安全的本地 PNG/JPEG/WebP 图片和最小安全 GFM 管道表格。其他 Markdown 语法会作为安全文本显示；不执行原始 HTML。中文面板（如有）仅为未核验的参考译文。</p>
  </section>
  <div class="workspace-resizer content-figures-resizer" id="content-figures-resizer" data-resizer="figures" role="separator" tabindex="0" aria-orientation="vertical" aria-label="调整正文区域与图表栏宽度" aria-controls="reading-surface figures-panel" aria-valuemin="18" aria-valuemax="60" aria-valuenow="28"></div>
  <aside class="figures-panel" id="figures-panel" aria-label="权威英文图表栏">
    <header class="panel-header">
      <div><p class="eyebrow">权威英文来源</p><h2>图与表</h2></div>
    </header>
    <p class="figures-boundary">Figure 1–7 与 Table 1–2 来自英文权威转录；图片视觉细节仍以本地 PDF 为准。</p>
    <div class="figures-surface reading-surface" id="figures-surface">{figures_markup}</div>
  </aside>
  <div class="workspace-resizer figures-session-resizer" id="figures-session-resizer" data-resizer="session" role="separator" tabindex="0" aria-orientation="vertical" aria-label="调整图表栏与会话栏宽度" aria-controls="figures-panel session-panel" aria-valuemin="24" aria-valuemax="60" aria-valuenow="42"></div>
  <aside class="session-panel" id="session-panel" aria-label="阅读会话条目">
    <header class="panel-header">
      <div><p class="eyebrow">结构化会话</p><h2>阅读条目 <span id="entry-count">0</span></h2></div>
      <button type="button" id="add-llm-answer">粘贴 LLM 回答</button>
    </header>
    <div class="muted-summary" id="muted-summary" hidden></div>
    <nav class="session-tabs" role="tablist" aria-label="会话条目视图">
      <button type="button" id="session-tab-excerpts" role="tab" data-session-tab="excerpts" aria-selected="false" aria-controls="session-list" tabindex="-1">摘录 <span class="tab-count" data-tab-count="excerpts">0</span></button>
      <button type="button" id="session-tab-notes" role="tab" data-session-tab="notes" aria-selected="false" aria-controls="session-list" tabindex="-1">笔记 <span class="tab-count" data-tab-count="notes">0</span></button>
      <button type="button" id="session-tab-qa" role="tab" data-session-tab="qa" aria-selected="false" aria-controls="session-list" tabindex="-1">问答 <span class="tab-count" data-tab-count="qa">0</span></button>
      <button type="button" id="session-tab-all" role="tab" data-session-tab="all" aria-selected="true" aria-controls="session-list">全部 <span class="tab-count" data-tab-count="all">0</span></button>
    </nav>
    <div class="session-list" id="session-list" role="tabpanel" aria-labelledby="session-tab-all"><p class="empty-state">选择正文后创建摘录、笔记或问题。</p></div>
    <button type="button" id="clear-recovery" class="text-button danger">清除本地恢复数据</button>
  </aside>
</main>

<dialog id="entry-dialog">
  <form method="dialog" id="entry-form">
    <header><div><p class="eyebrow" id="entry-dialog-type"></p><h2 id="entry-dialog-title">创建条目</h2></div><button type="button" class="icon-button" data-close-dialog="entry-dialog" aria-label="关闭">×</button></header>
    <p>来源：<span class="origin-badge" id="entry-origin"></span></p>
    <label>来源定位<input id="entry-locator" type="text" required></label>
    <label>选中文本<textarea id="entry-selected-text" rows="3" readonly></textarea></label>
    <label>条目内容<textarea id="entry-content" rows="7" required></textarea></label>
    <div class="dialog-actions"><button type="button" data-close-dialog="entry-dialog">取消</button><button type="submit" class="primary">保存条目</button></div>
  </form>
</dialog>

<dialog id="answer-dialog">
  <form method="dialog" id="answer-form">
    <header><div><p class="eyebrow">手动外部 LLM 工作流</p><h2>粘贴并链接回答</h2></div><button type="button" class="icon-button" data-close-dialog="answer-dialog" aria-label="关闭">×</button></header>
    <p>来源：<span class="origin-badge">llm</span> · 默认未验证</p>
    <label>对应的人类问题<select id="answer-question" required></select></label>
    <label>模型标签（可选）<input id="answer-model-label" type="text"></label>
    <label>外部 LLM 回答<textarea id="answer-content" rows="9" required></textarea></label>
    <div class="dialog-actions"><button type="button" data-close-dialog="answer-dialog">取消</button><button type="submit" class="primary">保存回答</button></div>
  </form>
</dialog>

<dialog id="packet-dialog">
  <form method="dialog">
    <header><div><p class="eyebrow">仅手动复制</p><h2>外部 LLM 问题包</h2></div><button type="button" class="icon-button" data-close-dialog="packet-dialog" aria-label="关闭">×</button></header>
    <p>工作区不会发送、打开或自动处理此内容。</p>
    <textarea id="packet-content" rows="14" readonly></textarea>
    <div class="dialog-actions"><button type="button" data-close-dialog="packet-dialog">关闭</button><button type="button" id="copy-packet" class="primary">复制问题包</button></div>
  </form>
</dialog>

<script id="rw-bootstrap" type="application/json">{bootstrap_json}</script>
<script>
{javascript}
</script>
</body>
</html>
"""


def generate_reading_workspace(
    markdown_path: str | Path,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    *,
    index_path: str | Path = DEFAULT_INDEX_PATH,
    reference_translation: str | Path | None = None,
) -> Path:
    """Generate one self-contained offline Reading Workspace page."""

    source_path = Path(markdown_path)
    destination = Path(output_path)
    markdown_text = source_path.read_text(encoding="utf-8-sig")
    translation_path = Path(reference_translation) if reference_translation is not None else None
    translation_text = (
        translation_path.read_text(encoding="utf-8-sig")
        if translation_path is not None
        else None
    )
    concept_index = load_concept_index(index_path)
    javascript = JAVASCRIPT_PATH.read_text(encoding="utf-8")
    stylesheet = STYLESHEET_PATH.read_text(encoding="utf-8")
    source_label = _source_label(source_path)
    rendered = render_reading_html(
        markdown_text,
        concept_index,
        source_label=source_label,
        title=_document_title(markdown_text, source_path.stem),
        javascript=javascript,
        stylesheet=stylesheet,
        source_directory=source_path.parent,
        reference_translation_text=translation_text,
        reference_translation_directory=(
            translation_path.parent if translation_path is not None else None
        ),
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(rendered)
    return destination


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="为一篇 UTF-8 Markdown 资料生成自包含的离线阅读工作区。",
        add_help=False,
    )
    parser._positionals.title = "位置参数"
    parser._optionals.title = "选项"
    parser.add_argument("-h", "--help", action="help", help="显示此帮助信息并退出")
    parser.add_argument("markdown_file", type=Path, help="一篇 UTF-8 Markdown 技术资料")
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX_PATH,
        help="本地 Concept 索引路径",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="自包含 HTML 输出路径",
    )
    parser.add_argument(
        "--reference-translation",
        type=Path,
        default=None,
        help="可选的派生参考译文 Markdown 路径；启用中英并列显示",
    )
    parser.add_argument("--open", action="store_true", help="生成后在默认浏览器中打开")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        output_path = generate_reading_workspace(
            args.markdown_file,
            args.output,
            index_path=args.index,
            reference_translation=args.reference_translation,
        )
    except (OSError, HoverIndexError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    resolved_output = output_path.resolve()
    print(f"已生成离线阅读工作区：{resolved_output}")
    if args.open and not webbrowser.open(resolved_output.as_uri()):
        print("无法自动打开浏览器，请手动打开生成的 HTML 文件。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

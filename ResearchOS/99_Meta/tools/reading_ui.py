"""Generate a self-contained offline Reading Workspace for one Markdown source.

The renderer intentionally supports only the RW-01 subset: headings,
paragraphs, flat ordered and unordered lists, links, inline code, and fenced
code blocks. Unsupported Markdown remains visible as escaped text. Raw HTML is
never executed.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import tempfile
import webbrowser
from pathlib import Path
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
FENCE_PATTERN = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([^`]*)$")
UNORDERED_LIST_PATTERN = re.compile(r"^\s{0,3}[-+*]\s+(.+)$")
ORDERED_LIST_PATTERN = re.compile(r"^\s{0,3}(\d+)[.)]\s+(.+)$")
LINK_PATTERN = re.compile(
    r"\[([^\]\n]+)\]\(\s*(<[^>\n]+>|[^\s)\n]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"
)
CJK_PATTERN = re.compile(r"[\u3400-\u9fff]")
ALLOWED_LINK_SCHEMES = {"", "file", "http", "https", "mailto"}


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


class _MarkdownRenderer:
    def __init__(
        self,
        concept_index: Mapping[str, Mapping[str, Any]],
    ) -> None:
        self.concept_index = concept_index
        self.block_number = 0
        self.section_number = 0
        self.hit_number = 0
        self.current_section_id = "section-000"
        self.current_locator = "文档开头"
        self.concepts_seen: set[str] = set()

    def _next_block(self) -> str:
        self.block_number += 1
        return f"block-{self.block_number:04d}"

    def _next_section(self, locator: str) -> str:
        self.section_number += 1
        self.current_section_id = f"section-{self.section_number:03d}"
        self.current_locator = locator
        return self.current_section_id

    def _source_attributes(self, block_id: str, kind: str) -> str:
        return (
            f' data-source-block="true" data-block-id="{_escape(block_id)}"'
            f' data-section-id="{_escape(self.current_section_id)}"'
            f' data-source-kind="{_escape(kind)}"'
            f' data-locator="{_escape(self.current_locator)}"'
        )

    def _concept_hit(
        self,
        match: Mapping[str, Any],
        block_id: str,
    ) -> str:
        self.hit_number += 1
        concept = str(match["concept"])
        self.concepts_seen.add(concept)
        card_id = f"rw-concept-card-{self.hit_number:05d}"
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
            link_match = LINK_PATTERN.search(value, cursor) if allow_links else None
            link_position = link_match.start() if link_match else -1
            positions = [position for position in (code_position, link_position) if position >= 0]
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

    def render(self, markdown_text: str) -> str:
        lines = markdown_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        rendered: list[str] = []
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
                self._next_section(locator)
                block_id = self._next_block()
                rendered.append(
                    f"<h{level}{self._source_attributes(block_id, 'heading')}>"
                    f"{self._render_inline(heading_text, block_id)}</h{level}>"
                )
                position += 1
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
) -> str:
    """Render one source into a self-contained Reading Workspace page."""

    renderer = _MarkdownRenderer(concept_index)
    rendered_source = renderer.render(markdown_text)
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
    hit_status = (
        f"{renderer.hit_number} 处命中 · {len(renderer.concepts_seen)} 个概念 · "
        "仅使用本地索引"
    )
    bootstrap_json = _safe_json_for_script(bootstrap)
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
    <p class="eyebrow">Personal Research OS · RW-01</p>
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
    </select>
  </label>
  <label class="checkbox-control"><input id="highlight-toggle" type="checkbox" checked> 显示概念高亮</label>
  <button type="button" id="restore-muted">恢复静音项</button>
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
    <section class="selection-tools" id="selection-tools" hidden>
      <div><span class="selection-label">已选择：</span><span id="selection-preview"></span></div>
      <div class="button-row">
        <button type="button" data-create-entry="source_excerpt">保存摘录</button>
        <button type="button" data-create-entry="human_note">添加个人笔记</button>
        <button type="button" data-create-entry="human_question">提出问题</button>
      </div>
    </section>
    <article class="reading-surface" id="reading-surface">{rendered_source}</article>
    <p class="subset-note">RW-01 仅渲染标题、段落、扁平列表、链接、行内代码和围栏代码块。其他 Markdown 语法会作为安全文本显示；不执行原始 HTML。</p>
  </section>
  <aside class="session-panel" aria-label="阅读会话条目">
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
) -> Path:
    """Generate one self-contained offline Reading Workspace page."""

    source_path = Path(markdown_path)
    destination = Path(output_path)
    markdown_text = source_path.read_text(encoding="utf-8-sig")
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
    parser.add_argument("--open", action="store_true", help="生成后在默认浏览器中打开")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        output_path = generate_reading_workspace(
            args.markdown_file,
            args.output,
            index_path=args.index,
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

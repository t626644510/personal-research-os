from __future__ import annotations

import base64
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "ResearchOS" / "99_Meta" / "tools"
NOTES_DIR = REPO_ROOT / "ResearchOS" / "00_Inbox" / "notes"
READING_JAVASCRIPT_PATH = TOOLS_DIR / "reading_ui.js"
REAL_READING_ROOT = (
    REPO_ROOT / "ResearchOS" / "00_Inbox" / "reading" / "ipac2019-weprb066"
)
REAL_SOURCE_PATH = REAL_READING_ROOT / "_local" / "source.reading.md"
REAL_TRANSLATION_PATH = REAL_READING_ROOT / "_local" / "source.zh-CN.reading.md"
REAL_SESSION_PATH = REAL_READING_ROOT / "_local" / "reading_session.md"
NODE_EXECUTABLE = shutil.which("node")
sys.path.insert(0, str(TOOLS_DIR))

from hover_ui import generate_hover_demo  # noqa: E402
from reading_ui import generate_reading_workspace, main  # noqa: E402


SYNTHETIC_INDEX = {
    "HOM impedance": {
        "id": "hom_impedance",
        "path": "01_Concept/HOM impedance.md",
        "aliases": ["HOM", "高次模阻抗"],
        "category": ["RF engineering"],
        "hover_summary": "用于本地提示的紧凑<摘要>。",
        "related_concepts": ["Wakefield"],
    },
    "Wakefield": {
        "id": "wakefield",
        "path": "01_Concept/Wakefield.md",
        "aliases": ["wake field", "尾场"],
        "category": ["accelerator physics"],
        "hover_summary": "束团经过后留下的电磁场。",
        "related_concepts": [],
    },
}

ONE_PIXEL_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class SourceBlockCollector(HTMLParser):
    """Collect visible source-block text without tooltip-only descendants."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict[str, str]] = []
        self.current: dict[str, object] | None = None
        self.root_tag = ""
        self.hidden_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        if self.current is None and attributes.get("data-source-block") == "true":
            self.current = {
                "block_id": attributes.get("data-block-id", ""),
                "source_origin": attributes.get("data-source-origin", ""),
                "source_locator": attributes.get("data-locator", ""),
                "text": [],
            }
            self.root_tag = tag
            return
        if self.current is None:
            return
        classes = set(attributes.get("class", "").split())
        if self.hidden_depth:
            self.hidden_depth += 1
        elif attributes.get("role") == "tooltip" or "hover-card" in classes or "annotation-badge" in classes:
            self.hidden_depth = 1

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return
        if self.hidden_depth:
            self.hidden_depth -= 1
            return
        if tag != self.root_tag:
            return
        text = "".join(self.current.pop("text"))
        block = {key: str(value) for key, value in self.current.items()}
        block["visible_text"] = text
        block["block_key"] = str(len(self.blocks))
        self.blocks.append(block)
        self.current = None
        self.root_tag = ""

    def handle_data(self, data: str) -> None:
        if self.current is not None and not self.hidden_depth:
            self.current["text"].append(data)


def write_index(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(SYNTHETIC_INDEX, handle, ensure_ascii=False)


class ReadingUITests(unittest.TestCase):
    def run_reading_workspace_model(self, body: str, payload: object) -> object:
        if NODE_EXECUTABLE is None:
            self.skipTest("Node.js is unavailable for the optional pure-model check")
        harness = (
            'const fs = require("fs");\n'
            "const model = require(process.argv[1]);\n"
            'const input = JSON.parse(fs.readFileSync(0, "utf8"));\n'
            f"{body}\n"
        )
        completed = subprocess.run(
            [NODE_EXECUTABLE, "-e", harness, str(READING_JAVASCRIPT_PATH)],
            input=json.dumps(payload, ensure_ascii=False),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    @staticmethod
    def presentation_entries() -> list[dict[str, str]]:
        return [
            {"entry_id": "excerpt-1", "entry_type": "source_excerpt"},
            {"entry_id": "question-1", "entry_type": "human_question"},
            {
                "entry_id": "answer-2a",
                "entry_type": "llm_answer",
                "question_entry_id": "question-2",
            },
            {"entry_id": "note-1", "entry_type": "human_note"},
            {"entry_id": "question-2", "entry_type": "human_question"},
            {
                "entry_id": "answer-1a",
                "entry_type": "llm_answer",
                "question_entry_id": "question-1",
            },
            {"entry_id": "question-3", "entry_type": "human_question"},
            {
                "entry_id": "answer-1b",
                "entry_type": "llm_answer",
                "question_entry_id": "question-1",
            },
        ]

    def generate(self, markdown: str) -> tuple[str, Path, Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        source_path = root / "technical source.md"
        index_path = root / "concept_index.json"
        output_path = root / "workspace.html"
        source_path.write_text(markdown, encoding="utf-8")
        write_index(index_path)
        generated = generate_reading_workspace(
            source_path,
            output_path,
            index_path=index_path,
        )
        return generated.read_text(encoding="utf-8"), source_path, output_path

    def generate_with_translation(
        self,
        markdown: str,
        translation: str,
    ) -> tuple[str, Path, Path, Path]:
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        root = Path(temporary_directory.name)
        source_path = root / "technical source.md"
        translation_path = root / "source.zh-CN.reading.md"
        index_path = root / "concept_index.json"
        output_path = root / "workspace.html"
        source_path.write_text(markdown, encoding="utf-8")
        translation_path.write_text(translation, encoding="utf-8")
        write_index(index_path)
        generated = generate_reading_workspace(
            source_path,
            output_path,
            index_path=index_path,
            reference_translation=translation_path,
        )
        return generated.read_text(encoding="utf-8"), source_path, translation_path, output_path

    def generate_real_pair(self) -> str:
        if not REAL_SOURCE_PATH.is_file() or not REAL_TRANSLATION_PATH.is_file():
            self.skipTest("RW-02 local real-source pair is unavailable")
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        output_path = Path(temporary_directory.name) / "real-workspace.html"
        generate_reading_workspace(
            REAL_SOURCE_PATH,
            output_path,
            reference_translation=REAL_TRANSLATION_PATH,
        )
        return output_path.read_text(encoding="utf-8")

    def real_session_payload(self) -> dict[str, object]:
        if not REAL_SESSION_PATH.is_file():
            self.skipTest("RW-02 local real session is unavailable")
        markdown = REAL_SESSION_PATH.read_text(encoding="utf-8")
        match = re.search(
            r"<!--[ \t]*rw-session-v0\.1[ \t]*-->[ \t]*\r?\n"
            r"[ \t]*```json[ \t]*\r?\n([\s\S]*?)\r?\n[ \t]*```",
            markdown,
        )
        self.assertIsNotNone(match)
        return json.loads(match.group(1))

    def test_cli_generates_and_opens_one_local_self_contained_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_path = root / "source.md"
            index_path = root / "concept_index.json"
            output_path = root / "workspace.html"
            source_path.write_text("# 标题\n\nHOM impedance\n", encoding="utf-8")
            write_index(index_path)

            with patch("reading_ui.webbrowser.open", return_value=True) as open_browser:
                with redirect_stdout(io.StringIO()) as stdout:
                    exit_code = main(
                        [
                            str(source_path),
                            "--index",
                            str(index_path),
                            "--output",
                            str(output_path),
                            "--open",
                        ]
                    )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.is_file())
            self.assertIn("已生成离线阅读工作区", stdout.getvalue())
            open_browser.assert_called_once_with(output_path.resolve().as_uri())

    def test_output_inlines_local_assets_without_remote_dependencies(self) -> None:
        page, source_path, _ = self.generate("# 本地页面\n\nHOM impedance\n")

        self.assertIn("<style>\n:root", page)
        self.assertIn('id="rw-bootstrap" type="application/json"', page)
        self.assertIn("window.ReadingWorkspace", page)
        self.assertIn(".workspace-shell", page)
        self.assertNotRegex(page, r"<script\s+[^>]*src=")
        self.assertNotRegex(page, r"<link\s+[^>]*rel=[\"']?stylesheet")
        self.assertNotIn("@import", page)
        self.assertNotIn("@font-face", page)
        self.assertNotIn("fetch(", page)
        self.assertNotIn("XMLHttpRequest", page)
        self.assertNotIn("sendBeacon", page)
        self.assertNotIn("WebSocket", page)
        self.assertNotIn(str(source_path.parent), page)
        self.assertNotIn('id="reference-mode"', page)
        self.assertNotIn('id="translation-reading-surface"', page)

    def test_local_images_embed_raster_data_uris_and_block_unsafe_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_directory = root / "source"
            assets_directory = source_directory / "assets"
            source_directory.mkdir()
            assets_directory.mkdir()
            (assets_directory / "safe.png").write_bytes(ONE_PIXEL_PNG)
            (assets_directory / "vector.svg").write_text(
                '<svg><script>alert("svg")</script></svg>',
                encoding="utf-8",
            )
            source_path = source_directory / "source.md"
            index_path = root / "concept_index.json"
            output_path = root / "workspace.html"
            source_path.write_text(
                "# Images\n\n"
                '![HOM impedance](assets/safe.png "Caption & <title>")\n\n'
                "![Remote](https://example.test/remote.png)\n\n"
                "![Absolute](C:/outside.png)\n\n"
                "![Traversal](../outside.png)\n\n"
                "![Missing](assets/missing.png)\n\n"
                "![SVG](assets/vector.svg)\n\n"
                '<script>alert("raw")</script>\n',
                encoding="utf-8",
            )
            write_index(index_path)
            generate_reading_workspace(source_path, output_path, index_path=index_path)
            page = output_path.read_text(encoding="utf-8")

        self.assertEqual(page.count('<figure class="source-figure'), 6)
        self.assertEqual(page.count("图片不可用："), 5)
        self.assertEqual(page.count('src="data:image/png;base64,'), 1)
        self.assertIn(base64.b64encode(ONE_PIXEL_PNG).decode("ascii"), page)
        self.assertIn('alt="HOM impedance"', page)
        self.assertIn('title="Caption &amp; &lt;title&gt;"', page)
        self.assertIn("图片路径不安全", page)
        self.assertIn("图片缺失", page)
        self.assertIn("图片格式不受支持", page)
        self.assertNotIn(str(root), page)
        self.assertNotIn("<svg", page)
        self.assertNotIn('data:image/svg', page)
        self.assertNotIn('<script>alert("raw")</script>', page)
        self.assertIn("&lt;script&gt;alert(\"raw\")&lt;/script&gt;", page)
        self.assertEqual(page.count('class="concept-hit"'), 0)

    def test_symlink_escaping_image_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_directory = root / "source"
            assets_directory = source_directory / "assets"
            source_directory.mkdir()
            assets_directory.mkdir()
            outside_path = root / "outside.png"
            outside_path.write_bytes(ONE_PIXEL_PNG)
            symlink_path = assets_directory / "escape.png"
            try:
                symlink_path.symlink_to(outside_path)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            source_path = source_directory / "source.md"
            index_path = root / "concept_index.json"
            output_path = root / "workspace.html"
            source_path.write_text("![Escaping](assets/escape.png)\n", encoding="utf-8")
            write_index(index_path)
            generate_reading_workspace(source_path, output_path, index_path=index_path)
            page = output_path.read_text(encoding="utf-8")

        self.assertIn("图片路径不安全", page)
        self.assertNotIn("data:image/png;base64", page)
        self.assertNotIn(str(outside_path), page)

    def test_optional_translation_supports_bilingual_rows_and_limited_chinese_entries(self) -> None:
        page, source_path, translation_path, _ = self.generate_with_translation(
            "# English source\n\nHOM impedance is discussed.\n",
            "# 中文参考\n\n高次模阻抗也在讨论。\n",
        )

        self.assertIn('id="reference-mode"', page)
        self.assertIn('<option value="english">英文原文</option>', page)
        self.assertIn('<option value="bilingual" selected>中英并列</option>', page)
        self.assertIn('<option value="translation">中文参考</option>', page)
        self.assertIn('id="reading-surface"', page)
        self.assertIn('class="reference-surfaces reference-mode-bilingual"', page)
        self.assertIn('data-reference-mode="bilingual"', page)
        self.assertEqual(page.count('data-reference-section-row="'), 1)
        self.assertIn('data-reference-pane="english"', page)
        self.assertIn('data-reference-pane="translation"', page)
        self.assertIn('data-source-origin="authoritative_source"', page)
        self.assertIn('data-source-origin="reference_translation"', page)
        self.assertIn('data-canonical-locator="English source"', page)
        self.assertIn("reference-mode-${normalized}", page)
        self.assertIn("中文参考译文 / 机器或 LLM 辅助 / 未核验", page)
        self.assertIn("中文参考", page)
        self.assertEqual(page.count('data-concept="HOM impedance"'), 2)

        english_blocks = set(
            re.findall(
                r'data-source-block="true" data-block-id="(block-\d{4})"',
                page,
            )
        )
        translation_blocks = set(
            re.findall(
                r'data-source-block="true" data-block-id="(translation-block-\d{4})"',
                page,
            )
        )
        self.assertTrue(english_blocks)
        self.assertTrue(translation_blocks)
        self.assertTrue(english_blocks.isdisjoint(translation_blocks))
        self.assertNotIn("clearTranslationSelection", page)
        self.assertIn("selectionRoots.forEach", page)
        self.assertIn('id="selection-source-excerpt"', page)
        self.assertIn('id="selection-origin-note"', page)
        self.assertIn('selected_text_origin: origin', page)
        self.assertIn('selected_block_id: startBlock.dataset.blockId', page)
        self.assertIn(
            'selected_text_origin: ReadingWorkspaceModel.selectedTextOrigin(question)',
            page,
        )
        self.assertIn("answer.selected_block_id = question.selected_block_id", page)
        self.assertIn("中文参考译文仅可创建个人笔记或问题", page)
        self.assertIn("excerptButton.hidden = isTranslation", page)
        self.assertIn(".reference-mode-english .reference-section-row", page)
        self.assertIn(".reference-mode-translation .reference-section-row", page)
        self.assertIn("@media (max-width: 50rem)", page)
        self.assertIn("overflow-x: hidden", page)
        self.assertIn("position: fixed", page)
        self.assertIn("max-height: calc(100vh - 1.5rem)", page)
        self.assertIn("overflow-wrap: anywhere", page)
        self.assertNotIn(str(translation_path), page)
        self.assertNotIn(translation_path.name, page)

        bootstrap_match = re.search(
            r'<script id="rw-bootstrap" type="application/json">(.*?)</script>',
            page,
            re.DOTALL,
        )
        self.assertIsNotNone(bootstrap_match)
        bootstrap = json.loads(bootstrap_match.group(1))
        self.assertNotIn("translation", bootstrap)
        self.assertNotIn("reference_mode", bootstrap)
        self.assertNotIn("presentation", bootstrap)
        self.assertEqual(bootstrap["source_label"], source_path.name)

        session_function_start = page.index("function sessionPayload")
        session_function_end = page.index("function assertObject", session_function_start)
        self.assertNotIn("translation", page[session_function_start:session_function_end])
        self.assertNotIn("<script src=", page)
        self.assertNotIn("<link rel=", page)
        self.assertNotIn("@import", page)
        self.assertNotIn("fetch(", page)
        self.assertNotIn("XMLHttpRequest", page)
        self.assertNotIn("WebSocket", page)
        self.assertNotIn("sendBeacon", page)
        page.encode("utf-8")

    def test_cli_accepts_reference_translation_option(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_path = root / "source.md"
            translation_path = root / "source.zh-CN.reading.md"
            index_path = root / "concept_index.json"
            output_path = root / "workspace.html"
            source_path.write_text("# English\n\nHOM impedance\n", encoding="utf-8")
            translation_path.write_text("# 中文\n\n高次模阻抗\n", encoding="utf-8")
            write_index(index_path)
            with redirect_stdout(io.StringIO()):
                exit_code = main(
                    [
                        str(source_path),
                        "--index",
                        str(index_path),
                        "--reference-translation",
                        str(translation_path),
                        "--output",
                        str(output_path),
                    ]
                )
            page = output_path.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertIn('id="reference-mode"', page)
        self.assertIn('data-reference-pane="translation"', page)

    def test_real_pair_has_18_aligned_rows_and_one_authoritative_media_rail(self) -> None:
        page = self.generate_real_pair()

        self.assertEqual(page.count('data-reference-section-row="'), 18)
        self.assertNotIn('id="reference-alignment-warning"', page)
        self.assertEqual(page.count('<img class="source-image"'), 7)
        self.assertEqual(page.count('<table class="source-table">'), 2)
        self.assertEqual(page.count('data-media-placeholder="'), 18)
        self.assertNotIn(str(REAL_READING_ROOT), page)
        self.assertEqual(
            re.findall(r'data-figure-item="((?:figure|table)-\d+)"', page),
            [
                "figure-1",
                "table-1",
                "figure-2",
                "figure-3",
                "figure-4",
                "figure-5",
                "table-2",
                "figure-6",
                "figure-7",
            ],
        )
        body_before_figures = page.split('<aside class="figures-panel"', 1)[0]
        self.assertNotIn('<img class="source-image"', body_before_figures)
        self.assertNotIn('<table class="source-table">', body_before_figures)
        figure_rail = page.split('<aside class="figures-panel"', 1)[1]
        self.assertIn('data-concept="R over Q"', figure_rail)
        source_block_ids = re.findall(
            r'data-source-block="true" data-block-id="([^"]+)"',
            page,
        )
        self.assertTrue(source_block_ids)
        self.assertEqual(len(source_block_ids), len(set(source_block_ids)))
        self.assertEqual(page.count('role="separator"'), 3)

    def test_missing_translation_section_warns_and_preserves_all_body_text(self) -> None:
        page, _, _, _ = self.generate_with_translation(
            "# One\n\nFirst body.\n\n## Two\n\nSecond body.\n",
            "# 一\n\n第一段。\n",
        )

        self.assertEqual(page.count('data-reference-section-row="'), 2)
        self.assertIn('id="reference-alignment-warning"', page)
        self.assertIn("未配对小节已保留", page)
        self.assertIn("First body.", page)
        self.assertIn("Second body.", page)
        self.assertIn("第一段。", page)
        self.assertIn("此英文小节没有对应的中文参考译文", page)

    def test_minimal_gfm_table_is_escaped_hover_enabled_and_not_duplicated(self) -> None:
        page, _, _, _ = self.generate_with_translation(
            "# Source\n\n**Table 1. Safe table**\n\n"
            "| Property | Value |\n| --- | ---: |\n"
            "| HOM impedance | <img src=x onerror=alert(1)> |\n",
            "# 参考\n\n**表 1（Table 1）。安全表**\n\n"
            "| 参数 | 值 |\n| --- | --- |\n| 高次模阻抗 | 不可信 HTML |\n",
        )

        self.assertEqual(page.count('<table class="source-table">'), 1)
        self.assertEqual(page.count('data-figure-item="table-1"'), 1)
        self.assertEqual(page.count('data-media-placeholder="table-1"'), 2)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", page)
        self.assertNotIn("<img src=x onerror=alert(1)>", page)
        self.assertIn('data-concept="HOM impedance"', page)

    def test_selection_provenance_validation_and_optional_field_snapshots(self) -> None:
        result = self.run_reading_workspace_model(
            """
const authoritativeExcerpt = {
  entry_id: "e1", entry_type: "source_excerpt",
  selected_text_origin: "authoritative_source", selected_block_id: "block-1",
};
const translatedNote = {
  entry_id: "n1", entry_type: "human_note",
  selected_text_origin: "reference_translation", selected_block_id: "translation-block-1",
};
const translatedQuestion = {
  entry_id: "q1", entry_type: "human_question",
  selected_text_origin: "reference_translation", selected_block_id: "translation-block-1",
};
const translatedAnswer = {
  entry_id: "a1", entry_type: "llm_answer",
  selected_text_origin: "reference_translation", selected_block_id: "translation-block-1",
};
function outcome(callback) {
  try { return { ok: true, value: callback() }; }
  catch (error) { return { ok: false, message: error.message }; }
}
process.stdout.write(JSON.stringify({
  authoritative_excerpt: outcome(() => model.validateSelectionFields(authoritativeExcerpt)),
  translated_note: outcome(() => model.validateSelectionFields(translatedNote)),
  translated_question: outcome(() => model.validateSelectionFields(translatedQuestion)),
  translated_answer: outcome(() => model.validateSelectionFields(translatedAnswer, translatedQuestion)),
  translated_excerpt: outcome(() => model.validateSelectionFields({
    entry_id: "bad-excerpt", entry_type: "source_excerpt",
    selected_text_origin: "reference_translation",
  })),
  invalid_origin: outcome(() => model.validateSelectionFields({
    entry_id: "bad-origin", entry_type: "human_note", selected_text_origin: "machine_guess",
  })),
  mismatched_answer: outcome(() => model.validateSelectionFields({
    entry_id: "bad-answer", entry_type: "llm_answer",
    selected_text_origin: "authoritative_source",
  }, translatedQuestion)),
  legacy_origin: model.selectedTextOrigin({ entry_type: "human_note" }),
  legacy_snapshot: model.selectionFieldSnapshot({ entry_type: "human_note" }),
  new_snapshot: model.selectionFieldSnapshot(translatedNote),
}));
""",
            {},
        )

        self.assertTrue(result["authoritative_excerpt"]["ok"])
        self.assertTrue(result["translated_note"]["ok"])
        self.assertTrue(result["translated_question"]["ok"])
        self.assertTrue(result["translated_answer"]["ok"])
        self.assertFalse(result["translated_excerpt"]["ok"])
        self.assertIn("不能创建 source_excerpt", result["translated_excerpt"]["message"])
        self.assertFalse(result["invalid_origin"]["ok"])
        self.assertFalse(result["mismatched_answer"]["ok"])
        self.assertIn("必须继承问题", result["mismatched_answer"]["message"])
        self.assertEqual(result["legacy_origin"], "authoritative_source")
        self.assertEqual(result["legacy_snapshot"], {})
        self.assertEqual(
            result["new_snapshot"],
            {
                "selected_text_origin": "reference_translation",
                "selected_block_id": "translation-block-1",
            },
        )

    def test_new_selection_fields_round_trip_without_backfilling_legacy_entries(self) -> None:
        payload = {
            "format_version": "rw-session-v0.1",
            "source_label": "source.md",
            "session_id": "rw-session-v0.1:source.md",
            "session_state": "active",
            "entries": [
                {
                    "entry_id": "legacy",
                    "entry_type": "human_note",
                    "selected_text": "old",
                },
                {
                    "entry_id": "translated",
                    "entry_type": "human_question",
                    "selected_text": "new",
                    "selected_text_origin": "reference_translation",
                    "selected_block_id": "translation-block-0002",
                },
            ],
            "preferences": {},
            "exported_at": "2026-08-11T00:00:00Z",
        }
        result = self.run_reading_workspace_model(
            """
const markdown = model.buildSessionMarkdownEnvelope(input.payload);
const reparsed = model.parseSessionMarkdownEnvelope(markdown);
process.stdout.write(JSON.stringify({
  reparsed,
  legacy_fields: model.selectionFieldSnapshot(reparsed.entries[0]),
  new_fields: model.selectionFieldSnapshot(reparsed.entries[1]),
}));
""",
            {"payload": payload},
        )

        self.assertEqual(result["reparsed"], payload)
        self.assertEqual(result["legacy_fields"], {})
        self.assertEqual(
            result["new_fields"],
            {
                "selected_text_origin": "reference_translation",
                "selected_block_id": "translation-block-0002",
            },
        )

    def test_real_legacy_session_locates_all_five_annotations_without_guessing(self) -> None:
        page = self.generate_real_pair()
        collector = SourceBlockCollector()
        collector.feed(page)
        payload = self.real_session_payload()
        self.assertEqual(len(payload["entries"]), 5)
        self.assertTrue(
            all(
                "selected_text_origin" not in entry and "selected_block_id" not in entry
                for entry in payload["entries"]
            )
        )

        result = self.run_reading_workspace_model(
            """
process.stdout.write(JSON.stringify(
  model.resolveBlockAnnotations(input.entries, input.blocks)
));
""",
            {"entries": payload["entries"], "blocks": collector.blocks},
        )

        self.assertEqual(result["unlocatedCount"], 0)
        self.assertEqual(len(result["blockCounts"]), 5)
        self.assertEqual(sum(result["blockCounts"].values()), 5)

    def test_stale_existing_block_id_falls_back_to_unique_locator_and_text(self) -> None:
        result = self.run_reading_workspace_model(
            """
const blocks = [
  { block_key: "wrong", block_id: "block-stale", source_origin: "authoritative_source", source_locator: "Wrong", visible_text: "unrelated text" },
  { block_key: "correct", block_id: "block-current", source_origin: "authoritative_source", source_locator: "Section 1", visible_text: "prefix selected passage suffix" },
  { block_key: "translation", block_id: "translation-block-current", source_origin: "reference_translation", source_locator: "Section 1", visible_text: "prefix selected passage suffix" },
];
const entries = [
  { entry_id: "note", entry_type: "human_note", source_locator: "Section 1", selected_text: "selected passage", selected_block_id: "block-stale" },
];
process.stdout.write(JSON.stringify(model.resolveBlockAnnotations(entries, blocks)));
""",
            {},
        )

        self.assertEqual(result, {"blockCounts": {"correct": 1}, "unlocatedCount": 0})

    def test_stale_existing_block_id_with_ambiguous_fallback_is_unlocated(self) -> None:
        result = self.run_reading_workspace_model(
            """
const blocks = [
  { block_key: "wrong", block_id: "block-stale", source_origin: "authoritative_source", source_locator: "Wrong", visible_text: "unrelated text" },
  { block_key: "candidate-1", block_id: "block-current-1", source_origin: "authoritative_source", source_locator: "Section 1", visible_text: "prefix selected passage suffix" },
  { block_key: "candidate-2", block_id: "block-current-2", source_origin: "authoritative_source", source_locator: "Section 1", visible_text: "another selected passage copy" },
];
const entries = [
  { entry_id: "note", entry_type: "human_note", source_locator: "Section 1", selected_text: "selected passage", selected_block_id: "block-stale" },
];
process.stdout.write(JSON.stringify(model.resolveBlockAnnotations(entries, blocks)));
""",
            {},
        )

        self.assertEqual(result, {"blockCounts": {}, "unlocatedCount": 1})

    def test_stale_existing_block_id_with_no_fallback_is_unlocated(self) -> None:
        result = self.run_reading_workspace_model(
            """
const blocks = [
  { block_key: "wrong", block_id: "block-stale", source_origin: "authoritative_source", source_locator: "Wrong", visible_text: "unrelated text" },
];
const entries = [
  { entry_id: "note", entry_type: "human_note", source_locator: "Section 1", selected_text: "selected passage", selected_block_id: "block-stale" },
];
process.stdout.write(JSON.stringify(model.resolveBlockAnnotations(entries, blocks)));
""",
            {},
        )

        self.assertEqual(result, {"blockCounts": {}, "unlocatedCount": 1})

    def test_verified_block_id_wins_when_locator_and_text_also_match(self) -> None:
        result = self.run_reading_workspace_model(
            """
const blocks = [
  { block_key: "correct", block_id: "block-current", source_origin: "authoritative_source", source_locator: "Section 1", visible_text: "prefix selected passage suffix" },
  { block_key: "duplicate", block_id: "block-other", source_origin: "authoritative_source", source_locator: "Section 1", visible_text: "another selected passage copy" },
];
const entries = [
  { entry_id: "note", entry_type: "human_note", source_locator: "Section 1", selected_text: "selected passage", selected_block_id: "block-current" },
];
process.stdout.write(JSON.stringify(model.resolveBlockAnnotations(entries, blocks)));
""",
            {},
        )

        self.assertEqual(result, {"blockCounts": {"correct": 1}, "unlocatedCount": 0})

    def test_annotation_resolution_handles_translation_delete_ambiguity_and_bad_ids(self) -> None:
        result = self.run_reading_workspace_model(
            """
const blocks = [
  { block_key: "en", block_id: "block-1", source_origin: "authoritative_source", source_locator: "One", visible_text: "same text" },
  { block_key: "en2", block_id: "block-2", source_origin: "authoritative_source", source_locator: "One", visible_text: "same text" },
  { block_key: "zh", block_id: "translation-block-1", source_origin: "reference_translation", source_locator: "One", visible_text: "中文选择" },
];
const entries = [
  { entry_id: "zh-note", entry_type: "human_note", source_locator: "One", selected_text: "中文选择", selected_text_origin: "reference_translation", selected_block_id: "translation-block-1" },
  { entry_id: "bad-id", entry_type: "human_note", source_locator: "One", selected_text: "same text", selected_block_id: "missing" },
  { entry_id: "ambiguous", entry_type: "human_question", source_locator: "One", selected_text: "same text" },
  { entry_id: "answer", entry_type: "llm_answer", source_locator: "One", selected_text: "same text" },
];
process.stdout.write(JSON.stringify({
  before: model.resolveBlockAnnotations(entries, blocks),
  after_delete: model.resolveBlockAnnotations([], blocks),
}));
""",
            {},
        )

        self.assertEqual(result["before"]["blockCounts"], {"zh": 1})
        self.assertEqual(result["before"]["unlocatedCount"], 2)
        self.assertEqual(result["after_delete"], {"blockCounts": {}, "unlocatedCount": 0})

    def test_presentation_layout_clamps_resizes_resets_and_stays_session_external(self) -> None:
        result = self.run_reading_workspace_model(
            """
const metrics = {
  rootFontPx: 16, workspaceWidthPx: 1920, bodyWidthPx: 760, separatorWidthPx: 8,
};
const base = model.clampPresentationLayout(model.defaultPresentationLayout, metrics);
const wide = model.clampPresentationLayout(model.defaultPresentationLayout, {
  rootFontPx: 16, workspaceWidthPx: 3840, bodyWidthPx: 2240, separatorWidthPx: 8,
});
const language = model.resizePresentationLayout(base, "language", 10000, metrics);
const session = model.resizePresentationLayout(base, "session", -160, metrics);
const reset = model.presentationLayoutForPreset(session, "balanced");
const invalid = model.normalizePresentationLayout({
  language_ratio: "bad", figures_width_rem: null, session_width_rem: Infinity,
  session_width_preset: "giant",
});
process.stdout.write(JSON.stringify({ base, wide, language, session, reset, invalid }));
""",
            {},
        )

        self.assertEqual(result["base"]["figures_width_rem"], 28)
        self.assertEqual(result["base"]["session_width_rem"], 42)
        self.assertEqual(result["wide"]["figures_width_rem"], 28)
        self.assertEqual(result["wide"]["session_width_rem"], 42)
        self.assertLess(result["language"]["language_ratio"], 1)
        self.assertGreater(result["language"]["language_ratio"], 0.5)
        self.assertEqual(result["session"]["session_width_preset"], "custom")
        self.assertEqual(result["reset"]["session_width_preset"], "balanced")
        self.assertEqual(result["reset"]["session_width_rem"], 42)
        self.assertEqual(result["invalid"], result["base"])

        page, _, _, _ = self.generate_with_translation(
            "# English\n\nBody.\n",
            "# 中文\n\n正文。\n",
        )
        for resizer_id in (
            "language-resizer",
            "content-figures-resizer",
            "figures-session-resizer",
        ):
            self.assertRegex(
                page,
                rf'id="{resizer_id}"[^>]*role="separator"[^>]*tabindex="0"[^>]*aria-orientation="vertical"',
            )
        self.assertIn("setPointerCapture", page)
        self.assertIn('addEventListener("keydown"', page)
        self.assertIn('addEventListener("dblclick"', page)
        self.assertIn('id="reset-layout"', page)
        self.assertIn(
            "personal-research-os:reading-workspace:presentation:v1",
            page,
        )
        layout_start = page.index("function setPresentationLayout")
        layout_end = page.index("function restorePresentationLayout", layout_start)
        layout_path = page[layout_start:layout_end]
        self.assertLess(
            layout_path.index("applyPresentationLayout(value)"),
            layout_path.index("persistPresentationLayout"),
        )
        session_start = page.index("function sessionPayload")
        session_end = page.index("function assertObject", session_start)
        session_path = page[session_start:session_end]
        for layout_field in (
            "language_ratio",
            "figures_width_rem",
            "session_width_rem",
            "presentationLayout",
        ):
            self.assertNotIn(layout_field, session_path)
        self.assertNotIn("width: min(100%, 100rem)", page)
        self.assertIn("grid-template-columns:", page)
        self.assertIn("@media (max-width: 50rem)", page)
        self.assertIn(".workspace-resizer {\n    display: none !important;", page)

    def test_renders_required_markdown_subset_and_escapes_raw_html(self) -> None:
        page, _, _ = self.generate(
            "# 标题\n\n"
            "普通段落与 `HOM`。\n\n"
            "- 无序项\n- 第二项\n\n"
            "3. 有序项\n4. 第二项\n\n"
            "```python\nHOM\n<script>alert('fence')</script>\n```\n\n"
            "<script>alert('raw')</script>\n"
        )

        self.assertIn('<h1 data-source-block="true"', page)
        self.assertIn('<p data-source-block="true"', page)
        self.assertIn('<ul class="source-list"', page)
        self.assertIn('<ol class="source-list"', page)
        self.assertIn('<code>HOM</code>', page)
        self.assertIn('<pre class="fenced-code"', page)
        self.assertIn("&lt;script&gt;alert('fence')&lt;/script&gt;", page)
        self.assertIn("&lt;script&gt;alert('raw')&lt;/script&gt;", page)
        self.assertNotIn("<script>alert('raw')</script>", page)
        self.assertNotIn("<script>alert('fence')</script>", page)

    def test_excludes_frontmatter_code_and_link_targets_from_highlights(self) -> None:
        page, _, _ = self.generate(
            "---\nterm: HOM\n---\n"
            "# Section\n\n"
            "HOM outside. `HOM` [HOM](notes/HOM-target.md)\n\n"
            "```text\nHOM\n```\n"
        )

        self.assertEqual(page.count('class="concept-hit"'), 2)
        frontmatter = re.search(r'<pre class="frontmatter".*?</pre>', page, re.DOTALL)
        fenced = re.search(r'<pre class="fenced-code".*?</pre>', page, re.DOTALL)
        self.assertIsNotNone(frontmatter)
        self.assertIsNotNone(fenced)
        self.assertNotIn("concept-hit", frontmatter.group(0))
        self.assertNotIn("concept-hit", fenced.group(0))
        self.assertIn("<code>HOM</code>", page)
        self.assertIn('href="notes/HOM-target.md"', page)
        self.assertRegex(page, r'<a href="notes/HOM-target\.md"[^>]*>.*concept-hit')

    def test_preserves_longest_alias_matching_and_chinese_card_content(self) -> None:
        page, _, _ = self.generate(
            "# 高次模阻抗\n\nHOM impedance、HOM、高次模阻抗与尾场。\n"
        )

        self.assertEqual(page.count('class="concept-hit"'), 5)
        self.assertIn('data-term-label="HOM impedance"', page)
        self.assertIn('<span class="concept-text">HOM impedance</span>', page)
        self.assertIn('<span class="card-title">高次模阻抗（HOM impedance）</span>', page)
        self.assertIn("用于本地提示的紧凑&lt;摘要&gt;。", page)
        self.assertIn('<span class="card-title">尾场（Wakefield）</span>', page)
        self.assertIn("束团经过后留下的电磁场。", page)

    def test_link_schemes_are_safely_allowed_or_neutralized(self) -> None:
        page, _, _ = self.generate(
            "# Links\n\n"
            "[安全](https://example.test/path) "
            "[相对](notes/local.md) "
            "[危险](javascript:alert(1))\n"
        )

        self.assertIn('href="https://example.test/path"', page)
        self.assertIn('href="notes/local.md"', page)
        self.assertIn('<span class="unsafe-link" title="已阻止不安全链接">危险</span>', page)
        self.assertNotIn('href="javascript:', page)

    def test_block_and_section_metadata_is_deterministic(self) -> None:
        markdown = "前言。\n\n# One\n\nFirst.\n\n## Two\n\n- Item\n"
        first, _, _ = self.generate(markdown)
        second, _, _ = self.generate(markdown)

        metadata_pattern = re.compile(
            r'data-block-id="block-\d{4}" data-section-id="section-\d{3}" '
            r'data-source-kind="[^"]+" data-locator="[^"]+"'
        )
        self.assertEqual(metadata_pattern.findall(first), metadata_pattern.findall(second))
        self.assertIn('data-block-id="block-0001" data-section-id="section-000"', first)
        self.assertIn('data-section-id="section-001" data-source-kind="heading" data-locator="One"', first)
        self.assertIn('data-section-id="section-002" data-source-kind="list-item" data-locator="Two"', first)

    def test_session_invariants_recovery_and_error_surfaces_are_embedded(self) -> None:
        page, _, _ = self.generate("# Session\n\nHOM\n")

        self.assertIn('"format_version":"rw-session-v0.1"', page)
        self.assertIn('"source_excerpt":"source"', page)
        self.assertIn('"human_note":"human"', page)
        self.assertIn('"human_question":"human"', page)
        self.assertIn('"llm_answer":"llm"', page)
        self.assertIn('id="save-state"', page)
        self.assertIn('id="recovery-banner"', page)
        self.assertIn('id="recover-draft"', page)
        self.assertIn('id="discard-draft"', page)
        self.assertIn('id="message-surface"', page)
        self.assertIn("localStorage.setItem", page)
        self.assertIn("author_type 与 entry_type 不匹配", page)
        self.assertIn("问题链接已保留", page)
        self.assertIn("buildSessionMarkdown", page)
        self.assertIn("importSessionMarkdown", page)
        self.assertIn('role="tablist"', page)
        self.assertIn('data-session-tab="excerpts"', page)
        self.assertIn('data-session-tab="notes"', page)
        self.assertIn('data-session-tab="qa"', page)
        self.assertIn('data-session-tab="all"', page)
        self.assertIn("尚无回答", page)

    def test_session_panel_width_presets_normalize_deterministically(self) -> None:
        result = self.run_reading_workspace_model(
            """
const accepted = ["compact", "balanced", "wide"];
const normalizedAccepted = Object.fromEntries(
  accepted.map((value) => [value, model.normalizeSessionPanelWidth(value)]),
);
const normalizedInvalid = [null, "", "giant", 42].map(
  (value) => model.normalizeSessionPanelWidth(value),
);
process.stdout.write(JSON.stringify({
  widths: model.sessionPanelWidths,
  default_value: model.defaultSessionPanelWidth,
  normalized_accepted: normalizedAccepted,
  normalized_invalid: normalizedInvalid,
}));
""",
            {},
        )

        self.assertEqual(
            result["widths"],
            {"compact": "34rem", "balanced": "42rem", "wide": "50rem"},
        )
        self.assertEqual(result["default_value"], "balanced")
        self.assertEqual(
            result["normalized_accepted"],
            {"compact": "compact", "balanced": "balanced", "wide": "wide"},
        )
        self.assertEqual(result["normalized_invalid"], ["balanced"] * 4)

    def test_generated_html_has_accessible_panel_width_selector(self) -> None:
        page, _, _ = self.generate("# Width selector\n\nHOM impedance\n")
        selector = re.search(
            r'<label>会话栏宽度\s*<select id="session-panel-width" '
            r'aria-label="会话栏宽度">(.*?)</select>\s*</label>',
            page,
            re.DOTALL,
        )
        self.assertIsNotNone(selector)
        options = selector.group(1)
        self.assertIn('<option value="compact">紧凑 / Compact · 34rem</option>', options)
        self.assertIn(
            '<option value="balanced" selected>平衡 / Balanced · 42rem</option>',
            options,
        )
        self.assertIn('<option value="wide">宽屏 / Wide · 50rem</option>', options)
        self.assertIn('<option value="custom" disabled>自定义 / Custom</option>', options)
        self.assertIn("--session-panel-width: 42rem", page)
        self.assertIn("minmax(24rem, var(--session-panel-width))", page)
        self.assertIn(
            "personal-research-os:reading-workspace:presentation:v1",
            page,
        )

    def test_session_tabs_preserve_canonical_entries_and_order(self) -> None:
        entries = self.presentation_entries()
        result = self.run_reading_workspace_model(
            """
const before = JSON.stringify(input.entries);
const tabs = {};
for (const tabName of ["excerpts", "notes", "qa", "all"]) {
  tabs[tabName] = model.entriesForTab(input.entries, tabName).map((entry) => entry.entry_id);
}
process.stdout.write(JSON.stringify({ tabs, unchanged: before === JSON.stringify(input.entries) }));
""",
            {"entries": entries},
        )

        self.assertTrue(result["unchanged"])
        self.assertEqual(result["tabs"]["excerpts"], ["excerpt-1"])
        self.assertEqual(result["tabs"]["notes"], ["note-1"])
        self.assertEqual(
            result["tabs"]["qa"],
            [
                "question-1",
                "answer-2a",
                "question-2",
                "answer-1a",
                "question-3",
                "answer-1b",
            ],
        )
        self.assertEqual(
            result["tabs"]["all"],
            [entry["entry_id"] for entry in entries],
        )

    def test_question_answer_groups_use_question_entry_id(self) -> None:
        result = self.run_reading_workspace_model(
            """
const before = JSON.stringify(input.entries);
const groups = model.groupQuestionAnswers(input.entries).map((group) => ({
  question_id: group.question.entry_id,
  answer_ids: group.answers.map((answer) => answer.entry_id),
}));
process.stdout.write(JSON.stringify({ groups, unchanged: before === JSON.stringify(input.entries) }));
""",
            {"entries": self.presentation_entries()},
        )

        self.assertTrue(result["unchanged"])
        self.assertEqual(
            result["groups"],
            [
                {"question_id": "question-1", "answer_ids": ["answer-1a", "answer-1b"]},
                {"question_id": "question-2", "answer_ids": ["answer-2a"]},
                {"question_id": "question-3", "answer_ids": []},
            ],
        )

    def test_rw_session_v01_export_import_remains_backward_compatible(self) -> None:
        payload = {
            "format_version": "rw-session-v0.1",
            "source_label": "00_Inbox/notes/legacy source.md",
            "session_id": "rw-session-v0.1:00_Inbox/notes/legacy source.md",
            "session_state": "active",
            "entries": [
                {
                    "entry_id": "legacy-question",
                    "entry_type": "human_question",
                    "created_at": "2026-08-04T10:00:00+08:00",
                    "author_type": "human",
                    "source_locator": "Section 2",
                    "selected_text": "Legacy selection",
                    "content": "Legacy question?",
                    "confidence": "medium",
                    "verification": "unverified",
                },
                {
                    "entry_id": "legacy-answer",
                    "entry_type": "llm_answer",
                    "created_at": "2026-08-04T10:01:00+08:00",
                    "author_type": "llm",
                    "source_locator": "Section 2",
                    "selected_text": "Legacy selection",
                    "content": "Legacy answer with ``` and 中文。",
                    "confidence": "not_assessed",
                    "verification": "unverified",
                    "question_entry_id": "legacy-question",
                },
            ],
            "preferences": {
                "density": "paragraph",
                "highlights_enabled": True,
                "muted_concepts": [],
                "muted_terms": ["HOM"],
            },
            "exported_at": "2026-08-04T10:02:00+08:00",
        }
        legacy_markdown = (
            "# Reading Workspace Session\n\n"
            "- Format: rw-session-v0.1\n"
            "- Source: 00_Inbox/notes/legacy source.md\n"
            "- Session state: active\n"
            "- Exported at: 2026-08-04T10:02:00+08:00\n\n"
            "The fenced JSON block is the authoritative lossless session payload.\n\n"
            "<!-- rw-session-v0.1 -->\n"
            "```json\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
            "```\n"
        )
        result = self.run_reading_workspace_model(
            """
const parsedLegacy = model.parseSessionMarkdownEnvelope(input.legacy_markdown);
const exported = model.buildSessionMarkdownEnvelope(parsedLegacy);
const reparsed = model.parseSessionMarkdownEnvelope(exported);
process.stdout.write(JSON.stringify({
  format_version: model.formatVersion,
  parsed_legacy: parsedLegacy,
  reparsed,
  exported,
}));
""",
            {"legacy_markdown": legacy_markdown},
        )

        self.assertEqual(result["format_version"], "rw-session-v0.1")
        self.assertEqual(result["parsed_legacy"], payload)
        self.assertEqual(result["reparsed"], payload)
        self.assertEqual(
            result["exported"].encode("utf-8"),
            legacy_markdown.encode("utf-8"),
        )
        self.assertEqual(
            [entry["entry_id"] for entry in result["reparsed"]["entries"]],
            ["legacy-question", "legacy-answer"],
        )
        self.assertNotIn("session_view", result["reparsed"])
        self.assertNotIn("source_text", result["reparsed"])
        self.assertNotIn("session_panel_width", result["reparsed"])
        self.assertNotIn("session_panel_width", result["exported"])
        self.assertNotIn("layout_width", result["exported"])

    def test_session_envelope_preserves_embedded_triple_backticks(self) -> None:
        page, _, _ = self.generate("# Session envelope\n\nHOM impedance\n")
        pattern_literal = re.search(
            r'^\s*const SESSION_ENVELOPE_PATTERN = ("(?:\\.|[^"\\])*");$',
            page,
            re.MULTILINE,
        )
        self.assertIsNotNone(pattern_literal)
        envelope_pattern = re.compile(
            json.loads(pattern_literal.group(1)),
            re.IGNORECASE | re.MULTILINE,
        )

        payload = {
            "format_version": "rw-session-v0.1",
            "source_label": "00_Inbox/notes/高次模阻抗.md",
            "session_id": "rw-session-v0.1:00_Inbox/notes/高次模阻抗.md",
            "session_state": "active",
            "entries": [
                {
                    "entry_id": "rw-entry-0001",
                    "entry_type": "source_excerpt",
                    "created_at": "2026-08-04T09:00:00+08:00",
                    "author_type": "source",
                    "source_locator": "第 1 节 / 引言",
                    "selected_text": "原文中的高次模阻抗。",
                    "content": "原文中的高次模阻抗。",
                    "confidence": "not_assessed",
                    "verification": "not_applicable",
                },
                {
                    "entry_id": "rw-entry-0002",
                    "entry_type": "human_note",
                    "created_at": "2026-08-04T09:01:00+08:00",
                    "author_type": "human",
                    "source_locator": "第 2 节 / 计算",
                    "selected_text": "选择的中文原文 ``` 不构成会话围栏。",
                    "content": (
                        "中文注释与 marker-like 文本：<!-- rw-session-v0.1 -->\n"
                        "```python\nprint('尾场')\n```\n"
                        "尾注 ```json 也不是会话边界。"
                    ),
                    "confidence": "high",
                    "verification": "human_checked",
                },
                {
                    "entry_id": "rw-entry-0003",
                    "entry_type": "human_question",
                    "created_at": "2026-08-04T09:02:00+08:00",
                    "author_type": "human",
                    "source_locator": "第 3 节 / 讨论",
                    "selected_text": "这个峰值如何核验？",
                    "content": "``` 是否会破坏会话 envelope？",
                    "confidence": "medium",
                    "verification": "unverified",
                },
                {
                    "entry_id": "rw-entry-0004",
                    "entry_type": "llm_answer",
                    "created_at": "2026-08-04T09:03:00+08:00",
                    "author_type": "llm",
                    "source_locator": "第 3 节 / 讨论",
                    "selected_text": "这个峰值如何核验？",
                    "content": "回答包含字面量 ```、```json 与中文：高次模阻抗。",
                    "confidence": "low",
                    "verification": "rejected",
                    "question_entry_id": "rw-entry-0003",
                    "model_label": "disposable-manual-answer",
                },
            ],
            "preferences": {
                "density": "section",
                "highlights_enabled": False,
                "muted_concepts": ["HOM impedance"],
                "muted_terms": ["高次模阻抗"],
            },
            "exported_at": "2026-08-04T09:04:00+08:00",
        }
        markdown = (
            "# Reading Workspace Session\n\n"
            "<!-- rw-session-v0.1 -->\n"
            "```json\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
            "```\n"
        )

        envelope = envelope_pattern.search(markdown)
        self.assertIsNotNone(envelope)
        restored = json.loads(envelope.group(1))
        self.assertEqual(restored, payload)
        self.assertEqual(
            [entry["entry_id"] for entry in restored["entries"]],
            ["rw-entry-0001", "rw-entry-0002", "rw-entry-0003", "rw-entry-0004"],
        )
        self.assertEqual(restored["entries"][3]["question_entry_id"], "rw-entry-0003")

        malformed = markdown.replace("\n```\n", "\n``` trailing text\n", 1)
        self.assertIsNone(envelope_pattern.search(malformed))

    def test_bootstrap_json_cannot_be_terminated_by_concept_metadata(self) -> None:
        malicious_index = json.loads(json.dumps(SYNTHETIC_INDEX))
        malicious_index["HOM impedance"]["hover_summary"] = "safe </script><script>alert(1)</script>"
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_path = root / "source.md"
            index_path = root / "index.json"
            output_path = root / "page.html"
            source_path.write_text("# Title\n\nHOM impedance\n", encoding="utf-8")
            index_path.write_text(json.dumps(malicious_index), encoding="utf-8")
            generate_reading_workspace(source_path, output_path, index_path=index_path)
            page = output_path.read_text(encoding="utf-8")

        self.assertNotIn("safe </script><script>alert(1)</script>", page)
        self.assertIn("safe &lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertEqual(page.count('<script id="rw-bootstrap"'), 1)

    def test_real_source_uses_real_index_and_keeps_old_hover_ui_working(self) -> None:
        source_path = NOTES_DIR / "HOM impedance reading note.md"
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            reading_output = root / "reading.html"
            hover_output = root / "hover.html"
            generate_reading_workspace(source_path, reading_output)
            _, hover_matches = generate_hover_demo(source_path, hover_output)
            page = reading_output.read_text(encoding="utf-8")

        self.assertIn("高次模阻抗阅读笔记 · 离线阅读工作区", page)
        self.assertIn('data-concept="HOM impedance"', page)
        self.assertIn('data-concept="Bunch spectrum"', page)
        self.assertIn("本地已保存", page)
        self.assertIn("HOM impedance", {match["concept"] for match in hover_matches})


if __name__ == "__main__":
    unittest.main()

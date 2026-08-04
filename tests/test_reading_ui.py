import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "ResearchOS" / "99_Meta" / "tools"
NOTES_DIR = REPO_ROOT / "ResearchOS" / "00_Inbox" / "notes"
READING_JAVASCRIPT_PATH = TOOLS_DIR / "reading_ui.js"
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
        self.assertIn("--session-panel-width: 42rem", page)
        self.assertIn("min(var(--session-panel-width), 52vw)", page)
        self.assertIn(
            "personal-research-os:reading-workspace:presentation:session-panel-width",
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

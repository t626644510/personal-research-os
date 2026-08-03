import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "ResearchOS" / "99_Meta" / "tools"
NOTES_DIR = REPO_ROOT / "ResearchOS" / "00_Inbox" / "notes"
sys.path.insert(0, str(TOOLS_DIR))

from hover_resolver import load_concept_index, resolve_mentions  # noqa: E402
from hover_ui import (  # noqa: E402
    CATEGORY_LABELS,
    CJK_PATTERN,
    generate_hover_demo,
    main,
)


SYNTHETIC_INDEX = {
    "HOM impedance": {
        "id": "never_show_this_id",
        "path": "01_Concept/never-show-full-note.md",
        "aliases": ["HOM", "高次模阻抗"],
        "category": ["RF engineering"],
        "hover_summary": "用于本地提示的紧凑<摘要>。",
        "related_concepts": ["Wakefield"],
    },
    "Wakefield": {
        "path": "01_Concept/Wakefield.md",
        "aliases": ["wake field", "尾场"],
        "hover_summary": "束团经过后留下的电磁场。",
    },
}


class HoverUITests(unittest.TestCase):
    def test_generates_self_contained_cards_from_local_index(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            note_path = root / "review.md"
            index_path = root / "concept_index.json"
            output_path = root / "hover.html"
            note_path.write_text(
                "# 中文审阅笔记\n\n高次模阻抗之后是 <script>alert('x')</script>，"
                "尾场仍然存在。\n",
                encoding="utf-8",
            )
            index_path.write_text(
                json.dumps(SYNTHETIC_INDEX), encoding="utf-8"
            )

            generated_path, matches = generate_hover_demo(
                note_path, output_path, index_path=index_path
            )
            page = generated_path.read_text(encoding="utf-8")

        self.assertEqual(
            [match["concept"] for match in matches],
            ["HOM impedance", "Wakefield"],
        )
        self.assertIn('<html lang="zh-CN">', page)
        self.assertIn("<title>中文审阅笔记 · 离线概念百科</title>", page)
        self.assertIn('<span class="concept-text">高次模阻抗</span>', page)
        self.assertIn(
            '<span class="card-title">高次模阻抗（HOM impedance）</span>', page
        )
        self.assertIn("用于本地提示的紧凑&lt;摘要&gt;。", page)
        self.assertIn("分类：</span>射频工程", page)
        self.assertIn("相关概念：</span>尾场（Wakefield）", page)
        self.assertIn("2 处命中 · 2 个概念 · 仅使用本地索引", page)
        self.assertIn("&lt;script&gt;alert('x')&lt;/script&gt;", page)
        self.assertNotIn("Category:", page)
        self.assertNotIn("Related:", page)
        self.assertNotIn("<script", page)
        self.assertNotIn("http://", page)
        self.assertNotIn("https://", page)
        self.assertNotIn("never_show_this_id", page)
        self.assertNotIn("never-show-full-note.md", page)

    def test_cli_open_uses_generated_local_file_uri(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            note_path = root / "review.md"
            index_path = root / "concept_index.json"
            output_path = root / "hover.html"
            note_path.write_text("高次模阻抗\n", encoding="utf-8")
            index_path.write_text(
                json.dumps(SYNTHETIC_INDEX), encoding="utf-8"
            )

            with patch("hover_ui.webbrowser.open", return_value=True) as open_browser:
                with redirect_stdout(io.StringIO()):
                    exit_code = main(
                        [
                            str(note_path),
                            "--index",
                            str(index_path),
                            "--output",
                            str(output_path),
                            "--open",
                        ]
                    )

            self.assertEqual(exit_code, 0)
            open_browser.assert_called_once_with(output_path.resolve().as_uri())

    def test_realistic_notes_resolve_expected_concepts(self) -> None:
        expected_by_note = {
            "HOM impedance reading note.md": {
                "HOM impedance",
                "Bunch spectrum",
                "Q factor",
                "External Q",
                "Wakefield",
                "Longitudinal impedance",
                "HOM coupler",
            },
            "CST wakefield solver note.md": {
                "CST wakefield solver",
                "Gaussian bunch",
                "Longitudinal wake potential",
                "Transverse wake potential",
                "Kick factor",
                "Loss factor",
                "Eigenmode solver",
                "S parameter",
            },
            "Q0 measurement note.md": {
                "Q factor",
                "Loaded Q",
                "External Q",
                "S parameter",
                "R over Q",
                "Shunt impedance",
            },
            "PSO impedance fitting note.md": {
                "HOM impedance",
                "Longitudinal impedance",
                "Q factor",
                "Bunch spectrum",
                "Beam coupling impedance",
                "Wakefield",
            },
        }
        index = load_concept_index()

        for filename, expected in expected_by_note.items():
            with self.subTest(note=filename):
                text = (NOTES_DIR / filename).read_text(encoding="utf-8")
                matches = resolve_mentions(text, index)
                resolved = {match["concept"] for match in matches}
                self.assertIsNotNone(CJK_PATTERN.search(text.splitlines()[0]))
                self.assertTrue(
                    any(CJK_PATTERN.search(match["matched_term"]) for match in matches)
                )
                self.assertTrue(expected <= resolved, expected - resolved)

    def test_real_index_has_complete_chinese_display_metadata(self) -> None:
        index = load_concept_index()
        categories: set[str] = set()
        for canonical_name, entry in index.items():
            with self.subTest(concept=canonical_name):
                self.assertTrue(
                    any(CJK_PATTERN.search(alias) for alias in entry["aliases"]),
                    f"{canonical_name} has no Chinese alias",
                )
                summary = entry["hover_summary"].lstrip()
                self.assertTrue(
                    CJK_PATTERN.match(summary)
                    or summary.startswith(("CST ", "R/Q ")),
                    f"{canonical_name} summary is not Chinese-primary",
                )
            categories.update(entry.get("category", []))

        self.assertEqual(categories - CATEGORY_LABELS.keys(), set())


if __name__ == "__main__":
    unittest.main()

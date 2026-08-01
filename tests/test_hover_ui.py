import json
import io
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
from hover_ui import generate_hover_demo, main  # noqa: E402


SYNTHETIC_INDEX = {
    "HOM impedance": {
        "id": "never_show_this_id",
        "path": "01_Concept/never-show-full-note.md",
        "aliases": ["HOM"],
        "category": ["RF & beam physics"],
        "hover_summary": "A compact <local> summary.",
        "related_concepts": ["Wakefield"],
    },
    "Wakefield": {
        "path": "01_Concept/Wakefield.md",
        "aliases": ["wake field"],
        "hover_summary": "The field left behind a bunch.",
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
                "# Review\n\nHOM impedance follows <script>alert('x')</script>. "
                "The wake field remains.\n",
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
        self.assertIn('<span class="concept-text">HOM impedance</span>', page)
        self.assertIn('<span class="card-title">HOM impedance</span>', page)
        self.assertIn("A compact &lt;local&gt; summary.", page)
        self.assertIn("RF &amp; beam physics", page)
        self.assertIn("Related:</span> Wakefield", page)
        self.assertIn("&lt;script&gt;alert('x')&lt;/script&gt;", page)
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
            note_path.write_text("HOM impedance\n", encoding="utf-8")
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
                resolved = {
                    match["concept"] for match in resolve_mentions(text, index)
                }
                self.assertTrue(expected <= resolved, expected - resolved)


if __name__ == "__main__":
    unittest.main()

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "ResearchOS" / "99_Meta" / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from hover_resolver import (  # noqa: E402
    HoverIndexError,
    load_concept_index,
    resolve_mentions,
)


SYNTHETIC_INDEX = {
    "HOM impedance": {
        "id": "hom_impedance",
        "path": "01_Concept/HOM impedance.md",
        "aliases": ["HOM"],
        "category": ["accelerator physics"],
        "hover_summary": "A resonant beam-coupling impedance.",
        "related_concepts": ["Wakefield"],
    },
    "Q factor": {
        "id": "q_factor",
        "path": "01_Concept/Q factor.md",
        "aliases": ["Q"],
        "category": ["RF engineering"],
        "hover_summary": "Stored energy relative to loss.",
        "related_concepts": [],
    },
    "Wakefield": {
        "path": "01_Concept/Wakefield.md",
        "aliases": ["wake field", "尾场"],
        "hover_summary": "The electromagnetic response behind a bunch.",
    },
}


class HoverResolverTests(unittest.TestCase):
    def test_prefers_longest_term_at_the_same_position(self) -> None:
        matches = resolve_mentions(
            "HOM impedance is not the same string as HOM.", SYNTHETIC_INDEX
        )
        self.assertEqual(
            [match["matched_term"] for match in matches], ["HOM impedance", "HOM"]
        )
        self.assertEqual(
            [match["concept"] for match in matches],
            ["HOM impedance", "HOM impedance"],
        )

    def test_supports_aliases_case_insensitively(self) -> None:
        matches = resolve_mentions(
            "# Notes\nA WAKE FIELD can ring after the bunch.", SYNTHETIC_INDEX
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["concept"], "Wakefield")
        self.assertEqual(matches[0]["matched_text"], "WAKE FIELD")

    def test_ascii_boundaries_avoid_substring_false_positives(self) -> None:
        matches = resolve_mentions("HOMogeneous Qubit quality", SYNTHETIC_INDEX)
        self.assertEqual(matches, [])

    def test_returns_ordered_non_overlapping_offsets(self) -> None:
        text = "Q, then wake field, then HOM   impedance."
        matches = resolve_mentions(text, SYNTHETIC_INDEX)
        self.assertEqual(
            [match["concept"] for match in matches],
            ["Q factor", "Wakefield", "HOM impedance"],
        )
        for match in matches:
            self.assertEqual(
                text[match["start"] : match["end"]], match["matched_text"]
            )

    def test_legacy_index_defaults_new_fields(self) -> None:
        match = resolve_mentions("尾场", SYNTHETIC_INDEX)[0]
        self.assertEqual(match["concept"], "Wakefield")
        self.assertIsNone(match["id"])
        self.assertEqual(match["category"], [])
        self.assertEqual(match["related_concepts"], [])

    def test_rejects_ambiguous_terms(self) -> None:
        ambiguous_index = {
            "First": {
                "path": "first.md",
                "aliases": ["shared"],
                "hover_summary": "First summary.",
            },
            "Second": {
                "path": "second.md",
                "aliases": ["Shared"],
                "hover_summary": "Second summary.",
            },
        }
        with self.assertRaisesRegex(HoverIndexError, "term 'Shared' is shared"):
            resolve_mentions("shared", ambiguous_index)

    def test_loads_legacy_json_index(self) -> None:
        legacy_index = {"Wakefield": SYNTHETIC_INDEX["Wakefield"]}
        with tempfile.TemporaryDirectory() as temporary_directory:
            index_path = Path(temporary_directory) / "concept_index.json"
            with index_path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(json.dumps(legacy_index))
            loaded = load_concept_index(index_path)
        self.assertEqual(loaded, legacy_index)

    def test_real_index_resolves_canonical_and_alias_terms(self) -> None:
        matches = resolve_mentions("Bunch spectrum overlaps 高次模阻抗.")
        self.assertEqual(
            [match["concept"] for match in matches],
            ["Bunch spectrum", "HOM impedance"],
        )


if __name__ == "__main__":
    unittest.main()

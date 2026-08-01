import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "ResearchOS" / "99_Meta" / "tools"
CONCEPT_DIR = REPO_ROOT / "ResearchOS" / "01_Concept"
sys.path.insert(0, str(TOOLS_DIR))

from concept_tools import ConceptFormatError, scan_concepts  # noqa: E402


class ConceptIndexTests(unittest.TestCase):
    def test_scan_preserves_old_fields_and_adds_p01_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "concept_index.json"
            index = scan_concepts(CONCEPT_DIR, output_path)

        self.assertGreaterEqual(len(index), 25)
        wakefield = index["Wakefield"]
        self.assertEqual(wakefield["path"], "01_Concept/Wakefield.md")
        self.assertIn("wake field", wakefield["aliases"])
        self.assertTrue(wakefield["hover_summary"])
        self.assertEqual(wakefield["id"], "wakefield")
        self.assertIn("accelerator physics", wakefield["category"])
        self.assertIn("HOM impedance", wakefield["related_concepts"])

    def test_all_related_concepts_use_canonical_index_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            index = scan_concepts(
                CONCEPT_DIR, Path(temporary_directory) / "concept_index.json"
            )

        canonical_names = set(index)
        for concept_name, entry in index.items():
            with self.subTest(concept=concept_name):
                self.assertTrue(set(entry["related_concepts"]) <= canonical_names)
                self.assertNotIn(concept_name, entry["related_concepts"])

    def test_index_generation_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            first_path = Path(temporary_directory) / "first.json"
            second_path = Path(temporary_directory) / "second.json"
            scan_concepts(CONCEPT_DIR, first_path)
            scan_concepts(CONCEPT_DIR, second_path)
            self.assertEqual(first_path.read_bytes(), second_path.read_bytes())

    def test_related_alias_is_normalized_to_canonical_name(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            copied_concepts = temporary_root / "01_Concept"
            shutil.copytree(CONCEPT_DIR, copied_concepts)
            concept_path = copied_concepts / "Beam coupling impedance.md"
            concept_text = concept_path.read_text(encoding="utf-8")
            with concept_path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(
                    concept_text.replace("- [[Wakefield]]", "- [[wake field]]")
                )

            index = scan_concepts(
                copied_concepts, temporary_root / "concept_index.json"
            )
            self.assertIn(
                "Wakefield", index["Beam coupling impedance"]["related_concepts"]
            )

    def test_invalid_related_link_keeps_existing_index(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            copied_concepts = temporary_root / "01_Concept"
            shutil.copytree(CONCEPT_DIR, copied_concepts)
            wakefield_path = copied_concepts / "Wakefield.md"
            wakefield_text = wakefield_path.read_text(encoding="utf-8")
            with wakefield_path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(
                    wakefield_text.replace(
                        "- [[HOM impedance]]", "- [[Missing concept for test]]"
                    )
                )
            output_path = temporary_root / "concept_index.json"
            sentinel = '{"sentinel": true}\n'
            with output_path.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(sentinel)

            with self.assertRaisesRegex(
                ConceptFormatError, "related concept 'Missing concept for test'"
            ):
                scan_concepts(copied_concepts, output_path)
            self.assertEqual(output_path.read_text(encoding="utf-8"), sentinel)


if __name__ == "__main__":
    unittest.main()

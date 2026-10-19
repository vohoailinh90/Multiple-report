"""scripts/decks.py: which decks are missing or stale, and the index of lessons."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("decks", ROOT / "scripts" / "decks.py")
decks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decks)

LESSON = "---\nid: L01\ntitle: Dopamine và động lực\ntopic: than-kinh\ndate: 2026-10-19\n---\n# Dopamine\n"


class DeckTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        self.folder = self.root / "lessons" / "L01"
        self.folder.mkdir(parents=True)
        (self.folder / "lesson.md").write_text(LESSON, encoding="utf-8")
        (self.folder / "slides.json").write_text('{"title": "x", "slides": []}', encoding="utf-8")

    def run_main(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                code = decks.main(list(args), root=self.root)
            except SystemExit as exc:
                code, _ = 1, print(exc)
        return code, out.getvalue()

    def save_pptx(self, data: bytes = b"PK\x03\x04deck") -> None:
        (self.folder / "L01.pptx").write_bytes(data)

    def test_a_lesson_without_a_deck_is_listed(self):
        self.assertEqual(self.run_main("todo")[1], "L01\tno .pptx\n")

    def test_a_recorded_deck_is_current_until_its_slides_change(self):
        self.save_pptx()
        self.assertEqual(self.run_main("record", "L01", "--canvas", "cvs_1")[0], 0)
        self.assertEqual(json.loads((self.folder / "deck.json").read_text())["canvas"], "cvs_1")
        self.assertEqual(self.run_main("todo")[1], "")
        (self.folder / "slides.json").write_text('{"title": "y", "slides": []}', encoding="utf-8")
        self.assertIn("slides.json changed", self.run_main("todo")[1])

    def test_a_deck_without_its_record_is_listed(self):
        self.save_pptx()
        self.assertIn("no deck.json", self.run_main("todo")[1])

    def test_record_refuses_a_file_that_is_not_a_pptx(self):
        self.save_pptx(b"<html>download page</html>")
        code, out = self.run_main("record", "L01", "--canvas", "cvs_1")
        self.assertEqual(code, 1)
        self.assertIn("not a PowerPoint file", out)
        self.assertIn("not a PowerPoint file", self.run_main("todo")[1])

    def test_a_folder_without_slides_is_not_a_lesson(self):
        (self.root / "lessons" / "drafts").mkdir()
        self.assertEqual(self.run_main("todo")[1], "L01\tno .pptx\n")

    def test_the_index_lists_each_lesson_and_links_its_deck_once_built(self):
        self.assertEqual(self.run_main("index")[0], 0)
        index = (self.root / "lessons" / "README.md").read_text(encoding="utf-8")
        self.assertIn("| Thần kinh | 2026-10-19 | [L01](L01/lesson.md) | Dopamine và động lực | chưa có |", index)
        self.assertEqual(self.run_main("index", "--check")[0], 0)
        self.save_pptx()
        self.run_main("record", "L01", "--canvas", "cvs_1")
        self.assertEqual(self.run_main("index", "--check")[0], 1, "the deck link is now stale in the index")
        self.run_main("index")
        self.assertIn("[L01.pptx](L01/L01.pptx)", (self.root / "lessons" / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

"""scripts/deckgen/check_lesson.py: the structural gate, with the body/facts rules of the deeper lessons."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_lesson", ROOT / "scripts" / "deckgen" / "check_lesson.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

# Synthetic lesson: placeholder words, only its structure matters.
FILLER = " ".join(["chữ"] * 60)
BOOK = "https://rotel.pressbooks.pub/biologicalpsychology/chapter/the-brain/"
REFS = [f"- [S1] Hove & Martinez, Biological Psychology, 2.6, {BOOK}"] + [
    f"- [S{k}] Tác giả {k}, Tên nguồn {k}, 2001, https://example.org/{k}" for k in range(2, 6)]
LESSON = (
    "---\nid: L99\ntitle: Bài thử\ntopic: nao-bo\ndate: 2026-10-20\n---\n# Bài thử\n\n"
    f"## Tóm tắt\n\n{FILLER} [S1] [S2].\n\n"
    f"## Hạnh nhân\n\n{FILLER} [S1] [S3] [S4] [S5].\n\n"
    "## Nguồn tham khảo\n\n" + "\n".join(REFS) + "\n")
BODY = "**Hạnh nhân** " + " ".join(["chữ"] * 70) + " [S1]."
SLIDES = [
    {"title": "Mở bài", "section": "Tóm tắt", "sources": ["S1"], "bullets": ["một", "hai"], "notes": "n",
     "layout": "card-grid", "tone": "light"},
    {"title": "Hạnh nhân là gì", "section": "Hạnh nhân", "sources": ["S1"], "body": BODY,
     "bullets": ["Ở đâu: sâu trong não"], "notes": "n", "layout": "explainer", "tone": "dark"},
    {"title": "Hồ sơ hạnh nhân", "section": "Hạnh nhân", "sources": ["S3"], "bullets": [],
     "facts": [{"label": f"Nhãn {k}", "text": f"ý {k} [S3]"} for k in range(6)], "notes": "n",
     "layout": "profile-card", "tone": "light"},
    {"title": "Hai phía", "section": "Hạnh nhân", "sources": ["S4"], "bullets": ["A: một", "B: hai"], "notes": "n",
     "layout": "two-column-comparison", "tone": "dark"},
    {"title": "Ba bước", "section": "Hạnh nhân", "sources": ["S5"], "bullets": ["một", "hai", "ba"], "notes": "n",
     "layout": "flow", "tone": "light"},
    {"title": "Nguồn tham khảo", "section": "Nguồn tham khảo", "sources": ["S1", "S2"],
     "bullets": [f"S{k}: nguồn {k}" for k in range(1, 6)], "notes": "n", "layout": "references", "tone": "dark"},
]
EXPECTED = {"id": "L99", "title": "Bài thử", "topic": "nao-bo", "sections": ["Tóm tắt", "Hạnh nhân", "Nguồn tham khảo"],
            "required_urls": [BOOK], "min_independent_sources": 4, "min_words": 100, "max_words": 30000,
            "min_citations": 6, "key_terms": ["Hạnh nhân"], "language": "vi", "slides": {"min": 5, "max": 60},
            "min_layouts": 5, "section_min_slides": 3, "section_min_exempt": ["Tóm tắt", "Nguồn tham khảo"]}


class GateTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        (self.root / "lessons" / "L99").mkdir(parents=True)

    def run_gate(self, slides=None, expected=None, lesson=LESSON):
        (self.root / "lessons" / "L99" / "lesson.md").write_text(lesson, encoding="utf-8")
        (self.root / "lessons" / "L99" / "slides.json").write_text(
            json.dumps({"title": "Bài thử", "subtitle": "s", "slides": slides or SLIDES}, ensure_ascii=False), encoding="utf-8")
        (self.root / "lessons" / "L99.expected.json").write_text(
            json.dumps(expected or EXPECTED, ensure_ascii=False), encoding="utf-8")
        errs, warn, _ = gate.check(self.root, "L99")
        return errs, warn

    def mutated(self, k, **changes):
        slides = copy.deepcopy(SLIDES)
        for key, value in changes.items():
            if value is None:
                slides[k].pop(key, None)
            else:
                slides[k][key] = value
        return slides

    def test_the_synthetic_lesson_passes(self):
        self.assertEqual(self.run_gate(), ([], []))

    def test_every_finished_lesson_passes_its_gate(self):
        """A lesson whose spec says it is being written is skipped until the orchestrator merges it."""
        for lid in sorted(p.stem.split(".")[0] for p in (ROOT / "lessons").glob("*.expected.json")):
            spec = ROOT / "lessons" / f"{lid}.spec.md"
            if spec.is_file() and "Trạng thái: đang viết" in spec.read_text(encoding="utf-8"):
                continue
            with self.subTest(lesson=lid):
                self.assertEqual(gate.check(ROOT, lid)[0], [])

    def test_an_explainer_needs_a_body_within_bounds(self):
        self.assertIn("explainer needs a body: Hạnh nhân là gì", self.run_gate(self.mutated(1, body=None))[0])
        errs, _ = self.run_gate(self.mutated(1, body=" ".join(["chữ"] * 150)))
        self.assertIn("body 150 words: Hạnh nhân là gì", errs)
        _, warn = self.run_gate(self.mutated(1, body=" ".join(["chữ"] * 45)))
        self.assertIn("body 45 words (aim 60-110): Hạnh nhân là gì", warn)

    def test_a_body_on_a_layout_that_does_not_draw_it_is_refused(self):
        errs, _ = self.run_gate(self.mutated(3, body=BODY))
        self.assertIn("body is not drawn by two-column-comparison: Hai phía", errs)

    def test_a_profile_card_takes_three_to_six_facts_and_no_bullets(self):
        seven = [{"label": "a", "text": "b"}] * 7
        self.assertIn("profile-card needs 3-6 facts: Hồ sơ hạnh nhân", self.run_gate(self.mutated(2, facts=seven))[0])
        self.assertIn("profile-card needs facts: Hồ sơ hạnh nhân", self.run_gate(self.mutated(2, facts=None))[0])
        self.assertIn("profile-card draws facts, not bullets: Hồ sơ hạnh nhân",
                      self.run_gate(self.mutated(2, bullets=["x"]))[0])

    def test_each_content_section_needs_three_slides(self):
        slides = [s for k, s in enumerate(SLIDES) if k != 4]
        slides[3] = {**slides[3], "layout": "flow"}  # keep five kinds of layout
        self.assertIn("section has 3 slides: Hạnh nhân", self.run_gate(slides, {**EXPECTED, "section_min_slides": 4})[0])
        self.assertEqual(self.run_gate(slides)[0], [], "three slides are enough")

    def test_independent_sources_and_required_textbook_url(self):
        errs, _ = self.run_gate(expected={**EXPECTED, "min_independent_sources": 5})
        self.assertIn("independent sources 4 < 5", errs)
        errs, _ = self.run_gate(expected={**EXPECTED, "required_urls": [BOOK + "x/"]})
        self.assertIn(f"required source missing: {BOOK}x/", errs)

    def test_a_slide_may_only_cite_listed_sources(self):
        errs, _ = self.run_gate(self.mutated(3, bullets=["A: một [S9]", "B: hai"]))
        self.assertIn("slide cites S9, not in the reference list: Hai phía", errs)

    def test_images_only_on_layouts_that_draw_them(self):
        img = [{"file": "images/x.png", "alt": "a", "credit": "c", "url": "u"}]
        (self.root / "lessons" / "L99" / "images").mkdir()
        (self.root / "lessons" / "L99" / "images" / "x.png").write_bytes(b"png")
        errs, _ = self.run_gate(self.mutated(4, images=img))
        self.assertIn("images are drawn only by figure and annotated-figure: Ba bước", errs)
        self.assertIn("figure needs images: Ba bước", self.run_gate(self.mutated(4, layout="figure"))[0])

    def test_the_reference_list_does_not_count_as_citations(self):
        errs, _ = self.run_gate(expected={**EXPECTED, "min_citations": 7})
        self.assertIn("cites 6", errs)


if __name__ == "__main__":
    unittest.main()

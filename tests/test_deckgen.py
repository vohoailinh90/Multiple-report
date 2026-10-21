"""scripts/deckgen: every page of every lesson renders to well-formed Moda markup, and the new layouts draw what the gate allows."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures" / "deckgen"


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "deckgen" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gen = load("gen")


def opts(lid):
    path = ROOT / "scripts" / "deckgen" / "opts" / f"{lid}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def in_progress(lid):
    """A lesson whose spec says it is being written: its new figures have no Moda id yet (scripts/deckgen/file_ids.json)."""
    spec = ROOT / "lessons" / f"{lid}.spec.md"
    return spec.is_file() and "Trạng thái: đang viết" in spec.read_text(encoding="utf-8")


def texts(markup):
    """(x, width, font-size, text) of every <text> node."""
    tree = ET.fromstring(markup)
    return [(float(t.get("x")), float(t.get("width")), int(t.get("font-size", 0)), "".join(t.itertext()))
            for t in tree.iter("text")]


class GenTests(unittest.TestCase):
    def test_every_page_of_every_lesson_is_well_formed_and_never_below_22px(self):
        lessons = sorted(p.parent.name for p in (ROOT / "lessons").glob("*/slides.json") if not in_progress(p.parent.name))
        self.assertTrue(lessons)
        for lid in lessons:
            n = len(json.loads((ROOT / "lessons" / lid / "slides.json").read_text(encoding="utf-8"))["slides"])
            for i in range(n + 1):
                markup = gen.page(lid, i, opts(lid))
                with self.subTest(lesson=lid, page=i):
                    sizes = [size for _, _, size, _ in texts(markup)]
                    self.assertGreaterEqual(min(sizes), 22)

    def test_no_text_is_estimated_to_overflow_its_box(self):
        """gen.fit sizes every long text to its box; a layout with a box too small for its text fails here, not on Moda."""
        pages = [("T00", i, json.loads((FIX / "opts.json").read_text(encoding="utf-8")), FIX / "slides.json") for i in range(1, 6)]
        for lid in sorted(p.parent.name for p in (ROOT / "lessons").glob("*/slides.json") if not in_progress(p.parent.name)):
            n = len(json.loads((ROOT / "lessons" / lid / "slides.json").read_text(encoding="utf-8"))["slides"])
            pages += [(lid, i, opts(lid), None) for i in range(1, n + 1)]
        for lid, i, o, path in pages:
            with self.subTest(lesson=lid, page=i):
                self.assertEqual(gen.overflows(gen.page(lid, i, o, path)), [])

    def demo(self, i):
        return gen.page("T00", i, json.loads((FIX / "opts.json").read_text(encoding="utf-8")), FIX / "slides.json")

    def test_explainer_draws_the_body_with_coloured_terms_and_its_cards(self):
        markup = self.demo(1)
        body = next(t for t in ET.fromstring(markup).iter("text") if t.get("format") == "html")
        self.assertIn('<span style="color: #1F3FD1; font-weight: 700">Hạnh nhân</span>', markup)
        self.assertIn('<span style="color: #B45309; font-weight: 700">hệ viền</span>', markup, "concept 1 keeps its colour")
        self.assertIn("[S3]</span>", markup)
        self.assertNotIn("**", markup)
        self.assertGreaterEqual(int(body.get("font-size")), 30)
        labels = [t for _, _, _, t in texts(markup)]
        for label in ("Ở đâu", "Làm gì", "Đừng hiểu nhầm"):
            self.assertIn(label, labels)

    def test_profile_card_draws_one_card_per_fact(self):
        markup = self.demo(2)
        facts = json.loads((FIX / "slides.json").read_text(encoding="utf-8"))["slides"][1]["facts"]
        drawn = [t for _, _, _, t in texts(markup)]
        for fact in facts:
            self.assertIn(fact["label"], drawn)
            self.assertIn(fact["text"].replace("**", ""), drawn)
        self.assertTrue(all(size >= 28 for _, _, size, t in texts(markup) if t in {f["text"] for f in facts}))

    def test_annotated_figure_draws_image_credit_glosses_and_body(self):
        markup = self.demo(3)
        self.assertEqual(len(list(ET.fromstring(markup).iter("image"))), 1)
        drawn = " ".join(t for _, _, _, t in texts(markup))
        self.assertIn("Hình: OpenStax Psychology 2e", drawn)
        self.assertIn("Reuptake inhibitor", drawn)
        self.assertIn("serotonin ở lại lâu hơn", drawn)

    def test_references_use_two_columns_beyond_six(self):
        markup = self.demo(5)
        xs = {x for x, _, _, t in texts(markup) if re.fullmatch(r"S\d+", t)}
        self.assertEqual(len(xs), 2)
        self.assertNotIn("Nguồn: [", markup, "the sources slide does not cite itself")

    def test_a_long_deck_keeps_the_footer_out_of_the_logo_corner(self):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        kinds = ["card-grid", "numbered-rows"]
        slides = [{"title": f"Slide {k}", "section": "A", "sources": [], "bullets": ["một", "hai"],
                   "notes": "", "layout": kinds[k % 2], "tone": "light"} for k in range(60)]
        path = root / "slides.json"
        path.write_text(json.dumps({"title": "t", "subtitle": "s", "slides": slides}), encoding="utf-8")
        for i in (1, 60):
            footer = [(x, w) for x, w, _, t in texts(gen.page("L09", i, {}, path)) if t.startswith("Multiple-report")]
            self.assertEqual(len(footer), 1)
            x, w = footer[0]
            self.assertLessEqual(x + w, 1650, "the bottom-right corner stays empty for the Moda logo")

    def test_the_last_layer_ends_above_the_source_line(self):
        """Six layers used to end at y=980 and cover the source line drawn at y=944."""
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        for count in range(1, 7):
            slide = {"title": "Lớp", "section": "A", "sources": ["S1"], "bullets": ["lớp"] * count, "notes": "",
                     "layout": "layers", "tone": "light"}
            path = root / "slides.json"
            path.write_text(json.dumps({"title": "t", "subtitle": "s", "slides": [slide]}), encoding="utf-8")
            tree = ET.fromstring(gen.page("L09", 1, {}, path))
            with self.subTest(layers=count):
                bottoms = [float(r.get("y")) + float(r.get("height")) for r in tree.iter("rectangle") if r.get("corner-radius") == "22"]
                self.assertEqual(len(bottoms), count)
                self.assertLessEqual(max(bottoms), 944)

    def test_moda_ids_are_per_lesson_not_per_file_name(self):
        """A file name uploaded for one lesson must not stand in for a different file of the same name in another."""
        fig = {"title": "Hình", "section": "A", "sources": [], "bullets": ["một"], "notes": "", "layout": "figure", "tone": "light",
               "images": [{"file": "images/a.png", "alt": "a", "credit": "c", "url": "u"}]}
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        path = root / "slides.json"
        path.write_text(json.dumps({"title": "t", "subtitle": "s", "slides": [fig]}), encoding="utf-8")
        self.addCleanup(gen.FILE_IDS.pop, "L40/images/a.png", None)
        gen.FILE_IDS["L40/images/a.png"] = "file_AAA"
        self.assertIn('src="file_AAA"', gen.page("L40", 1, {}, path))
        with self.assertRaises(SystemExit) as caught:
            gen.page("L41", 1, {}, path)
        self.assertIn("L41/images/a.png has no Moda id", str(caught.exception))

    def test_mk_never_overwrites_an_existing_expected_file(self):
        mk = load("mk")
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        (root / "lessons" / "L90").mkdir(parents=True)
        (root / "lessons" / "L90" / "lesson.md").write_text("# t\n\n## A\n\n## Nguồn tham khảo\n", encoding="utf-8")
        self.addCleanup(setattr, mk, "ROOT", mk.ROOT)
        mk.ROOT = root
        mk.deep_expected("L90", "t", "nao-bo", ["A"], [], ["x"])
        written = (root / "lessons" / "L90.expected.json").read_text(encoding="utf-8")
        with self.assertRaises(SystemExit):
            mk.deep_expected("L90", "đổi", "nao-bo", ["B"], [], ["y"])
        with self.assertRaises(SystemExit):
            mk.build("L90", "đổi", "s", "nao-bo", {}, [], [])
        self.assertEqual((root / "lessons" / "L90.expected.json").read_text(encoding="utf-8"), written)

    def test_a_long_big_number_wraps_and_shrinks_instead_of_being_clipped(self):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        title = "Một tiêu đề dài bảy mươi lăm ký tự dùng làm số lớn khi không có giá trị riêng " + "x" * 5
        slide = {"title": title, "section": "A", "sources": [], "bullets": ["một"], "notes": "", "layout": "one-big-number", "tone": "dark"}
        path = root / "slides.json"
        path.write_text(json.dumps({"title": "t", "subtitle": "s", "slides": [slide]}), encoding="utf-8")
        markup = gen.page("L09", 1, {}, path)
        self.assertEqual(gen.overflows(markup), [])
        node = next(t for t in ET.fromstring(markup).iter("text") if t.get("font-family") == "Bricolage Grotesque" and t.get("height") == "360")
        self.assertLess(int(node.get("font-size")), 120)
        self.assertIsNone(node.get("max-lines"))
        short = gen.page("L09", 1, {"big": {"1": "86 tỷ"}}, path)
        node = next(t for t in ET.fromstring(short).iter("text") if t.get("height") == "360")
        self.assertEqual((node.get("font-size"), node.get("max-lines")), ("300", "1"))

    def test_fit_shrinks_long_text_but_not_below_the_floor(self):
        short, long = "một câu ngắn", " ".join(["chữ"] * 400)
        self.assertEqual(gen.fit(short, 600, 200, 40), 40)
        self.assertLess(gen.fit(long[:400], 600, 200, 40), 40)
        self.assertEqual(gen.fit(long, 600, 200, 40, floor=26), 26)


if __name__ == "__main__":
    unittest.main()

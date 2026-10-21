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
        self.assertIn("profile-card draws 0-0 bullets, found 1: Hồ sơ hạnh nhân",
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
        img = [{"file": "images/x.png", "alt": "a", "credit": "c", "url": "https://example.org/x.png"}]
        (self.root / "lessons" / "L99" / "images").mkdir()
        (self.root / "lessons" / "L99" / "images" / "x.png").write_bytes(b"png")
        errs, _ = self.run_gate(self.mutated(4, images=img))
        self.assertIn("images are drawn only by figure and annotated-figure: Ba bước", errs)
        self.assertIn("figure needs images: Ba bước", self.run_gate(self.mutated(4, layout="figure"))[0])

    def test_three_text_heavy_slides_in_a_row_are_refused(self):
        img = [{"file": "images/x.png", "alt": "a", "credit": "c", "url": "https://example.org/x.png"}]
        (self.root / "lessons" / "L99" / "images").mkdir()
        (self.root / "lessons" / "L99" / "images" / "x.png").write_bytes(b"png")
        heavy = self.mutated(3, layout="annotated-figure", body=" ".join(["chữ"] * 50), images=img, bullets=[])
        self.assertIn("three text-heavy slides in a row from slide 2", self.run_gate(heavy)[0])

    def test_a_layout_must_get_the_bullets_its_renderer_draws(self):
        """gen.py draws at most 4 nodes of a connection-diagram and divides by the bullet count of a flow."""
        errs, _ = self.run_gate(self.mutated(4, layout="connection-diagram", bullets=list("abcde")))
        self.assertIn("connection-diagram draws 1-4 bullets, found 5: Ba bước", errs)
        errs, _ = self.run_gate(self.mutated(4, bullets=[]))
        self.assertIn("flow draws 1-5 bullets, found 0: Ba bước", errs)
        errs, _ = self.run_gate(self.mutated(4, layout="one-highlighted-sentence", bullets=list("abcde")))
        self.assertIn("one-highlighted-sentence draws 1-4 bullets, found 5: Ba bước", errs)

    def test_an_expected_url_must_sit_on_its_own_reference_line(self):
        (self.root / "lessons" / "L99").mkdir(exist_ok=True)
        urls = {f"S{k}": f"https://example.org/{k}" for k in range(2, 6)}
        expected = {k: v for k, v in EXPECTED.items() if k not in ("required_urls", "min_independent_sources")}
        expected["sources"] = {"S1": BOOK, **urls}
        self.assertEqual(self.run_gate(expected=expected)[0], [])
        swapped = {**expected["sources"], "S2": urls["S3"], "S3": urls["S2"]}  # both URLs are in the lesson, on the wrong lines
        errs, _ = self.run_gate(expected={**expected, "sources": swapped})
        self.assertIn("url of S2 is not on its own reference line", errs)
        self.assertIn("url of S3 is not on its own reference line", errs)

    def test_every_accepted_layout_has_a_renderer_and_bullet_limits(self):
        """A layout the gate accepts must not crash validation or gen.py (2x2-matrix was accepted with neither)."""
        gen = importlib.util.module_from_spec(importlib.util.spec_from_file_location("gen", ROOT / "scripts" / "deckgen" / "gen.py"))
        gen.__spec__.loader.exec_module(gen)
        drawn = set(gen.LAYOUTS) | set(gen.INDEXED)
        self.assertEqual(set(gate.LAYOUTS), drawn)
        self.assertEqual(set(gate.BULLETS), drawn)
        errs, _ = self.run_gate(self.mutated(4, layout="2x2-matrix"))
        self.assertIn("unknown layout 2x2-matrix: Ba bước", errs)

    def test_a_slide_title_fits_two_lines(self):
        errs, _ = self.run_gate(self.mutated(4, title="Ba " + "bước " * 25))
        self.assertTrue(any(e.startswith("title>90: ") for e in errs))

    def test_the_deck_title_must_be_the_lesson_title(self):
        slides = {"title": "Tiêu đề cũ", "subtitle": "s", "slides": SLIDES}
        (self.root / "lessons" / "L99" / "lesson.md").write_text(LESSON, encoding="utf-8")
        (self.root / "lessons" / "L99" / "slides.json").write_text(json.dumps(slides, ensure_ascii=False), encoding="utf-8")
        (self.root / "lessons" / "L99.expected.json").write_text(json.dumps(EXPECTED, ensure_ascii=False), encoding="utf-8")
        errs, _, _ = gate.check(self.root, "L99")
        self.assertIn("deck title 'Tiêu đề cũ' differs from the lesson title", errs)

    def test_a_tone_must_be_light_or_dark(self):
        errs, _ = self.run_gate(self.mutated(4, tone="ligt"))
        self.assertIn("tone 'ligt' is not light or dark: Ba bước", errs)

    def test_the_references_slide_lists_every_source_exactly_once(self):
        subset = self.mutated(5, bullets=[f"S{k}: nguồn {k}" for k in range(1, 5)])
        self.assertIn("references slide lists ['S1', 'S2', 'S3', 'S4'], the reference list has ['S1', 'S2', 'S3', 'S4', 'S5']",
                      self.run_gate(subset)[0])
        twice = self.mutated(5, bullets=["S1: a", "S1: b", "S3: c", "S4: d", "S5: e"])
        self.assertTrue(any(e.startswith("references slide lists") for e in self.run_gate(twice)[0]))

    def test_text_that_cannot_fit_its_box_at_the_smallest_font_is_refused(self):
        """Six 160-character timeline bullets pass the length limit but need about 211px in a 190px box."""
        long = " ".join(["chữ"] * 36)[:160]
        errs, _ = self.run_gate(self.mutated(4, layout="timeline", bullets=[long] * 6))
        self.assertTrue(any(e.startswith("text does not fit its box on timeline (Ba bước)") for e in errs), errs)
        errs, _ = self.run_gate(self.mutated(4, layout="timeline", bullets=["ngắn"] * 6))
        self.assertEqual(errs, [])

    def test_the_front_matter_date_is_required_and_iso(self):
        for date_line in ("", "date: 20/10/2026\n", "date: 2026-13-01\n"):
            errs, _ = self.run_gate(lesson=LESSON.replace("date: 2026-10-20\n", date_line))
            with self.subTest(date_line=date_line):
                self.assertTrue(any(e.startswith("date must be YYYY-MM-DD") for e in errs), errs)

    def test_a_citation_drawn_on_a_slide_must_be_in_its_sources(self):
        errs, _ = self.run_gate(self.mutated(3, bullets=["A: một [S2]", "B: hai"]))
        self.assertIn("slide text cites S2 but its sources omit it: Hai phía", errs)
        self.assertEqual(self.run_gate(self.mutated(3, bullets=["A: một [S4]", "B: hai"]))[0], [])

    def test_slides_follow_the_section_order_and_the_sources_slide_is_last(self):
        swapped = copy.deepcopy(SLIDES)
        swapped[0]["section"], swapped[-1]["section"] = swapped[-1]["section"], swapped[0]["section"]
        errs, _ = self.run_gate(swapped)
        self.assertIn("slides do not follow the order of the lesson's sections", errs)
        self.assertIn("the last slide must be the sources slide (section Nguồn tham khảo)", errs)
        lookup = self.mutated(5, layout="lookup-table")
        self.assertIn("the last slide of a deep lesson must use the references layout", self.run_gate(lookup)[0])
        shallow = {k: v for k, v in EXPECTED.items() if k not in ("section_min_slides", "section_min_exempt")}
        self.assertEqual(self.run_gate(lookup, shallow)[0], [], "older lessons may end on any layout in the sources section")
        early = self.mutated(4, layout="references", bullets=["S1: a"])
        self.assertIn("a references slide must be the last slide", self.run_gate(early)[0])

    def test_a_slide_missing_a_renderer_field_is_reported_not_crashed(self):
        """A profile-card without bullets, or a slide without sources, used to pass the gate and fail in gen.py."""
        errs, _ = self.run_gate(self.mutated(2, bullets=None))
        self.assertIn("slide 3 lacks 'bullets' of the right type", errs)
        errs, _ = self.run_gate(self.mutated(4, sources=None))
        self.assertIn("slide 5 lacks 'sources' of the right type", errs)
        errs, _ = self.run_gate(self.mutated(4, bullets=["một", 2, "ba"]))
        self.assertIn("slide 5 has a bullet that is not text", errs)

    def test_a_slide_the_renderer_cannot_draw_is_an_error_but_a_missing_moda_id_is_a_warning(self):
        img = [{"file": "images/x.png", "alt": "a", "credit": "c", "url": "https://example.org/x.png"}]
        (self.root / "lessons" / "L99" / "images").mkdir()
        (self.root / "lessons" / "L99" / "images" / "x.png").write_bytes(b"png")
        errs, warn = self.run_gate(self.mutated(4, layout="figure", images=img, bullets=["một"]))
        self.assertEqual(errs, [])
        self.assertTrue(any("has no Moda id" in w for w in warn), warn)
        original = gate.gen().page
        gate.gen().page = lambda *a, **k: (_ for _ in ()).throw(KeyError("boom"))
        self.addCleanup(setattr, gate.gen(), "page", original)
        errs, _ = self.run_gate()
        self.assertTrue(any("does not render: KeyError" in e for e in errs), errs)

    def test_values_of_the_wrong_type_are_errors_not_crashes(self):
        errs, _ = self.run_gate(self.mutated(2, facts=[{"label": 4, "text": "x"}] * 3))
        self.assertIn("slide 3: facts must be a list of {label, text} with text values", errs)
        errs, _ = self.run_gate(self.mutated(1, body=7))
        self.assertIn("slide 2: body is not text", errs)
        errs, _ = self.run_gate(self.mutated(4, sources=["S5", 5]))
        self.assertIn("slide 5 has a source that is not text", errs)
        errs, _ = self.run_gate(self.mutated(4, layout="figure", images=["x.png"], bullets=["một"]))
        self.assertIn("slide 5: images must be a list of entries with non-empty text values and an http(s) url", errs)

    def test_a_reference_label_must_be_the_one_the_renderer_draws(self):
        """gen.references labels a card with the text before ': ', else with its position."""
        errs, _ = self.run_gate(self.mutated(5, bullets=["S1: a", "S2 nguồn hai", "S3: c", "S4: d", "S5: e"]))
        self.assertTrue(any(e.startswith("references slide lists") for e in errs), errs)

    def test_one_url_under_several_labels_is_one_independent_source(self):
        lesson = LESSON
        for k in range(3, 6):
            lesson = lesson.replace(f"https://example.org/{k}", "https://example.org/2/")
        errs, _ = self.run_gate(lesson=lesson)
        self.assertIn("independent sources 1 < 4", errs)

    def test_paragraph_spacing_counts_toward_the_height_of_a_body(self):
        """Eleven short paragraphs need their 18px gaps: 11 lines of 30px text alone would fit, with the gaps they do not."""
        body = "\n\n".join(["**Hạnh nhân** là một khối nhỏ [S1]."] * 11)
        errs, _ = self.run_gate(self.mutated(1, body=body))
        self.assertTrue(any(e.startswith("text does not fit its box on explainer (Hạnh nhân là gì)") for e in errs), errs)

    def test_a_citation_in_a_title_or_fact_label_must_be_in_the_sources_too(self):
        errs, _ = self.run_gate(self.mutated(4, title="Ba bước [S2]"))
        self.assertIn("slide text cites S2 but its sources omit it: Ba bước [S2]", errs)
        facts = [{"label": "Nhãn [S2]", "text": f"ý {k} [S3]"} for k in range(3)]
        errs, _ = self.run_gate(self.mutated(2, facts=facts))
        self.assertIn("slide text cites S2 but its sources omit it: Hồ sơ hạnh nhân", errs)

    def test_a_bibliography_label_may_not_repeat(self):
        lesson = LESSON.replace("- [S3] Tác giả 3", "- [S2] Tác giả 3")
        errs, _ = self.run_gate(lesson=lesson)
        self.assertIn("reference label S2 is used twice", errs)

    def test_malformed_front_matter_is_reported_not_crashed(self):
        for bad in ("topic:nao-bo", "date: 2026-10-20\ndate: 2026-10-21"):
            lesson = LESSON.replace("topic: nao-bo", bad)
            errs, _ = self.run_gate(lesson=lesson)
            with self.subTest(bad=bad):
                self.assertTrue(any(e.startswith("front matter line is not") for e in errs), errs)

    def test_text_past_a_nodes_max_lines_is_clipped_so_it_is_refused(self):
        """A card-grid label may wrap to two lines; this one needs three even at the smallest size."""
        label = "abcdefghij " * 5
        errs, _ = self.run_gate(self.mutated(0, bullets=[f"{label}: giải thích", "hai: ba", "bốn: năm", "sáu: bảy"]))
        self.assertTrue(any(e.startswith("text does not fit its box on card-grid") for e in errs), errs)
        errs, _ = self.run_gate(self.mutated(0, bullets=["Nhãn ngắn: giải thích", "hai: ba", "bốn: năm", "sáu: bảy"]))
        self.assertEqual(errs, [])

    def test_a_reference_card_needs_text_after_its_label(self):
        errs, _ = self.run_gate(self.mutated(5, bullets=[f"S{k}: " for k in range(1, 6)]))
        self.assertIn("reference card has no text after its label: S1: ", errs)
        errs, _ = self.run_gate(self.mutated(5, bullets=[f"S{k}:" for k in range(1, 6)]))
        self.assertIn("reference card has no ': ' after its label: S1:", errs)

    def test_image_credit_url_and_alt_must_not_be_blank(self):
        img = [{"file": "images/x.png", "alt": "a", "credit": " ", "url": ""}]
        errs, _ = self.run_gate(self.mutated(4, layout="figure", images=img, bullets=["một"]))
        self.assertIn("slide 5: images must be a list of entries with non-empty text values and an http(s) url", errs)

    def test_a_lesson_marked_vietnamese_must_be_written_in_vietnamese(self):
        english = LESSON.replace(FILLER, " ".join(["plain english words without marks"] * 12))
        errs, _ = self.run_gate(lesson=english)
        self.assertTrue(any(e.startswith("the lesson is not Vietnamese with diacritics") for e in errs), errs)
        errs, _ = self.run_gate(lesson=english, expected={**EXPECTED, "language": "en"})
        self.assertFalse(any("Vietnamese" in e for e in errs))

    def test_every_reference_needs_a_url_and_a_placeholder_is_not_an_independent_source(self):
        lesson = LESSON.replace("- [S2] Tác giả 2, Tên nguồn 2, 2001, https://example.org/2", "- [S2] placeholder")
        errs, _ = self.run_gate(lesson=lesson)
        self.assertIn("reference S2 has no http(s) URL", errs)
        self.assertIn("independent sources 3 < 4", errs)
        shallow = {k: v for k, v in EXPECTED.items() if k not in ("section_min_slides", "section_min_exempt")}
        errs, _ = self.run_gate(lesson=lesson, expected=shallow)
        self.assertNotIn("reference S2 has no http(s) URL", errs, "older lessons may cite a book without a URL")
        self.assertIn("independent sources 3 < 4", errs, "but a source without a URL is never counted as independent")

    def test_an_image_url_must_be_a_web_link(self):
        img = [{"file": "images/x.png", "alt": "a", "credit": "c", "url": "unknown"}]
        errs, _ = self.run_gate(self.mutated(4, layout="figure", images=img, bullets=["một"]))
        self.assertIn("slide 5: images must be a list of entries with non-empty text values and an http(s) url", errs)

    def test_a_malformed_slides_file_is_reported_not_crashed(self):
        for bad in ({"title": "Bài thử", "subtitle": "s"}, {"title": "Bài thử", "subtitle": "s", "slides": "x"},
                    {"title": "Bài thử", "subtitle": "s", "slides": []}, {"title": "t", "subtitle": "s", "slides": [1]}, ["x"]):
            (self.root / "lessons" / "L99" / "lesson.md").write_text(LESSON, encoding="utf-8")
            (self.root / "lessons" / "L99" / "slides.json").write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
            (self.root / "lessons" / "L99.expected.json").write_text(json.dumps(EXPECTED, ensure_ascii=False), encoding="utf-8")
            errs, _, _ = gate.check(self.root, "L99")
            with self.subTest(bad=bad):
                self.assertEqual(errs, ['slides.json must be an object with a non-empty list "slides" of objects'])
        (self.root / "lessons" / "L99" / "slides.json").write_text("{", encoding="utf-8")
        self.assertTrue(gate.check(self.root, "L99")[0][0].startswith("slides.json is not valid JSON"))

    def test_the_cover_must_be_drawable(self):
        d = {"title": "Bài thử", "slides": SLIDES}  # no subtitle
        (self.root / "lessons" / "L99" / "lesson.md").write_text(LESSON, encoding="utf-8")
        (self.root / "lessons" / "L99" / "slides.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        (self.root / "lessons" / "L99.expected.json").write_text(json.dumps(EXPECTED, ensure_ascii=False), encoding="utf-8")
        errs, _, _ = gate.check(self.root, "L99")
        self.assertIn("slides.json needs a text subtitle (drawn on the cover)", errs)
        original = gate.gen().cover
        gate.gen().cover = lambda *a, **k: (_ for _ in ()).throw(KeyError("subtitle"))
        self.addCleanup(setattr, gate.gen(), "cover", original)
        errs, _ = self.run_gate()
        self.assertTrue(any(e.startswith("slide 0 (the cover) does not render: KeyError") for e in errs), errs)

    def test_the_reference_list_does_not_count_as_citations(self):
        errs, _ = self.run_gate(expected={**EXPECTED, "min_citations": 7})
        self.assertIn("cites 6", errs)


if __name__ == "__main__":
    unittest.main()

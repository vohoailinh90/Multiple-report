"""scripts/pptx_fonts.py: Moda exports Arial as Inter; the exported PPTX is rewritten back to Arial (owner, 2026-11-08)."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pptx_fonts", ROOT / "scripts" / "pptx_fonts.py")
pf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pf)

SLIDE = ('<?xml version="1.0"?><p:sld xmlns:a="a" xmlns:p="p"><a:p>'
         '<a:r><a:rPr lang="en-US" sz="1650"><a:latin typeface="Inter" pitchFamily="34"/><a:ea typeface="Inter"/><a:cs typeface="Inter"/></a:rPr><a:t>Thân</a:t></a:r>'
         '<a:r><a:rPr lang="en-US" sz="1650"><a:latin typeface="Inter SemiBold"/></a:rPr><a:t>Nhãn</a:t></a:r>'
         '<a:r><a:rPr lang="en-US" sz="7600" b="1"><a:latin typeface="Bricolage Grotesque ExtraBold"/></a:rPr><a:t>Tiêu đề</a:t></a:r>'
         '<a:endParaRPr lang="en-US"><a:latin typeface="Inter"/></a:endParaRPr></a:p></p:sld>')


class PptxFontTests(unittest.TestCase):
    def test_inter_becomes_arial_titles_and_other_parts_are_kept(self):
        path = Path(tempfile.mkdtemp()) / "deck.pptx"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("ppt/slides/slide1.xml", SLIDE)
            z.writestr("ppt/theme/theme1.xml", '<a:latin typeface="Inter"/>')  # not a slide: untouched
        self.assertEqual(pf.patch(str(path)), 2)
        with zipfile.ZipFile(path) as z:
            slide = z.read("ppt/slides/slide1.xml").decode("utf-8")
            self.assertEqual(z.read("ppt/theme/theme1.xml").decode(), '<a:latin typeface="Inter"/>')
        self.assertNotIn("Inter", slide)
        self.assertEqual(slide.count('typeface="Arial"'), 6)
        self.assertIn('typeface="Bricolage Grotesque ExtraBold"', slide)
        self.assertIn('<a:rPr lang="en-US" sz="1650" b="1"><a:latin typeface="Arial"/>', slide, "SemiBold keeps its weight as Arial bold")
        self.assertIn("Tiêu đề", slide)


if __name__ == "__main__":
    unittest.main()

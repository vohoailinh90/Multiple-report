"""Write slides.json and expected.json for a lesson from a compact spec."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def slide(title, section, bullets, notes, layout, tone, sources=()):
    return {"title": title, "section": section, "sources": list(sources), "bullets": bullets,
            "notes": notes, "layout": layout, "tone": tone}


def build(lid, title, subtitle, topic, sources, key_terms, slides, min_words=700, min_cites=6):
    base = ROOT / "lessons" / lid
    body = (base / "lesson.md").read_text(encoding="utf-8")
    import re
    sections = re.findall(r"^## (.+)$", body, re.M)
    (base / "slides.json").write_text(
        json.dumps({"title": title, "subtitle": subtitle, "slides": slides}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    expected = {"id": lid, "title": title, "topic": topic, "sections": sections, "sources": sources,
                "min_words": min_words, "max_words": 30000, "min_citations": min_cites, "key_terms": key_terms,
                "language": "vi", "slides": {"min": 8, "max": 40}}
    (ROOT / "lessons" / f"{lid}.expected.json").write_text(
        json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

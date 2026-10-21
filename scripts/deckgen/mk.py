"""Write slides.json and expected.json for a lesson from a compact spec (used for L01-L06; deeper lessons write slides.json by hand)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# expected.json of a lesson written to the deeper standard (docs/ban-giao-mo-rong-noi-dung.md, section 3).
DEEP = {"min_words": 3500, "max_words": 30000, "min_citations": 12, "min_independent_sources": 4, "min_layouts": 8,
        "section_min_slides": 3, "section_min_exempt": ["Tóm tắt", "Điều cần nhớ", "Lưu ý", "Nguồn tham khảo"],
        "notes_words": [80, 200], "min_images": 4, "language": "vi", "slides": {"min": 30, "max": 60}}


def slide(title, section, bullets, notes, layout, tone, sources=()):
    return {"title": title, "section": section, "sources": list(sources), "bullets": bullets,
            "notes": notes, "layout": layout, "tone": tone}


def write_expected(lid, expected):
    """expected.json is the contract written before lesson.md: never regenerate it from a lesson that may have drifted."""
    path = ROOT / "lessons" / f"{lid}.expected.json"
    if path.exists():
        raise SystemExit(f"{path.name} exists: it is the gate's oracle and is not rewritten to match the lesson")
    path.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build(lid, title, subtitle, topic, sources, key_terms, slides, min_words=700, min_cites=6):
    if (ROOT / "lessons" / f"{lid}.expected.json").exists():
        write_expected(lid, {})  # refuses before anything is written
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
    write_expected(lid, expected)


def deep_expected(lid, title, topic, sections, required_urls, key_terms, **overrides):
    """expected.json for a deeper lesson, from its spec: the writer finds the other sources, the gate counts them."""
    expected = {"id": lid, "title": title, "topic": topic, "sections": sections, "required_urls": required_urls,
                "key_terms": key_terms, **DEEP, **overrides}
    write_expected(lid, expected)

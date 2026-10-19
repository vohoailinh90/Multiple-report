#!/usr/bin/env python3
"""Which lessons still need a PowerPoint deck, and the record of each deck made.

Every lesson in lessons/<id>/ has a slides.json (the approved outline). Its deck is
lessons/<id>/<id>.pptx, built with Moda by Claude, and lessons/<id>/deck.json records the
sha256 of the slides.json it was built from. Whether a deck is missing or stale is a
computable question, so this script answers it rather than a model.

    python3 scripts/decks.py todo                     # ids whose deck is missing or older than slides.json
    python3 scripts/decks.py record L01 --canvas cvs_...   # after saving lessons/L01/L01.pptx
    python3 scripts/decks.py index                    # rewrite lessons/README.md (the table of lessons)
    python3 scripts/decks.py index --check            # exit 1 if lessons/README.md is out of date
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = {
    "than-kinh": "Thần kinh",
    "nao-bo": "Não bộ",
    "triet-hoc": "Triết học",
    "suc-khoe": "Sức khỏe",
    "quan-ly-du-an": "Quản lý dự án",
    "ky-thuat": "Kỹ thuật",
    "khac": "Khác",
}
PPTX_MAGIC = b"PK\x03\x04"  # a .pptx is a zip archive


def lessons_dir(root: Path) -> Path:
    return root / "lessons"


def lesson_ids(root: Path) -> list[str]:
    base = lessons_dir(root)
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir() and (p / "slides.json").is_file())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deck_problem(root: Path, lesson: str) -> str | None:
    """Why this lesson's deck must be (re)built, or None when it is current."""
    folder = lessons_dir(root) / lesson
    pptx, record = folder / f"{lesson}.pptx", folder / "deck.json"
    if not pptx.is_file():
        return "no .pptx"
    if pptx.read_bytes()[:4] != PPTX_MAGIC:
        return ".pptx is not a PowerPoint file"
    if not record.is_file():
        return "no deck.json"
    try:
        built_from = json.loads(record.read_text(encoding="utf-8")).get("slides_sha256")
    except ValueError:
        return "deck.json is not JSON"
    if built_from != sha256(folder / "slides.json"):
        return "slides.json changed since the deck was built"
    return None


def front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    if not lines or lines[0].strip() != "---":
        return {}
    found: dict[str, str] = {}
    for row in lines[1:]:
        if row.strip() == "---":
            break
        key, sep, value = row.partition(":")
        if sep:
            found[key.strip()] = value.strip().strip('"')
    return found


def render_index(root: Path) -> str:
    rows = []
    for lesson in lesson_ids(root):
        meta = front_matter(lessons_dir(root) / lesson / "lesson.md")
        deck = f"[{lesson}.pptx]({lesson}/{lesson}.pptx)" if deck_problem(root, lesson) is None else "chưa có"
        rows.append((TOPICS.get(meta.get("topic", ""), meta.get("topic", "?")), meta.get("date", ""), lesson,
                     meta.get("title", lesson), deck))
    rows.sort()
    out = ["# Mục lục bài học", "",
           "<!-- Sinh bởi `python3 scripts/decks.py index`; đừng sửa tay. -->", "",
           "| Chủ đề | Ngày | Bài | Tiêu đề | Slide |", "|---|---|---|---|---|"]
    out += [f"| {topic} | {date} | [{lesson}]({lesson}/lesson.md) | {title} | {deck} |"
            for topic, date, lesson, title, deck in rows]
    if not rows:
        out.append("| | | | (chưa có bài nào) | |")
    return "\n".join(out) + "\n"


def cmd_todo(root: Path, _args) -> int:
    for lesson in lesson_ids(root):
        problem = deck_problem(root, lesson)
        if problem:
            print(f"{lesson}\t{problem}")
    return 0


def cmd_record(root: Path, args) -> int:
    folder = lessons_dir(root) / args.id
    if not (folder / "slides.json").is_file():
        raise SystemExit(f"{folder}/slides.json not found")
    pptx = folder / f"{args.id}.pptx"
    if not pptx.is_file() or pptx.read_bytes()[:4] != PPTX_MAGIC:
        raise SystemExit(f"{pptx} is missing or not a PowerPoint file: export the deck as PPTX first")
    record = {"slides_sha256": sha256(folder / "slides.json"), "pptx_sha256": sha256(pptx),
              "canvas": args.canvas, "built": _dt.date.today().isoformat()}
    (folder / "deck.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"recorded {folder / 'deck.json'}")
    return 0


def cmd_index(root: Path, args) -> int:
    target = lessons_dir(root) / "README.md"
    text = render_index(root)
    if args.check:
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        if current != text:
            print(f"{target} is out of date: python3 scripts/decks.py index", file=sys.stderr)
            return 1
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target}")
    return 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("todo", help="lessons whose deck is missing or stale")
    record = sub.add_parser("record", help="write deck.json after saving the .pptx")
    record.add_argument("id")
    record.add_argument("--canvas", required=True, help="the Moda canvas id or URL")
    index = sub.add_parser("index", help="rewrite lessons/README.md")
    index.add_argument("--check", action="store_true", help="fail instead of writing when it is out of date")
    args = parser.parse_args(argv)
    return {"todo": cmd_todo, "record": cmd_record, "index": cmd_index}[args.command](root, args)


if __name__ == "__main__":
    sys.exit(main())

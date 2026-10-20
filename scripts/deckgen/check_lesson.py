#!/usr/bin/env python3
"""Structural check of a lesson against the repo rules. Usage: check_lesson.py <root> <id>..."""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])  # repo root, thường "."
bad = 0
for lid in sys.argv[2:]:
    base = root / "lessons" / lid
    body = (base / "lesson.md").read_text(encoding="utf-8")
    sl = json.loads((base / "slides.json").read_text(encoding="utf-8"))
    ex = json.loads((root / "lessons" / f"{lid}.expected.json").read_text(encoding="utf-8"))
    errs = []; warn = []
    fm = re.match(r"---\n(.*?)\n---\n# ([^\n]+)\n", body, re.S)
    if not fm: errs.append("front matter")
    else:
        meta = dict(l.split(": ", 1) for l in fm.group(1).splitlines())
        if meta.get("id") != lid: errs.append("id")
        if meta.get("title") != ex["title"] or fm.group(2) != ex["title"]: errs.append("title mismatch")
        if meta.get("topic") not in {"than-kinh","nao-bo","triet-hoc","suc-khoe","quan-ly-du-an","ky-thuat","khac"}: errs.append("topic")
        if meta.get("topic") != ex["topic"]: errs.append("topic vs expected")
    secs = re.findall(r"^## (.+)$", body, re.M)
    if secs != ex["sections"]: errs.append(f"sections differ: {secs}")
    if secs[-1] != "Nguồn tham khảo": errs.append("last section")
    S = sl["slides"]
    if {s["section"] for s in S} != set(secs): errs.append(f"slide sections differ: {set(secs)^{s['section'] for s in S}}")
    if not (ex["slides"]["min"] <= len(S) <= ex["slides"]["max"]): errs.append("slide count")
    lay = [s["layout"] for s in S]; tone = [s["tone"] for s in S]
    if len(set(lay)) < 5: errs.append("layout kinds")
    if any(a == b for a, b in zip(lay, lay[1:])): errs.append("adjacent layout")
    run = 1  # cover is dark
    prev = "dark"
    for t in tone:
        run = run + 1 if t == prev else 1
        prev = t
        if run > 3: errs.append("tone run"); break
    for s in S:
        if len(s["bullets"]) > 6: errs.append(f"too many bullets: {s['title']}")
        for b in s["bullets"]:
            if len(b) > 160: errs.append(f"bullet>160: {b}")
            if len(b.split()) > 10: warn.append(f"bullet>10 words: {b}")
    w = len(body.split()); c = len(re.findall(r"\[S\d+\]", body))
    if not (ex["min_words"] <= w <= ex["max_words"]): errs.append(f"words {w}")
    if c < ex["min_citations"]: errs.append(f"cites {c}")
    for term in ex["key_terms"]:
        if term not in body: errs.append(f"key term missing: {term}")
    refs = set(re.findall(r"^- \[(S\d+)\] ", body, re.M))
    used = set(re.findall(r"\[(S\d+)\]", body.split("## Nguồn tham khảo")[0]))
    if used - refs: errs.append(f"cited but not listed: {used-refs}")
    if refs - used: errs.append(f"listed but never cited: {refs-used}")
    if set(ex["sources"]) != refs: errs.append("expected sources differ")
    for k, url in ex["sources"].items():
        if url and url not in body: errs.append(f"url of {k} not in lesson")
    health = meta.get("topic") in {"suc-khoe"} or "Lưu ý" in ex["sections"]
    print(f"{lid}: {len(S)} slides, {len(set(lay))} layouts, {w} words, {c} cites -> {'OK' if not errs else errs}{' WARN ' + str(warn) if warn else ''}")
    bad += bool(errs)
sys.exit(1 if bad else 0)

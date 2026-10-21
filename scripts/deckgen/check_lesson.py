#!/usr/bin/env python3
"""Structural check of a lesson against the repo rules. Usage: check_lesson.py <root> <id>...

Reads lessons/<id>/lesson.md, lessons/<id>/slides.json and lessons/<id>.expected.json. Keys of expected.json:
  id, title, topic, sections, min_words, max_words, min_citations, key_terms, slides {min, max}   (always)
  sources                   {"S1": url}: the exact reference list (older lessons L00-L06)
  required_urls             [url]: urls the reference list must contain; other sources are allowed
  min_independent_sources   references whose url is not the textbook (rotel.pressbooks.pub)
  min_layouts               kinds of layout (default 5)
  section_min_slides        slides per `## ` section, except those in section_min_exempt
  notes_words [lo, hi]      warn when a slide's notes fall outside
  min_images                warn when the slides show fewer figures
Errors fail the gate; warnings are printed and must be explained, not ignored.
"""
import importlib.util, json, re, sys
from pathlib import Path

TOPICS = {"than-kinh", "nao-bo", "triet-hoc", "suc-khoe", "quan-ly-du-an", "ky-thuat", "khac"}
OLD = {"sequence-diagram", "flow", "two-column-comparison", "lookup-table", "card-grid", "numbered-rows",
       "connection-diagram", "layers", "timeline", "one-big-number", "one-highlighted-sentence", "figure"}
BODY = {"explainer": (40, 130, 60, 110), "annotated-figure": (30, 80, 40, 70)}  # hard lo, hard hi, target lo, target hi
LAYOUTS = OLD | set(BODY) | {"profile-card", "references"}
# bullets each renderer in gen.py draws without crashing or dropping content: (min, max)
BULLETS = {"card-grid": (1, 4), "flow": (1, 5), "two-column-comparison": (2, 6), "lookup-table": (1, 6),
           "numbered-rows": (1, 6), "layers": (1, 6), "timeline": (1, 6), "connection-diagram": (1, 4),
           "one-big-number": (1, 3), "one-highlighted-sentence": (1, 4), "sequence-diagram": (1, 6),
           "figure": (1, 4), "explainer": (0, 3), "annotated-figure": (0, 3), "profile-card": (0, 0),
           "references": (1, 18)}
HEAVY = {"explainer", "profile-card", "annotated-figure"}  # at most two of these in a row (handoff 6.2: interleave with diagrams)
TEXTBOOK = "rotel.pressbooks.pub"
CITE = re.compile(r"\[(S\d+)\]")
TONES = {"light", "dark"}
URL = re.compile(r"https?://[^\s/$.?#][^\s]*\.[^\s]+|https?://localhost\S*", re.I)
VI_MARKS = re.compile("[ăâđêôơưàáạảãằắặẳẵầấậẩẫèéẹẻẽềếệểễìíịỉĩòóọỏõồốộổỗờớợởỡùúụủũừứựửữỳýỵỷỹ]", re.I)
IMG_KEYS = ("file", "alt", "credit", "url")
FIELDS = {"title": str, "section": str, "layout": str, "tone": str, "sources": list, "bullets": list, "notes": str}
DATE = re.compile(r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])")
_gen = None


def gen():
    """scripts/deckgen/gen.py, loaded once: the gate asks the renderer whether a slide's text fits its boxes."""
    global _gen
    if _gen is None:
        spec = importlib.util.spec_from_file_location("deckgen_gen", Path(__file__).with_name("gen.py"))
        _gen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_gen)
    return _gen


def words(t):
    return len(t.split())


def overflow(root, lid, S, sl_path):
    """A slide whose text cannot fit its boxes even at the smallest font gen.py allows (the 160-character limit alone allows it)."""
    opts_file = Path(root) / "scripts" / "deckgen" / "opts" / f"{lid}.json"
    opts = json.loads(opts_file.read_text(encoding="utf-8")) if opts_file.is_file() else {}
    g, errs, warn = gen(), [], []
    for i, s in enumerate([None, *S]):  # page 0 is the cover
        if s is None:
            s = {"title": "the cover", "layout": "cover"}
        elif s.get("layout") not in LAYOUTS or s.get("tone") not in TONES:
            continue  # reported above
        try:
            markup = g.page(lid, i, opts, sl_path)
        except SystemExit as e:
            (warn if "has no Moda id" in str(e) else errs).append(f"slide {i} ({s['title']}): {e}")  # a new figure gets its id when the deck is built
            continue
        except Exception as e:  # the documented generation command would fail the same way
            errs.append(f"slide {i} ({s['title']}) does not render: {type(e).__name__}: {e}")
            continue
        errs += [f"text does not fit its box on {s['layout']} ({s['title']}): {t[:50]}" for t in g.overflows(markup)]
    return errs, warn


def check(root, lid):
    """(errors, warnings, summary line) for one lesson."""
    root = Path(root)
    base = root / "lessons" / lid
    body = (base / "lesson.md").read_text(encoding="utf-8")
    sl_path = base / "slides.json"
    try:
        sl = json.loads(sl_path.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"slides.json is not valid JSON: {e}"], [], f"{lid}: slides.json is malformed"
    if not (isinstance(sl, dict) and isinstance(sl.get("slides"), list) and sl["slides"]
            and all(isinstance(s, dict) for s in sl["slides"])):
        return ['slides.json must be an object with a non-empty list "slides" of objects'], [], f"{lid}: slides.json is malformed"
    ex = json.loads((root / "lessons" / f"{lid}.expected.json").read_text(encoding="utf-8"))
    errs, warn = [], []
    fm = re.match(r"---\n(.*?)\n---\n# ([^\n]+)\n", body, re.S)
    if not fm:
        errs.append("front matter")
    else:
        meta = dict(l.split(": ", 1) for l in fm.group(1).splitlines())
        if meta.get("id") != lid: errs.append("id")
        if meta.get("title") != ex["title"] or fm.group(2) != ex["title"]: errs.append("title mismatch")
        if meta.get("topic") not in TOPICS: errs.append("topic")
        if meta.get("topic") != ex["topic"]: errs.append("topic vs expected")
        if not DATE.fullmatch(meta.get("date", "")): errs.append(f"date must be YYYY-MM-DD, found {meta.get('date')!r}")
    if sl.get("title") != ex["title"]: errs.append(f"deck title {sl.get('title')!r} differs from the lesson title")
    secs = re.findall(r"^## (.+)$", body, re.M)
    if secs != ex["sections"]: errs.append(f"sections differ: {secs}")
    if not secs or secs[-1] != "Nguồn tham khảo": errs.append("last section")
    text, _, reflist = body.partition("\n## Nguồn tham khảo\n")
    refs = dict(re.findall(r"^- \[(S\d+)\] (.+)$", reflist, re.M))
    used = set(CITE.findall(text))
    if used - set(refs): errs.append(f"cited but not listed: {sorted(used - set(refs))}")
    if set(refs) - used: errs.append(f"listed but never cited: {sorted(set(refs) - used)}")
    if "sources" in ex:
        if set(ex["sources"]) != set(refs): errs.append("expected sources differ")
        for k, url in ex["sources"].items():
            if url and url not in refs.get(k, ""): errs.append(f"url of {k} is not on its own reference line")
    for url in ex.get("required_urls", []):
        if not any(url in r for r in refs.values()): errs.append(f"required source missing: {url}")
    if "section_min_slides" in ex:  # a deep lesson gives every source a URL; older lessons cite books and articles without one
        errs += [f"reference {k} has no http(s) URL" for k, r in refs.items() if not URL.search(r)]
    indep = [k for k, r in refs.items() if TEXTBOOK not in r and URL.search(r)]
    if len(indep) < ex.get("min_independent_sources", 0):
        errs.append(f"independent sources {len(indep)} < {ex['min_independent_sources']}")
    for img in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", body):
        if not (base / img).is_file(): errs.append(f"image in lesson.md missing: {img}")

    S = sl["slides"]
    bad = [f"slide {i} lacks {k!r} of the right type" for i, s in enumerate(S, 1) for k, kind in FIELDS.items()
           if not isinstance(s.get(k), kind)]
    bad += [f"slide {i} has a bullet that is not text" for i, s in enumerate(S, 1) if isinstance(s.get("bullets"), list)
            and not all(isinstance(b, str) for b in s["bullets"])]
    bad += [f"slide {i} has a source that is not text" for i, s in enumerate(S, 1) if isinstance(s.get("sources"), list)
            and not all(isinstance(b, str) for b in s["sources"])]
    bad += [f"slide {i}: body is not text" for i, s in enumerate(S, 1) if "body" in s and not isinstance(s["body"], str)]
    bad += [f"slide {i}: facts must be a list of {{label, text}} with text values" for i, s in enumerate(S, 1) if "facts" in s
            and not (isinstance(s["facts"], list) and all(isinstance(f, dict) and isinstance(f.get("label"), str)
                                                          and isinstance(f.get("text"), str) for f in s["facts"]))]
    bad += [f"slide {i}: images must be a list of entries with non-empty text values and an http(s) url" for i, s in enumerate(S, 1) if "images" in s
            and not (isinstance(s["images"], list) and all(isinstance(m, dict) and all(isinstance(m.get(k), str) and m[k].strip() for k in IMG_KEYS)
                                                           and URL.fullmatch(m["url"].strip())
                                                           for m in s["images"]))]
    if not isinstance(sl.get("subtitle"), str): bad.append("slides.json needs a text subtitle (drawn on the cover)")
    if bad:
        return errs + bad, warn, f"{lid}: slides.json is incomplete"
    if {s["section"] for s in S} != set(secs): errs.append(f"slide sections differ: {set(secs) ^ {s['section'] for s in S}}")
    order = [secs.index(s["section"]) for s in S if s["section"] in secs]
    if order != sorted(order): errs.append("slides do not follow the order of the lesson's sections")
    if S and S[-1]["section"] != "Nguồn tham khảo": errs.append("the last slide must be the sources slide (section Nguồn tham khảo)")
    if S and "section_min_slides" in ex and S[-1]["layout"] != "references":  # lessons of the deep standard list their sources in full
        errs.append("the last slide of a deep lesson must use the references layout")
    if any(s["layout"] == "references" for s in S[:-1]): errs.append("a references slide must be the last slide")
    if not (ex["slides"]["min"] <= len(S) <= ex["slides"]["max"]): errs.append(f"slide count {len(S)}")
    lay = [s["layout"] for s in S]; tone = [s["tone"] for s in S]
    errs += [f"tone {t!r} is not light or dark: {s['title']}" for s, t in zip(S, tone) if t not in TONES]
    if len(set(lay)) < ex.get("min_layouts", 5): errs.append(f"layout kinds {len(set(lay))}")
    if any(a == b for a, b in zip(lay, lay[1:])): errs.append("adjacent layout")
    heavy = [i for i in range(len(lay) - 2) if set(lay[i:i + 3]) <= HEAVY]
    if heavy: errs.append(f"three text-heavy slides in a row from slide {heavy[0] + 1}")
    run, prev = 1, "dark"  # the cover is dark
    for t in tone:
        run = run + 1 if t == prev else 1
        prev = t
        if run > 3: errs.append("tone run"); break
    if "section_min_slides" in ex:
        exempt = set(ex.get("section_min_exempt", []))
        for sec in secs:
            if sec in exempt: continue
            mine = [s for s in S if s["section"] == sec]
            if len(mine) < ex["section_min_slides"]: errs.append(f"section has {len(mine)} slides: {sec}")
            if not any(s.get("body") or s.get("facts") for s in mine): warn.append(f"section without explainer/profile-card: {sec}")
    lo_hi = ex.get("notes_words")
    figures = 0
    for s in S:
        name, L = s["title"], s["layout"]
        bl = s.get("bullets", [])
        if L not in LAYOUTS: errs.append(f"unknown layout {L}: {name}"); continue
        if len(name) > 90: errs.append(f"title>90: {name}")
        lo, hi = BULLETS[L]  # every layout in LAYOUTS has a renderer in gen.py and an entry here (tested)
        if not lo <= len(bl) <= hi: errs.append(f"{L} draws {lo}-{hi} bullets, found {len(bl)}: {name}")
        if L == "references":
            errs += [f"reference>110: {b}" for b in bl if len(b) > 110]
            labels = [b.split(": ", 1)[0] if ": " in b else b for b in bl]  # the card label is what gen.split_kv puts before ": "
            if sorted(labels) != sorted(refs):
                errs.append(f"references slide lists {sorted(labels)}, the reference list has {sorted(refs)}")
        else:
            errs += [f"bullet>160: {b}" for b in bl if len(b) > 160]
        if L == "annotated-figure": errs += [f"gloss>70: {b}" for b in bl if len(b) > 70]
        if "body" in s:
            if L not in BODY: errs.append(f"body is not drawn by {L}: {name}")
            else:
                hard_lo, hard_hi, lo, hi = BODY[L]
                w = words(s["body"].replace("**", ""))
                if not hard_lo <= w <= hard_hi: errs.append(f"body {w} words: {name}")
                elif not lo <= w <= hi: warn.append(f"body {w} words (aim {lo}-{hi}): {name}")
                if s["body"].count("**") % 2: errs.append(f"unpaired ** in body: {name}")
        elif L in BODY:
            errs.append(f"{L} needs a body: {name}")
        if "facts" in s:
            f = s["facts"]
            if L != "profile-card": errs.append(f"facts are not drawn by {L}: {name}")
            elif not 3 <= len(f) <= 6: errs.append(f"profile-card needs 3-6 facts: {name}")
            for fact in f:
                if set(fact) != {"label", "text"}: errs.append(f"fact keys {sorted(fact)}: {name}"); continue
                if len(fact["label"]) > 40: errs.append(f"fact label>40: {fact['label']}")
                if len(fact["text"]) > 160: errs.append(f"fact text>160: {fact['text']}")
        elif L == "profile-card":
            errs.append(f"profile-card needs facts: {name}")
        if L in ("figure", "annotated-figure"):
            if not s.get("images"): errs.append(f"{L} needs images: {name}")
        elif s.get("images"):
            errs.append(f"images are drawn only by figure and annotated-figure: {name}")
        for img in s.get("images", []):
            figures += 1
            if not {"file", "alt", "credit", "url"} <= set(img): errs.append(f"image entry incomplete: {name}")
            elif not (base / img["file"]).is_file(): errs.append(f"image missing: {img['file']}")
        drawn = " ".join([s.get("body", ""), *bl, *(x["text"] for x in s.get("facts", []) if "text" in x)])
        for k in set(s.get("sources", [])) | set(CITE.findall(drawn)):
            if k not in refs: errs.append(f"slide cites {k}, not in the reference list: {name}")
        if s["section"] != "Nguồn tham khảo":  # the footer lists `sources` only, so a citation drawn in the text must be there too
            errs += [f"slide text cites {k} but its sources omit it: {name}" for k in sorted(set(CITE.findall(drawn)) - set(s.get("sources", [])))]
        if lo_hi and s["section"] != "Nguồn tham khảo" and not lo_hi[0] <= words(s.get("notes", "")) <= lo_hi[1]:
            warn.append(f"notes {words(s.get('notes', ''))} words: {name}")
    over_errs, over_warn = overflow(root, lid, S, sl_path)
    errs += over_errs; warn += over_warn
    if figures < ex.get("min_images", 0): warn.append(f"{figures} figures < {ex['min_images']}")
    if ex.get("language") == "vi":
        prose = [w for w in re.sub(r"[^\w\s]", " ", text).split() if w.isalpha()]
        marked = sum(1 for w in prose if VI_MARKS.search(w))
        if not prose or marked / len(prose) < 0.25: errs.append(f"the lesson is not Vietnamese with diacritics ({marked} of {len(prose)} words carry them)")
    w = words(body); c = len(CITE.findall(text))
    if not ex["min_words"] <= w <= ex["max_words"]: errs.append(f"words {w}")
    if c < ex["min_citations"]: errs.append(f"cites {c}")
    for term in ex["key_terms"]:
        if term not in body: errs.append(f"key term missing: {term}")
    explained = sum(1 for s in S if s.get("body") or s.get("facts"))
    summary = (f"{lid}: {len(S)} slides ({explained} with body/facts), {len(set(lay))} layouts, {w} words, "
               f"{c} cites, {len(refs)} sources ({len(indep)} independent), {figures} figures")
    return errs, warn, summary


def main(argv):
    root, bad = argv[1], 0
    for lid in argv[2:]:
        errs, warn, summary = check(root, lid)
        print(f"{summary} -> {'OK' if not errs else errs}")
        for w in warn:
            print(f"  WARN {w}")
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

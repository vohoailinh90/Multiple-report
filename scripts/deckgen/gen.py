#!/usr/bin/env python3
"""Moda markup for one page of a lesson deck, from lessons/<id>/slides.json.

usage: gen.py <lesson-id> <page 0..N> [--opts file.json] [--slides file.json]
page 0 is the cover, pages 1..N follow slides.json. Prints the <content>...</content> markup.
--slides reads another slides.json (the demo deck in tests/fixtures/deckgen/). Images are placed by <lesson id>/<file> from file_ids.json.
opts file: {"topic_label": "...", "question": "...", "motif": "...", "big": {"3": "86 tỷ"},
            "actors": {"6": ["A","B","C"]}, "mark": {"5": "có hoặc không"}, "concepts": ["hạnh nhân", ...]}
"concepts" gives each concept its colour (concept k takes accent (n + k) mod 4); a **term** in a body that names
a concept is drawn in that colour, any other **term** in the slide's first accent.
"""
import json, math, re, sys
from xml.sax.saxutils import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIGHT = dict(bg="#F3EEE3", ink="#14161C", card="#E8E0CF", diag="#FBF8F2", diagline="#DDD5C1", sub="#6B6A66",
             acc=["#1F3FD1", "#B45309", "#0F766E", "#E8472B"], tint=["#DDE3FA", "#F3DFB8", "#CFE8E2", "#F8D9D0"])
DARK = dict(bg="#14161C", ink="#F3EEE3", card="#1E212B", diag="#1E212B", diagline="#2C3040", sub="#9AA0B5",
            acc=["#7C93FF", "#FFB454", "#3DD6A0", "#FF6A4D"], tint=["#262C4A", "#4A3A22", "#1C4236", "#4A2A24"])
RED_LIGHT, RED_DARK = "#E8472B", "#FF6A4D"
M = 96  # margin
FLOOR = 22  # deck-style: nothing smaller
CITE = re.compile(r"(\[S\d+\](?:\s*\[S\d+\])*)")


def x(t):
    return escape(t, {'"': "&quot;"})


def pal(tone):
    return LIGHT if tone == "light" else DARK


def acc(p, n, k):
    return p["acc"][(n + k) % 4], p["tint"][(n + k) % 4]


def lines(text, w, size, cw):
    """Lines the text wraps to in a box w px wide, from an average glyph width of cw em."""
    per = max(1, int(w / (size * cw)))
    n = 0
    for para in text.split("\n"):
        n += 1; cur = 0
        for word in para.split():
            cur = len(word) if cur == 0 else cur + 1 + len(word)
            if cur > per and cur != len(word):
                n += 1; cur = len(word)
            while cur > per:
                n += 1; cur -= per
    return n


def fit(text, w, h, size, lh=1.25, floor=FLOOR, cw=0.55, max_lines=None):
    """Largest font size from size down (step 2, not below floor) whose wrapped text fits w x h in at most max_lines lines."""
    while size > floor and (lines(text, w, size, cw) * size * lh > h or (max_lines and lines(text, w, size, cw) > max_lines)):
        size -= 2
    return max(size, floor)


def rich_height(text, w, size, lh, spacing, cw=0.55):
    """Height of a body drawn as one <p> per blank-line-separated paragraph, `spacing` px between paragraphs."""
    paras = [q for q in re.split(r"\n\s*\n", plain(text).strip())]
    return sum(lines(q, w, size, cw) for q in paras) * size * lh + spacing * (len(paras) - 1)


def fit_rich(text, w, h, size, lh, floor, spacing=0, cw=0.55):
    """Largest font size from size down (step 2, not below floor) whose paragraphs, with their spacing, fit w x h."""
    while size > floor and rich_height(text, w, size, lh, spacing, cw) > h:
        size -= 2
    return max(size, floor)


def title(p, text, y=72, w=1728, h=190):
    size = fit(text, w, h, 76, 1.08, 56, 0.58)
    return (f'<text x="{M}" y="{y}" width="{w}" height="{h}" font-family="Bricolage Grotesque" font-weight="800" '
            f'font-size="{size}" color="{p["ink"]}" line-height="1.08" max-lines="2" vertical-align="top">{x(text)}</text>')


def footer(p, lid, i, total):
    red = RED_LIGHT if p is LIGHT else RED_DARK
    ink = p["ink"]
    step = min(24, 960 / total)  # long decks: closer dots, so the label never reaches the logo corner
    r1, r0 = min(8, step / 3), min(6, step / 4)
    dots = (f'<repeat count="{total}" as="d"><ellipse cx="{{105+d*{step:g}}}" cy="1010" rx="{{d=={i}?{r1:g}:{r0:g}}}" '
            f'ry="{{d=={i}?{r1:g}:{r0:g}}}" fill="{{d=={i}?\'{red}\':\'{ink}\'}}" opacity="{{d=={i}?1:0.28}}"/></repeat>')
    tx = round(M + total * step + 24)
    return dots + (f'\n<text x="{tx}" y="994" width="520" height="32" font-size="24" color="{p["sub"]}" vertical-align="middle" '
                   f'max-lines="1">Multiple-report · {lid} · {i + 1:02d}/{total:02d}</text>')


def split_kv(b):
    if ": " in b:
        k, v = b.split(": ", 1)
        return k, v
    return None, b


def rich(text, p, n, a, o):
    """Body text as Moda html: **term** in its concept colour, [Sn] in the secondary colour, blank line = paragraph."""
    concepts = [c.lower() for c in o.get("concepts", [])]

    def colour(term):
        t = term.lower()
        for k, c in enumerate(concepts):
            if c in t or t in c:
                return acc(p, n, k)[0]
        return a

    paras = []
    for para in re.split(r"\n\s*\n", text.strip()):
        out = []
        for j, part in enumerate(para.split("**")):
            if j % 2:
                out.append(f'<span style="color: {colour(part)}; font-weight: 700">{x(part)}</span>')
                continue
            for q, bit in enumerate(CITE.split(part)):
                out.append(f'<span style="color: {p["sub"]}">{x(bit)}</span>' if q % 2 else x(bit))
        paras.append("<p>" + "".join(out) + "</p>")
    return "".join(paras)


def plain(text):
    return text.replace("**", "")


def card_grid(p, n, s, o):
    bl = s["bullets"]; c = len(bl); gap = 36
    w = (1728 - gap * (c - 1)) / c
    out = []
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        xx = M + k * (w + gap)
        kk, vv = split_kv(b)
        out.append(f'<rectangle x="{xx:.0f}" y="320" width="{w:.0f}" height="520" corner-radius="28" fill="{p["card"]}"/>')
        out.append(f'<rectangle x="{xx:.0f}" y="320" width="{w:.0f}" height="16" corner-radius="8" fill="{a}"/>')
        out.append(f'<text x="{xx + 40:.0f}" y="372" width="{w - 80:.0f}" height="130" font-family="Bricolage Grotesque" font-weight="800" font-size="96" color="{a}" max-lines="1">{k + 1:02d}</text>')
        if kk:
            hs = fit(kk, w - 80, 110, 36, 1.2, 26, 0.58, 2)
            out.append(f'<text x="{xx + 40:.0f}" y="510" width="{w - 80:.0f}" height="110" font-weight="700" font-size="{hs}" color="{p["ink"]}" max-lines="2">{x(kk)}</text>')
            vs = fit(vv, w - 80, 200, 34, 1.3)
            out.append(f'<text x="{xx + 40:.0f}" y="630" width="{w - 80:.0f}" height="200" font-size="{vs}" color="{p["sub"]}" line-height="1.3">{x(vv)}</text>')
        else:
            bs = fit(b, w - 80, 320, 42, 1.25, 24, 0.57)
            out.append(f'<text x="{xx + 40:.0f}" y="510" width="{w - 80:.0f}" height="320" font-weight="600" font-size="{bs}" color="{p["ink"]}" line-height="1.25">{x(b)}</text>')
    return out


def flow(p, n, s, o):
    bl = s["bullets"]; c = len(bl); aw = 70
    w = (1728 - aw * (c - 1)) / c
    out = []
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        xx = M + k * (w + aw)
        out.append(f'<rectangle x="{xx:.0f}" y="360" width="{w:.0f}" height="400" corner-radius="28" fill="{p["diag"]}" stroke="{p["diagline"]}" stroke-width="3"/>')
        out.append(f'<ellipse cx="{xx + 64:.0f}" cy="424" rx="34" ry="34" fill="{a}"/>')
        out.append(f'<text x="{xx + 30:.0f}" y="390" width="68" height="68" font-weight="800" font-size="34" color="{"#FFFFFF" if p is LIGHT else "#14161C"}" text-align="center" vertical-align="middle">{k + 1}</text>')
        bs = fit(b, w - 64, 260, 36, 1.25, FLOOR, 0.57)
        out.append(f'<text x="{xx + 32:.0f}" y="480" width="{w - 64:.0f}" height="260" font-weight="600" font-size="{bs}" color="{p["ink"]}" line-height="1.25">{x(b)}</text>')
        if k < c - 1:
            ax = xx + w + 8
            out.append(f'<line x1="{ax:.0f}" y1="560" x2="{ax + aw - 16:.0f}" y2="560" stroke="{p["sub"]}" stroke-width="5" arrow-end="triangle"/>')
    return out


def two_col(p, n, s, o):
    bl = s["bullets"]; out = []
    cols = bl[:2]; rest = bl[2:]
    w = 846
    for k, b in enumerate(cols):
        a, t = acc(p, n, k)
        xx = M + k * (w + 36)
        kk, vv = split_kv(b)
        out.append(f'<rectangle x="{xx}" y="300" width="{w}" height="{440 if rest else 560}" corner-radius="28" fill="{t}"/>')
        out.append(f'<rectangle x="{xx}" y="300" width="14" height="{440 if rest else 560}" corner-radius="7" fill="{a}"/>')
        h = kk if kk else ("Một phía" if k == 0 else "Phía kia")
        hs = fit(h, w - 96, 100, 56, 1.1, 36, 0.6, 2)
        out.append(f'<text x="{xx + 48}" y="336" width="{w - 96}" height="100" font-family="Bricolage Grotesque" font-weight="800" font-size="{hs}" color="{a}" max-lines="2">{x(h)}</text>')
        vh = 240 if rest else 330
        vs = fit(vv, w - 96, vh, 42, 1.3)
        out.append(f'<text x="{xx + 48}" y="450" width="{w - 96}" height="{vh}" font-size="{vs}" color="{p["ink"]}" line-height="1.3">{x(vv)}</text>')
    if rest:
        line = " · ".join(rest)
        rs = fit(line, 1648, 130, 38, 1.2, 24, 0.57)
        out.append(f'<rectangle x="{M}" y="780" width="1728" height="130" corner-radius="24" fill="{p["card"]}"/>')
        out.append(f'<text x="{M + 40}" y="780" width="1648" height="130" font-weight="600" font-size="{rs}" color="{p["ink"]}" vertical-align="middle" line-height="1.2">{x(line)}</text>')
    return out


def lookup(p, n, s, o):
    bl = s["bullets"]; out = []
    rh = min(140, 570 // max(len(bl), 1))
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        yy = 290 + k * (rh + 14)
        kk, vv = split_kv(b)
        out.append(f'<rectangle x="{M}" y="{yy}" width="1728" height="{rh}" corner-radius="20" fill="{p["card"] if k % 2 == 0 else p["diag"]}" stroke="{p["diagline"]}" stroke-width="2"/>')
        out.append(f'<rectangle x="{M}" y="{yy}" width="14" height="{rh}" corner-radius="7" fill="{a}"/>')
        if kk:
            ks = fit(kk, 620, rh - 16, 40, 1.15, 24, 0.6)
            vs = fit(vv, 1000, rh - 16, 36, 1.2)
            out.append(f'<text x="{M + 40}" y="{yy}" width="620" height="{rh}" font-weight="800" font-size="{ks}" color="{a}" vertical-align="middle" line-height="1.15">{x(kk)}</text>')
            out.append(f'<text x="{M + 700}" y="{yy}" width="1000" height="{rh}" font-size="{vs}" color="{p["ink"]}" vertical-align="middle" line-height="1.2">{x(vv)}</text>')
        else:
            bs = fit(b, 1640, rh - 16, 40, 1.2, FLOOR, 0.58)
            out.append(f'<text x="{M + 40}" y="{yy}" width="1640" height="{rh}" font-weight="700" font-size="{bs}" color="{p["ink"]}" vertical-align="middle" line-height="1.2">{x(b)}</text>')
    return out


def numbered(p, n, s, o):
    bl = s["bullets"]; out = []
    rh = min(150, 620 // max(len(bl), 1))
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        yy = (250 if len(bl) >= 5 else 280) + k * (rh + 12)
        bs = fit(b, 1470, rh - 28, 40 if rh > 120 else 36, 1.2, FLOOR, 0.57)
        out.append(f'<text x="{M}" y="{yy}" width="170" height="{rh}" font-family="Bricolage Grotesque" font-weight="800" font-size="{min(116, rh - 14)}" color="{a}" vertical-align="middle" max-lines="1">{k + 1}</text>')
        out.append(f'<rectangle x="{M + 190}" y="{yy + 10}" width="1538" height="{rh - 20}" corner-radius="20" fill="{p["card"]}"/>')
        out.append(f'<text x="{M + 230}" y="{yy + 10}" width="1470" height="{rh - 20}" font-weight="600" font-size="{bs}" color="{p["ink"]}" vertical-align="middle" line-height="1.2">{x(b)}</text>')
    return out


def connection(p, n, s, o, idx):
    bl = s["bullets"]; c = len(bl); out = []
    cx, cy = 960, 590
    pos = {1: [(960, 330)], 2: [(420, 590), (1500, 590)], 3: [(380, 400), (1540, 400), (960, 850)],
           4: [(380, 380), (1540, 380), (380, 800), (1540, 800)]}[min(c, 4)]
    for k, b in enumerate(bl[:4]):
        a, t = acc(p, n, k)
        px, py = pos[k]
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="{a}" stroke-width="6"/>')
    centre = o.get("center", {}).get(str(idx), s["title"])
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="230" ry="150" fill="{p["ink"]}"/>')
    out.append(f'<text x="{cx - 200}" y="{cy - 120}" width="400" height="240" font-family="Bricolage Grotesque" font-weight="800" font-size="{fit(centre, 400, 240, 44, 1.1, 26, 0.6)}" color="{p["bg"]}" text-align="center" vertical-align="middle" line-height="1.1">{x(centre)}</text>')
    for k, b in enumerate(bl[:4]):
        a, t = acc(p, n, k)
        px, py = pos[k]
        out.append(f'<rectangle x="{px - 270}" y="{py - 80}" width="540" height="160" corner-radius="24" fill="{p["diag"]}" stroke="{a}" stroke-width="5"/>')
        out.append(f'<text x="{px - 240}" y="{py - 80}" width="480" height="160" font-weight="700" font-size="{fit(b, 480, 144, 34, 1.15, FLOOR, 0.58)}" color="{p["ink"]}" text-align="center" vertical-align="middle" line-height="1.15">{x(b)}</text>')
    return out


def layers(p, n, s, o):
    bl = s["bullets"]; out = []
    rh = min(170, (630 - 16 * (len(bl) - 1)) // max(len(bl), 1))  # the last layer ends by y=930, above the source line at 944
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        yy = 300 + k * (rh + 16)
        inset = k * 70
        bw = 1728 - 2 * inset - 80
        out.append(f'<rectangle x="{M + inset}" y="{yy}" width="{1728 - 2 * inset}" height="{rh}" corner-radius="22" fill="{t}" stroke="{a}" stroke-width="4"/>')
        out.append(f'<text x="{M + inset + 40}" y="{yy}" width="{bw}" height="{rh}" font-weight="700" font-size="{fit(b, bw, rh - 16, 38, 1.2, FLOOR, 0.58)}" color="{p["ink"]}" vertical-align="middle" text-align="center" line-height="1.2">{x(b)}</text>')
    return out


def timeline(p, n, s, o):
    bl = s["bullets"]; c = len(bl); out = []
    y0 = 610
    out.append(f'<line x1="{M}" y1="{y0}" x2="{M + 1728}" y2="{y0}" stroke="{p["sub"]}" stroke-width="6"/>')
    step = 1728 / c
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        cx = M + step * k + step / 2
        up = k % 2 == 0
        out.append(f'<ellipse cx="{cx:.0f}" cy="{y0}" rx="26" ry="26" fill="{a}"/>')
        ty = y0 - 250 if up else y0 + 60
        out.append(f'<line x1="{cx:.0f}" y1="{y0 + (-26 if up else 26)}" x2="{cx:.0f}" y2="{y0 + (-60 if up else 60)}" stroke="{a}" stroke-width="4"/>')
        out.append(f'<text x="{cx - step / 2 + 20:.0f}" y="{ty}" width="{step - 40:.0f}" height="190" font-weight="600" font-size="{fit(b, step - 40, 190, 36, 1.2, FLOOR, 0.57)}" color="{p["ink"]}" text-align="center" vertical-align="{"bottom" if up else "top"}" line-height="1.2">{x(b)}</text>')
    return out


def big(p, n, s, o, idx):
    a, t = acc(p, n, 0)
    num = o.get("big", {}).get(str(idx), s["title"])
    size = 300
    while size > 120 and len(num) * size * 0.6 > 1728:
        size -= 20
    one_line = len(num) * size * 0.6 <= 1728
    if not one_line:  # a long value (the slide title when opts has no "big") wraps and shrinks instead of being clipped
        size = fit(num, 1728, 360, 120, 1.0, 40, 0.6)
    out = [f'<text x="{M}" y="260" width="1728" height="360" font-family="Bricolage Grotesque" font-weight="800" font-size="{size}" color="{a}"{" max-lines=" + chr(34) + "1" + chr(34) if one_line else ""} line-height="1.0" vertical-align="middle">{x(num)}</text>']
    bl = list(s["bullets"][:3])
    if bl and bl[0].startswith(num):
        bl[0] = bl[0][len(num):].strip()
    lines_ = [z for z in bl if z]
    y, room = 640, 280  # under the number, above the sources line
    for b in lines_:
        h = room / len(lines_) - 10
        out.append(f'<text x="{M}" y="{y:.0f}" width="1728" height="{h:.0f}" font-weight="600" font-size="{fit(b, 1728, h, 44, 1.15, FLOOR, 0.57)}" color="{p["ink"]}" line-height="1.15" vertical-align="top">{x(b)}</text>')
        y += h + 10
    return out


def highlight(p, n, s, o, idx):
    a, t = acc(p, n, 0)
    sent = s["bullets"][0]
    size = fit(sent, 1660, 440, 92, 1.12, 52, 0.58)
    out = [f'<rectangle x="{M}" y="310" width="16" height="420" corner-radius="8" fill="{a}"/>']
    mark = o.get("mark", {}).get(str(idx))
    if mark and mark in sent:
        pre, post = sent.split(mark, 1)
        html = f'{x(pre)}<span style="color: {a}">{x(mark)}</span>{x(post)}'
        out.append(f'<text x="{M + 60}" y="300" width="1660" height="440" format="html" font-family="Bricolage Grotesque" font-weight="800" font-size="{size}" color="{p["ink"]}" line-height="1.12" vertical-align="middle"><p>{html}</p></text>')
    else:
        out.append(f'<text x="{M + 60}" y="300" width="1660" height="440" font-family="Bricolage Grotesque" font-weight="800" font-size="{size}" color="{p["ink"]}" line-height="1.12" vertical-align="middle">{x(sent)}</text>')
    subs = s["bullets"][1:4]
    step = 70 if len(subs) <= 2 else 54  # three lines start higher and tighten so the last ends above the sources line
    y0 = 780 if len(subs) <= 2 else 756
    for k, b in enumerate(subs):
        h = step - 6
        out.append(f'<text x="{M + 60}" y="{y0 + k * step}" width="1660" height="{h}" font-size="{fit(b, 1660, h, 36, 1.0, FLOOR)}" color="{p["sub"]}" max-lines="2">{x(b)}</text>')
    return out


def sequence(p, n, s, o, idx):
    bl = s["bullets"]; out = []
    actors = o.get("actors", {}).get(str(idx), ["Bên gửi", "Bên nhận"])
    na = len(actors)
    lane = 1728 / na
    cxs = [M + lane * i + lane / 2 for i in range(na)]
    for i, name in enumerate(actors):
        a, t = acc(p, n, i)
        out.append(f'<rectangle x="{cxs[i] - 220:.0f}" y="290" width="440" height="84" corner-radius="20" fill="{a}"/>')
        out.append(f'<text x="{cxs[i] - 220:.0f}" y="290" width="440" height="84" font-weight="800" font-size="34" color="{"#FFFFFF" if p is LIGHT else "#14161C"}" text-align="center" vertical-align="middle" max-lines="1">{x(name)}</text>')
        out.append(f'<line x1="{cxs[i]:.0f}" y1="374" x2="{cxs[i]:.0f}" y2="940" stroke="{p["diagline"]}" stroke-width="4" dash="10,10"/>')
    step = min(540 / max(len(bl), 1), 405 / max(len(bl) - 1, 1))  # a self-loop (95px tall) on the last step still ends above the source line
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        yy = 430 + k * step
        pr = o.get("pairs", {}).get(str(idx))
        if pr:
            i0, i1 = pr[k]
        else:
            i0 = k % (na - 1) if na > 1 else 0
            i1 = min(i0 + 1, na - 1)
        x1, x2 = cxs[i0], cxs[i1]
        if i0 == i1:
            out.append(f'<line x1="{x1:.0f}" y1="{yy + 5:.0f}" x2="{x1:.0f}" y2="{yy + 95:.0f}" stroke="{a}" stroke-width="5" arrow-end="triangle"/>')
            wtxt = lane - 80
            ss = fit(f"{k + 1}. {b}", wtxt, 90, 30, 1.1, FLOOR, 0.57)
            if x1 + 24 + wtxt > 1824:
                out.append(f'<text x="{x1 - 24 - wtxt:.0f}" y="{yy + 5:.0f}" width="{wtxt:.0f}" height="90" font-weight="600" font-size="{ss}" color="{p["ink"]}" text-align="right" vertical-align="middle" line-height="1.1">{k + 1}. {x(b)}</text>')
            else:
                out.append(f'<text x="{x1 + 24:.0f}" y="{yy + 5:.0f}" width="{wtxt:.0f}" height="90" font-weight="600" font-size="{ss}" color="{p["ink"]}" vertical-align="middle" line-height="1.1">{k + 1}. {x(b)}</text>')
            continue
        out.append(f'<line x1="{x1:.0f}" y1="{yy + 60:.0f}" x2="{x2:.0f}" y2="{yy + 60:.0f}" stroke="{a}" stroke-width="5" arrow-end="triangle"/>')
        lx = min(x1, x2)
        lw = abs(x2 - x1) - 20
        out.append(f'<text x="{lx + 10:.0f}" y="{yy - 24:.0f}" width="{lw:.0f}" height="80" font-weight="600" font-size="{fit(f"{k + 1}. {b}", lw, 80, 30, 1.1, FLOOR, 0.57)}" color="{p["ink"]}" text-align="center" vertical-align="bottom" line-height="1.1">{k + 1}. {x(b)}</text>')
    return out


FILE_IDS = json.loads((Path(__file__).resolve().parent / "file_ids.json").read_text())


def images(p, s, px, py, pw, ph):
    """White rounded frames holding the slide's images side by side, and the credit line at y=892."""
    out, imgs, gap = [], s["images"], 24
    cw = (pw - gap * (len(imgs) - 1)) / len(imgs)
    for k, im in enumerate(imgs):
        cx = px + k * (cw + gap)
        out.append(f'<rectangle x="{cx:.0f}" y="{py}" width="{cw:.0f}" height="{ph}" corner-radius="28" fill="#FFFFFF" stroke="{p["diagline"]}" stroke-width="3"/>')
        key = f'{s["_lid"]}/{im["file"]}'  # per lesson: two lessons may keep different files under one name
        if key not in FILE_IDS:
            raise SystemExit(f"{key} has no Moda id: upload it (upload url=...) and add it to scripts/deckgen/file_ids.json")
        fid = FILE_IDS[key]
        out.append(f'<image src="{fid}" x="{cx + 20:.0f}" y="{py + 20}" width="{cw - 40:.0f}" height="{ph - 40}" fit="contain"/>')
    credits = "; ".join(dict.fromkeys(im["credit"] for im in imgs))
    out.append(f'<text x="{M}" y="890" width="1728" height="52" font-size="22" color="{p["sub"]}" line-height="1.1" vertical-align="top">Hình: {x(credits)}</text>')
    return out


def gloss(p, a, b, rx, yy, rw, ch):
    """One 'reading the figure' card: English label of the figure in the accent, Vietnamese meaning under it."""
    out = [f'<rectangle x="{rx}" y="{yy:.0f}" width="{rw}" height="{ch:.0f}" corner-radius="20" fill="{p["card"]}"/>',
           f'<rectangle x="{rx}" y="{yy:.0f}" width="12" height="{ch:.0f}" corner-radius="6" fill="{a}"/>']
    kk, v = split_kv(b)
    if kk:
        out.append(f'<text x="{rx + 36}" y="{yy + 10:.0f}" width="{rw - 56}" height="{ch * 0.4:.0f}" font-weight="800" font-size="{fit(kk, rw - 56, ch * 0.4, 30, 1.0, FLOOR, 0.6)}" color="{a}" vertical-align="middle" max-lines="1">{x(kk)}</text>')
        out.append(f'<text x="{rx + 36}" y="{yy + ch * 0.4:.0f}" width="{rw - 56}" height="{ch * 0.56:.0f}" font-weight="600" font-size="{fit(v, rw - 56, ch * 0.56, 34, 1.15, FLOOR, 0.57)}" color="{p["ink"]}" vertical-align="middle" line-height="1.15">{x(v)}</text>')
    else:
        out.append(f'<text x="{rx + 36}" y="{yy:.0f}" width="{rw - 56}" height="{ch:.0f}" font-weight="600" font-size="{fit(b, rw - 56, ch - 16, 34, 1.2, FLOOR, 0.57)}" color="{p["ink"]}" vertical-align="middle" line-height="1.2">{x(b)}</text>')
    return out


def figure(p, n, s, o, idx):
    """Ảnh minh họa (từ sách miễn phí) bên trái, các dòng 'đọc hình' bên phải, dòng ghi nguồn ảnh."""
    px, py, pw, ph = M, 236, 1060, 640
    out = images(p, s, px, py, pw, ph)
    bl = s["bullets"]; rx = px + pw + 40; rw = 1920 - M - rx
    ch = min(150, (ph - 24 * (len(bl) - 1)) / len(bl))
    for k, b in enumerate(bl):
        out += gloss(p, acc(p, n, idx + k)[0], b, rx, py + k * (ch + 24), rw, ch)
    return out


def annotated_figure(p, n, s, o, idx):
    """Như figure, nhưng cột phải là tối đa 3 thẻ chú giải ngắn và một khối giải thích (body) 40-70 chữ."""
    px, py, pw, ph = M, 236, 940, 640
    out = images(p, s, px, py, pw, ph)
    bl = s.get("bullets", []); rx = px + pw + 40; rw = 1920 - M - rx
    ch, gap = (88, 14) if len(bl) >= 3 else (104, 16)
    for k, b in enumerate(bl):
        out += gloss(p, acc(p, n, idx + k)[0], b, rx, py + k * (ch + gap), rw, ch)
    a, t = acc(p, n, idx)
    by = py + len(bl) * (ch + gap); bh = ph - (by - py)
    size = fit_rich(s["body"], rw - 64, bh - 56, 34, 1.3, 24)
    out.append(f'<rectangle x="{rx}" y="{by}" width="{rw}" height="{bh}" corner-radius="20" fill="{t}"/>')
    out.append(f'<text x="{rx + 32}" y="{by + 28}" width="{rw - 64}" height="{bh - 56}" format="html" font-size="{size}" color="{p["ink"]}" line-height="1.3" vertical-align="top">{rich(s["body"], p, n, a, o)}</text>')
    return out


def explainer(p, n, s, o, idx):
    """Cột trái: đoạn giải thích (body) 60-110 chữ, từ khoá tô màu khái niệm. Cột phải: 2-3 thẻ lấy từ bullets."""
    bl = s.get("bullets", []); out = []
    a, t = acc(p, n, 0)
    y0, h = 290, 590
    bw = 1110 if bl else 1688
    size = fit_rich(s["body"], bw, h, 38, 1.35, 30, 18)
    out.append(f'<rectangle x="{M}" y="{y0 + 6}" width="10" height="{h - 12}" corner-radius="5" fill="{a}"/>')
    out.append(f'<text x="{M + 40}" y="{y0}" width="{bw}" height="{h}" format="html" font-size="{size}" color="{p["ink"]}" line-height="1.35" paragraph-spacing="18" vertical-align="top">{rich(s["body"], p, n, a, o)}</text>')
    if bl:
        rx = M + 40 + bw + 48; rw = 1920 - M - rx; gap = 24
        ch = (h - gap * (len(bl) - 1)) / len(bl)
        for k, b in enumerate(bl):
            ak, tk = acc(p, n, k)
            yy = y0 + k * (ch + gap)
            kk, v = split_kv(b)
            out.append(f'<rectangle x="{rx}" y="{yy:.0f}" width="{rw}" height="{ch:.0f}" corner-radius="22" fill="{p["card"]}"/>')
            out.append(f'<rectangle x="{rx}" y="{yy:.0f}" width="{rw}" height="10" corner-radius="5" fill="{ak}"/>')
            top = 30
            if kk:
                out.append(f'<text x="{rx + 32}" y="{yy + 28:.0f}" width="{rw - 64}" height="40" font-weight="800" font-size="26" color="{ak}" max-lines="1">{x(kk)}</text>')
                top = 76
            vs = fit(v, rw - 64, ch - top - 20, 32, 1.22, 24)
            out.append(f'<text x="{rx + 32}" y="{yy + top:.0f}" width="{rw - 64}" height="{ch - top - 20:.0f}" font-weight="600" font-size="{vs}" color="{p["ink"]}" line-height="1.22" vertical-align="top">{x(v)}</text>')
    return out


def profile_card(p, n, s, o, idx):
    """Thẻ hồ sơ (bộ phận, chất dẫn truyền, cảm xúc): lưới 2x2 hoặc 3x2 lấy từ facts, nhãn màu khái niệm."""
    f = s["facts"]; c = len(f)
    cols = 2 if c in (2, 4) else 3
    rows = math.ceil(c / cols)
    y0, h, gap = 286, 624, 28
    cw = (1728 - gap * (cols - 1)) / cols; ch = (h - gap * (rows - 1)) / rows
    out = []
    for k, fact in enumerate(f):
        a, t = acc(p, n, k)
        r, q = divmod(k, cols)
        xx = M + q * (cw + gap); yy = y0 + r * (ch + gap)
        out.append(f'<rectangle x="{xx:.0f}" y="{yy:.0f}" width="{cw:.0f}" height="{ch:.0f}" corner-radius="24" fill="{p["card"]}"/>')
        out.append(f'<rectangle x="{xx:.0f}" y="{yy:.0f}" width="12" height="{ch:.0f}" corner-radius="6" fill="{a}"/>')
        out.append(f'<text x="{xx + 40:.0f}" y="{yy + 22:.0f}" width="{cw - 64:.0f}" height="42" font-weight="800" font-size="{fit(fact["label"], cw - 64, 42, 28, 1.0, FLOOR, 0.6)}" color="{a}" max-lines="1">{x(fact["label"])}</text>')
        ts = fit(plain(fact["text"]), cw - 64, ch - 92, 34, 1.25, 28)
        out.append(f'<text x="{xx + 40:.0f}" y="{yy + 76:.0f}" width="{cw - 64:.0f}" height="{ch - 92:.0f}" format="html" font-weight="500" font-size="{ts}" color="{p["ink"]}" line-height="1.25" vertical-align="top">{rich(fact["text"], p, n, a, o)}</text>')
    return out


def references(p, n, s, o):
    """Danh sách nguồn (tối đa 18): một cột nếu ≤ 6, hai cột nếu nhiều hơn; 'S1: ...' cho nhãn màu."""
    bl = s["bullets"]; c = len(bl); out = []
    cols = 1 if c <= 6 else 2
    per = math.ceil(c / cols)
    y0, h, gap = 270, 650, 12
    cw = (1728 - 40 * (cols - 1)) / cols
    rh = min(140, (h - gap * (per - 1)) / per)
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        q, r = divmod(k, per)
        xx = M + q * (cw + 40); yy = y0 + r * (rh + gap)
        kk, v = split_kv(b)
        out.append(f'<rectangle x="{xx:.0f}" y="{yy:.0f}" width="{cw:.0f}" height="{rh:.0f}" corner-radius="16" fill="{p["card"]}"/>')
        out.append(f'<text x="{xx + 24:.0f}" y="{yy:.0f}" width="92" height="{rh:.0f}" font-weight="800" font-size="26" color="{a}" vertical-align="middle" max-lines="1">{x(kk or str(k + 1))}</text>')
        out.append(f'<text x="{xx + 120:.0f}" y="{yy:.0f}" width="{cw - 144:.0f}" height="{rh:.0f}" font-size="{fit(v, cw - 144, rh - 12, 28, 1.18, FLOOR)}" color="{p["ink"]}" vertical-align="middle" line-height="1.18">{x(v)}</text>')
    return out


LAYOUTS = {"card-grid": card_grid, "flow": flow, "two-column-comparison": two_col, "lookup-table": lookup,
           "numbered-rows": numbered, "layers": layers, "timeline": timeline, "references": references}
INDEXED = {"connection-diagram": connection, "one-big-number": big, "one-highlighted-sentence": highlight,
           "sequence-diagram": sequence, "figure": figure, "annotated-figure": annotated_figure,
           "explainer": explainer, "profile-card": profile_card}


def cover(lid, d, o, total):
    n = int(lid[1:]); p = DARK
    out = ['<background fill="#14161C"/>']
    mot = o.get("motif", "grid")
    if mot == "grid":
        for g in range(1, 8):
            out.append(f'<line x1="{1920 - g * 110}" y1="0" x2="{1920 - g * 110}" y2="1080" stroke="#1E212B" stroke-width="3"/>')
        for g in range(1, 6):
            out.append(f'<line x1="900" y1="{g * 180}" x2="1920" y2="{g * 180}" stroke="#1E212B" stroke-width="3"/>')
    elif mot == "pulse":
        out.append('<path d="M760 560 L1180 560 L1250 300 L1350 820 L1450 420 L1520 560 L1920 560" stroke="#3DD6A0" stroke-width="7" fill="none" opacity="0.16"/>')
    elif mot == "dots":
        out.append('<repeat count="48" as="i"><ellipse cx="{1000+(i%8)*110}" cy="{120+Math.floor(i/8)*150}" rx="{i%3==0?20:10}" ry="{i%3==0?20:10}" fill="{i%3==0?\'#FFB454\':\'#2C3040\'}" opacity="0.22"/></repeat>')
    elif mot == "split":
        out.append('<ellipse cx="1400" cy="540" rx="330" ry="330" start-angle="90" sweep-angle="180" fill="#1E212B"/>')
        out.append('<ellipse cx="1400" cy="540" rx="330" ry="330" start-angle="270" sweep-angle="180" fill="#262C4A"/>')
        out.append('<line x1="1400" y1="200" x2="1400" y2="880" stroke="#14161C" stroke-width="8"/>')
    elif mot == "rings":
        out.append('<repeat count="6" as="i"><ellipse cx="1500" cy="480" rx="{90+i*85}" ry="{90+i*85}" stroke="#2C3040" stroke-width="4" fill="none"/></repeat>')
        out.append('<ellipse cx="1500" cy="480" rx="26" ry="26" fill="#FF6A4D" opacity="0.7"/>')
    elif mot == "feed":
        out.append('<repeat count="5" as="i"><rectangle x="{1250+i*24}" y="{90+i*130}" width="540" height="100" corner-radius="24" fill="#1E212B" stroke="#2C3040" stroke-width="3" opacity="0.55"/></repeat>')
    out.append(f'<text x="{M}" y="96" width="1200" height="40" font-weight="700" font-size="28" letter-spacing="6" color="{p["sub"]}" max-lines="1">{x(o.get("topic_label", d["subtitle"]).upper())}</text>')
    out.append(f'<text x="{M}" y="170" width="1500" height="400" font-family="Bricolage Grotesque" font-weight="800" font-size="108" color="{p["ink"]}" line-height="1.04" max-lines="4" vertical-align="top">{x(d["title"])}</text>')
    if o.get("question"):
        out.append(f'<text x="{M}" y="590" width="1400" height="120" font-weight="600" font-size="44" color="{p["acc"][(n) % 4]}" line-height="1.2" max-lines="2">{x(o["question"])}</text>')
    cards = o.get("cards", [])
    cw = (1728 - 28 * (len(cards) - 1)) / max(len(cards), 1)
    for k, c in enumerate(cards):
        a = p["acc"][(n + k) % 4]
        xx = M + k * (cw + 28)
        out.append(f'<rectangle x="{xx:.0f}" y="780" width="{cw:.0f}" height="170" corner-radius="28" fill="{p["card"]}" stroke="{a}" stroke-width="4"/>')
        out.append(f'<text x="{xx + 28:.0f}" y="780" width="{cw - 56:.0f}" height="170" font-weight="700" font-size="{fit(c, cw - 56, 160, 34, 1.15, 24, 0.58)}" color="{p["ink"]}" vertical-align="middle" line-height="1.15" max-lines="3">{x(c)}</text>')
    return out


def page(lid, i, o, slides=None):
    path = Path(slides) if slides else ROOT / "lessons" / lid / "slides.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    total = len(d["slides"]) + 1
    n = int(lid[1:])
    if i == 0:
        body = cover(lid, d, o, total)
    else:
        s = {**d["slides"][i - 1], "_lid": lid}
        p = pal(s["tone"])
        body = [f'<background fill="{p["bg"]}"/>', title(p, s["title"])]
        lay = s["layout"]
        if lay in LAYOUTS:
            body += LAYOUTS[lay](p, n, s, o)
        elif lay in INDEXED:
            body += INDEXED[lay](p, n, s, o, i)
        else:
            raise SystemExit("layout not implemented: " + lay)
        if s["sources"] and s["section"] != "Nguồn tham khảo":
            body.append(f'<text x="{M}" y="944" width="1728" height="36" font-size="24" color="{p["sub"]}" max-lines="1">Nguồn: {x(" ".join("[" + z + "]" for z in s["sources"]))}</text>')
        body.append(footer(p, lid, i, total))
    return '<content font-family="Be Vietnam Pro">\n' + "\n".join(body) + "\n</content>"


def overflows(markup):
    """Texts of a page that wrap to more height than their box has at the size fit() settled on (an estimate, cw 0.55)."""
    import html
    import xml.etree.ElementTree as ET
    bad = []
    for node in ET.fromstring(markup).iter("text"):
        text = html.unescape("".join(node.itertext()))
        if len(text) < 20 and node.get("font-family") != "Bricolage Grotesque" and not node.get("max-lines"):
            continue
        display = node.get("font-family") == "Bricolage Grotesque"  # wider glyphs, tighter leading
        w, h, size = float(node.get("width")), float(node.get("height")), int(node.get("font-size"))
        paras = node.findall("p")
        if paras:  # an html body: one <p> per paragraph, drawn at the node's own leading and paragraph spacing
            need = sum(lines(html.unescape("".join(q.itertext())), w, size, 0.55) for q in paras) * size * float(node.get("line-height", 1.15))
            need += float(node.get("paragraph-spacing", 0)) * (len(paras) - 1)
        else:
            need = lines(text, w, size, 0.58 if display else 0.55) * size * float(node.get("line-height", 1.08 if display else 1.15))
        cap = node.get("max-lines")  # Moda drops the lines past max-lines, so the text must wrap to no more
        clipped = bool(cap) and not paras and lines(text, w, size, 0.58 if display else 0.55) > int(cap)
        if need > h * 1.05 or clipped:
            bad.append(text)
    return bad


def arg(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


if __name__ == "__main__":
    lid, i = sys.argv[1], int(sys.argv[2])
    opts = arg("--opts")
    o = json.loads(Path(opts).read_text(encoding="utf-8")) if opts else {}
    print(page(lid, i, o, arg("--slides")))

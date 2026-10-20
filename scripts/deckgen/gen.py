#!/usr/bin/env python3
"""Moda markup for one page of a lesson deck, from lessons/<id>/slides.json.

usage: gen.py <lesson-id> <page 0..N> [--opts file.json]
page 0 is the cover, pages 1..N follow slides.json. Prints the <content>...</content> markup.
opts file: {"topic_label": "...", "question": "...", "motif": "...", "big": {"3": "86 tỷ"},
            "actors": {"6": ["A","B","C"]}, "mark": {"5": "có hoặc không"}}
"""
import json, sys
from xml.sax.saxutils import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIGHT = dict(bg="#F3EEE3", ink="#14161C", card="#E8E0CF", diag="#FBF8F2", diagline="#DDD5C1", sub="#6B6A66",
             acc=["#1F3FD1", "#B45309", "#0F766E", "#E8472B"], tint=["#DDE3FA", "#F3DFB8", "#CFE8E2", "#F8D9D0"])
DARK = dict(bg="#14161C", ink="#F3EEE3", card="#1E212B", diag="#1E212B", diagline="#2C3040", sub="#9AA0B5",
            acc=["#7C93FF", "#FFB454", "#3DD6A0", "#FF6A4D"], tint=["#262C4A", "#4A3A22", "#1C4236", "#4A2A24"])
RED_LIGHT, RED_DARK = "#E8472B", "#FF6A4D"
M = 96  # margin


def x(t):
    return escape(t, {'"': "&quot;"})


def pal(tone):
    return LIGHT if tone == "light" else DARK


def acc(p, n, k):
    return p["acc"][(n + k) % 4], p["tint"][(n + k) % 4]


def title(p, text, y=72, size=76, w=1728, h=190):
    return (f'<text x="{M}" y="{y}" width="{w}" height="{h}" font-family="Bricolage Grotesque" font-weight="800" '
            f'font-size="{size}" color="{p["ink"]}" line-height="1.08" max-lines="2" vertical-align="top">{x(text)}</text>')


def footer(p, lid, i, total):
    red = RED_LIGHT if p is LIGHT else RED_DARK
    ink = p["ink"]
    dots = (f'<repeat count="{total}" as="d"><ellipse cx="{{105+d*24}}" cy="1010" rx="{{d=={i}?8:6}}" ry="{{d=={i}?8:6}}" '
            f'fill="{{d=={i}?\'{red}\':\'{ink}\'}}" opacity="{{d=={i}?1:0.28}}"/></repeat>')
    tx = M + total * 24 + 24
    return dots + (f'\n<text x="{tx}" y="994" width="700" height="32" font-size="24" color="{p["sub"]}" vertical-align="middle" '
                   f'max-lines="1">Multiple-report · {lid} · {i + 1:02d}/{total:02d}</text>')


def split_kv(b):
    if ": " in b:
        k, v = b.split(": ", 1)
        return k, v
    return None, b


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
        head = kk if kk else None
        if head:
            out.append(f'<text x="{xx + 40:.0f}" y="510" width="{w - 80:.0f}" height="110" font-weight="700" font-size="36" color="{p["ink"]}" max-lines="2">{x(head)}</text>')
            out.append(f'<text x="{xx + 40:.0f}" y="630" width="{w - 80:.0f}" height="220" font-size="34" color="{p["sub"]}" line-height="1.3">{x(vv)}</text>')
        else:
            out.append(f'<text x="{xx + 40:.0f}" y="510" width="{w - 80:.0f}" height="340" font-weight="600" font-size="42" color="{p["ink"]}" line-height="1.25">{x(b)}</text>')
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
        out.append(f'<text x="{xx + 32:.0f}" y="480" width="{w - 64:.0f}" height="260" font-weight="600" font-size="36" color="{p["ink"]}" line-height="1.25">{x(b)}</text>')
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
        out.append(f'<text x="{xx + 48}" y="336" width="{w - 96}" height="100" font-family="Bricolage Grotesque" font-weight="800" font-size="56" color="{a}" max-lines="2">{x(h)}</text>')
        out.append(f'<text x="{xx + 48}" y="450" width="{w - 96}" height="{240 if rest else 330}" font-size="42" color="{p["ink"]}" line-height="1.3">{x(vv)}</text>')
    if rest:
        out.append(f'<rectangle x="{M}" y="780" width="1728" height="130" corner-radius="24" fill="{p["card"]}"/>')
        out.append(f'<text x="{M + 40}" y="780" width="1648" height="130" font-weight="600" font-size="38" color="{p["ink"]}" vertical-align="middle" max-lines="2">{x(" · ".join(rest))}</text>')
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
            out.append(f'<text x="{M + 40}" y="{yy}" width="620" height="{rh}" font-weight="800" font-size="40" color="{a}" vertical-align="middle" max-lines="2">{x(kk)}</text>')
            out.append(f'<text x="{M + 700}" y="{yy}" width="1000" height="{rh}" font-size="36" color="{p["ink"]}" vertical-align="middle" line-height="1.2" max-lines="2">{x(vv)}</text>')
        else:
            out.append(f'<text x="{M + 40}" y="{yy}" width="1640" height="{rh}" font-weight="700" font-size="40" color="{p["ink"]}" vertical-align="middle" max-lines="2">{x(b)}</text>')
    return out


def numbered(p, n, s, o):
    bl = s["bullets"]; out = []
    rh = min(150, 620 // max(len(bl), 1))
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        yy = (250 if len(bl) >= 5 else 280) + k * (rh + 12)
        out.append(f'<text x="{M}" y="{yy}" width="170" height="{rh}" font-family="Bricolage Grotesque" font-weight="800" font-size="{min(116, rh - 14)}" color="{a}" vertical-align="middle" max-lines="1">{k + 1}</text>')
        out.append(f'<rectangle x="{M + 190}" y="{yy + 10}" width="1538" height="{rh - 20}" corner-radius="20" fill="{p["card"]}"/>')
        out.append(f'<text x="{M + 230}" y="{yy + 10}" width="1470" height="{rh - 20}" font-weight="600" font-size="{40 if rh > 120 else 36}" color="{p["ink"]}" vertical-align="middle" line-height="1.2" max-lines="2">{x(b)}</text>')
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
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="230" ry="150" fill="{p["ink"]}"/>')
    out.append(f'<text x="{cx - 200}" y="{cy - 120}" width="400" height="240" font-family="Bricolage Grotesque" font-weight="800" font-size="44" color="{p["bg"]}" text-align="center" vertical-align="middle" line-height="1.1" max-lines="4">{x(o.get("center", {}).get(str(idx), s["title"]))}</text>')
    for k, b in enumerate(bl[:4]):
        a, t = acc(p, n, k)
        px, py = pos[k]
        out.append(f'<rectangle x="{px - 270}" y="{py - 80}" width="540" height="160" corner-radius="24" fill="{p["diag"]}" stroke="{a}" stroke-width="5"/>')
        out.append(f'<text x="{px - 240}" y="{py - 80}" width="480" height="160" font-weight="700" font-size="34" color="{p["ink"]}" text-align="center" vertical-align="middle" line-height="1.15" max-lines="3">{x(b)}</text>')
    return out


def layers(p, n, s, o):
    bl = s["bullets"]; out = []
    rh = min(170, 600 // max(len(bl), 1))
    for k, b in enumerate(bl):
        a, t = acc(p, n, k)
        yy = 300 + k * (rh + 16)
        inset = k * 70
        out.append(f'<rectangle x="{M + inset}" y="{yy}" width="{1728 - 2 * inset}" height="{rh}" corner-radius="22" fill="{t}" stroke="{a}" stroke-width="4"/>')
        out.append(f'<text x="{M + inset + 40}" y="{yy}" width="{1728 - 2 * inset - 80}" height="{rh}" font-weight="700" font-size="38" color="{p["ink"]}" vertical-align="middle" text-align="center" max-lines="2">{x(b)}</text>')
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
        kk, vv = split_kv(b)
        out.append(f'<line x1="{cx:.0f}" y1="{y0 + (-26 if up else 26)}" x2="{cx:.0f}" y2="{y0 + (-60 if up else 60)}" stroke="{a}" stroke-width="4"/>')
        out.append(f'<text x="{cx - step / 2 + 20:.0f}" y="{ty}" width="{step - 40:.0f}" height="190" font-weight="600" font-size="36" color="{p["ink"]}" text-align="center" vertical-align="{"bottom" if up else "top"}" line-height="1.2">{x(b)}</text>')
    return out


def big(p, n, s, o, idx):
    a, t = acc(p, n, 0)
    num = o.get("big", {}).get(str(idx), s["title"])
    out = [f'<text x="{M}" y="260" width="1728" height="360" font-family="Bricolage Grotesque" font-weight="800" font-size="300" color="{a}" max-lines="1" vertical-align="middle">{x(num)}</text>']
    bl = list(s["bullets"][:3])
    if bl and bl[0].startswith(num):
        bl[0] = bl[0][len(num):].strip()
    for k, b in enumerate([z for z in bl if z]):
        out.append(f'<text x="{M}" y="{650 + k * 96}" width="1728" height="90" font-weight="600" font-size="44" color="{p["ink"]}" max-lines="2">{x(b)}</text>')
    return out


def highlight(p, n, s, o, idx):
    a, t = acc(p, n, 0)
    sent = s["bullets"][0]
    out = [f'<rectangle x="{M}" y="310" width="16" height="420" corner-radius="8" fill="{a}"/>']
    mark = o.get("mark", {}).get(str(idx))
    if mark and mark in sent:
        pre, post = sent.split(mark, 1)
        html = f'{x(pre)}<span style="color: {a}">{x(mark)}</span>{x(post)}'
        out.append(f'<text x="{M + 60}" y="300" width="1660" height="440" format="html" font-family="Bricolage Grotesque" font-weight="800" font-size="92" color="{p["ink"]}" line-height="1.12" vertical-align="middle"><p>{html}</p></text>')
    else:
        out.append(f'<text x="{M + 60}" y="300" width="1660" height="440" font-family="Bricolage Grotesque" font-weight="800" font-size="92" color="{p["ink"]}" line-height="1.12" vertical-align="middle">{x(sent)}</text>')
    for k, b in enumerate(s["bullets"][1:3]):
        out.append(f'<text x="{M + 60}" y="{780 + k * 70}" width="1660" height="64" font-size="36" color="{p["sub"]}" max-lines="1">{x(b)}</text>')
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
    step = 540 / max(len(bl), 1)
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
            if x1 + 24 + wtxt > 1824:
                out.append(f'<text x="{x1 - 24 - wtxt:.0f}" y="{yy + 5:.0f}" width="{wtxt:.0f}" height="90" font-weight="600" font-size="30" color="{p["ink"]}" text-align="right" vertical-align="middle" max-lines="2" line-height="1.1">{k + 1}. {x(b)}</text>')
            else:
                out.append(f'<text x="{x1 + 24:.0f}" y="{yy + 5:.0f}" width="{wtxt:.0f}" height="90" font-weight="600" font-size="30" color="{p["ink"]}" vertical-align="middle" max-lines="2" line-height="1.1">{k + 1}. {x(b)}</text>')
            continue
        out.append(f'<line x1="{x1:.0f}" y1="{yy + 60:.0f}" x2="{x2:.0f}" y2="{yy + 60:.0f}" stroke="{a}" stroke-width="5" arrow-end="triangle"/>')
        lx = min(x1, x2)
        out.append(f'<text x="{lx + 10:.0f}" y="{yy - 4:.0f}" width="{abs(x2 - x1) - 20:.0f}" height="60" font-weight="600" font-size="30" color="{p["ink"]}" text-align="center" vertical-align="bottom" max-lines="2" line-height="1.1">{k + 1}. {x(b)}</text>')
    return out


FILE_IDS = json.loads((Path(__file__).resolve().parent / "file_ids.json").read_text())


def figure(p, n, s, o, idx):
    """Ảnh minh họa (từ sách miễn phí) bên trái, các dòng 'đọc hình' bên phải, dòng ghi nguồn ảnh."""
    out = []
    imgs = s["images"]
    px, py, pw, ph = M, 236, 1060, 640
    gap = 24
    cw = (pw - gap * (len(imgs) - 1)) / len(imgs)
    for k, im in enumerate(imgs):
        cx = px + k * (cw + gap)
        out.append(f'<rectangle x="{cx:.0f}" y="{py}" width="{cw:.0f}" height="{ph}" corner-radius="28" fill="#FFFFFF" stroke="{p["diagline"]}" stroke-width="3"/>')
        fid = FILE_IDS[Path(im["file"]).name]
        out.append(f'<image src="{fid}" x="{cx + 20:.0f}" y="{py + 20}" width="{cw - 40:.0f}" height="{ph - 40}" fit="contain"/>')
    # right column: glosses
    bl = s["bullets"]; rx = px + pw + 40; rw = 1920 - M - rx
    ch = min(150, (ph - 24 * (len(bl) - 1)) / len(bl))
    for k, b in enumerate(bl):
        a, t = acc(p, n, idx + k)
        yy = py + k * (ch + 24)
        out.append(f'<rectangle x="{rx}" y="{yy:.0f}" width="{rw}" height="{ch:.0f}" corner-radius="20" fill="{p["card"]}"/>')
        out.append(f'<rectangle x="{rx}" y="{yy:.0f}" width="12" height="{ch:.0f}" corner-radius="6" fill="{a}"/>')
        kk, v = split_kv(b)
        if kk:
            out.append(f'<text x="{rx + 36}" y="{yy + 14:.0f}" width="{rw - 56}" height="{ch * 0.38:.0f}" font-weight="800" font-size="30" color="{a}" vertical-align="middle" max-lines="1">{x(kk)}</text>')
            out.append(f'<text x="{rx + 36}" y="{yy + ch * 0.4:.0f}" width="{rw - 56}" height="{ch * 0.55:.0f}" font-weight="600" font-size="34" color="{p["ink"]}" vertical-align="middle" line-height="1.15" max-lines="2">{x(v)}</text>')
        else:
            out.append(f'<text x="{rx + 36}" y="{yy:.0f}" width="{rw - 56}" height="{ch:.0f}" font-weight="600" font-size="34" color="{p["ink"]}" vertical-align="middle" line-height="1.2" max-lines="3">{x(b)}</text>')
    credits = "; ".join(dict.fromkeys(im["credit"] for im in imgs))
    out.append(f'<text x="{M}" y="892" width="1728" height="36" font-size="22" color="{p["sub"]}" max-lines="1">Hình: {x(credits)}</text>')
    return out


LAYOUTS = {"card-grid": card_grid, "flow": flow, "two-column-comparison": two_col, "lookup-table": lookup,
           "numbered-rows": numbered, "layers": layers, "timeline": timeline}


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
        out.append(f'<text x="{xx + 28:.0f}" y="780" width="{cw - 56:.0f}" height="170" font-weight="700" font-size="34" color="{p["ink"]}" vertical-align="middle" line-height="1.15" max-lines="3">{x(c)}</text>')
    return out


def page(lid, i, o):
    d = json.loads((ROOT / "lessons" / lid / "slides.json").read_text(encoding="utf-8"))
    total = len(d["slides"]) + 1
    n = int(lid[1:])
    if i == 0:
        body = cover(lid, d, o, total)
    else:
        s = d["slides"][i - 1]
        p = pal(s["tone"])
        body = [f'<background fill="{p["bg"]}"/>', title(p, s["title"])]
        lay = s["layout"]
        if lay in LAYOUTS:
            body += LAYOUTS[lay](p, n, s, o)
        elif lay == "connection-diagram":
            body += connection(p, n, s, o, i)
        elif lay == "one-big-number":
            body += big(p, n, s, o, i)
        elif lay == "one-highlighted-sentence":
            body += highlight(p, n, s, o, i)
        elif lay == "sequence-diagram":
            body += sequence(p, n, s, o, i)
        elif lay == "figure":
            body += figure(p, n, s, o, i)
        else:
            raise SystemExit("layout not implemented: " + lay)
        if s["sources"] and s["title"] != "Nguồn tham khảo":
            body.append(f'<text x="{M}" y="944" width="1728" height="36" font-size="24" color="{p["sub"]}" max-lines="1">Nguồn: {x(" ".join("[" + z + "]" for z in s["sources"]))}</text>')
        body.append(footer(p, lid, i, total))
    return '<content font-family="Be Vietnam Pro">\n' + "\n".join(body) + "\n</content>"


if __name__ == "__main__":
    lid, i = sys.argv[1], int(sys.argv[2])
    o = {}
    if "--opts" in sys.argv:
        o = json.loads(Path(sys.argv[sys.argv.index("--opts") + 1]).read_text(encoding="utf-8"))
    print(page(lid, i, o))

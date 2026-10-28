#!/usr/bin/env python3
"""Moda markup for the 18 pages of the L19 deck (transistors), drawn by hand: symbols, circuits and cross-sections.

usage: L19_pages.py <page 0..17>   prints the <content>...</content> markup of one page (0 = cover).

gen.py draws text layouts only; this deck needs circuit symbols and current arrows, so every page is drawn here, from the texts of
lessons/L19/slides.json (titles, bullets, bodies, credits) and the palette and footer of gen.py. One colour per terminal on every page:
Base/Gate orange, Collector/Drain blue, Emitter/Source green. Control current: thin orange arrow; main current: thick blue arrow.
"""
import json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen
from gen import LIGHT, DARK, M, x, fit, split_kv, plain

LID = "L19"
B, C, E = "#DD4B0E", "#2F6BEF", "#0B8A5F"  # Base/Gate, Collector/Drain, Emitter/Source: the same hex on light and dark pages
PIN = {"b": B, "g": B, "c": C, "d": C, "e": E, "s": E}
DATA = json.loads((gen.ROOT / "lessons" / LID / "slides.json").read_text(encoding="utf-8"))
SL = DATA["slides"]
TOTAL = len(SL) + 1
OPTS = json.loads((gen.ROOT / "scripts" / "deckgen" / "opts" / f"{LID}.json").read_text(encoding="utf-8"))
gen.CONCEPT_COLORS.update({k.lower(): v for k, v in OPTS.get("concept_colors", {}).items()})


# ---------------------------------------------------------------- primitives
def T(xx, yy, w, h, t, size, col, wt=500, al=None, va="top", lh=None, ml=None, font=None):
    a = f'<text x="{xx:.0f}" y="{yy:.0f}" width="{w:.0f}" height="{h:.0f}" font-size="{size}" color="{col}"'
    if wt != 400: a += f' font-weight="{wt}"'
    if al: a += f' text-align="{al}"'
    if va != "top": a += f' vertical-align="{va}"'
    if lh: a += f' line-height="{lh}"'
    if ml: a += f' max-lines="{ml}"'
    if font: a += f' font-family="{font}"'
    return a + f'>{x(t)}</text>'


def R(xx, yy, w, h, fill, stroke=None, r=20, sw=3):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rectangle x="{xx:.0f}" y="{yy:.0f}" width="{w:.0f}" height="{h:.0f}" corner-radius="{r}" fill="{fill}"{s}/>'


def Ln(x1, y1, x2, y2, col, w=6, arrow=False):
    a = f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-width="{w}"'
    if arrow: a += f' arrow-end="triangle" pointer-length="{2 * w + 14}" pointer-width="{2 * w + 12}"'
    return a + "/>"


def Pa(d, col, w=6):
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none"/>'


def Dot(cx, cy, r, fill):
    return f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r}" ry="{r}" fill="{fill}"/>'


def tag(cx, cy, letter, col):
    """Round badge with the pin letter; the label is inside the shape, so it is centred for free."""
    return f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="19" ry="19" fill="{col}"/>' + T(cx - 19, cy - 19, 38, 38, letter, 24, "#FFFFFF", 800, "center", "middle", ml=1)


def pal(i):
    return gen.pal(SL[i - 1]["tone"])


def frame(p, xx, yy, w, h, key):
    """White frame with the photo; key is the file name under lessons/L19/images/."""
    fid = gen.FILE_IDS[f"{LID}/images/{key}"]
    return R(xx, yy, w, h, "#FFFFFF", p["diagline"], 24) + f'<image src="{fid}" x="{xx + 14:.0f}" y="{yy + 14:.0f}" width="{w - 28:.0f}" height="{h - 28:.0f}" fit="contain"/>'


def credit(p, s, y=890):
    c = "; ".join(dict.fromkeys(im["credit"] for im in s.get("images", [])))
    return T(M, y, 1728, 52, "Hình: " + c, 22, p["sub"], 400, lh=1.1)


def panel(p, xx, yy, w, h):
    return R(xx, yy, w, h, p["diag"], p["diagline"], 28)


def gloss(p, items, xx, yy, w, ch, gap):
    out = []
    for k, b in enumerate(items):
        out += gen.gloss(p, p["sub"], b, xx, yy + k * (ch + gap), w, ch)  # a label that names no pin gets a neutral bar
    return out


def body_panel(p, s, xx, yy, w, h, size=34):
    a = p["ink"]  # a bold term that names no pin stays in the ink colour: the three pin colours mean pins only
    sz = gen.fit_rich(s["body"], w - 64, h - 56, size, 1.3, 24)
    return [R(xx, yy, w, h, p["card"], None, 22),
            f'<text x="{xx + 32:.0f}" y="{yy + 28:.0f}" width="{w - 64:.0f}" height="{h - 56:.0f}" format="html" font-size="{sz}" color="{p["ink"]}" line-height="1.3" vertical-align="top">{gen.rich(s["body"], p, 19, a, OPTS)}</text>']


# ---------------------------------------------------------------- symbols (unit u = s px; y up is negative)
def _pts(flip, s, cx, cy):
    def f(u, v):
        return cx + u * s, cy + (-v if flip else v) * s
    return f


def bjt(kind, cx, cy, s, ink, tags=True):
    """NPN (collector up, arrow out of the emitter) or PNP (the mirror image: emitter up, arrow into the bar). Returns (markup, terminals)."""
    flip = kind == "pnp"
    f = _pts(flip, s, cx, cy)
    P = lambda *a: " ".join(f"{'ML'[i > 0]}{f(*pt)[0]:.0f} {f(*pt)[1]:.0f}" for i, pt in enumerate(a))
    o = [Ln(*f(0, -0.5), *f(0, 0.5), ink, 10), Ln(*f(-1.15, 0), *f(0, 0), B, 7),
         Pa(P((0, -0.22), (0.65, -0.72), (0.65, -1.25)), C, 7), Ln(*f(0.65, 0.72), *f(0.65, 1.25), E, 7)]
    if kind == "npn":  # arrowhead at the outer end of the emitter diagonal, pointing away from the bar
        o.append(Ln(*f(0, 0.22), *f(0.65, 0.72), E, 7, True))
    else:  # arrowhead at the bar, pointing into the transistor
        o.append(Ln(*f(0.65, 0.72), *f(0, 0.22), E, 7, True))
    t = {"b": f(-1.15, 0), "c": f(0.65, -1.25), "e": f(0.65, 1.25)}
    if tags:
        o.append(tag(t["b"][0] - 30, t["b"][1], "B", B))
        for k, letter in (("c", "C"), ("e", "E")):
            tx, ty = t[k]
            o.append(tag(tx + 38, ty + (-8 if ty < cy else 8), letter, PIN[k]))
    return "".join(o), t


def mos(kind, cx, cy, s, ink, tags=True):
    """Enhancement MOSFET, three terminals, body tied to the source. N: drain up, arrow into the channel. P: mirror image, source up, arrow out."""
    flip = kind == "p"
    f = _pts(flip, s, cx, cy)
    P = lambda *a: " ".join(f"{'ML'[i > 0]}{f(*pt)[0]:.0f} {f(*pt)[1]:.0f}" for i, pt in enumerate(a))
    o = [Ln(*f(-1.2, 0), *f(-0.25, 0), B, 7), Ln(*f(-0.25, -0.5), *f(-0.25, 0.5), ink, 9)]
    for a_, b_ in ((-0.56, -0.28), (-0.14, 0.14), (0.28, 0.56)):
        o.append(Ln(*f(0, a_), *f(0, b_), ink, 9))
    o += [Pa(P((0, -0.42), (0.65, -0.42), (0.65, -1.25)), C, 7), Pa(P((0, 0.42), (0.65, 0.42), (0.65, 1.25)), E, 7),
          Ln(*f(0.65, 0), *f(0.65, 0.42), E, 7)]
    if kind == "n":  # arrow on the source side, pointing into the channel
        o.append(Ln(*f(0.65, 0), *f(0, 0), E, 7, True))
    else:  # pointing out of the channel
        o.append(Ln(*f(0, 0), *f(0.65, 0), E, 7, True))
    t = {"g": f(-1.2, 0), "d": f(0.65, -1.25), "s": f(0.65, 1.25)}
    if tags:
        o.append(tag(t["g"][0] - 30, t["g"][1], "G", B))
        for k, letter in (("d", "D"), ("s", "S")):
            tx, ty = t[k]
            o.append(tag(tx + 38, ty + (-8 if ty < cy else 8), letter, PIN[k]))
    return "".join(o), t


def jfet(kind, cx, cy, s, ink, tags=True):
    """JFET: channel line, gate lead with an arrow into the channel (N) or out of it (P)."""
    f = _pts(False, s, cx, cy)
    P = lambda *a: " ".join(f"{'ML'[i > 0]}{f(*pt)[0]:.0f} {f(*pt)[1]:.0f}" for i, pt in enumerate(a))
    o = [Ln(*f(0, -0.62), *f(0, 0.62), ink, 10), Pa(P((0, -0.42), (0.55, -0.42), (0.55, -1.25)), C, 7), Pa(P((0, 0.42), (0.55, 0.42), (0.55, 1.25)), E, 7)]
    if kind == "n":
        o.append(Ln(*f(-1.15, 0), *f(0, 0), B, 7, True))
    else:
        o += [Ln(*f(0, 0), *f(-0.55, 0), B, 7, True), Ln(*f(-0.55, 0), *f(-1.15, 0), B, 7)]
    t = {"g": f(-1.15, 0), "d": f(0.55, -1.25), "s": f(0.55, 1.25)}
    if tags:
        o.append(tag(t["g"][0] - 30, t["g"][1], "G", B))
        o.append(tag(t["d"][0] + 38, t["d"][1] - 8, "D", C))
        o.append(tag(t["s"][0] + 38, t["s"][1] + 8, "S", E))
    return "".join(o), t


def resistor(xx, yy, w, h, ink, vertical=False, label=None, lab_col=None, size=24):
    o = [R(xx, yy, w, h, "none", ink, 6, 5)]
    if label:
        o.append(T(xx + (w + 12 if vertical else 0), yy + (0 if vertical else -34), 90 if vertical else w, h if vertical else 30, label, size, lab_col or ink, 700,
                   None if vertical else "center", "middle" if vertical else "bottom"))
    return "".join(o)


def ground(cx, cy, ink):
    return Ln(cx, cy, cx, cy + 10, ink, 6) + "".join(Ln(cx - 34 + k * 9, cy + 10 + k * 14, cx + 34 - k * 9, cy + 10 + k * 14, ink, 6) for k in range(3))


def rail(xx1, xx2, yy, label, ink, right=False):
    lab = T(xx2 + 10, yy - 22, 80, 44, label, 28, ink, 800, "left", "middle", ml=1) if right else T(xx1 - 90, yy - 22, 80, 44, label, 28, ink, 800, "right", "middle", ml=1)
    return Ln(xx1, yy, xx2, yy, ink, 6) + lab


# ---------------------------------------------------------------- pages
def cover():
    o = OPTS
    out = ['<background fill="#14161C"/>']
    p = DARK
    out.append(T(M, 78, 1200, 40, o["topic_label"].upper(), 28, p["sub"], 700, ml=1).replace('font-size="28"', 'font-size="28" letter-spacing="6"'))
    out.append(f'<text x="{M}" y="150" width="1130" height="470" font-family="Bricolage Grotesque" font-weight="800" font-size="104" color="{p["ink"]}" line-height="1.04" max-lines="5" vertical-align="top">{x(DATA["title"])}</text>')
    out.append(T(M, 640, 1150, 110, o["question"], 40, "#FFB454", 600, lh=1.2, ml=2))
    cards = [("Base / Gate", B), ("Collector / Drain", C), ("Emitter / Source", E)]
    cw = 560
    for k, (c, col) in enumerate(cards):
        xx = M + k * (cw + 24)
        out.append(R(xx, 800, cw, 150, p["card"], col, 28, 5))
        out.append(Dot(xx + 56, 875, 18, col))
        out.append(T(xx + 96, 800, cw - 120, 150, c, 38, p["ink"], 700, va="middle", ml=2))
    # decoration: a big NPN symbol on the right
    mk, t = bjt("npn", 1560, 430, 190, "#F3EEE3")
    out.append(mk)
    return out


def p1():
    s, p = SL[0], pal(1)
    out = [panel(p, M, 250, 930, 640)]
    pipe_y = 600
    out += [R(140, pipe_y - 40, 370, 80, "#CDDCFB", C, 14, 4), R(640, pipe_y - 40, 290, 80, "#BDE5D6", E, 14, 4),
            R(500, pipe_y - 90, 150, 180, "#3A3F4B", None, 22), R(555, 410, 40, 100, "#3A3F4B", None, 8), R(480, 380, 190, 36, B, None, 16),
            Ln(165, pipe_y, 470, pipe_y, C, 12, True), Ln(665, pipe_y, 905, pipe_y, E, 12, True)]
    out.append(T(M + 30, 262, 870, 60, "Tay van nhỏ = cực điều khiển (Base / Gate)", 30, B, 800, "center", "middle", ml=1))
    out.append(Ln(575, 326, 575, 372, B, 6, True))
    out.append(T(700, 380, 220, 40, "xoay nhẹ", 28, B, 700, "left", "middle", ml=1))
    out.append(T(140, 660, 370, 110, "Nước vào = dòng chính vào (Collector / Drain)", 28, C, 800, "center", lh=1.15))
    out.append(T(640, 660, 290, 110, "Nước ra = dòng ra (Emitter / Source)", 28, E, 800, "center", lh=1.15))
    out.append(T(M + 40, 810, 850, 60, "Xoay nhẹ tay van, dòng nước lớn đổi theo", 30, p["sub"], 600, "center", "middle", ml=1))
    out += body_panel(p, s, 1056, 250, 768, 380, 32)
    for k, b in enumerate(s["bullets"]):
        yy = 656 + k * 84
        kk, v = split_kv(b)
        col = (B, C, E)[k]
        out.append(R(1056, yy, 768, 72, p["card"], None, 18) + R(1056, yy, 12, 72, col, None, 6))
        out.append(T(1090, yy, 720, 72, b, fit(b, 720, 66, 28, 1.15, 22, 0.57, 2), p["ink"], 600, va="middle", lh=1.1, ml=2))
    return out


def tree_leaf(p, cx, label, sym, kind):
    out = [R(cx - 110, 660, 220, 220, p["card"], p["diagline"], 22)]
    mk = {"bjt": bjt, "mos": mos, "jfet": jfet}[sym](kind, cx - 12, 745, 48, p["ink"], False)[0]
    out.append(mk)
    out.append(T(cx - 110, 826, 220, 46, label, 30, p["ink"], 800, "center", "middle", ml=1))
    return out


def p2():
    s, p = SL[1], pal(2)
    ink = p["ink"]
    out = [R(790, 262, 340, 78, ink, None, 22), T(790, 262, 340, 78, "Transistor", 44, p["bg"], 800, "center", "middle", ml=1, font="Bricolage Grotesque")]
    out += [Ln(960, 340, 960, 372, ink, 5), Ln(430, 372, 1275, 372, ink, 5), Ln(430, 372, 430, 400, ink, 5), Ln(1275, 372, 1275, 400, ink, 5)]
    for cx, w, name, sub in ((430, 520, "BJT", "điều khiển bằng dòng Base"), (1275, 600, "FET", "điều khiển bằng điện áp Gate")):
        out.append(R(cx - w / 2, 400, w, 100, p["diag"], ink, 22, 4))
        out.append(T(cx - w / 2, 404, w, 48, name, 40, ink, 800, "center", "middle", ml=1, font="Bricolage Grotesque"))
        out.append(T(cx - w / 2, 452, w, 40, sub, 26, p["sub"], 600, "center", "middle", ml=1))
    out += [Ln(430, 500, 430, 580, ink, 5), Ln(300, 580, 560, 580, ink, 5), Ln(300, 580, 300, 660, ink, 5), Ln(560, 580, 560, 660, ink, 5)]
    out += [Ln(1275, 500, 1275, 520, ink, 5), Ln(1015, 520, 1535, 520, ink, 5), Ln(1015, 520, 1015, 540, ink, 5), Ln(1535, 520, 1535, 540, ink, 5)]
    for cx, name, sub in ((1015, "MOSFET", "bật khi VGS vượt Vth"), (1535, "JFET", "thường dẫn khi VGS = 0")):
        out.append(R(cx - 215, 540, 430, 90, p["diag"], ink, 20, 4))
        out.append(T(cx - 215, 544, 430, 44, name, 34, ink, 800, "center", "middle", ml=1, font="Bricolage Grotesque"))
        out.append(T(cx - 215, 588, 430, 36, sub, 24, p["sub"], 600, "center", "middle", ml=1))
    out += [Ln(1015, 630, 1015, 645, ink, 5), Ln(900, 645, 1130, 645, ink, 5), Ln(900, 645, 900, 660, ink, 5), Ln(1130, 645, 1130, 660, ink, 5)]
    out += [Ln(1535, 630, 1535, 645, ink, 5), Ln(1420, 645, 1650, 645, ink, 5), Ln(1420, 645, 1420, 660, ink, 5), Ln(1650, 645, 1650, 660, ink, 5)]
    out += tree_leaf(p, 300, "NPN", "bjt", "npn") + tree_leaf(p, 560, "PNP", "bjt", "pnp")
    out += tree_leaf(p, 900, "Kênh N", "mos", "n") + tree_leaf(p, 1130, "Kênh P", "mos", "p")
    out += tree_leaf(p, 1420, "Kênh N", "jfet", "n") + tree_leaf(p, 1650, "Kênh P", "jfet", "p")
    return out


def p3():
    s, p = SL[2], pal(3)
    out = []
    y, h = 250, 396
    # photos: lineup (wide), TO-220 (tall), D2PAK (wide)
    out.append(frame(p, M, y, 660, h, "so-sanh-vo.jpg"))
    out.append(frame(p, 780, y, 260, h, "to220-fqp30n06l.jpg"))
    out.append(frame(p, 1080, y, 744, h, "d2pak.jpg"))
    caps = [(M, 660, "TO-92 và SOT-23", "TO-92 là viên nhựa ba chân thẳng hàng (2N3906); SOT-23 là vỏ dán, nhỏ nhất trong ảnh"),
            (780, 260, "TO-220", "tai kim loại bắt tản nhiệt"),
            (1080, 744, "D2PAK", "vỏ công suất dạng dán; que diêm làm thước đo")]
    for xx, w, name, cap in caps:
        out.append(T(xx, y + h + 6, w, 40, name, 30, p["ink"], 800, ml=1))
        out.append(T(xx, y + h + 44, w, 66, cap, fit(cap, w, 66, 24, 1.15, 22, 0.57, 2), p["sub"], 500, lh=1.15, ml=2))
    # pin-order strip
    sy = 790
    out.append(R(M, sy, 1728, 84, p["card"], None, 20))
    out.append(T(M + 28, sy, 600, 84, "Thứ tự chân: mỗi loại một kiểu, xem datasheet", 28, p["ink"], 700, va="middle", lh=1.1, ml=2))
    out.append(T(M + 660, sy, 200, 84, "2N3906 in:", 26, p["sub"], 600, va="middle", ml=1))
    for k, (ch, col) in enumerate((("E", E), ("B", B), ("C", C))):
        out.append(tag(M + 900 + k * 56, sy + 42, ch, col))
    out.append(T(M + 1100, sy, 280, 84, "IRLZ24N (TO-220):", 26, p["sub"], 600, va="middle", ml=2, lh=1.1))
    for k, (ch, col) in enumerate((("G", B), ("D", C), ("S", E))):
        out.append(tag(M + 1440 + k * 56, sy + 42, ch, col))
    out.append(credit(p, s))
    return out


def p4():
    s, p = SL[3], pal(4)
    out = [frame(p, M, 250, 400, 630, "bc547.jpg"), panel(p, 530, 250, 500, 630)]
    mk, t = bjt("npn", 770, 565, 128, p["ink"])
    out.append(mk)
    # control: IB into the base, VBE note
    bx, by = t["b"]
    out.append(Ln(bx - 110, by, bx - 62, by, B, 6, True))
    out.append(T(bx - 195, by - 50, 100, 36, "IB", 28, B, 800, "center", "middle", ml=1))
    out.append(T(548, 790, 464, 70, "VBE ≈ 0,6 V (nhiều giáo trình làm tròn 0,7 V)", 26, p["sub"], 600, "center", "middle", lh=1.1, ml=2))
    out += gloss(p, s["bullets"], 1060, 250, 764, 88, 14)
    out += body_panel(p, s, 1060, 250 + 3 * 102, 764, 630 - 3 * 102, 34)
    out.append(credit(p, s))
    return out


def circuit_npn(p, cx, cy, s_, rows):
    ink = p["ink"]
    mk, t = bjt("npn", cx, cy, s_, ink)
    out = [mk]
    cxw, cyw = t["c"]
    exw, eyw = t["e"]
    bxw, byw = t["b"]
    top = 300
    out.append(rail(cxw - 140, cxw + 140, top, "+V", ink))
    out.append(Ln(cxw, top, cxw, top + 40, ink, 6))
    out.append(R(cxw - 120, top + 40, 240, 100, p["card"], ink, 14, 4))
    out.append(T(cxw - 120, top + 40, 240, 100, "Tải: LED hoặc relay", 26, ink, 700, "center", "middle", lh=1.1, ml=2))
    out.append(Ln(cxw, top + 140, cxw, cyw - 22, ink, 6))
    out.append(Ln(exw, eyw + 22, exw, eyw + 54, ink, 6))
    out.append(ground(exw, eyw + 54, ink))
    # base side: resistor and control input
    rx = bxw - 220
    out.append(Ln(bxw - 38, byw, rx + 120, byw, ink, 6))
    out.append(resistor(rx, byw - 22, 120, 44, ink, False, "RB", ink))
    out.append(Ln(rx, byw, rx - 70, byw, ink, 6))
    out.append(Dot(rx - 70, byw, 9, ink))
    out.append(T(rx - 290, byw - 40, 210, 80, "tín hiệu từ vi điều khiển", 24, p["sub"], 600, "right", "middle", lh=1.1, ml=2))
    # currents
    out.append(Ln(rx - 56, byw + 46, rx + 100, byw + 46, B, 6, True))
    out.append(T(rx - 56, byw + 52, 160, 36, "IB (nhỏ)", 26, B, 800, "center", "middle", ml=1))
    out.append(Ln(cxw + 92, top + 150, cxw + 92, cyw - 34, C, 14, True))
    out.append(T(cxw + 116, top + 150, 120, 44, "IC", 30, C, 800, "left", "middle", ml=1))
    out.append(Ln(exw + 92, eyw + 12, exw + 92, eyw + 46, E, 10, True))
    out.append(T(exw + 116, eyw + 6, 120, 44, "IE", 30, E, 800, "left", "middle", ml=1))
    return out


def p5():
    s, p = SL[4], pal(5)
    out = [panel(p, M, 250, 1010, 640)]
    out += circuit_npn(p, 700, 650, 100, None)
    rx, rw = 1140, 684
    cols = (B, C, p["ink"], E, p["sub"])
    for k, b in enumerate(s["bullets"]):
        yy = 250 + k * 130
        out.append(R(rx, yy, rw, 118, p["card"], None, 20) + R(rx, yy, 12, 118, cols[k], None, 6))
        out.append(T(rx + 36, yy, rw - 56, 118, b, fit(b, rw - 56, 108, 32, 1.2, 24, 0.57), p["ink"], 600 if k != 2 else 800, va="middle", lh=1.2))
    return out


def circuit_pnp(p, cx, cy, s_):
    ink = p["ink"]
    mk, t = bjt("pnp", cx, cy, s_, ink)
    out = [mk]
    exw, eyw = t["e"]
    cxw, cyw = t["c"]
    bxw, byw = t["b"]
    top = 290
    out.append(rail(exw - 110, exw + 110, top, "+V", ink))
    out.append(Ln(exw, top, exw, eyw - 22, ink, 6))
    out.append(Ln(cxw, cyw + 22, cxw, cyw + 60, ink, 6))
    out.append(R(cxw - 110, cyw + 60, 220, 90, p["card"], ink, 14, 4))
    out.append(T(cxw - 110, cyw + 60, 220, 90, "Tải", 28, ink, 700, "center", "middle", ml=1))
    out.append(Ln(cxw, cyw + 150, cxw, cyw + 170, ink, 6))
    out.append(ground(cxw, cyw + 170, ink))
    rx = bxw - 200
    out.append(Ln(bxw - 38, byw, rx + 110, byw, ink, 6))
    out.append(resistor(rx, byw - 22, 110, 44, ink, False, "RB", ink))
    out.append(Ln(rx, byw, rx - 50, byw, ink, 6))
    out.append(Dot(rx - 50, byw, 9, ink))
    out.append(T(rx - 52, byw + 108, 230, 70, "kéo xuống thấp để bật", 24, p["sub"], 600, "left", lh=1.1, ml=2))
    # currents: IB leaves the base (arrow points away from the transistor), IE in, IC out
    out.append(Ln(rx + 100, byw + 46, rx - 40, byw + 46, B, 6, True))
    out.append(T(rx - 40, byw + 56, 160, 36, "IB (ra)", 26, B, 800, "center", "middle", ml=1))
    out.append(Ln(exw + 92, eyw - 80, exw + 92, eyw - 30, E, 12, True))
    out.append(T(exw + 116, eyw - 90, 140, 44, "IE", 30, E, 800, "left", "middle", ml=1))
    out.append(Ln(cxw + 92, cyw + 14, cxw + 92, cyw + 56, C, 12, True))
    out.append(T(cxw + 116, cyw + 8, 140, 44, "IC", 30, C, 800, "left", "middle", ml=1))
    return out


def p6():
    s, p = SL[5], pal(6)
    out = [frame(p, M, 250, 330, 630, "pnp-2n3906.jpg"), panel(p, 450, 250, 560, 630)]
    out += circuit_pnp(p, 760, 560, 96)
    out += gloss(p, s["bullets"], 1040, 250, 784, 88, 14)
    out += body_panel(p, s, 1040, 250 + 3 * 102, 784, 630 - 3 * 102, 34)
    out.append(credit(p, s))
    return out


def p7():
    s, p = SL[6], pal(7)
    out = [frame(p, M, 250, 400, 630, "irfibc30.jpg"), panel(p, 530, 250, 500, 630)]
    mk, t = mos("n", 760, 565, 128, p["ink"])
    out.append(mk)
    gx, gy = t["g"]
    out.append(T(548, 790, 464, 70, "VGS = điện áp giữa Gate và Source; bật khi VGS > Vth", 26, p["sub"], 600, "center", "middle", lh=1.1, ml=2))
    out.append(Ln(gx - 130, gy, gx - 66, gy, B, 6, True))
    out.append(T(gx - 235, gy - 50, 130, 36, "VGS", 28, B, 800, "center", "middle", ml=1))
    out += gloss(p, s["bullets"], 1060, 250, 764, 140, 24)
    out.append(credit(p, s))
    return out


def p8():
    s, p = SL[7], pal(8)
    ink = p["ink"]
    out = [panel(p, M, 250, 1010, 640)]
    mk, t = mos("n", 690, 650, 100, ink)
    out.append(mk)
    gx, gy = t["g"]
    dx, dy = t["d"]
    sx, sy = t["s"]
    top = 300
    out.append(rail(dx - 140, dx + 140, top, "+V", ink))
    out.append(Ln(dx, top, dx, top + 40, ink, 6))
    out.append(R(dx - 120, top + 40, 240, 100, p["card"], ink, 14, 4))
    out.append(T(dx - 120, top + 40, 240, 100, "Tải: LED, relay, van", 26, ink, 700, "center", "middle", lh=1.1, ml=2))
    out.append(Ln(dx, top + 140, dx, dy - 22, ink, 6))
    out.append(Ln(sx, sy + 22, sx, sy + 54, ink, 6))
    out.append(ground(sx, sy + 54, ink))
    rx = gx - 38 - 120 - 70
    out.append(Ln(gx - 38, gy, rx + 110, gy, ink, 6))
    out.append(resistor(rx, gy - 22, 110, 44, ink, False, "RG", ink))
    out.append(Ln(rx, gy, rx - 60, gy, ink, 6))
    out.append(Dot(rx - 60, gy, 9, ink))
    out.append(T(rx - 280, gy - 40, 210, 80, "điện áp từ vi điều khiển", 24, p["sub"], 600, "right", "middle", lh=1.1, ml=2))
    # pull-down from the gate node to ground
    jx = gx - 90
    out.append(Dot(jx, gy, 9, ink))
    out.append(Ln(jx, gy, jx, gy + 90, ink, 6))
    out.append(resistor(jx - 22, gy + 90, 44, 90, ink, True, "RGS", ink))
    out.append(Ln(jx, gy + 180, jx, gy + 210, ink, 6))
    out.append(ground(jx, gy + 210, ink))
    # control (voltage only) and main current
    out.append(T(rx - 56, gy - 112, 330, 40, "IG ≈ 0 ở trạng thái tĩnh", 26, B, 800, "left", "middle", ml=1))
    out.append(Ln(dx + 92, top + 150, dx + 92, dy - 34, C, 14, True))
    out.append(T(dx + 116, top + 150, 160, 44, "ID", 30, C, 800, "left", "middle", ml=1))
    out.append(Ln(sx + 92, sy + 12, sx + 92, sy + 46, C, 12, True))
    out.append(T(sx + 116, sy + 6, 120, 44, "ID", 30, C, 800, "left", "middle", ml=1))
    rx2, rw = 1140, 684
    for k, b in enumerate(s["bullets"]):
        yy = 250 + k * 130
        col = (E, C, B, p["ink"], p["sub"])[k]
        out.append(R(rx2, yy, rw, 118, p["card"], None, 20) + R(rx2, yy, 12, 118, col, None, 6))
        out.append(T(rx2 + 36, yy, rw - 56, 118, b, fit(b, rw - 56, 108, 32, 1.2, 24, 0.57), p["ink"], 600, va="middle", lh=1.2))
    return out


def circuit_pmos(p, cx, cy, s_):
    ink = p["ink"]
    mk, t = mos("p", cx, cy, s_, ink)
    out = [mk]
    gx, gy = t["g"]
    sxw, syw = t["s"]
    dxw, dyw = t["d"]
    top = 290
    out.append(rail(sxw - 110, sxw + 110, top, "+V", ink, True))
    out.append(Ln(sxw, top, sxw, syw - 22, ink, 6))
    out.append(Ln(dxw, dyw + 22, dxw, dyw + 56, ink, 6))
    out.append(R(dxw - 110, dyw + 56, 220, 90, p["card"], ink, 14, 4))
    out.append(T(dxw - 110, dyw + 56, 220, 90, "Tải", 28, ink, 700, "center", "middle", ml=1))
    out.append(Ln(dxw, dyw + 146, dxw, dyw + 166, ink, 6))
    out.append(ground(dxw, dyw + 166, ink))
    rx = gx - 38 - 110 - 40
    out.append(Ln(gx - 38, gy, rx + 110, gy, ink, 6))
    out.append(resistor(rx, gy - 22, 110, 44, ink, False, "RG", ink))
    out.append(Ln(rx, gy, rx - 40, gy, ink, 6))
    out.append(Dot(rx - 40, gy, 9, ink))
    out.append(T(rx - 52, gy + 30, 200, 70, "kéo xuống thấp để bật", 24, p["sub"], 600, "left", lh=1.1, ml=2))
    # pull-up from the gate node to +V (keeps VGS = 0 when the input floats)
    jx = gx - 76
    out.append(Dot(jx, gy, 9, ink))
    out.append(Ln(jx, gy, jx, gy - 40, ink, 6))
    out.append(resistor(jx - 20, gy - 130, 40, 90, ink, True, "RGS", ink, 22))
    out.append(Ln(jx, gy - 130, jx, top, ink, 6))
    out.append(Ln(jx, top, sxw - 110, top, ink, 6))
    out.append(Dot(jx, top, 9, ink))
    out.append(Ln(sxw + 92, syw - 80, sxw + 92, syw - 30, C, 12, True))
    out.append(T(sxw + 116, syw - 92, 120, 44, "ID", 30, C, 800, "left", "middle", ml=1))
    out.append(Ln(dxw + 92, dyw + 14, dxw + 92, dyw + 52, C, 12, True))
    out.append(T(dxw + 116, dyw + 8, 120, 44, "ID", 30, C, 800, "left", "middle", ml=1))
    return out


def p9():
    s, p = SL[8], pal(9)
    out = [frame(p, M, 250, 460, 330, "irfi9540.jpg"), panel(p, M, 600, 460, 280)]
    out.append(T(M + 24, 612, 412, 256, "IRFI9540: kênh P, cùng vỏ TO-220 fullpak với IRFIBC30 (kênh N); chỉ mã ghi trên thân phân biệt được", 26, p["ink"], 600, "left", "middle", lh=1.2, ml=6))
    out.append(panel(p, 580, 250, 540, 630))
    out += circuit_pmos(p, 850, 580, 92)
    out += gloss(p, s["bullets"], 1150, 250, 674, 88, 14)
    out += body_panel(p, s, 1150, 250 + 3 * 102, 674, 630 - 3 * 102, 32)
    out.append(credit(p, s))
    return out


def cross(p, xx, yy, w, kind):
    """Cross-section sketch inside a card at (xx, yy) of width w: substrate, two wells, oxide, gate, carriers."""
    n = kind == "n"
    sub_fill, well_fill = ("#E9D2BF", "#9CB7E6") if n else ("#BFD6E9", "#E3A894")
    sub_lab, well_lab = ("Đế loại P", "N+") if n else ("Đế loại N", "P+")
    o = []
    gx0, gx1 = xx + 250, xx + w - 250
    sy = yy + 150
    o.append(R(xx + 20, sy, w - 40, 170, sub_fill, None, 10))
    o.append(R(xx + 60, sy, 190, 74, well_fill, None, 8) + R(xx + w - 250, sy, 190, 74, well_fill, None, 8))
    o.append(T(xx + 60, sy, 190, 74, well_lab, 28, "#14161C", 800, "center", "middle", ml=1))
    o.append(T(xx + w - 250, sy, 190, 74, well_lab, 28, "#14161C", 800, "center", "middle", ml=1))
    o.append(R(gx0 - 30, sy - 22, gx1 - gx0 + 60, 20, "#D9D9D9", "#9A9A9A", 4, 2))      # oxide
    o.append(R(gx0 - 30, sy - 78, gx1 - gx0 + 60, 56, B, None, 8))                       # gate metal
    o.append(T(gx0 - 30, sy - 78, gx1 - gx0 + 60, 56, "Gate", 26, "#FFFFFF", 800, "center", "middle", ml=1))
    o.append(R(xx + 104, sy - 36, 100, 34, E, None, 6) + Ln(xx + 154, sy - 36, xx + 154, sy - 96, E, 6))
    o.append(R(xx + w - 204, sy - 36, 100, 34, C, None, 6) + Ln(xx + w - 154, sy - 36, xx + w - 154, sy - 96, C, 6))
    o.append(tag(xx + 154, sy - 118, "S", E) + tag(xx + w - 154, sy - 118, "D", C))
    o.append(tag((gx0 + gx1) / 2, sy - 118, "G", B))
    o.append(T(xx + 20, sy + 94, w - 40, 36, sub_lab, 26, "#14161C", 700, "center", "middle", ml=1))
    # carriers in the channel: electrons (dark, minus) or holes (light, plus)
    n_c = 6
    for k in range(n_c):
        cx = gx0 + 20 + k * ((gx1 - gx0 - 40) / (n_c - 1))
        if n:
            o.append(Dot(cx, sy + 18, 17, "#1B2A66") + T(cx - 17, sy + 1, 34, 34, "−", 26, "#FFFFFF", 800, "center", "middle", ml=1))
        else:
            o.append(Dot(cx, sy + 18, 17, "#FFFFFF") + f'<ellipse cx="{cx:.0f}" cy="{sy + 18:.0f}" rx="17" ry="17" fill="none" stroke="#8A2B14" stroke-width="3"/>' + T(cx - 17, sy + 1, 34, 34, "+", 26, "#8A2B14", 800, "center", "middle", ml=1))
    return o


def p10():
    s, p = SL[9], pal(10)
    out = []
    w = 846
    for k, (kind, head, volt, sub) in enumerate((("n", "Kênh N", "VGS dương", "electron chạy từ Source đến Drain; dòng quy ước chảy D → S"),
                                                   ("p", "Kênh P", "VGS âm", "lỗ trống chạy từ Source đến Drain; dòng quy ước chảy S → D"))):
        xx = M + k * (w + 36)
        out.append(R(xx, 250, w, 520, p["card"], None, 26))
        out.append(T(xx + 30, 262, 300, 50, head, 38, p["ink"], 800, va="middle", ml=1, font="Bricolage Grotesque"))
        out.append(T(xx + 330, 262, w - 360, 50, volt + (": kéo electron lên mặt" if kind == "n" else ": kéo lỗ trống lên mặt"), 26, B, 800, "right", "middle", ml=1))
        out += cross(p, xx, 340, w, kind)
        out.append(T(xx + 30, 690, w - 60, 66, sub, fit(sub, w - 60, 66, 26, 1.15, 22, 0.57, 2), p["sub"], 600, "center", "middle", lh=1.15, ml=2))
    out.append(R(M, 790, 1728, 86, p["diag"], p["diagline"], 20))
    out.append(T(M + 28, 790, 1672, 86, "Kênh N dẫn bằng electron · Kênh P dẫn bằng lỗ trống (hole)", 34, p["ink"], 800, "center", "middle", ml=1))
    return out


def p11():
    s, p = SL[10], pal(11)
    out = [frame(p, M, 250, 330, 630, "jfet-k170.jpg"), panel(p, 450, 250, 560, 630)]
    mk, t = jfet("n", 690, 520, 110, p["ink"])
    out.append(mk)
    out.append(T(470, 706, 520, 40, "JFET kênh N (mũi tên ở Gate chỉ vào kênh)", 24, p["sub"], 600, "center", "middle", ml=1))
    out.append(Ln(480, 770, 640, 770, C, 16, True))
    out.append(T(660, 744, 330, 52, "VGS = 0: ID lớn", 28, p["ink"], 800, "left", "middle", ml=1))
    out.append(Ln(480, 830, 520, 830, C, 5, True))
    out.append(T(560, 804, 440, 52, "VGS âm: ID giảm đến 0", 28, p["ink"], 800, "left", "middle", ml=1))
    out += gloss(p, s["bullets"], 1040, 250, 784, 140, 24)
    out.append(credit(p, s))
    return out


def p12():
    s, p = SL[11], pal(12)
    ink = p["ink"]
    cols = (440, 640, 648)
    x0 = [M, M + 440 + 0, M + 440 + 640]
    out = [R(M, 250, 1728, 64, ink, None, 16)]
    heads = ("Tiêu chí", "BJT", "MOSFET")
    xx = M
    for k, h in enumerate(heads):
        out.append(T(xx + 24, 250, cols[k] - 48, 64, h, 32, p["bg"], 800, va="middle", ml=1))
        xx += cols[k]
    rh, gap = 104, 8
    for r, b in enumerate(s["bullets"]):
        kk, vv = split_kv(b)
        a, c_ = (z.replace(" (BJT)", "").replace(" (MOSFET)", "") for z in vv.split(" · "))
        yy = 326 + r * (rh + gap)
        out.append(R(M, yy, 1728, rh, p["card"] if r % 2 == 0 else p["diag"], p["diagline"], 16, 2))
        xx = M
        for k, txt in enumerate((kk, a, c_)):
            size = fit(txt, cols[k] - 48, rh - 14, 30 if k else 32, 1.15, 22, 0.57, 3)
            out.append(T(xx + 24, yy, cols[k] - 48, rh, txt, size, ink if k else p["acc"][1], 800 if k == 0 else 500, va="middle", lh=1.15, ml=3))
            xx += cols[k]
    return out


def sym_card(p, xx, yy, w, h, kind, name, arrow_txt, cur_txt, on_txt):
    ink = p["ink"]
    out = [R(xx, yy, w, h, p["card"], None, 26)]
    sym = {"npn": lambda: bjt("npn", xx + 150, yy + 210, 74, ink), "pnp": lambda: bjt("pnp", xx + 150, yy + 210, 74, ink),
           "n": lambda: mos("n", xx + 150, yy + 210, 74, ink), "p": lambda: mos("p", xx + 150, yy + 210, 74, ink)}[kind]()
    out.append(sym[0])
    out.append(Ln(xx + w - 70, yy + 130, xx + w - 70, yy + 290, C, 12, True))
    out.append(T(xx + w - 120, yy + 300, 100, 36, "dòng", 24, C, 800, "center", "middle", ml=1))
    out.append(T(xx + 24, yy + 350, w - 48, 54, name, 40, ink, 800, ml=1, font="Bricolage Grotesque"))
    out.append(T(xx + 24, yy + 410, w - 48, 90, arrow_txt, fit(arrow_txt, w - 48, 90, 28, 1.15, 22, 0.57, 3), ink, 600, lh=1.15, ml=3))
    out.append(T(xx + 24, yy + 500, w - 48, 60, cur_txt, 28, C, 800, va="middle", ml=1))
    out.append(T(xx + 24, yy + 560, w - 48, 70, on_txt, fit(on_txt, w - 48, 70, 26, 1.15, 22, 0.57, 2), B, 700, lh=1.15, ml=2))
    return out


def p13():
    s, p = SL[12], pal(13)
    out = []
    w, gap = 408, 32
    spec = (("npn", "NPN", "Mũi tên ở Emitter chỉ ra ngoài", "Dòng C → E", "Bật: Base cao hơn Emitter ~0,6 V"),
            ("pnp", "PNP", "Mũi tên ở Emitter chỉ vào trong", "Dòng E → C", "Bật: Base thấp hơn Emitter ~0,6 V"),
            ("n", "N-MOS", "Mũi tên chỉ vào kênh", "Dòng D → S", "Bật: VGS > Vth (dương)"),
            ("p", "P-MOS", "Mũi tên chỉ ra khỏi kênh", "Dòng S → D", "Bật: VGS âm, dưới −|Vth|"))
    for k, sp in enumerate(spec):
        out += sym_card(p, M + k * (w + gap), 250, w, 640, *sp)
    return out


def p14():
    s, p = SL[13], pal(14)
    ink = p["ink"]
    out = [panel(p, M, 250, 860, 640)]
    # meter body
    out += [R(130, 285, 330, 260, "#2B2F3A", None, 28), R(160, 312, 270, 96, "#C9D8B8", None, 12),
            T(160, 312, 270, 96, "sụt áp thuận", 30, "#1B2A14", 800, "center", "middle", ml=1),
            Dot(295, 478, 40, "#555B6A"), T(255, 458, 80, 40, "diode", 22, "#FFFFFF", 700, "center", "middle", ml=1)]
    out.append(Dot(200, 545, 14, "#D32F2F") + Dot(390, 545, 14, "#14161C"))
    # NPN under test
    mk, t = bjt("npn", 640, 560, 100, ink)
    out.append(mk)
    bx, by = t["b"]
    cx_, cy_ = t["c"]
    ex_, ey_ = t["e"]
    out.append(Pa(f"M200 548 C 200 640 {bx - 150:.0f} {by:.0f} {bx - 70:.0f} {by:.0f}", "#D32F2F", 7))
    out.append(Dot(bx - 70, by, 10, "#D32F2F"))
    out.append(Pa(f"M390 548 C 470 420 {cx_ + 20:.0f} {cy_ - 30:.0f} {cx_ - 20:.0f} {cy_ + 40:.0f}", "#14161C" if p is LIGHT else "#F3EEE3", 7))
    out.append(Dot(cx_ - 20, cy_ + 40, 10, "#14161C" if p is LIGHT else "#F3EEE3"))
    out.append(T(150, 790, 800, 80, "Que đỏ (+) ở Base; que đen (−) lần lượt ở Collector rồi Emitter", 26, p["sub"], 600, "center", "middle", lh=1.15, ml=2))
    rx, rw = 1000, 824
    cols = (ink,) * 4  # the step numbers carry no pin meaning, so no pin colour
    for k, b in enumerate(s["bullets"]):
        yy = 250 + k * 162
        out.append(R(rx, yy, rw, 148, p["card"], None, 22) + R(rx, yy, 12, 148, cols[k], None, 6))
        out.append(T(rx + 40, yy, 84, 148, str(k + 1), 56, cols[k], 800, va="middle", ml=1, font="Bricolage Grotesque"))
        out.append(T(rx + 130, yy, rw - 154, 148, b, fit(b, rw - 154, 136, 30, 1.2, 22, 0.57), ink, 600, va="middle", lh=1.2))
    return out


def cmos_inverter(p, cx, cy):
    ink = p["ink"]
    o = [panel(p, cx - 210, 250, 420, 630)]
    mp, tp = mos("p", cx + 20, cy - 130, 64, ink, False)
    mn, tn = mos("n", cx + 20, cy + 140, 64, ink, False)
    o += [mp, mn]
    top = tp["s"][1] - 30
    o.append(Ln(tp["s"][0], tp["s"][1], tp["s"][0], top, ink, 6) + Ln(tp["s"][0] - 60, top, tp["s"][0] + 60, top, ink, 6) + T(tp["s"][0] - 150, top - 22, 80, 44, "+V", 26, ink, 800, "right", "middle", ml=1))
    gnd = tn["s"][1] + 24
    o.append(Ln(tn["s"][0], tn["s"][1], tn["s"][0], gnd, ink, 6) + ground(tn["s"][0], gnd, ink))
    # drains joined to the output; gates joined to the input
    out_x = tp["d"][0]
    o.append(Pa(f"M{tp['d'][0]:.0f} {tp['d'][1]:.0f} L{tn['d'][0]:.0f} {tn['d'][1]:.0f}", ink, 6))
    midy = (tp["d"][1] + tn["d"][1]) / 2
    o.append(Ln(out_x, midy, out_x + 80, midy, ink, 6) + Dot(out_x, midy, 9, ink) + T(out_x + 90, midy - 22, 120, 44, "Vra", 26, ink, 800, "left", "middle", ml=1))
    gxp, gyp = tp["g"]
    gxn, gyn = tn["g"]
    o.append(Pa(f"M{gxp:.0f} {gyp:.0f} L{gxp - 40:.0f} {gyp:.0f} L{gxn - 40:.0f} {gyn:.0f} L{gxn:.0f} {gyn:.0f}", B, 6))
    midg = (gyp + gyn) / 2
    o.append(Ln(gxp - 40, midg, gxp - 100, midg, B, 6) + Dot(gxp - 40, midg, 9, B) + T(gxp - 180, midg - 22, 70, 44, "Vào", 26, B, 800, "right", "middle", ml=1))
    o.append(T(cx - 200, 250 + 580 - 4, 400, 44, "PMOS ở trên + NMOS ở dưới", 24, p["sub"], 600, "center", "middle", ml=1))
    return o


def p15():
    s, p = SL[14], pal(15)
    out = [frame(p, M, 250, 470, 470, "renault-sot223.jpg"), R(M, 740, 470, 140, p["card"], None, 20)]
    out.append(T(M + 20, 740, 430, 140, "Bo mạch bộ điều khiển Renault: transistor NPN BCP56-16 vỏ SOT-223", 24, p["ink"], 600, va="middle", lh=1.2, ml=4))
    out += cmos_inverter(p, 890, 560)
    out += gloss(p, s["bullets"], 1140, 250, 684, 88, 14)
    out += body_panel(p, s, 1140, 250 + 3 * 102, 684, 630 - 3 * 102, 32)
    out.append(credit(p, s))
    return out


def p16():
    s, p = SL[15], pal(16)
    ink = p["ink"]
    out = [panel(p, M, 250, 880, 640), T(M + 30, 262, 820, 50, "Cheat sheet", 36, p["acc"][1], 800, ml=1, font="Bricolage Grotesque")]
    rows = (("npn", "NPN: IB vào, VBE ≈ 0,6 V, IC = β·IB, dòng C → E"),
            ("pnp", "PNP: IB ra, Base thấp hơn Emitter, dòng E → C"),
            ("n", "N-MOS: bật khi VGS > Vth, gần như không có IG, dòng D → S"),
            ("p", "P-MOS: bật khi VGS âm, dòng S → D"),
            ("j", "JFET: thường dẫn khi VGS = 0, VGS ngược chiều bóp kênh"))
    for k, (kind, txt) in enumerate(rows):
        yy = 322 + k * 112
        out.append(R(M + 24, yy, 832, 100, p["card"], None, 18))
        sym = {"npn": lambda: bjt("npn", M + 92, yy + 50, 34, ink, False), "pnp": lambda: bjt("pnp", M + 92, yy + 50, 34, ink, False),
               "n": lambda: mos("n", M + 92, yy + 50, 34, ink, False), "p": lambda: mos("p", M + 92, yy + 50, 34, ink, False),
               "j": lambda: jfet("n", M + 92, yy + 50, 34, ink, False)}[kind]()
        out.append(sym[0])
        out.append(T(M + 170, yy, 670, 100, txt, fit(txt, 670, 92, 28, 1.15, 22, 0.57, 3), ink, 600, va="middle", lh=1.15, ml=3))
    rx, rw = 1020, 804
    out.append(T(rx, 262, rw, 50, "Tự kiểm tra", 36, p["acc"][1], 800, ml=1, font="Bricolage Grotesque"))
    for k, b in enumerate(s["bullets"]):
        yy = 322 + k * 112
        out.append(R(rx, yy, rw, 100, p["card"], None, 18))
        out.append(T(rx + 20, yy, 70, 100, str(k + 1), 52, p["acc"][1], 800, va="middle", ml=1, font="Bricolage Grotesque"))
        out.append(T(rx + 100, yy, rw - 124, 100, b, fit(b, rw - 124, 92, 28, 1.15, 22, 0.57, 3), ink, 600, va="middle", lh=1.15, ml=3))
    return out


PAGES = {1: p1, 2: p2, 3: p3, 4: p4, 5: p5, 6: p6, 7: p7, 8: p8, 9: p9, 10: p10, 11: p11, 12: p12, 13: p13, 14: p14, 15: p15, 16: p16}


def page(i):
    if i == 17:  # the sources slide of gen.py, with neutral labels: the accent colours cycle there and would read as pin colours
        import re
        return re.sub(r'(font-weight="800" font-size="26" color=")#[0-9A-Fa-f]{6}', r'\1#9AA0B5', gen.page(LID, 17, OPTS))
    if i == 0:
        body = cover()
    else:
        s = SL[i - 1]
        p = gen.pal(s["tone"])
        body = [f'<background fill="{p["bg"]}"/>', gen.title(p, s["title"])] + PAGES[i]()
        body.append(T(M, 944, 1728, 36, "Nguồn: " + " ".join(f"[{z}]" for z in s["sources"]), 24, p["sub"], 500, ml=1))
        body.append(gen.footer(p, LID, i, TOTAL))
    return '<content font-family="Be Vietnam Pro">\n' + "\n".join(z for z in body if z) + "\n</content>"


if __name__ == "__main__":
    print(page(int(sys.argv[1])))

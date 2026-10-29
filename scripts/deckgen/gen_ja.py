"""Japanese deck markup for L17/L18 (docs/deck-style.md): gen.py with CJK-aware wrapping (Moda breaks lines only at spaces, so phrase spaces are inserted) and Noto Sans JP.
usage: gen_ja.py <L17|L18> <page 0..N> | check   (reads lessons/<id>/slides.ja.json and scripts/deckgen/opts/<id>.ja.json)"""
import importlib.util, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("g", ROOT / "scripts/deckgen/gen.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
def _w(tok, size):
    return sum(size * (1.0 if ord(c) > 0x2E7F else 0.58) for c in tok)
def lines_ja(text, w, size, cw):
    """Moda breaks only at spaces: greedy fill by space-separated phrase, a phrase wider than the box wraps by itself."""
    n = 0
    for para in zw(text).split("\n"):
        n += 1; cur = 0.0
        for tok in para.split(" "):
            tw = _w(tok, size)
            sp = size * 0.3 if cur else 0
            if cur and cur + sp + tw > w:
                n += 1; cur = 0.0; sp = 0
            if tw > w:
                n += int(tw // w); cur = tw % w
            else:
                cur += sp + tw
    return n
g.lines = lines_ja
from xml.sax.saxutils import escape as _esc
def _hira(c): return "\u3041" <= c <= "\u309f"
def _punct(c): return c in "、。：！？；，"
def _open_ok(c): return ord(c) > 0x2E7F and not _hira(c) and c not in "、。，．）」』】〕！？：；ー・" or (c.isascii() and c.isalnum())
def zw(t):
    """Insert a real space at phrase boundaries (kana/punctuation followed by kanji, katakana or a letter): Moda wraps only at spaces."""
    out = []
    for i, ch in enumerate(t):
        out.append(ch)
        nxt = t[i + 1] if i + 1 < len(t) else ""
        if not nxt or nxt == " " or ch == " ": continue
        if ch == "、" and nxt.isdigit(): continue
        if (_hira(ch) or _punct(ch) or ch in "）」』】") and _open_ok(nxt):
            out.append(" ")
    return "".join(out)
g.x = lambda t: _esc(zw(t), {'"': "&quot;"})
LID = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1][0] == "L" else "L17"
OPTS = json.loads((ROOT / f"scripts/deckgen/opts/{LID}.ja.json").read_text(encoding="utf-8"))
SL = ROOT / f"lessons/{LID}/slides.ja.json"
def page(i):
    m = g.page(LID, i, OPTS, str(SL))
    m = m.replace('font-family="Bricolage Grotesque"', 'font-family="Noto Sans JP"').replace('<content font-family="Be Vietnam Pro">', '<content font-family="Noto Sans JP">')
    return m.replace("Nguồn:", "出典:").replace("Hình:", "図:")
if __name__ == "__main__":
    if sys.argv[2] == "check":
        n = len(json.loads(SL.read_text(encoding="utf-8"))["slides"]) + 1
        for i in range(n):
            g.PENDING_IDS = []
            try: mk = g.page(LID, i, OPTS, str(SL))
            except SystemExit as e: print(i, "ERR", e); continue
            for t in g.overflows(mk): print(i, "OVERFLOW", t[:60])
            if g.PENDING_IDS: print(i, "pending ids", g.PENDING_IDS)
    else:
        print(page(int(sys.argv[2])))

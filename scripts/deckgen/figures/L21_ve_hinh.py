#!/usr/bin/env python3
"""Sơ đồ vector của bài L21 (kim tự tháp bộ nhớ, bản đồ trong máy, cell NAND, 3D NAND, SATA/NVMe, PCIe, CMR/SMR, SRAM/DRAM, HBM, CXL).

usage: L21_ve_hinh.py <thư mục ra>   viết các tệp .svg, rồi thử đổi sang .png bằng Playwright (node) nếu có.
Màu mỗi nhóm cố định: HDD hổ phách, SSD xanh dương, RAM xanh ngọc, HBM đỏ, nhóm khác tím. Chữ ≥ 28 để còn đọc được khi hình thu còn khoảng 64%.
"""
import math, os, subprocess, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
from xml.sax.saxutils import escape
HDD, HDDT = "#B45309", "#F3DFB8"; SSD, SSDT = "#1F3FD1", "#DDE3FA"; RAM, RAMT = "#0F766E", "#CFE8E2"
HBM, HBMT = "#E8472B", "#F8D9D0"; OTH, OTHT = "#7A4FB5", "#E6DDF3"; INK, SUB, LINE, BG = "#14161C", "#6B6A66", "#DDD5C1", "#FBF8F2"
FONT = "Inter, DejaVu Sans, sans-serif"
class S:
    def __init__(s, w, h, bg="#FFFFFF"):
        s.w, s.h, s.o = w, h, [f'<rect width="{w}" height="{h}" fill="{bg}"/>']
    def add(s, x): s.o.append(x); return s
    def rect(s, x, y, w, h, fill="none", stroke="none", sw=2, r=10, extra=""):
        return s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
    def text(s, x, y, t, size=28, fill=INK, w=500, anchor="start", bold=False, lh=1.2):
        weight = 700 if bold else 500; a = {"start": "start", "middle": "middle", "end": "end"}[anchor]
        for k, line in enumerate(str(t).split("\n")):
            s.add(f'<text x="{x}" y="{y + k * size * lh:.0f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{a}">{escape(line)}</text>')
        return s
    def line(s, x1, y1, x2, y2, c=INK, sw=3, dash=""):
        return s.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}" {"stroke-dasharray=%s" % chr(34)+dash+chr(34) if dash else ""}/>')
    def arrow(s, x1, y1, x2, y2, c=INK, sw=4, head=14):
        import math
        a = math.atan2(y2 - y1, x2 - x1); hx, hy = x2 - head * math.cos(a), y2 - head * math.sin(a)
        s.line(x1, y1, hx, hy, c, sw)
        p = [(x2, y2), (hx + head * .55 * math.sin(a), hy - head * .55 * math.cos(a)), (hx - head * .55 * math.sin(a), hy + head * .55 * math.cos(a))]
        return s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in p)}" fill="{c}"/>')
    def num(s, n, x, y, c=INK, r=22):
        s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')
        return s.text(x, y + r * .36, n, int(r * 1.15), "#FFFFFF", anchor="middle", bold=True)
    def circle(s, x, y, r, fill="none", stroke="none", sw=2): return s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def save(s, path): open(os.path.join(OUT, path), "w", encoding="utf-8").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}">' + "".join(s.o) + "</svg>")

s = S(1500, 1000)
rows = [("Thanh ghi (Register)", "dưới 1 ns · vài trăm byte", "đắt nhất", RAM, RAMT),
        ("Cache SRAM (L1–L3)", "khoảng 1–10 ns · KB đến chục MB", "rất đắt", RAM, RAMT),
        ("RAM (DRAM)", "khoảng 50–100 ns · GB", "khoảng 13–19 USD/GB", RAM, RAMT),
        ("SSD (NAND flash)", "khoảng 10–100 µs · TB", "khoảng 0,08–0,19 USD/GB", SSD, SSDT),
        ("HDD (đĩa cơ)", "khoảng 5–15 ms · chục TB", "khoảng 0,02–0,04 USD/GB", HDD, HDDT),
        ("Băng từ (Tape)", "giây đến phút · 40 TB/cuộn", "thường rẻ nhất khi lưu lâu dài", OTH, OTHT)]
top, bot = 20, 980; n = len(rows); rh = (bot - top) / n; cx = 292
s.arrow(18, 960, 18, 50, SUB, 5)
for i, (nm, lat, price, c, tint) in enumerate(rows):
    y0 = top + i * rh; y1 = y0 + rh - 8
    wt = 60 + i * 70; wb = 60 + (i + 1) * 70 - 6
    s.add(f'<polygon points="{cx-wt/2:.0f},{y0:.0f} {cx+wt/2:.0f},{y0:.0f} {cx+wb/2:.0f},{y1:.0f} {cx-wb/2:.0f},{y1:.0f}" fill="{c}"/>')
    s.text(cx, y0 + rh / 2 + 12, str(i + 1), 44, "#FFFFFF", anchor="middle", bold=True)
    s.rect(560, y0, 920, rh - 8, tint, c, 3, 16)
    s.text(584, y0 + 48, nm, 42, c, bold=True)
    s.text(584, y0 + 94, lat, 38, INK)
    s.text(584, y0 + 136, price, 38, INK, bold=True)
s.save("pyramid.svg")

# ---- A. Bo nho vs luu tru (ban lam viec / tu ho so / kho)
s = S(1600, 940)
s.rect(30, 330, 250, 280, BG, LINE, 3, 20); s.text(155, 440, "CPU", 54, INK, anchor="middle", bold=True); s.text(155, 490, "người làm việc", 34, SUB, anchor="middle")
cols = [("RAM", "mặt bàn làm việc", "nhanh, nhỏ, mất điện là trống", RAM, RAMT, 80, "bộ nhớ (volatile)"),
        ("SSD", "tủ hồ sơ", "nhanh vừa, giữ dữ liệu khi tắt máy", SSD, SSDT, 350, "lưu trữ (non-volatile)"),
        ("HDD · Băng từ", "kho lưu trữ", "chậm, rất rẻ, chứa nhiều nhất", HDD, HDDT, 620, "lưu trữ (non-volatile)")]
for i, (nm, ana, d, c, t, dy, tag) in enumerate(cols):
    y = 70 + i * 290
    s.rect(560, y, 1010, 250, t, c, 4, 24)
    s.text(590, y + 62, nm, 50, c, bold=True); s.text(590, y + 112, "như " + ana, 38, INK, bold=True)
    s.text(590, y + 158, d, 34, INK); s.rect(590, y + 184, 440 if i < 2 else 440, 48, c, "none", 0, 24)
    s.text(610, y + 219, tag, 32, "#FFFFFF", bold=True)
    s.arrow(280, 470, 556, y + 125, c, 5)
s.save("bo-nho-vs-luu-tru.svg")

# ---- B. Ban do cac thanh phan trong may
s = S(1600, 940)
s.rect(20, 20, 1560, 900, "#EAF2EC", "#9BB5A3", 4, 30)
s.text(50, 76, "Mainboard (bo mạch chủ)", 36, SUB, bold=True)
s.rect(120, 130, 270, 270, "#FFFFFF", INK, 4, 14); s.rect(150, 160, 210, 210, "#C9CDD6", INK, 3, 10)
s.text(255, 255, "CPU", 52, INK, anchor="middle", bold=True); s.text(255, 310, "thanh ghi +\ncache SRAM", 30, INK, anchor="middle")
s.num(1, 120, 130, RAM, 26)
for k in range(4): s.rect(520 + k * 70, 120, 48, 360, RAMT, RAM, 4, 8)
s.text(660, 540, "RAM (DIMM)", 38, RAM, anchor="middle", bold=True); s.num(2, 520, 120, RAM, 26)
s.rect(120, 470, 380, 70, SSDT, SSD, 4, 10); s.text(145, 518, "M.2 NVMe SSD", 36, SSD, bold=True); s.num(3, 120, 470, SSD, 26)
s.rect(120, 590, 420, 56, HDDT, HDD, 3, 10); s.text(145, 630, "cổng SATA", 34, HDD, bold=True)
s.rect(120, 700, 420, 190, "#FFFFFF", HDD, 4, 10); s.text(330, 790, "HDD 3.5\"", 40, HDD, anchor="middle", bold=True); s.text(330, 840, "(nối bằng cáp SATA)", 30, SUB, anchor="middle"); s.num(4, 120, 700, HDD, 26)
s.rect(800, 590, 740, 300, "#FFFFFF", HBM, 5, 20); s.text(830, 650, "Card đồ họa / GPU AI", 38, INK, bold=True); s.num(5, 800, 590, HBM, 26)
s.rect(840, 690, 260, 170, "#C9CDD6", INK, 3, 10); s.text(970, 790, "GPU", 50, INK, anchor="middle", bold=True)
for k in range(2): s.rect(1130, 690 + k * 90, 170, 80, HBMT, HBM, 4, 10)
s.text(1215, 740, "HBM", 34, HBM, anchor="middle", bold=True); s.text(1215, 830, "HBM", 34, HBM, anchor="middle", bold=True)
s.text(1330, 760, "hoặc\nGDDR", 32, HBM, bold=True)
s.arrow(255, 402, 255, 468, SSD, 5); s.arrow(390, 260, 518, 260, RAM, 5)
s.rect(800, 130, 740, 400, "#FFFFFF", LINE, 3, 20)
leg = [(RAM, "RAM, cache: bộ nhớ (mất khi tắt)"), (SSD, "SSD: lưu trữ flash (giữ dữ liệu)"), (HDD, "HDD: lưu trữ đĩa cơ (giữ dữ liệu)"), (HBM, "HBM/GDDR: bộ nhớ của GPU")]
s.text(830, 186, "Chú giải màu", 36, INK, bold=True)
for k, (c, t) in enumerate(leg): s.rect(830, 220 + k * 70, 44, 44, c, "none", 0, 8); s.text(895, 256 + k * 70, t, 32, INK)
s.save("ban-do-trong-may.svg")

# ---- C. Cell NAND: so bit tren cell
s = S(1600, 940)
names = [("SLC", 1, SSD), ("MLC", 2, SSD), ("TLC", 3, SSD), ("QLC", 4, SSD), ("PLC", 5, OTH)]
s.text(30, 62, "Mỗi cell lưu n bit = phải phân biệt 2ⁿ mức điện tích", 40, INK, bold=True)
for i, (nm, b, c) in enumerate(names):
    y = 120 + i * 160; lv = 2 ** b
    s.text(30, y + 68, nm, 56, c, bold=True); s.text(30, y + 112, f"{b} bit/cell", 34, SUB)
    s.text(1570, y + 112, f"{lv} mức", 40, INK, anchor="end", bold=True)
    x0, wtot = 330, 900; gap = 6; bw = (wtot - gap * (lv - 1)) / lv
    for k in range(lv):
        sh = 0.35 + 0.65 * k / max(1, lv - 1)
        h = 40 + 70 * sh
        s.rect(x0 + k * (bw + gap), y + 120 - h + 10, bw, h, c, "none", 0, 4 if lv > 8 else 8)
    s.line(x0, y + 134, x0 + wtot, y + 134, INK, 3)
s.arrow(330, 905, 1230, 905, INK, 4); s.text(780, 936, "điện tích trong cell (điện áp ngưỡng) tăng dần", 28, SUB, anchor="middle") if False else s.text(780, 930, "mức điện tích tăng dần", 30, SUB, anchor="middle")
s.save("cell-slc-plc.svg")

# ---- D. 3D NAND
s = S(1600, 940)
s.text(400, 70, "NAND phẳng (planar)", 44, INK, anchor="middle", bold=True); s.text(1130, 70, "3D NAND xếp tầng", 44, SSD, anchor="middle", bold=True)
for k in range(8): s.rect(60 + k * 85, 520, 70, 60, SSDT, SSD, 3, 8)
s.rect(40, 590, 700, 50, "#C9CDD6", INK, 3, 6); s.text(400, 700, "cell trải trên một lớp:\nmuốn nhiều hơn phải thu nhỏ cell", 36, INK, anchor="middle")
s.text(400, 800, "(cell càng nhỏ càng khó giữ điện tích)", 30, SUB, anchor="middle")
for k in range(8):
    y = 130 + k * 66
    s.rect(800, y, 660, 46, SSDT, SSD, 3, 6)
    for j in range(5): s.rect(830 + j * 125, y + 6, 40, 34, SSD, "none", 0, 4)
s.rect(800, 130 + 8 * 66, 660, 50, "#C9CDD6", INK, 3, 6)
s.text(1130, 800, "xếp các lớp cell lên cao, đục lỗ\nthẳng đứng xuyên qua tất cả các lớp", 36, INK, anchor="middle")
s.text(1130, 900, "SK hynix: 321 tầng (QLC, 2026)", 36, SSD, anchor="middle", bold=True)
s.arrow(1500, 650, 1500, 140, SSD, 6); s.text(1470, 400, "", 20)
s.save("nand-3d.svg")

# ---- E. SATA vs NVMe
s = S(1600, 940)
def chain(y, c, tint, title, items, speed):
    s.text(30, y, title, 46, c, bold=True)
    x = 30; w = (1540 - 30 * (len(items) - 1)) / len(items)
    for k, t in enumerate(items):
        xx = 30 + k * (w + 30)
        s.rect(xx, y + 30, w, 150, tint, c, 4, 20); s.text(xx + w / 2, y + 120, t, 34, INK, anchor="middle", bold=True, lh=1.15)
        if k: s.arrow(xx - 30, y + 105, xx, y + 105, c, 5, 12)
    s.text(30, y + 235, speed, 40, c, bold=True)
chain(70, HDD, HDDT, "SATA (SSD 2.5\"): qua nhiều chặng", ["CPU", "Chipset", "Bộ điều khiển\nSATA/AHCI", "Cáp SATA", "SSD"], "tối đa 6 Gb/s (khoảng 550–600 MB/s thực tế)")
chain(520, SSD, SSDT, "NVMe (M.2): đi thẳng từ CPU", ["CPU", "4 làn PCIe", "SSD NVMe"], "PCIe 4.0 x4: khoảng 8 GB/s · PCIe 5.0 x4: khoảng 16 GB/s")
s.save("sata-vs-nvme.svg")

# ---- F. CMR vs SMR
s = S(1600, 940)
def tracks(y, c, tint, shingled):
    for k in range(6):
        if shingled: s.rect(40 + k * 90, y, 330, 70, tint, c, 3, 8)
        else: s.rect(40 + k * 250, y, 220, 70, tint, c, 3, 8)
    return
s.text(40, 60, "CMR: mỗi track có khoảng cách riêng", 42, HDD, bold=True)
for k in range(5): s.rect(40, 100 + k * 80, 1000, 56, HDDT, HDD, 3, 8)
s.text(1070, 190, "ghi lại một track không\nảnh hưởng track bên cạnh", 34, INK)
s.text(40, 560, "SMR: các track xếp chồng như ngói", 42, HDD, bold=True)
for k in range(5): s.rect(40 + k * 18, 600 + k * 56, 1000 - k * 18, 74, HDDT, HDD, 3, 8)
s.text(1070, 700, "ghi lại một track phải ghi lại\ncả nhóm track chồng lên nó", 34, INK)
s.text(1070, 830, "→ ghi ngẫu nhiên chậm hơn,\nđổi lại chứa được nhiều hơn", 34, HDD, bold=True)
s.save("cmr-smr.svg")
# ---- G. SRAM vs DRAM cell
s = S(1600, 940)
s.text(400, 70, "SRAM: 6 transistor / bit", 44, RAM, anchor="middle", bold=True); s.text(1200, 70, "DRAM: 1 transistor + 1 tụ / bit", 44, RAM, anchor="middle", bold=True)
for k, (x, y) in enumerate([(220, 240), (580, 240), (220, 480), (580, 480), (400, 360), (400, 600)]):
    s.rect(x - 70, y - 50, 140, 100, RAMT, RAM, 4, 14); s.text(x, y + 14, "T" + str(k + 1), 40, RAM, anchor="middle", bold=True)
s.text(400, 790, "giữ bit bằng mạch chốt,\nkhông cần làm tươi (refresh)", 36, INK, anchor="middle")
s.text(400, 890, "nhanh · tốn diện tích · đắt → dùng làm cache", 34, RAM, anchor="middle", bold=True)
s.rect(1000, 250, 200, 130, RAMT, RAM, 4, 14); s.text(1100, 330, "Transistor", 34, RAM, anchor="middle", bold=True)
s.rect(1320, 250, 120, 330, "#FFFFFF", RAM, 5, 14); s.rect(1325, 420, 110, 155, RAM, "none", 0, 10); s.text(1380, 330, "Tụ", 38, RAM, anchor="middle", bold=True)
s.line(1200, 315, 1320, 315, RAM, 5); s.text(1250, 300, "", 20)
s.text(1220, 640, "điện tích trong tụ rò dần\n→ phải làm tươi (refresh) liên tục", 36, INK, anchor="middle")
s.text(1220, 780, "rất gọn · rẻ hơn / bit → dùng làm RAM", 34, RAM, anchor="middle", bold=True)
s.text(1220, 890, "(cắm điện mới giữ được dữ liệu)", 32, SUB, anchor="middle")
s.save("sram-dram.svg")
# ---- H. HBM stack cutaway with numbered parts (side view)
s = S(1600, 940)
s.rect(30, 800, 1540, 60, "#C9CDD6", INK, 3, 8); s.text(800, 842, "tấm nền gói chip (package substrate)", 32, INK, anchor="middle")
s.rect(30, 730, 1540, 70, OTHT, OTH, 3, 8); s.text(700, 777, "interposer (tấm silicon nối)", 34, OTH, anchor="middle", bold=True); s.num(5, 1520, 765, OTH, 24)
s.rect(1100, 360, 460, 370, "#C9CDD6", INK, 4, 14); s.text(1330, 560, "GPU / bộ xử lý AI", 36, INK, anchor="middle", bold=True)
s.rect(60, 630, 470, 100, HBMT, HBM, 4, 8); s.text(295, 692, "die đáy (logic)", 34, HBM, anchor="middle", bold=True)
for k in range(8): s.rect(60, 576 - k * 46, 470, 40, HBMT, HBM, 3, 6)
for x in (120, 200, 295, 390, 470): s.line(x, 230, x, 630, HBM, 4)
for k in range(8):
    for x in (120, 200, 295, 390, 470): s.circle(x, 596 - k * 46, 6, HBM)
def lab(n, y, text, ty, c=INK):
    s.num(n, 600, ty, c, 24); s.text(640, ty + 11, text, 34, c, bold=True); s.line(536, y, 576, ty, c, 3)
lab(1, 300, "die DRAM xếp chồng (4–16 lớp)", 190, HBM)
lab(2, 400, "TSV: đục lỗ xuyên die", 330)
lab(3, 625, "microbump (chấm nối)", 480)
lab(4, 680, "die đáy: giao tiếp với GPU", 620, HBM)
s.arrow(530, 680, 1100, 680, HBM, 6); s.text(600, 705, "", 20)
s.text(30, 910, "Bus rộng qua interposer: HBM3/3E 1024 bit · HBM4 2048 bit", 36, HBM, bold=True)
s.save("hbm-stack.svg")
# ---- J. CXL
s = S(1600, 940)
s.rect(40, 330, 280, 280, "#C9CDD6", INK, 4, 18); s.text(180, 480, "CPU", 54, INK, anchor="middle", bold=True)
s.rect(520, 120, 520, 220, RAMT, RAM, 4, 18); s.text(780, 205, "RAM DDR5 gắn trực tiếp", 36, RAM, anchor="middle", bold=True); s.text(780, 260, "nhanh nhất, số khe có hạn", 32, INK, anchor="middle"); s.arrow(320, 420, 520, 270, RAM, 6)
s.rect(520, 600, 520, 220, OTHT, OTH, 4, 18); s.text(780, 685, "Thẻ nhớ CXL (qua PCIe)", 36, OTH, anchor="middle", bold=True); s.text(780, 740, "chậm hơn chút, thêm dung lượng", 32, INK, anchor="middle"); s.arrow(320, 520, 520, 670, OTH, 6)
s.rect(1240, 600, 320, 220, SSDT, SSD, 4, 18); s.text(1400, 700, "SSD", 50, SSD, anchor="middle", bold=True); s.text(1400, 760, "chậm hơn nhiều", 32, INK, anchor="middle"); s.arrow(1040, 710, 1240, 710, SUB, 5)
s.text(40, 900, "CXL xếp giữa RAM và SSD: thêm bộ nhớ lớn mà không cần thêm khe DIMM", 34, OTH, bold=True)
s.save("cxl.svg")
# ---- K. PCIe/SATA link bandwidth bars
s = S(1600, 940)
s.text(30, 60, "Băng thông tối đa của đường truyền (một chiều, GB/s)", 40, INK, bold=True)
bars = [("SATA III", 0.6, HDD, ""), ("PCIe 3.0 x4", 4, SSD, ""), ("PCIe 4.0 x4", 8, SSD, ""), ("PCIe 5.0 x4", 16, SSD, "ổ Gen5 (Micron 6600 ION): 13,7 GB/s (đọc)"), ("PCIe 6.0 x4", 32, OTH, "ổ Gen6 doanh nghiệp: 28 GB/s (đọc)")]
x0, wmax = 400, 1100
for i, (nm, v, c, note) in enumerate(bars):
    y = 90 + i * 150; w = max(10, v / 32 * wmax)
    s.text(30, y + 70, nm, 38, c, bold=True); s.rect(x0, y + 20, w, 80, c, "none", 0, 8)
    s.text(x0 + w + 16 if v < 20 else x0 + w - 16, y + 76, f"{str(v).replace('.', ',')}", 40, INK if v < 20 else "#FFFFFF", anchor="start" if v < 20 else "end", bold=True)
    if note: s.text(x0, y + 135, note, 30, c, bold=True)
s.text(30, 932, "Tính từ tốc độ truyền bit, chưa trừ chi phí giao thức; ổ thực tế thấp hơn.", 28, SUB)
s.save("pcie-bars.svg")

RENDER = """const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [,, i,o,w,h]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:2});
await p.setContent('<body style="margin:0;background:#fff">'+fs.readFileSync(i,'utf8')+'</body>');await p.screenshot({path:o,clip:{x:0,y:0,width:+w,height:+h}});await b.close();})();"""
def size(path):
    import re
    m = re.search(r'width="(\d+)" height="(\d+)"', open(path, encoding="utf-8").read(400))
    return m.group(1), m.group(2)


if __name__ == "__main__":
    js = os.path.join(OUT, "_render.js"); open(js, "w").write(RENDER)
    for name in sorted(f for f in os.listdir(OUT) if f.endswith(".svg")):
        subprocess.run(["node", js, os.path.join(OUT, name), os.path.join(OUT, name[:-4] + ".png"), *size(os.path.join(OUT, name))], check=False)
    os.remove(js)

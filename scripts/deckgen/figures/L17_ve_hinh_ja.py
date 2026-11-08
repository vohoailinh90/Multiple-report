import math, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf")
plt.rcParams["font.family"] = "IPAPGothic"
plt.rcParams["axes.unicode_minus"] = False
OUT = sys.argv[1]
C = dict(urea="#E91EC8", biuret="#1B8A1B", ammelide="#E60000", cyan="#7B1FA2", total="#1A237E", gas="#B8B8B8")
T = [133, 190, 225, 250, 275, 325, 350, 400, 450]
D = {  # urea, biuret, ammelide, cyanuric, total (user table, +-2 %)
    133: (100, 0, 0, 0, 100), 190: (46, 28, 0.5, 2.5, 77), 225: (4.5, 14, 3.5, 22, 43), 250: (0.5, 1, 4, 23.5, 30),
    275: (0, 0, 5.5, 24, 30), 325: (0, 0, 5.5, 15, 20), 350: (0, 0, 5.5, 2, 8), 400: (0, 0, 1, 0, 2.5), 450: (0, 0, 0, 0, 1)}
NAMES = ["尿素", "ビウレット", "アンメリド", "シアヌル酸", "固体の合計\n(total recovery)"]
KEYS = ["urea", "biuret", "ammelide", "cyan", "total"]

def f(v, approx=True):
    if v == 0: return "0"
    s = f"{v:g}"
    return s if (v == 100 or not approx) else "~" + s

def zone(name, temps, size):
    fig = plt.figure(figsize=size, dpi=200); fig.patch.set_facecolor("white")
    n = len(temps)
    ax = fig.add_axes([0.02, 0.52, 0.96, 0.46]); ax.set_xlim(0, 6.4); ax.set_ylim(0, n + 1.25); ax.axis("off")
    cw = [1.1] + [1.0, 1.0, 1.05, 1.05, 1.3]
    xs = [0]; [xs.append(xs[-1] + w) for w in cw]
    top = n + 1.25
    for j, k in enumerate(KEYS):
        ax.add_patch(Rectangle((xs[j + 1] + 0.03, top - 1.2), cw[j + 1] - 0.06, 1.2, color=C[k]))
        ax.text(xs[j + 1] + cw[j + 1] / 2, top - 0.6, NAMES[j], ha="center", va="center", color="white", fontsize=11.5, fontweight="bold", linespacing=1.1)
    ax.text(xs[0] + 0.05, top - 0.6, "温度\n(°C)", ha="left", va="center", fontsize=11.5, fontweight="bold", color="#14161C", linespacing=1.1)
    for r, t in enumerate(temps):
        y = top - 1.2 - (r + 1)
        if r % 2 == 0: ax.add_patch(Rectangle((0, y), 6.4, 1, color="#F3EEE3"))
        ax.text(xs[0] + 0.05, y + 0.5, f"{t}", ha="left", va="center", fontsize=17, fontweight="bold", color="#14161C")
        for j, k in enumerate(KEYS):
            v = D[t][j]
            ax.text(xs[j + 1] + cw[j + 1] / 2, y + 0.5, f(v, t != 133), ha="center", va="center", fontsize=17, fontweight="bold" if v else "normal", color=C[k] if v else "#8A8A8A")
    ax.text(6.4, 0.0, "質量%、グラフから読み取り、誤差±2%", ha="right", va="bottom", fontsize=9, color="#6B6A66")
    bx = fig.add_axes([0.13, 0.11, 0.85, 0.30]); bx.set_xlim(0, 100); bx.set_ylim(-0.6, n - 0.4); bx.invert_yaxis()
    for r, t in enumerate(temps):
        left = 0
        parts = [(D[t][i], KEYS[i]) for i in range(4)]
        gas = max(0, 100 - sum(p[0] for p in parts))
        for v, k in parts + [(gas, "gas")]:
            if v <= 0: continue
            bx.barh(r, v, left=left, color=C[k], height=0.7, hatch="//" if k == "gas" else None, edgecolor="white" if k == "gas" else C[k], linewidth=0)
            if v >= 9: bx.text(left + v / 2, r, f"{f(v)}", ha="center", va="center", color="white" if k != "gas" else "#333", fontsize=10, fontweight="bold")
            left += v
    bx.set_yticks(range(n)); bx.set_yticklabels([f"{t}°C" for t in temps], fontsize=11, fontweight="bold")
    bx.set_xticks([0, 25, 50, 75, 100]); bx.set_xticklabels(["0", "25", "50", "75", "100%"], fontsize=10)
    for s in ("top", "right"): bx.spines[s].set_visible(False)
    fig.text(0.13, 0.015, "棒＝当初の尿素を100%に換算。灰色の斜線＝気体になった分（NH3、HNCO、CO2など）。100%から固体の合計を引いて推定", fontsize=8.5, color="#6B6A66", ha="left")
    fig.savefig(f"{OUT}/{name}.png", facecolor="white"); plt.close(fig)

def chart(name, size):
    fig = plt.figure(figsize=size, dpi=200); ax = fig.add_axes([0.08, 0.12, 0.89, 0.80])
    zones = [(133, 190, "#FFF4D6"), (190, 325, "#FBE0DC"), (325, 400, "#FDEBD3"), (400, 450, "#E1F2E6")]
    for a, b, c in zones: ax.axvspan(a, b, color=c, lw=0)
    st = dict(lw=2.2, ms=8)
    ser = [("total", "total recovery", "D", 4, C["total"]), ("urea", "urea", "s", 0, C["urea"]), ("biuret", "biuret", "^", 1, C["biuret"]),
           ("ammelide", "ammelide", "D", 2, C["ammelide"]), ("cyan", "cyanuric acid", "o", 3, C["cyan"])]
    for key, lab, m, i, col in ser:
        fill = "white" if key in ("ammelide", "cyan") else col
        ax.plot(T, [D[t][i] for t in T], color=col, marker=m, mfc=fill, mec=col if fill == "white" else col, mew=1.6, label=lab, **st)
    ax.set_xlim(120, 460); ax.set_ylim(-3, 106); ax.set_xticks([133, 190, 225, 250, 275, 325, 350, 400, 450])
    ax.set_xlabel("温度 (°C)", fontsize=12); ax.set_ylabel("質量 (%)", fontsize=12); ax.tick_params(labelsize=10.5)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.annotate("ビウレットは190°Cで\n約28%のピーク", (190, 28), (212, 62), fontsize=10.5, color=C["biuret"], fontweight="bold", arrowprops=dict(arrowstyle="->", color=C["biuret"]))
    ax.annotate("シアヌル酸\n約22〜24%", (262, 24), (292, 46), fontsize=10.5, color=C["cyan"], fontweight="bold", arrowprops=dict(arrowstyle="->", color=C["cyan"]))
    ax.annotate("アンメリド約5.5%\n約350°Cまで安定", (325, 5.5), (352, 30), fontsize=10.5, color=C["ammelide"], fontweight="bold", arrowprops=dict(arrowstyle="->", color=C["ammelide"]))
    ax.text(140, 91, "尿素が溶ける\n100%", fontsize=10.5, color=C["urea"], fontweight="bold")
    ax.text(404, 40, "堆積物は\nほぼ消える", fontsize=10.5, color="#2E7D32", fontweight="bold")
    for xv in (160, 170): ax.axvline(xv, color="#8A8A8A", lw=1, ls=":")
    ax.text(165, -1.5, "160・170°C：\n測定点なし", fontsize=8, color="#555", ha="center", va="bottom")
    ax.legend(loc="upper right", fontsize=9, frameon=True, framealpha=0.95, bbox_to_anchor=(0.99, 0.99))
    fig.savefig(f"{OUT}/{name}.png", facecolor="white"); plt.close(fig)

def heat(name, size):
    fig = plt.figure(figsize=size, dpi=200)
    sx = fig.add_axes([0.07, 0.62, 0.90, 0.30]); sx.set_xlim(120, 460); sx.set_ylim(0, 1); sx.axis("off")
    bands = [(133, 190, "#F2C14E", "注意", "尿素・ビウレット\nが多い"), (190, 325, "#D64545", "危険", "シアヌル酸 約22〜24%\nアンメリド 約5.5%"),
             (325, 400, "#F29E4C", "減少", "シアヌル酸は約0\nアンメリドは残る"), (400, 450, "#3DA35D", "安全", "約2.5%以下")]
    for a, b, c, lab, sub in bands:
        sx.add_patch(Rectangle((a, 0.02), b - a, 0.96, color=c, lw=0))
        sx.text((a + b) / 2, 0.66, lab, ha="center", va="center", color="white", fontsize=12.5 if b - a > 60 else 9.5, fontweight="bold")
        sx.text((a + b) / 2, 0.30, sub, ha="center", va="center", color="white", fontsize=9.5 if b - a > 60 else 7.5, fontweight="bold", linespacing=1.1)
    ax = fig.add_axes([0.07, 0.14, 0.90, 0.40])
    for a, b, c, *_ in bands: ax.axvspan(a, b, color=c, alpha=0.13, lw=0)
    ax.fill_between(T, [D[t][4] for t in T], color=C["total"], alpha=0.18)
    ax.plot(T, [D[t][4] for t in T], color=C["total"], marker="D", lw=2.2, ms=6, label="固体の合計 (total recovery)")
    ax.plot(T, [D[t][3] for t in T], color=C["cyan"], marker="o", mfc="white", lw=2.2, ms=6, label="Cyanuric acid")
    ax.plot(T, [D[t][2] for t in T], color=C["ammelide"], marker="D", mfc="white", lw=2.2, ms=6, label="Ammelide")
    ax.set_xlim(120, 460); ax.set_ylim(0, 105); ax.set_xticks(T); ax.tick_params(labelsize=10)
    ax.set_xlabel("温度 (°C)", fontsize=11); ax.set_ylabel("質量 (%)", fontsize=11)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(loc="upper right", fontsize=9.5, frameon=False)
    fig.text(0.07, 0.015, "色の帯は本資料がS1のグラフから推論したもので、メーカーの適合しきい値ではない", fontsize=8.5, color="#6B6A66")
    fig.savefig(f"{OUT}/{name}.png", facecolor="white"); plt.close(fig)

def mol(name, size):
    fig = plt.figure(figsize=size, dpi=200); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 9); ax.set_ylim(0, 6); ax.axis("off")
    def atom(x, y, t, col="#14161C", fs=13): ax.text(x, y, t, ha="center", va="center", fontsize=fs, fontweight="bold", color=col, bbox=dict(fc="white", ec="none", pad=0.6))
    def bond(p, q, col, dbl=False):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=2)
        if dbl:
            dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy); nx, ny = -dy / L * 0.07, dx / L * 0.07
            ax.plot([p[0] + nx, q[0] + nx], [p[1] + ny, q[1] + ny], color=col, lw=2)
    def ring(cx, cy, r, kinds, col):
        pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in (90, 30, -30, -90, -150, 150)]
        for i in range(6): bond(pts[i], pts[(i + 1) % 6], col)
        for p, k in zip(pts, kinds):
            if k[0] == "N": atom(*p, "N", col, 11)
        outs = {}
        for i, (p, k) in enumerate(zip(pts, kinds)):
            if k in ("O", "OH", "NH2"):
                a = math.radians([90, 30, -30, -90, -150, 150][i]); q = (p[0] + 0.5 * math.cos(a), p[1] + 0.5 * math.sin(a))
                bond(p, q, col, k == "O"); atom(*q, {"O": "O", "OH": "OH", "NH2": "NH₂"}[k], col, 11)
    rows = [("Urea", "CO(NH₂)₂", "urea", "Tốt: nguồn NH₃", 5.25), ("Biuret", "C₂H₅N₃O₂", "biuret", "Trung gian", 3.95),
            ("Ammelide", "C₃H₄N₄O₂", "ammelide", "Xấu: cặn bền", 2.65), ("Cyanuric acid", "C₃H₃N₃O₃", "cyan", "Xấu: cặn chính", 1.0)]
    for nm, fm, key, role, y in rows:
        col = C[key]
        ax.add_patch(FancyBboxPatch((0.15, y - 0.55), 8.7, 1.1 if key != "cyan" else 1.3, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#FBF8F2", ec=col, lw=2))
        ax.text(0.4, y + 0.18, nm, fontsize=15, fontweight="bold", color=col, va="center")
        ax.text(0.4, y - 0.22, fm, fontsize=10.5, color="#555", va="center")
        ax.text(8.7, y, role, fontsize=11.5, fontweight="bold", color="#14161C", va="center", ha="right")
    # urea
    cx, cy = 5.2, 5.25; bond((cx, cy), (cx, cy + 0.4), C["urea"], True); atom(cx, cy + 0.5, "O", C["urea"], 11)
    for s in (-1, 1): bond((cx, cy), (cx + s * 0.4, cy - 0.28), C["urea"]); atom(cx + s * 0.55, cy - 0.34, "NH₂", C["urea"], 11)
    # biuret
    g = C["biuret"]; y = 3.9
    pc1, pn, pc2 = (4.55, y), (5.25, y + 0.3), (5.95, y)
    bond(pc1, pn, g); bond(pn, pc2, g); atom(*pn, "NH", g, 11)
    for pc, s in ((pc1, -1), (pc2, 1)):
        bond(pc, (pc[0] + s * 0.05, pc[1] + 0.4), g, True); atom(pc[0] + s * 0.05, pc[1] + 0.5, "O", g, 11)
        bond(pc, (pc[0] + s * 0.05, pc[1] - 0.35), g); atom(pc[0] + s * 0.05, pc[1] - 0.46, "NH₂", g, 11)
    ring(5.25, 2.65, 0.42, ["O", "N", "O", "N", "NH2", "N"], C["ammelide"])
    ring(5.25, 1.0, 0.42, ["OH", "N", "OH", "N", "OH", "N"], C["cyan"])
    fig.text(0.5, 0.012, "Cấu trúc vẽ đơn giản, không theo tỉ lệ", fontsize=8.5, color="#6B6A66", ha="center")
    fig.savefig(f"{OUT}/{name}.png", facecolor="white"); plt.close(fig)

A, B = (9.0, 6.0), (10.2, 6.0)
chart("ja-bieu-do", A)
zone("ja-vung-133", [133], B); zone("ja-vung-190", [190], A); zone("ja-vung-225-250", [225, 250], B)
zone("ja-vung-275-325", [275, 325], A); zone("ja-vung-350-450", [350, 400, 450], B)
heat("ja-ban-do-rui-ro", B)

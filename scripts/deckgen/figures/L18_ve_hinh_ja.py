"""Japanese figures of L18 (docs/deck-style.md): redrawn from the Vietnamese ones in lessons/L18/images, same colours and layout.
usage: python3 L18_ve_hinh_ja.py <output dir>
ja-cau-truc-bon-chat.png and ja-bieu-do-ve-lai.png are copies of the L17 Japanese figures (same drawing)."""
import sys, shutil
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
from matplotlib.text import Text
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Ellipse, Polygon
from matplotlib import font_manager as _fm
_fm.fontManager.addfont("/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf")
plt.rcParams["font.family"] = "IPAPGothic"
plt.rcParams["axes.unicode_minus"] = False
OUT = Path(sys.argv[1])
ROOT = Path(__file__).resolve().parents[3]
INK, SUB, CARD, EDGE = "#14161C", "#6B6A66", "#FBF8F2", "#DDD5C1"
URE, BIU, AMM, CYA, GAS, WAT, ICE = "#E91EC8", "#1B8A1B", "#E60000", "#7B1FA2", "#8C909A", "#1F6FEB", "#9AD7F6"


def canvas(w, h):
    """A pixel-space axes: (0,0) top left, w x h units (the figure is 200 dpi)."""
    k = 1.02 if w == 2000 else 1.0
    fig = plt.figure(figsize=(w / 200 * k, h / 200 * k), dpi=200)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc, ec="none", lw=0, r=14):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))


def txt(ax, x, y, s, size, color=INK, bold=False, ha="left", va="center", **kw):
    ax.text(x, y, s, fontsize=size * 0.66, color=color, fontweight="bold" if bold else "normal", ha=ha, va=va, linespacing=1.25, **kw)


def arrow(ax, p, q, color=INK, lw=3.2):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0, mutation_scale=22))


def save(fig, name):
    for t in fig.findobj(Text):  # IPAPGothic has no bold face: thicken bold text with a thin stroke of its own colour
        if t.get_text() and t.get_fontweight() in ("bold", 700):
            t.set_fontweight("normal"); t.set_path_effects([pe.withStroke(linewidth=1.0, foreground=t.get_color())])
    fig.savefig(OUT / f"{name}.png", facecolor="white", dpi=200); plt.close(fig)


def ban_do_nhiet_do():
    W, H = 2000, 1176
    fig, ax = canvas(W, H)
    txt(ax, 40, 40, "AdBlueの温度マップ", 26, INK, True)
    txt(ax, 1960, 40, "上が高温、下が低温", 15, SUB, ha="right")
    rows = [  # letter, colour, letter colour, temp, sub, chips
        ("I", GAS, "white", "450°C超", "尿素の堆積物はほぼ消える。NH3が酸化され得る", [("気体", GAS), ("耐熱性の痕跡", AMM)]),
        ("H", AMM, "white", "350〜450°C", "堆積物がゆっくり分解", [("アンメリド", AMM), ("アンメリン", AMM)]),
        ("G", CYA, "white", "250〜350°C", "安定な堆積物、シアヌル酸が昇華", [("シアヌル酸", CYA), ("アンメリド", AMM)]),
        ("F", BIU, "white", "190〜250°C", "強い変化：ビウレットが堆積物に", [("ビウレット", BIU), ("シアヌル酸", CYA), ("アンメリド", AMM)]),
        ("E", URE, "white", "130〜190°C", "尿素が溶けて分解", [("尿素", URE), ("NH3・HNCO", GAS), ("ビウレット", BIU)]),
        ("D", "#9B6FD6", "white", "70〜130°C", "水が蒸発、尿素が結晶化", [("水蒸気", WAT), ("尿素", URE)]),
        ("C", "#4F8DEB", "white", "30〜70°C", "液体、ゆっくり加水分解してNH3発生", [("水", WAT), ("尿素", URE), ("NH3", GAS)]),
        ("B", WAT, "white", "-5〜30°C", "安定した溶液、保管", [("水", WAT), ("尿素", URE)]),
        ("A", ICE, INK, "-5°C未満", "-11.5°Cから結晶化、約7%膨張", [("氷", ICE), ("尿素", URE)]),
    ]
    for i, (L, col, lc, temp, sub, chips) in enumerate(rows):
        y = 108 + i * 115.5
        rbox(ax, 40, y, 1920, 98, CARD, EDGE, 2.5, 12)
        rbox(ax, 40, y, 140, 98, col, r=12)
        txt(ax, 110, y + 49, L, 38, lc, True, ha="center")
        txt(ax, 210, y + 33, temp, 25, INK, True)
        txt(ax, 210, y + 73, sub, 15, SUB)
        cx = 1150
        for lab, c in chips:
            tw = 44 + len(lab) * 29
            rbox(ax, cx, y + 24, tw, 50, c, r=24)
            txt(ax, cx + tw / 2, y + 49, lab, 15, INK if c == ICE else "white", True, ha="center")
            cx += tw + 20
    save(fig, "ja-ban-do-nhiet-do")


def chuoi_phan_ung():
    W, H = 2000, 1176
    fig, ax = canvas(W, H)
    txt(ax, 40, 52, "尿素が熱で変わっていく反応の流れ", 26, INK, True)
    def box(x0, y0, x1, y1, col, text, size=21):
        rbox(ax, x0, y0, x1 - x0, y1 - y0, col, r=26); txt(ax, (x0 + x1) / 2, (y0 + y1) / 2, text, size, "white", True, ha="center")
    box(60, 295, 360, 445, URE, "尿素\nCO(NH2)2", 22)
    box(680, 118, 960, 235, GAS, "NH3", 24); box(680, 283, 960, 400, GAS, "HNCO", 24)
    box(1200, 118, 1800, 235, WAT, "HNCO + H2O → NH3 + CO2", 20)
    box(680, 565, 980, 705, BIU, "ビウレット", 24); box(1240, 565, 1600, 705, CYA, "シアヌル酸", 24)
    box(1680, 565, 1940, 705, AMM, "アンメリド", 22); box(680, 800, 980, 917, "#5E7D3B", "トリウレット", 22)
    box(1240, 824, 1540, 940, GAS, "3 HNCO（気体）", 21)
    arrow(ax, (362, 368), (672, 192)); arrow(ax, (362, 352), (672, 342)); arrow(ax, (203, 448), (672, 622))
    arrow(ax, (962, 340), (1194, 205), WAT); arrow(ax, (983, 635), (1232, 635)); arrow(ax, (1602, 635), (1672, 635))
    arrow(ax, (820, 708), (820, 792)); arrow(ax, (1400, 708), (1400, 815))
    txt(ax, 510, 460, "133°Cから", 15, SUB, ha="center")
    txt(ax, 400, 625, "2 尿素 → ビウレット + NH3\n（130〜190°C領域）", 15, SUB, ha="center")
    txt(ax, 1400, 352, "水があれば：望ましい経路", 15, WAT, ha="center")
    txt(ax, 1110, 572, "+ HNCO\n− NH3", 15, SUB, ha="center")
    txt(ax, 1610, 515, "+ HNCO\n（CO2も生成）", 15, SUB, ha="center")
    txt(ax, 870, 752, "+ 尿素", 15, SUB)
    txt(ax, 1440, 762, "昇華・分解\n約250〜300°Cから", 15, SUB)
    txt(ax, 60, 1058, "矢印は加熱実験で反応が始まる温度の目安。別の実験ではずれることがある（出典比較の項を参照）。", 13, SUB)
    txt(ax, 60, 1105, "出典：Tischer 2019 [S3]、Bernhard 2012 [S5]、Zhu 2023 [S8]。自作。", 13, SUB)
    save(fig, "ja-chuoi-phan-ung")


def thang_dong_bang():
    W, H = 1800, 1200
    fig, ax = canvas(W, H)
    txt(ax, 72, 48, "AdBlueが冷えて液体から固体になるまで", 25, INK, True)
    ax.add_patch(Rectangle((162, 180), 108, 512, color="#4F8FEB")); ax.add_patch(Rectangle((162, 692), 108, 208, color=ICE))
    ax.add_patch(Ellipse((216, 942), 144, 96, color=WAT))
    cards = [(204, 264, "25°C", "長期保管の上限 [S6]"), (420, 480, "-5°C", "結晶化を避けるため、これ以上に保つ [S6]"),
             (588, 648, "-11°C〜-11.5°C", "尿素の結晶化が始まる。Cefic -11.5、DieselNet -11 [S6][S13]"), (780, 840, "-11°C〜-15°C", "OCIの仕様書に記載の範囲 [S7]")]
    for y, ly, big, sub in cards:
        ax.plot([270, 362], [ly, ly], color=INK, lw=3)
        rbox(ax, 360, y, 1296, 120, CARD, EDGE, 2.5, 18)
        txt(ax, 397, y + 40, big, 24, INK, True); txt(ax, 397, y + 90, sub, 15, SUB)
    txt(ax, 72, 1050, "凍結：体積が約7%増える [S6]（同じ文書の物性表には「1.05」とも記載）。", 15, INK)
    txt(ax, 72, 1100, "自作。目盛りは縮尺どおりではない。", 13, SUB)
    save(fig, "ja-thang-dong-bang")


def han_dung():
    fig = plt.figure(figsize=(9, 6), dpi=200)
    ax = fig.add_axes([0.13, 0.17, 0.84, 0.66])
    cats = ["10°C以下", "25°C以下", "30°C以下", "35°C以下"]; cef = [36, 18, 12, 6]; oci = [36, 18, 12, None]
    for k, (c, o) in enumerate(zip(cef, oci)):
        ax.bar(k - 0.19, c, 0.36, color=WAT, label="Cefic 2011 [S6]" if k == 0 else None)
        ax.text(k - 0.19, c + 0.6, str(c), ha="center", fontsize=17, fontweight="bold", color=INK)
        if o:
            ax.bar(k + 0.19, o, 0.36, color="#9EC1F5", label="OCI 2024 [S7]" if k == 0 else None)
            ax.text(k + 0.19, o + 0.6, str(o), ha="center", fontsize=17, fontweight="bold", color=INK)
    ax.text(3.2, 1.2, "記載なし", ha="center", fontsize=12, color=SUB); ax.set_xlim(-0.55, 3.62)
    ax.set_xticks(range(4)); ax.set_xticklabels(cats, fontsize=15); ax.set_ylim(0, 42); ax.tick_params(axis="y", labelsize=12)
    ax.set_ylabel("最低使用期限（か月）", fontsize=13); ax.set_xlabel("製品の平均温度", fontsize=13)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(loc="upper right", fontsize=11, frameon=False)
    fig.text(0.13, 0.93, "AdBlueの使用期限は暑いと短くなる", fontsize=22, fontweight="bold", color=INK)
    save(fig, "ja-han-dung-theo-nhiet-do")


def giot_phun():
    W, H = 2000, 1176
    fig, ax = canvas(W, H)
    txt(ax, 40, 52, "配管の壁に当たるAdBlueの液滴：2つの状態（概念図）", 24, INK, True)
    for x0, title, sub in ((60, "壁がライデンフロスト温度未満", "液滴が付いて、液膜になり、堆積物"), (1060, "壁がライデンフロスト温度超", "液滴が蒸気の層の上で跳ね、液膜は少ない")):
        rbox(ax, x0, 165, 880, 870, CARD, EDGE, 2.5, 16)
        txt(ax, x0 + 440, 215, title, 20, INK, True, ha="center"); txt(ax, x0 + 440, 262, sub, 14, SUB, ha="center")
    for x, y in ((240, 488), (400, 535), (560, 582)):
        ax.add_patch(Ellipse((x, y), 56, 34, color=WAT)); arrow(ax, (x, y + 28), (x, 768), WAT, 2.6)
    ax.add_patch(Ellipse((460, 853), 520, 30, color="#4F8DEB")); txt(ax, 460, 790, "液膜", 19, WAT, True, ha="center")
    ax.add_patch(Polygon([(680, 868), (740, 842), (800, 824), (800, 868)], color=URE))
    txt(ax, 740, 690, "尿素、ビウレット、\nシアヌル酸の堆積物\n（液膜の縁）", 14, URE, ha="center")
    arrow(ax, (740, 745), (740, 805), URE, 2.2)
    rbox(ax, 120, 870, 760, 70, "#C97B63", r=0); txt(ax, 500, 905, "高温の配管の壁", 17, "white", ha="center")
    for x, y in ((1260, 458), (1500, 487), (1700, 511)):
        ax.add_patch(Ellipse((x, y), 56, 34, color=WAT))
    for x in (1260, 1500, 1700):
        ax.add_patch(Ellipse((x, 841), 52, 32, color=WAT)); ax.add_patch(Rectangle((x - 45, 858), 90, 10, color="#D8D2C4"))
        ax.annotate("", xy=(x + 55, 595), xytext=(x, 808), arrowprops=dict(arrowstyle="-|>", color=WAT, lw=2.4, connectionstyle="arc3,rad=-0.25", mutation_scale=18))
    txt(ax, 1500, 718, "蒸気の層", 18, SUB, ha="center")
    rbox(ax, 1120, 870, 760, 70, "#8B2A18", r=0); txt(ax, 1500, 905, "非常に高温の配管の壁", 17, "white", ha="center")
    txt(ax, 60, 1078, "考え方の出典：S12（堆積物はライデンフロスト温度まで形成）とS4（堆積物は液膜の縁）。", 13, SUB)
    txt(ax, 60, 1118, "尿素溶液のライデンフロスト温度：未確認。自作の図で、縮尺どおりではない。", 13, SUB)
    save(fig, "ja-giot-phun-bam-tuong")


def so_sanh_nguon():
    fig = plt.figure(figsize=(10.2, 6), dpi=200)
    ax = fig.add_axes([0.30, 0.21, 0.67, 0.65])
    rows = [("凍結・結晶化", -15, -11, None, ICE, -11.5), ("水の蒸発（TGA）", 20, 100, None, WAT, None), ("尿素の溶融", None, None, None, None, 132.5),
            ("尿素の分解（TGA）", 120, 230, None, URE, None), ("排気管内の加水分解（目安）", None, None, None, None, 180),
            ("噴射停止の閾値", 180, 250, None, "#B45309", None), ("ビウレットの溶融・固化", 192.5, 230, None, BIU, None),
            ("シアヌル酸の分解開始", 250, 260, None, CYA, None), ("シアヌル酸の昇華", 250, 360, None, CYA, 300),
            ("メラミンの分解", 250, 300, None, "#8E5FB5", None), ("アンメリドの分解", 360, 600, None, AMM, None), ("アンメリン・耐熱性の残渣", 360, 700, None, "#B02A2A", None)]
    for i, (lab, a, b, _, c, m) in enumerate(rows):
        if a is not None: ax.barh(i, b - a, left=a, color=c, height=0.55)
        if m is not None: ax.plot([m], [i], marker="D", color=INK, ms=11)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=12.5); ax.invert_yaxis()
    ax.set_xlim(-30, 720); ax.set_xticks(range(0, 701, 100)); ax.tick_params(axis="x", labelsize=12)
    ax.grid(axis="x", color="#E6E3D6"); ax.set_axisbelow(True); ax.set_xlabel("温度 (°C)", fontsize=13)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.text(0.03, 0.935, "出典ごとの温度の目印", fontsize=24, fontweight="bold", color=INK)
    fig.text(0.03, 0.075, "バー＝範囲、ひし形＝単一の目印。各バーの出典は資料の表にある。", fontsize=10.5, color=SUB)
    fig.text(0.03, 0.04, "アンメリドは約360°C（FVV）から600°Cでなくなる（Schaber）、アンメリンは700°Cまで（Schaber、FVV）。", fontsize=10.5, color=SUB)
    fig.text(0.03, 0.005, "記載の出典から作成した自作の図。", fontsize=10.5, color=SUB)
    save(fig, "ja-so-sanh-nguon")


def ban_do_he_thong():
    W, H = 2000, 1176
    fig, ax = canvas(W, H)
    txt(ax, 40, 52, "DNOxシステム：各部の温度（出典のある数値）", 25, INK, True)
    rows = [("タンク＋ヒーター", WAT, "-5〜25°Cに保つ。-11.5°Cから結晶化。局所的な過熱を避ける [S6]"),
            ("配管＋ポンプ", "#4F8DEB", "加熱が必要。停止時は溶液を排出するか凍結に耐える設計 [S13]"),
            ("噴射モジュール", URE, "排気管のすぐそば。Boschの閾値温度：公表されていない [S16]"),
            ("排気管＋ミキサー", BIU, "約180°Cから噴射、停止は200〜250°C、試験は200〜350°C [S4][S13]"),
            ("SCR", CYA, "硝酸アンモニウムは約100〜200°C未満、硫酸アンモニウムは約250°C未満 [S14]"),
            ("ASC", GAS, "NH3スリップは最大10 ppm [S14]。450°C超のNH3酸化：未確認")]
    for i, (lab, col, sub) in enumerate(rows):
        y = 153 + i * 135.3
        rbox(ax, 140, y, 1820, 112, CARD, EDGE, 2.5, 16)
        rbox(ax, 140, y, 440, 112, col, r=16); txt(ax, 360, y + 56, lab, 22, "white", True, ha="center")
        txt(ax, 620, y + 56, sub, 15.5, INK)
    arrow(ax, (70, 238), (70, 960), "#B45309", 5)
    ax.text(30, 600, "AdBlueはタンクの低温側から排気管の高温側へ進む", rotation=90, fontsize=10, fontweight="bold", color="#B45309", ha="center", va="center")
    txt(ax, 140, 1065, "数値のない部品は、読める出典が数値を公表していないため [S16]。", 14, SUB)
    txt(ax, 140, 1110, "[S4][S6][S13][S14][S16]から作成した自作の図で、特定メーカーの構成図ではない。", 14, SUB)
    save(fig, "ja-ban-do-he-thong")


def thanh_phan_cap():
    W, H = 1800, 1200
    fig, ax = canvas(W, H)
    txt(ax, 72, 48, "試験で採取した堆積物の温度別の組成", 25, INK, True)
    txt(ax, 72, 112, "定性的：出典はこれらの範囲の百分率を示していない", 15, SUB)
    cols = [(130, "200°C未満", "FVV [S4]", [(690, 243, URE, "尿素")]),
            (526, "200〜250°C", "FVV [S4]\nWeeks [S10]", [(274, 243, CYA, "シアヌル酸"), (278, 521, BIU, "ビウレット"), (132, 801, URE, "尿素（少量）")]),
            (922, "260°C以上", "FVV [S4]", [(98, 243, AMM, "アンメリド"), (586, 347, CYA, "シアヌル酸")]),
            (1318, "335〜425°C", "Weeks [S10]", [(690, 243, CYA, "シアヌル酸")])]
    for x, lab, src, blocks in cols:
        for h, y, c, t in blocks:
            ax.add_patch(Rectangle((x, y), 336, h, color=c)); txt(ax, x + 168, y + h / 2, t, 18, "white", True, ha="center")
        txt(ax, x + 168, 988, lab, 22, INK, True, ha="center"); txt(ax, x + 168, 1058 if "\n" not in src else 1058, src, 14, SUB, ha="center")
    txt(ax, 72, 1135, "ブロックの高さは順序の例示で、百分率ではない。200°Cでできた堆積物にはアンメリドも含まれる（FVV）。", 14, SUB)
    save(fig, "ja-thanh-phan-cap-theo-nhiet-do")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ban_do_nhiet_do(); chuoi_phan_ung(); thang_dong_bang(); han_dung(); giot_phun(); so_sanh_nguon(); ban_do_he_thong(); thanh_phan_cap()
    shutil.copy(ROOT / "lessons/L17/images/ja-cau-truc.png", OUT / "ja-cau-truc-bon-chat.png")
    shutil.copy(ROOT / "lessons/L17/images/ja-bieu-do.png", OUT / "ja-bieu-do-ve-lai.png")

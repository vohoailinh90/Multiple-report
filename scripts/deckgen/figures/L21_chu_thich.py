#!/usr/bin/env python3
"""Số chú thích (huy hiệu vàng + đường dẫn) vẽ lên bốn ảnh thật của bài L21.

usage: L21_chu_thich.py <thư mục ảnh gốc> <thư mục ra>
Ảnh gốc (tên tệp, lấy từ Wikimedia Commons, xem credit trong slides.json): hdd-mo.jpg, ssd-25-mo.jpg, rdimm-ecc.jpg, lto-trong.jpg.
Tọa độ của mỗi bộ phận được đặt thủ công sau khi xem ảnh; số trên ảnh khớp với chú giải trên slide.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# tên ảnh -> (tệp gốc, tệp ra, hệ số phóng ảnh gốc, hệ số tọa độ, bán kính huy hiệu, cỡ chữ, [(số, (x huy hiệu, y huy hiệu), (x đích, y đích))])
JOBS = {
    "hdd": ("hdd-mo.jpg", "hdd-trong-chu-thich.jpg", 1, 1, 40, 44,
            [(1, (1740, 400), (1728, 262)), (2, (1450, 80), (1300, 170)), (3, (900, 420), (900, 268)), (4, (330, 430), (330, 232))]),
    "ssd": ("ssd-25-mo.jpg", "ssd-trong-chu-thich.jpg", 1, 1.6, 34, 38,
            [(1, (380, 1330), (334, 1170)), (2, (1060, 1210), (790, 1190)), (3, (300, 900), (325, 995))]),
    "ram": ("rdimm-ecc.jpg", "dimm-chu-thich.jpg", 1, 1, 40, 44,
            [(1, (442, 1150), (442, 1005)), (2, (1130, 430), (1048, 500)), (3, (576, 650), (576, 520))]),
    "lto": ("lto-trong.jpg", "lto-trong-chu-thich.jpg", 2, 1, 40, 44,
            [(1, (300, 300), (410, 440)), (2, (880, 310), (700, 390)), (3, (150, 1010), (110, 885))]),
}
SS = 2  # vẽ ở độ phân giải gấp đôi rồi thu nhỏ để nét mịn


def annotate(src, dst, zoom, f, r, fs, marks):
    im = Image.open(src).convert("RGB")
    if zoom != 1:
        im = im.resize((im.width * zoom, im.height * zoom), Image.LANCZOS)
    big = im.resize((im.width * SS, im.height * SS), Image.LANCZOS)
    d = ImageDraw.Draw(big)
    font = ImageFont.truetype(FONT, int(fs * f * SS))
    k = f * SS
    for n, (bx, by), (tx, ty) in marks:
        bx, by, tx, ty, rr = bx * k, by * k, tx * k, ty * k, r * k
        d.line([(bx, by), (tx, ty)], fill="#14161C", width=int(12 * k))
        d.line([(bx, by), (tx, ty)], fill="#FFD400", width=int(6 * k))
        d.ellipse([tx - 11 * k, ty - 11 * k, tx + 11 * k, ty + 11 * k], fill="#FFD400", outline="#14161C", width=int(4 * k))
        d.ellipse([bx - rr, by - rr, bx + rr, by + rr], fill="#FFD400", outline="#14161C", width=int(5 * k))
        d.text((bx, by), str(n), font=font, fill="#14161C", anchor="mm")
    big.resize(im.size, Image.LANCZOS).save(dst, "JPEG", quality=90)


if __name__ == "__main__":
    src_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    for name, (a, b, zoom, f, r, fs, marks) in JOBS.items():
        annotate(os.path.join(src_dir, a), os.path.join(out_dir, b), zoom, f, r, fs, marks)
        print("ok", b)

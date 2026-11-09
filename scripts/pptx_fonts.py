"""Đổi font Inter (Moda thay Arial bằng Inter trên canvas) về Arial trong PPTX đã xuất: python3 pptx_fonts.py in.pptx.
SemiBold/ExtraBold thành Arial đậm (b="1"). Chỉ sửa ppt/slides/*.xml, các phần khác giữ nguyên."""
import re, shutil, sys, zipfile
from xml.dom import minidom

def patch(path):
    tmp = path + ".tmp"
    n = 0
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", item.filename):
                x = data.decode("utf-8")
                def rpr(m):
                    nonlocal n
                    attrs, inner = m.group(1), m.group(2)
                    if not re.search(r'typeface="Inter', inner):
                        return m.group(0)
                    heavy = bool(re.search(r'typeface="Inter (?:SemiBold|ExtraBold|Bold)"', inner))
                    inner = re.sub(r'typeface="Inter(?: (?:Light|Regular|Medium|SemiBold|ExtraBold|Bold))?"', 'typeface="Arial"', inner)
                    if heavy and ' b="' not in attrs:
                        attrs += ' b="1"'
                    n += 1
                    return f"<a:rPr{attrs}>{inner}</a:rPr>"
                x = re.sub(r"<a:rPr([^>]*)>(.*?)</a:rPr>", rpr, x, flags=re.S)
                x = re.sub(r'typeface="Inter[^"]*"', 'typeface="Arial"', x)  # endParaRPr and any leftovers
                minidom.parseString(x.encode("utf-8"))  # still well-formed
                data = x.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)
    return n

if __name__ == "__main__":
    print("runs patched:", patch(sys.argv[1]))

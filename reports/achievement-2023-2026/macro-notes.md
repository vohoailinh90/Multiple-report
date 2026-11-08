# Ghi chú về 2 file macro của Linh (đọc ngày 2026-11-02)

Nguồn: `NIKK_Translation_Tool.xlsm`, `Check_PDF_paper_size.xlsm`. Chỉ giải nén và đọc VBA, không chạy macro.

## 1. NIKK_Translation_Tool.xlsm (dự án dịch Anh–Nhật NIKK, 02/2023 → 04/2023 phát triển)

**Mục đích.** Tự động hóa dịch hàng loạt file Excel tiếng Nhật của khách hàng sang tiếng Anh, giữ nguyên bố cục.
Một "Translate Library" (file riêng) lưu cặp Nhật–Anh để dùng lại giữa các file và các dự án.

**4 pha (sheet General / Flow chart):** Input → Translate → Create English file → Print PDF.
1. *Input* (`LibInputByFolder`): mở lần lượt mọi file Excel trong thư mục tiếng Nhật, quét từng sheet (vùng in), ô và
   text box/shape (tự Ungroup), tên sheet, tên file; chỉ lấy ô có tiếng Nhật (`JapaneseIdentify`, `JapaneseExtract`,
   `isKanji`), ghi vào tab người tạo, rồi xóa trùng (`RemoveDuplicates` theo cột Nhật + Anh) và gộp vào tab Master.
   Có cột "Only Japanese Extract" (chỉ phần chữ Nhật), cột "Identify status/Duplicate identify" để đánh dấu mục cần
   người xem (`Identify`, `DuplicateDelete*`). Đổi chữ full-width ↔ half-width.
2. *Translate* (`GoogleTranslateS`, `GoogleTranslateF`): hàm dịch gọi Google Translate qua HTTP, chạy theo dải dòng
   "Translate from/to" trong Library, ghi vào cột Translation để người rà soát.
3. *Create English file* (`CopyToCustomerByFolder`, `ReplaceTextInShapes`, `TranslateSheetNames`,
   `ChangeFontIntoArial`): sao chép file Nhật sang thư mục Anh, thay chữ trong ô, text box, tên sheet và tên file
   bằng bản dịch trong Library (tra bằng MATCH), đổi font Arial.
4. *Print PDF* (`PrintAllSheetToPDFInAllFile`): xuất PDF toàn bộ file tiếng Anh.

**Quy mô.** ~1.200 dòng VBA, 17 module. 8 phiên bản trong 6 tuần (History): v1 22/02/2023 → v8 05/04/2023.
v7 (28/03/2023): "một cú click" cho cả thư mục. v8: dịch tự động bằng Google. File metadata: tạo 10/02/2023,
sửa lần cuối 06/11/2025 (vẫn được bảo trì).

**Số đo thật (sheet ẩn "Time estimate_Use tool" / "Time estimate_Not use tool", Example_JW-324).**
Mẫu: 108 từ mới (tài liệu JW-324). Đo 18/04/2023 (không dùng tool) và 19/04/2023 (dùng tool).
| | Không tool | Có tool |
|---|---|---|
| Tổng | 199,3 phút = 3,32 giờ | 47 phút = 0,78 giờ |
| Trong đó | tra trùng 45, dịch 45, thay vào file khách 105 | trích 5, dịch/rà 40, thay vào file 1 |
Tiết kiệm 2,54 giờ = **76%** (tính lại: (199,3 − 47) / 199,3 = 76,4%) = 1,41 phút mỗi từ.
Ô `P30 = P29*18000/60` = 423,05 → đơn vị thực tế là **GIỜ** cho một dự án giả định **18.000 từ**
(nhãn trong file ghi "minutes", là ghi nhầm; nên sửa nhãn trước khi gửi file này cho ai).
Với 423 giờ/dự án, "hơn 1.000 giờ" tương đương khoảng 2,4 dự án cỡ 18.000 từ. Con số 1.000 giờ là ước tính của Linh
cộng dồn các dự án; file chỉ chứng minh được tỉ lệ 76% trên mẫu 108 từ và giả định 18.000 từ/dự án.

## 2. Check_PDF_paper_size.xlsm (dự án dịch bản vẽ TEF, thư mục "PS-TEF10-2402_Drawing_translation_7th")

**Mục đích.** So sánh PDF bản vẽ đầu vào (tiếng Nhật, "JP") với đầu ra (tiếng Anh, "EN") để chắc rằng khổ giấy, hướng
giấy và số trang không bị đổi trong quá trình dịch; phát hiện lỗi dịch bản vẽ.

**Cách chạy (hướng dẫn nằm trong sheet General, tiếng Việt).** Chia lô 50 file PDF/lần:
1. Dán đường dẫn thư mục vào ô `C3` (cả thư mục JP và EN).
2. Nút *List* (`MakeDrawingList`): liệt kê tên file vào cột C.
3. Nút *Check paper size JP* / *EN* (`CheckPDF_PaperSize_JP/EN`): mở từng PDF bằng Adobe Acrobat (COM `AcroPDDoc`),
   đọc trang 1: số trang, kích thước X, Y (điểm /72 = inch), hướng (Horizontal/Vertical), và phân loại khổ **A5–A0**
   theo cạnh dài với khoảng dung sai (ví dụ A4: 11,5–11,9 in; A3: 16,3–16,7 in).
4. Kết quả JP (cột K–P) và EN (cột Q–V) nằm cạnh nhau cho từng file để so khớp; lặp lại cho lô tiếp theo.
Ngoài ra: `ReName` đổi tên hàng loạt theo cột D (tên mới) để khớp quy ước đặt tên giao hàng.

**Dữ liệu mẫu còn trong file (lô 101–150).** 50 file, khổ A4 ×38 và A3 ×12, JP và EN **khớp 50/50** về số trang,
khổ giấy và hướng giấy (0 sai khác). Thư mục nguồn nằm trên ổ mạng Bosch (không đưa vào deck).

**Quy mô.** ~300 dòng VBA (3 module chính). Sheet General có 1.788 dòng đánh số sẵn nhưng chỉ 50 dòng có dữ liệu.

**Lưu ý trung thực.** Metadata file ghi tác giả gốc là "Tomoya Kubo" (tạo 26/12/2018), sửa lần cuối bởi Linh 08/03/2024.
`MakeDrawingList`/`GetDocuments` có comment tiếng Nhật và nhắc `swDocumentManager` (SolidWorks): đây là mã có sẵn từ
workbook mẫu của đồng nghiệp. Phần Linh thêm: module `Check_Paper_Size` (đọc khổ/hướng/số trang bằng Acrobat, phân loại
khổ A0–A5), cột so sánh JP/EN, hướng dẫn tiếng Việt. Khi trình bày nên nói "mở rộng từ công cụ liệt kê bản vẽ có sẵn".
Chỉ kiểm trang đầu để suy ra khổ giấy (mọi trang khác được coi là cùng khổ). Cần Adobe Acrobat (không phải Reader).

# HANDOFF L02 (đào sâu): trạng thái dang dở

Chưa viết lại `lesson.md` và `slides.json` (vẫn là bản cũ trên main). Chưa chạy gate cho bản mới. Không mở PR.

## Đã làm
- Đọc giáo trình ROTEL: 3.1, 3.2, 3.3 (`types-of-cells-in-the-brain`), 3.4, 5.1, 5.5, 7.4, 8.5, 10.3, 2.7.
- Đọc Neuroscience Online (UTHealth) chương 3, 5, 6, 7, 8 (đọc kỹ), chương 1–2 (chỉ tìm đoạn về kỳ trơ, điện thế nghỉ).
- Kiểm DOI qua Crossref/PubMed và đọc **tóm tắt** của:
  - Azevedo 2009, 10.1002/cne.21974 (86,1 ± 8,1 tỷ tế bào NeuN dương; 84,6 ± 9,8 tỷ không phải nơron)
  - Herculano-Houzel 2009, 10.3389/neuro.09.031.2009
  - Bliss & Lømo 1973, 10.1113/jphysiol.1973.sp010273 (thỏ gây mê; 15/18 con; tăng cường 30 phút–10 giờ)
  - Bliss & Collingridge 1993, 10.1038/361031a0 (LTP là mô hình thực nghiệm chủ đạo cho học và nhớ; dạng phụ thuộc NMDA)
- Hodgkin & Huxley 1952, 10.1113/jphysiol.1952.sp004764: chỉ có tên và thông tin xuất bản (không có tóm tắt); chi tiết cơ chế phải lấy từ giáo trình và UTH.
- Thêm hai hình từ giáo trình 3.4 (Noba, CC BY-NC-SA, mục Media Attributions): `images/dien-the-nghi.jpeg` (Hình 7), `images/dien-the-hoat-dong.png` (Hình 8). Cùng ba hình cũ là 5 hình.

## Còn lại
1. Viết `lesson.md` đúng 14 mục như `L02.expected.json` (3.500–5.000 chữ, ≥ 12 trích dẫn).
2. Viết `slides.json` 34–54 slide, mỗi mục nội dung ≥ 3 slide, slide cuối `references` (tone `dark`).
3. Chạy `python3 scripts/deckgen/check_lesson.py . L02` và `python3 -m unittest discover -s tests`.
4. Đổi "đang viết" thành "xong" ở dòng Trạng thái của `lessons/L02.spec.md`; mở PR, xin Codex review.

## Dàn ý đã chốt (đề xuất nguồn)
- S1 giáo trình; S2 Hodgkin & Huxley 1952 (chỉ mức tên/siêu dữ liệu); S3 Neuroscience Online; S4 Azevedo 2009; S5 Herculano-Houzel 2009; S6 Bliss & Lømo 1973; S7 Bliss & Collingridge 1993 → 6 nguồn độc lập.
- Glia: giáo trình 3.3 (oligodendroglia, tế bào Schwann, astrocyte, microglia) + UTH ch. 8 (astrocyte hấp thu glutamate, đổi thành glutamine). Hai con số mâu thuẫn cần ghi là "đang tranh luận": Azevedo ≈ 1:1 so với UTH ≈ 360 tỷ glia / 90 tỷ nơron.
- Điện thế nghỉ ≈ −70 mV (giáo trình), UTH dùng −65/−60 mV trong ví dụ; ngưỡng ≈ −50 mV (giáo trình), −45 mV trong một ví dụ UTH; bơm Na/K 3 ra 2 vào; đỉnh +40 mV; tốc độ 0,1–100 m/s (UTH); nhảy cóc.
- Synapse: giả thuyết canxi và lượng tử của Katz (UTH ch. 5, ở synapse thần kinh–cơ); EPSP ≈ 1 mV ở nơron vận động tủy sống so với 50 mV ở synapse thần kinh–cơ; trễ 0,5–1 ms; có synapse điện (gap junction).
- Thuốc: chỉ nhóm (chặn thu hồi, chặn thụ thể, bắt chước/đồng vận, ức chế enzyme phân hủy; thêm tăng tổng hợp) + "ức chế cái ức chế"; không tên hoạt chất, không liều.
- Dẻo: Hebb, LTP (NMDA, Mg, Ca, chèn AMPA), LTD, dẻo ngắn hạn (UTH ch. 7).
- Kế hoạch khoảng 46–49 slide; tránh `one-big-number` vì `gen.py` lấy tiêu đề làm số khi `opts` thiếu.

## Lưu ý cho điều phối
- `scripts/deckgen/opts/L02.json` đánh chỉ số theo bản slide cũ (`actors`, `pairs`, `mark`, `center`) và chưa có `concepts`; cần đánh lại khi dựng deck mới.
- Spec ghi "3.2 tế bào, 3.3 xung, 3.4 synapse", thực tế giáo trình: 3.2 cấu tạo nơron, 3.3 các loại tế bào (glia), 3.4 giao tiếp trong và giữa nơron (xung và synapse).

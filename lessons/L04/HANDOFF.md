# L04 đào sâu: việc còn dở (WIP)

Đã xong: `lesson.md` viết lại đủ 12 mục theo `L04.expected.json` (khoảng 5.090 chữ tính cả front matter; cần cắt thêm ~100–150 chữ để vào khoảng 3.500–5.000), 9 nguồn S1–S9 (7 nguồn ngoài giáo trình; S2, S3, S4, S6, S8, S9 chỉ đọc tóm tắt qua Europe PMC/Crossref, S5 đọc toàn bài, S1 và S7 đọc chương thật), 5 hình trong `images/` (hai hình mới: `vo-van-dong-dong-tien.png`, `nao-benh-nhan-tan.jpg`, lấy từ giáo trình, giấy phép theo sách).

Chưa làm:
- `slides.json` vẫn là bản cũ (19 slide): cần viết lại 32–52 slide (kế hoạch ~44: Tóm tắt 2; Thùy trán 4; Vận động và Broca 6; PFC làm gì 4; Chức năng điều hành 5; Gage 5; Kiểm soát 4; Hai bán cầu 4; Chuyên biệt hóa 4; Hiểu lầm 4; Điều cần nhớ 1; Nguồn 1 slide `references`), dùng `body`/`facts`, `[Sn]` trên slide phải có trong `sources` của slide, notes 80–200 chữ, không quá hai slide nặng chữ liền nhau.
- Gate chưa chạy lại: `python3 scripts/deckgen/check_lesson.py . L04` sẽ báo lỗi (slides.json cũ lệch với lesson.md) và `python3 -m unittest discover -s tests`.
- Dòng "Trạng thái" trong `lessons/L04.spec.md` chưa đổi.
- `scripts/deckgen/opts/L04.json` có khóa theo chỉ số slide cũ (`mark`, `big`, `center`); cần cập nhật lúc dựng deck.
- Chưa mở PR, chưa xin review.

Lưu ý nội dung: đoạn "cắt thể chai để giảm động kinh" ghi rõ là kiến thức nền không có nguồn; giáo trình ghi Gage sống 12 năm, Macmillan ghi 11 năm rưỡi (đã nêu trong bài); `lesson.md` đã bỏ bước "thể chai không phải đường duy nhất" vì không có nguồn.

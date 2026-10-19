# Phong cách deck (Moda → PPTX)

Mọi deck của repo này dựng trên Moda theo một hệ thống chung, lấy từ deck System Design của
[tool-marketing-studio](https://github.com/vohoailinh90/tool-marketing-studio/blob/main/docs/sd101-slides.md): các deck nhận ra
là cùng một bộ, nhưng không deck nào giống deck nào. Phần cố định là thương hiệu (font, màu nền, footer, cỡ chữ tối thiểu);
phần thay đổi là layout, nhịp sáng tối và ý tưởng hình ảnh của từng bài.

## Cố định cho mọi deck

- Canvas `1920x1080`, category `slides`, **không brand kit** (`skip_brand_kit=true`), chỉ vector (không sinh ảnh).
  Tên canvas: `Multiple-report · <id> · <tiêu đề>`. Gửi link editor ngay khi canvas có.
- Font: **Bricolage Grotesque** 800 cho tiêu đề và số lớn, **Be Vietnam Pro** cho mọi chữ khác. Cỡ: tiêu đề bìa 108,
  tiêu đề slide 72–100, thân 34–40, nhãn 22–28; không gì dưới 22.
- Màu nền sáng: kem `#F3EEE3`, mực `#14161C`, thẻ `#E8E0CF`, thẻ sơ đồ `#FBF8F2` (viền `#DDD5C1`), chữ phụ `#6B6A66`.
  Accent trên nền sáng: xanh `#1F3FD1`, hổ phách `#B45309`, xanh ngọc `#0F766E`, đỏ `#E8472B`
  (nền nhạt tương ứng `#DDE3FA` `#F3DFB8` `#CFE8E2` `#F8D9D0`).
  Nền tối `#14161C`, thẻ `#1E212B`, chữ `#F3EEE3` / `#E4E1D8`, chữ phụ `#9AA0B5`; accent trên nền tối
  `#7C93FF` `#FFB454` `#3DD6A0` `#FF6A4D`.
- **Mỗi khái niệm một màu, giống nhau trên mọi slide.** Với n là số của bài (`L07` → 7), khái niệm thứ k (đếm từ 0) lấy
  accent số (n + k) mod 4 trong thứ tự xanh, hổ phách, xanh ngọc, đỏ.
- Footer trên mọi slide trừ bìa, góc dưới bên trái: một chấm tiến độ cho mỗi slide (chấm hiện tại màu đỏ) và
  `Multiple-report · L00 · 03/11`. **Để trống góc dưới bên phải** (logo Moda nằm ở đó khi xuất).
- Bìa (tối): nhãn chủ đề viết hoa giãn chữ, tiêu đề, câu hỏi mở bài, mỗi khái niệm chính một thẻ bo tròn viền màu của nó.
  Slide cuối là nguồn tham khảo, nền tối.
- Chữ: tiếng Việt có dấu; mỗi gạch đầu dòng tối đa 10 chữ, mỗi thẻ tối đa 3 gạch; một slide đọc trong 5 giây.
  Chỉ dùng nội dung của `slides.json`; không thêm số liệu, ví dụ hay khẳng định.

## Thay đổi theo từng deck

- **Ý tưởng hình ảnh:** một ý lấy từ chính chủ đề bài (`spec.md` ghi nó; ví dụ bài dopamine dựng quanh một tín hiệu
  thần kinh phát xung). Nói ý đó một dòng khi báo link canvas.
- **Layout:** mỗi slide trong `slides.json` có `layout` và `tone`. Gate `lesson_gates.py` bắt buộc: ít nhất 5 kiểu,
  không trùng kiểu ở hai slide liền nhau, không quá 3 slide liền cùng tone (tính cả bìa tối). Deck builder vẽ đúng kiểu đó:

| layout | Vẽ thế nào |
|---|---|
| `sequence-diagram` | các cột tác nhân, mũi tên tin nhắn đánh số từ trên xuống |
| `flow` | 3–5 hộp nối mũi tên trái sang phải, hộp quyết định khác màu |
| `two-column-comparison` | hai cột màu khác nhau, cùng hàng tiêu chí, một dòng kết luận dưới |
| `2x2-matrix` | hai trục có nhãn, bốn ô, mỗi ô một ý |
| `lookup-table` | `<table>` có hàng tiêu đề, tối đa 5 hàng, cột đầu đậm |
| `card-grid` | 2–4 thẻ bằng nhau, mỗi thẻ số hoặc nhãn màu và một câu |
| `numbered-rows` | các hàng đánh số lớn bên trái, câu bên phải |
| `connection-diagram` | các nút tròn hoặc thẻ nối bằng đường cong, nút trung tâm nổi bật |
| `layers` | các dải ngang chồng lên nhau, tầng trên cùng là thứ người dùng thấy |
| `timeline` | một trục ngang, các mốc có nhãn trên và dưới |
| `one-big-number` | một con số rất lớn (chỉ số bài học có nêu) và một câu giải thích |
| `one-highlighted-sentence` | một câu lớn, từ khóa tô màu của khái niệm |

## Quy trình

1. `moda_bootstrap`, `load_skill("moda-deck")`, `load_skill("markup")`. Không hỏi brand kit: câu trả lời là *không kit*.
2. Một canvas, đủ số trang ngay từ đầu (`page_count` = số slide của `slides.json` + 1 bìa).
3. Mỗi slide một lệnh `canvas_apply_markup`, không chụp màn hình giữa chừng.
4. Ô chữ bị `text_auto_shrunk`: sửa tất cả trong một lệnh `canvas_edit` (`fontSize` cỡ đã khai, `fitHeight: true`).
5. Xem **mọi** slide bằng `canvas_screenshot`, ba trang một lệnh; sửa chữ bị cắt, co nhỏ, chồng lên nhau.
6. `export` dạng **PPTX** (không PNG, không PDF), tải về `lessons/<id>/<id>.pptx`, rồi
   `python3 scripts/decks.py record <id> --canvas <URL>`: script kiểm PPTX có đúng số slide và ghi `deck.json`.

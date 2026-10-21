# Phong cách deck (Moda → PPTX)

Mọi deck của repo này dựng trên Moda theo một hệ thống chung, lấy từ deck System Design của
[tool-marketing-studio](https://github.com/vohoailinh90/tool-marketing-studio/blob/main/docs/sd101-slides.md): các deck nhận ra
là cùng một bộ, nhưng không deck nào giống deck nào. Phần cố định là thương hiệu (font, màu nền, footer, cỡ chữ tối thiểu);
phần thay đổi là layout, nhịp sáng tối và ý tưởng hình ảnh của từng bài.

## Cố định cho mọi deck

- Canvas `1920x1080`, category `slides`, **không brand kit** (`skip_brand_kit=true`), không sinh ảnh bằng máy. Hình có giấy phép lấy từ giáo trình
  (layout `figure`, bên dưới) được phép; mỗi hình phải có dòng tín dụng.
  Tên canvas: `Multiple-report · <id> · <tiêu đề>`. Gửi link editor ngay khi canvas có.
- Font: **Bricolage Grotesque** 800 cho tiêu đề và số lớn, **Be Vietnam Pro** cho mọi chữ khác. Cỡ: tiêu đề bìa 108,
  tiêu đề slide 56–76, thân 34–40, đoạn `body` của slide giải thích 30–38, chữ trong thẻ hồ sơ 28–34, nhãn 22–28; không gì dưới 22.
  `gen.py` tự hạ cỡ chữ theo độ dài (hàm `fit`), không xuống dưới mức sàn của từng ô.
- Màu nền sáng: kem `#F3EEE3`, mực `#14161C`, thẻ `#E8E0CF`, thẻ sơ đồ `#FBF8F2` (viền `#DDD5C1`), chữ phụ `#6B6A66`.
  Accent trên nền sáng: xanh `#1F3FD1`, hổ phách `#B45309`, xanh ngọc `#0F766E`, đỏ `#E8472B`
  (nền nhạt tương ứng `#DDE3FA` `#F3DFB8` `#CFE8E2` `#F8D9D0`).
  Nền tối `#14161C`, thẻ `#1E212B`, chữ `#F3EEE3` / `#E4E1D8`, chữ phụ `#9AA0B5`; accent trên nền tối
  `#7C93FF` `#FFB454` `#3DD6A0` `#FF6A4D`.
- **Mỗi khái niệm một màu, giống nhau trên mọi slide.** Với n là số của bài (`L07` → 7), khái niệm thứ k (đếm từ 0) lấy
  accent số (n + k) mod 4 trong thứ tự xanh, hổ phách, xanh ngọc, đỏ.
- Footer trên mọi slide trừ bìa, góc dưới bên trái: một chấm tiến độ cho mỗi slide (chấm hiện tại màu đỏ) và
  `Multiple-report · L00 · 03/11`. **Để trống góc dưới bên phải** (logo Moda nằm ở đó khi xuất). Deck dài hơn 40 trang thì chấm
  xích lại gần nhau để nhãn không chạm góc đó.
- Bìa (tối): nhãn chủ đề viết hoa giãn chữ, tiêu đề, câu hỏi mở bài, mỗi khái niệm chính một thẻ bo tròn viền màu của nó.
  Slide cuối là nguồn tham khảo, nền tối.
- Chữ: tiếng Việt có dấu. Chủ repo đã bỏ luật "một slide đọc trong 5 giây" (2026-10-20) cho mọi layout: slide được nhiều
  chữ, miễn đọc được. Slide giải thích mang đoạn `body` 60–110 chữ; gạch đầu dòng ≤ 160 ký tự, ≤ 6 gạch.
  Chỉ dùng nội dung của `slides.json`; không thêm số liệu, ví dụ hay khẳng định.

## Thay đổi theo từng deck

- **Ý tưởng hình ảnh:** một ý lấy từ chính chủ đề bài (`spec.md` ghi nó; ví dụ bài dopamine dựng quanh một tín hiệu
  thần kinh phát xung). Nói ý đó một dòng khi báo link canvas.
- **Layout:** mỗi slide trong `slides.json` có `layout` và `tone`. Gate (`scripts/deckgen/check_lesson.py`) bắt buộc: ít nhất 5 kiểu
  (bài theo chuẩn đào sâu: 8), không trùng kiểu ở hai slide liền nhau, không quá 3 slide liền cùng tone (tính cả bìa tối).
  Deck builder (`scripts/deckgen/gen.py`) vẽ đúng kiểu đó; bốn kiểu cuối của bảng thêm ngày 2026-10-20, dựng thử trên canvas
  `Multiple-report · T00 · Mẫu ba layout mới` từ `tests/fixtures/deckgen/slides.json`:

| layout | Vẽ thế nào |
|---|---|
| `sequence-diagram` | các cột tác nhân, mũi tên tin nhắn đánh số từ trên xuống |
| `flow` | 3–5 hộp nối mũi tên trái sang phải, hộp quyết định khác màu |
| `two-column-comparison` | hai cột màu khác nhau, cùng hàng tiêu chí, một dòng kết luận dưới |
| `2x2-matrix` | *(chưa có renderer trong `gen.py`; gate từ chối cho tới khi có)* hai trục có nhãn, bốn ô, mỗi ô một ý |
| `lookup-table` | `<table>` có hàng tiêu đề, tối đa 5 hàng, cột đầu đậm |
| `card-grid` | 2–4 thẻ bằng nhau, mỗi thẻ số hoặc nhãn màu và một câu |
| `numbered-rows` | các hàng đánh số lớn bên trái, câu bên phải |
| `connection-diagram` | các nút tròn hoặc thẻ nối bằng đường cong, nút trung tâm nổi bật |
| `layers` | các dải ngang chồng lên nhau, tầng trên cùng là thứ người dùng thấy |
| `timeline` | một trục ngang, các mốc có nhãn trên và dưới |
| `one-big-number` | một con số rất lớn (chỉ số bài học có nêu) và một câu giải thích |
| `one-highlighted-sentence` | một câu lớn, từ khóa tô màu của khái niệm |
| `figure` | khung trắng bo góc bên trái chứa hình (`fit="contain"`, tải bằng `upload url=`), bên phải 3 thẻ chú giải: nhãn tiếng Anh của hình màu nhấn, nghĩa tiếng Việt bên dưới; dòng `Hình: <tác giả, giấy phép, hình số, chương>` cỡ 22 ở y=890 (tối đa hai dòng), dòng `Nguồn:` ở y=944 |
| `explainer` | cột trái ~65% là đoạn `body` (cỡ 30–38, giãn dòng 1,35, vạch màu bên trái, `**từ khoá**` tô màu khái niệm, `[Sn]` màu chữ phụ); cột phải 2–3 thẻ lấy từ `bullets` dạng `Nhãn: nội dung` (Ở đâu / Làm gì / Đừng hiểu nhầm) |
| `profile-card` | thẻ hồ sơ: lưới 2×2 (4 mục) hoặc 3 cột (3, 5, 6 mục) lấy từ `facts`, nhãn màu khái niệm cỡ 28, chữ 28–34; không vẽ `bullets` |
| `annotated-figure` | như `figure` (khung hình rộng 980) nhưng cột phải là tối đa 3 thẻ chú giải ngắn (≤ 70 ký tự) và một khối nền nhạt chứa `body` 40–70 chữ |
| `references` | slide nguồn: mỗi nguồn một thẻ `S1` + tên rút gọn (≤ 110 ký tự); một cột đến 6 nguồn, hai cột đến 18 |

## Quy trình

1. `moda_bootstrap`, `load_skill("moda-deck")`, `load_skill("markup")`. Không hỏi brand kit: câu trả lời là *không kit*.
2. Một canvas, đủ số trang ngay từ đầu (`page_count` = số slide của `slides.json` + 1 bìa).
3. Mỗi slide một lệnh `canvas_apply_markup` với markup của `python3 scripts/deckgen/gen.py <id> <i> --opts scripts/deckgen/opts/<id>.json`
   (`i = 0` là bìa; trang `p_a` là 0, `p_b` là 1...). Nhiều lệnh song song trong một lượt được; không chụp màn hình giữa chừng.
   `opts/<id>.json` giữ nhãn bìa, câu hỏi mở bài, thẻ bìa, số lớn, câu tô màu và danh sách `concepts` (màu khái niệm của `**từ khoá**`).
4. Ô chữ bị `text_auto_shrunk`: sửa tất cả trong một lệnh `canvas_edit` (`fontSize` cỡ đã khai, `fitHeight: true`).
5. Xem **mọi** slide bằng `canvas_screenshot`, ba trang một lệnh; sửa chữ bị cắt, co nhỏ, chồng lên nhau.
6. `export` dạng **PPTX** (không PNG, không PDF), tải về `lessons/<id>/<id>.pptx`, rồi
   `python3 scripts/decks.py record <id> --canvas <URL>`: script kiểm PPTX có đúng số slide và ghi `deck.json`.

## Hình trong bài

- Ảnh nằm ở `lessons/<id>/images/` (ngoại lệ của quy tắc "chỉ PPTX"; `.gitignore` cho phép `lessons/*/images/*.png`), khai báo trong `slides.json` khóa `images` (`file`, `alt`, `credit`, `url`) và chèn vào `lesson.md` kèm chú thích và `Nguồn hình`.
- Chỉ dùng hình mà mục *Media Attributions* của chương ghi giấy phép cho phép dùng lại (giáo trình là CC BY-NC-SA 4.0). Giấy phép riêng của từng hình ghi như sách nêu; hình đã đối chiếu trên Wikimedia Commons: Blausen (CC BY 3.0), Gage (CC BY 2.5).
- Thêm một slide chen giữa làm dời chân trang (chấm tiến độ và NN/TT) của mọi slide sau, nên dựng lại cả deck trên canvas mới thay vì chèn.
- Áp markup lên trang đã có nội dung sẽ **thêm chồng**, không thay thế; sửa trang thì xoá nút cũ bằng `canvas_delete` hoặc dùng `canvas_edit`.

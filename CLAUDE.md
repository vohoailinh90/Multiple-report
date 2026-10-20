# Multiple-report: bài học đa ngành

Kho lưu những gì chủ repo đã hỏi Claude (thần kinh, não bộ, triết học, sức khỏe, quản lý dự án, kỹ thuật...),
mỗi chủ đề thành một bài học tiếng Việt có nguồn và một file PowerPoint, để đọc lại thay vì hỏi lại.

Bài học được viết theo quy trình `team-lesson` của
[claude-agent-routing-template](https://github.com/vohoailinh90/claude-agent-routing-template/blob/main/docs/vps-team-lesson.md):
Claude thiết kế và audit, model miễn phí trên VPS viết, Claude làm deck bằng Moda sau khi merge.

## Làm việc tự chủ

Chủ repo đã cho phép trước mọi việc trong repo này: tạo, sửa bài học, làm deck bằng Moda, xuất PPTX, commit và
push. Làm đến hết việc được giao, không dừng để xin xác nhận từng bước. Chỉ hỏi khi một quyết định về nội dung
thật sự thuộc về chủ repo (bài nói về điều gì), hoặc khi một công cụ từ chối và không có cách khác.

- Không giao việc Moda cho subagent: mỗi lệnh của subagent lại chờ chủ repo duyệt. Mọi lệnh Moda chạy trong
  phiên chính.
- Gộp lệnh: dựng mỗi deck bằng ít lệnh nhất có thể; không chụp màn hình sau mỗi lần sửa (tối đa một lần cuối).
- Quyền tool đã có trong `.claude/settings.json`. Nếu vẫn bị hỏi duyệt, báo một lần tên tool cần thêm, rồi làm tiếp.

## Cấu trúc một bài

```text
lessons/<id>.expected.json   các kiểm tra của gate (tester viết; không ai khác sửa)
lessons/<id>/lesson.md       bài học
lessons/<id>/slides.json     dàn ý slide đã duyệt
lessons/<id>/<id>.pptx       deck Moda (chỉ PPTX; không PNG, không PDF)
lessons/<id>/deck.json       hash của slides.json mà deck được dựng từ đó (scripts/decks.py record)
lessons/README.md            mục lục, sinh bởi scripts/decks.py index
```

`lesson.md`:
- front matter `---` với `id`, `title`, `topic`, `date` (YYYY-MM-DD), rồi `# <title>`;
- `topic` là một trong `than-kinh`, `nao-bo`, `triet-hoc`, `suc-khoe`, `quan-ly-du-an`, `ky-thuat`, `khac`;
- các mục `## ` theo spec; bài sức khỏe (hoặc có nội dung y tế) có `## Lưu ý` (không phải lời khuyên y tế);
  mục cuối luôn là `## Nguồn tham khảo` với mỗi nguồn một dòng `- [S1] tác giả, tên, năm, URL`;
- tiếng Việt có dấu; thuật ngữ kèm tiếng Anh trong ngoặc lần đầu; trích dẫn `[S1]` ngay sau ý;
- không bịa nguồn, số liệu, nghiên cứu, ngày tháng hay câu trích. Thiếu nguồn thì viết ý không kèm số liệu.

`slides.json`: `{"title", "subtitle", "slides": [{"title", "bullets", "notes", "section", "sources", "layout", "tone"}]}`,
thêm hai trường tuỳ chọn:
- `body`: đoạn giải thích hiện **trên slide**, 60–110 chữ (gate nhận 40–130), `[S1]` ngay sau ý, `**từ khoá**` được tô màu khái niệm.
  Chỉ dùng cho layout `explainer` (bắt buộc ở đó) và `annotated-figure` (40–70 chữ).
- `facts`: mảng 3–6 cặp `{"label", "text"}` (nhãn ≤ 40, chữ ≤ 160 ký tự) cho layout `profile-card` (thẻ hồ sơ của một bộ phận,
  chất dẫn truyền hay cảm xúc).

Slide giải thích dùng `body`; slide sơ đồ (`flow`, `card-grid`, `layers`...) vẫn dùng gạch ngắn (≤ 160 ký tự, ≤ 6 gạch; layout
`references` ≤ 18 nguồn). `notes` là lời giảng 80–200 chữ: ví dụ, chỗ dễ nhầm. Mỗi mục `## ` có ít nhất một slide; bài theo chuẩn
đào sâu (`docs/ban-giao-mo-rong-noi-dung.md`, mục 3) có ít nhất ba slide mỗi mục nội dung. `lessons/<id>.spec.md` là spec của bài
(điều phối viết, phiên viết đọc). Kiểm: `python3 scripts/deckgen/check_lesson.py . <id>`.

## Làm deck (PPTX) bằng Moda

Phong cách và quy trình: **`docs/deck-style.md`** (font, màu, footer, cách vẽ 17 kiểu layout, màu của từng khái niệm),
lấy từ deck System Design của tool-marketing-studio. Markup từng trang sinh bằng `scripts/deckgen/gen.py`.

1. `git pull`, rồi `python3 scripts/decks.py todo`: danh sách bài thiếu deck hoặc deck cũ. Làm tất cả.
2. Mỗi bài: đọc `slides.json` (không thêm ý mới). Một canvas, bìa tối rồi mỗi phần tử một slide theo đúng `layout` và
   `tone` của nó; nguồn `[S1]` ở chân slide. Logo Moda trên slide là chấp nhận được.
3. Xem mọi slide (ba trang một lệnh chụp), sửa một lần. Xuất **PPTX** (không PNG), tải về `lessons/<id>/<id>.pptx`,
   rồi `python3 scripts/decks.py record <id> --canvas <URL>`.
4. Hết bài: `python3 scripts/decks.py todo` không in gì; `python3 scripts/decks.py index`; commit
   (`decks: <ids>`) và push; báo link canvas của từng bài.

## Kiểm tra

`python3 -m unittest discover -s tests` (CI chạy lệnh này). Gate cấu trúc trong repo: `scripts/deckgen/check_lesson.py`
(có test). Gate `lesson_gates.py` của pipeline `team-lesson` nằm ở repo template; bản `f80c4cc` (2026-10-20) chỉ nhận 7 trường
slide (không `images`, `body`, `facts`), 12 layout (không `figure` và 4 layout mới), không nhận khóa lạ trong `expected.json` và mặc định
tối đa 20 slide, nên các bài có hình hoặc theo chuẩn đào sâu chưa chạy được qua pipeline đó cho đến khi repo template được cập nhật.

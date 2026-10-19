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

`slides.json`: `{"title", "subtitle", "slides": [{"title", "bullets", "notes", "section", "sources"}]}`. Gạch đầu
dòng là cụm từ ngắn (≤ 160 ký tự, ≤ 6 gạch), phần giải thích để trong `notes`; mỗi mục `## ` có ít nhất một slide.

## Làm deck (PPTX) bằng Moda

1. `git pull`, rồi `python3 scripts/decks.py todo`: danh sách bài thiếu deck hoặc deck cũ. Làm tất cả.
2. Mỗi bài: đọc `slides.json` (không thêm ý mới), tạo một deck Moda: slide tiêu đề, rồi mỗi phần tử một slide theo
   thứ tự (thẻ, bước đánh số hay hai cột khi hợp nội dung), nguồn `[S1]` ở chân slide; `notes` nằm sẵn trong
   slides.json và lesson.md, chỉ thêm làm ghi chú người trình bày nếu Moda hỗ trợ. Tiếng Việt, font `Be Vietnam Pro`, một
   theme chung cho cả repo (nền xanh navy đậm, điểm nhấn màu ấm). Logo Moda trên slide là chấp nhận được.
3. Xuất **PPTX**, tải về `lessons/<id>/<id>.pptx`, rồi `python3 scripts/decks.py record <id> --canvas <canvas id>`.
4. Hết bài: `python3 scripts/decks.py todo` không in gì; `python3 scripts/decks.py index`; commit
   (`decks: <ids>`) và push; báo link canvas của từng bài.

## Kiểm tra

`python3 -m unittest discover -s tests` (CI chạy lệnh này). Gate cấu trúc bài học (`lesson_gates.py`) nằm ở repo
template và chạy trong pipeline `team-lesson`.

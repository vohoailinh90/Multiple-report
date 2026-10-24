---
task_id: PSY-LESSON-A02-V1
lesson: A02
status: giao
claimed_by: null
claimed_at: null
heartbeat_at: null
canvas_url: null
branch: psychology/lesson-a02
base: psychology/batch-02-three-decks
assigned: 2026-10-24
---
# Lệnh giao việc A02 — Individual Psychology và quan điểm toàn thể

Hợp đồng giao việc cho **một** sub-agent của phiên thực thi (Codex), do phiên điều phối (Claude) soạn ngày 2026-10-24. Sổ chung: [COORDINATION.md](../../COORDINATION.md), mục "Batch 3". Chủ repo cho phép Codex viết bài và dùng Moda trong phạm vi bài này (ngoại lệ batch 3 so với quy trình "Codex chỉ review"); không mở rộng sang bài khác.

## 1. Nhận bài và chống trùng (làm đúng thứ tự, không hỏi ai)

1. `git fetch origin`. Làm việc trong worktree riêng của nhánh `psychology/lesson-a02` (PR nháp đã có sẵn, base `psychology/batch-02-three-decks`). Kiểm: `git branch -r | grep -i a02` chỉ ra đúng `origin/psychology/lesson-a02`, và không có PR nào khác mang mã A02 trong tiêu đề. Thấy khác đi thì dừng và báo.
2. Đọc front matter ở đầu file này. `status: giao` thì bạn nhận được. `status: đang làm` bởi chủ khác mà `heartbeat_at` chưa quá 24 giờ thì **dừng và báo**, không đoạt bài.
3. Sửa front matter: `status: đang làm`, `claimed_by` (tên agent hoặc phiên), `claimed_at` và `heartbeat_at` (UTC, dạng `2026-10-24T08:00:00Z`). Commit `claim: A02` và **push trước khi viết**.
4. Mỗi lần push về sau cập nhật `heartbeat_at`. Khi chuyển giai đoạn hoặc xong, đổi `status` (`chờ phản biện` khi đã push đủ).
5. Moda: `canvas_search` theo "A02" trước khi dựng. Thấy canvas của chính bài này thì dùng tiếp; không dựng canvas thứ hai. Tạo xong ghi ngay `canvas_url` vào front matter và push.
6. Không đụng F02, A01, J01 (đã xong ở PR #38) hay bài nào khác. Không tạo nhánh, PR hay canvas thứ hai cho A02.

## 2. Luật tự chủ (áp dụng cho phiên chính và mọi sub-agent)

- Chủ repo đã cho phép trước: nghiên cứu web, viết các file ở mục 4, Moda, commit và push lên đúng nhánh `psychology/lesson-a02`. Không xin xác nhận từng bước.
- Không xin nâng quyền hay duyệt mạng. Lệnh nào bị sandbox chặn (tải file, mạng ngoài) thì ghi hạn chế vào metadata, **không chờ duyệt**, làm tiếp, không thử lại quá một lần.
- Hỏi chủ repo **tối đa một lần cho cả bài**, gộp mọi vấn đề vào một câu, và chỉ khi (a) quyết định nội dung vượt phạm vi mục 3, hoặc (b) công cụ từ chối mà không có đường khác. Sau câu hỏi vẫn làm tiếp phần không bị chặn.
- Gộp lệnh: đọc nhiều file trong một lệnh, ghi mỗi file một lần, dựng deck bằng ít lệnh Moda nhất; chụp màn hình mỗi trang tối đa một lần ở bản cuối (ba trang một lệnh chụp).
- Sub-agent không dùng git, không gọi sub-agent con, không ghi ngoài mục 4. Phiên chính commit và push.
- Không bịa nguồn, số liệu, trang, ngày hay câu trích. Thiếu thì thu hẹp claim, ghi `chưa đánh giá` và giới hạn. Không tự xin review, không đánh dấu PR sẵn sàng, không merge: điều phối làm.

## 3. Phạm vi bài

**Dòng curriculum:** Hiểu *individual* là không thể chia cắt; kết nối hành vi, mục tiêu và bối cảnh xã hội. Ý tưởng hình: *con người trong các bối cảnh*.

**Đọc trước:** [A01](../lessons/01-cuoc-doi-va-khac-biet-voi-freud.md). Không lặp lại tiểu sử và việc tách nhóm ở A01, chỉ dẫn link khi cần. **Đọc tiếp:** A03 (Inferiority Feelings). A08 (phong cách sống), A09 (mục tiêu hư cấu) và A10 (quan tâm xã hội) chỉ được định vị bằng một đoạn ngắn "sẽ học ở bài…", không giải trước.

**Trọng tâm cần dạy**

1. Tên *Individual Psychology*: "individual" theo nghĩa không thể chia cắt, không phải chủ nghĩa cá nhân. Kiểm từ nguyên và cách chính Adler cùng người biên tập giải thích; thiếu nguồn thì nói hẹp lại.
2. Quan điểm toàn thể và tính thống nhất của nhân cách: suy nghĩ, cảm xúc, hành vi và triệu chứng được đọc như các phần của một chuyển động hướng tới mục tiêu. Đối chiếu công bằng với mô hình chia cấu phần ở F03, không xếp hạng đúng/sai.
3. Hành vi đọc theo hướng và ý nghĩa chủ quan (goal-directedness), con người trong bối cảnh xã hội (gia đình, nhóm, cộng đồng).
4. Ý nghĩa và giới hạn thực tiễn: đọc một hành vi trong mạng ý nghĩa là **giả thuyết** cần kiểm bằng đối thoại và dữ kiện, không phải suy "mục tiêu ẩn" từ một hành vi.

**Phải phân biệt:** *individual* ≠ *individualism*; "toàn thể" của Adler ≠ "holistic" theo nghĩa y học thay thế hay đời sống thường ngày; hướng đích (teleology) ≠ khẳng định mục tiêu luôn có ý thức; lời Adler ≠ chú giải của người biên tập tuyển tập (Ansbacher) ≠ phát triển của các nhà Adler sau này. A01 đã ghi giới hạn về văn bản qua trung gian; kế thừa và không giả vờ đã đọc bản gốc.

**Giới hạn bắt buộc (ngoài STANDARDS):** không dùng sự giống CBT làm bằng chứng cho học thuyết; tách bằng chứng cấp thành tố, gói trị liệu và toàn bộ học thuyết (đi sâu ở A15, ở đây chỉ nêu ranh giới); không dùng cách đọc toàn thể làm công cụ chẩn đoán hay suy động cơ của một người cụ thể; ví dụ và ca là giả định, có giải thích thay thế.

**Nguồn gợi ý (tự kiểm tra tồn tại, ấn bản và trang trước khi dùng; không phải nguồn đã đọc):**
- Adler, A. (1956), *The Individual Psychology of Alfred Adler*, Ansbacher & Ansbacher (biên tập). Đã có mục A-SRC01 trong [sources.md](sources.md), mới ở mức metadata; đây là tuyển tập hậu kỳ, phân biệt lời Adler với chú giải biên tập.
- Adler, A., *Understanding Human Nature* (bản gốc tiếng Đức 1927), *The Science of Living* (1929), *What Life Should Mean to You* (1931): kiểm năm gốc, bản dịch và trang thật sự đọc.
- Carlson, J., Watts, R. E. & Maniacci, M. (2006), *Adlerian Therapy: Theory and Practice*, American Psychological Association: giáo trình để đối chiếu cách trình bày hiện đại; kiểm thông tin xuất bản.
- Nguồn đã dùng ở A01 (xem [a01-research.md](a01-research.md)) khi nhắc lại bối cảnh.

**Ví dụ gợi ý (viết lại, có phân tích và giải thích thay thế):** một học sinh liên tục đến lớp muộn; một nhân viên từ chối nhận việc mới dù đủ năng lực; một người ngại đưa ý kiến trong họp nhóm. Nhấn mạnh cách đọc theo bối cảnh và nhiều giả thuyết cạnh tranh. Ca giả định phức tạp hơn do bạn thiết kế, không phải ca công bố.

## 4. Sản phẩm và quyền ghi

Chỉ ghi các file sau (thư mục tác giả `02-Alfred-Adler`). `COORDINATION.md` và mọi file dùng chung ở gốc `psychology-knowledge/` chỉ điều phối sửa.

| File | Nội dung | Giai đoạn |
|---|---|---|
| `02-Alfred-Adler/lessons/02-individual-psychology-va-quan-diem-toan-the.md` | Bài đủ A–L; front matter `id`, `title`, `topic: khac`, `date` (ngày sửa thực tế), `status: drafted`, `review_status: pending`, `visual_status` | 1 |
| `02-Alfred-Adler/references/a02-research.md` | Search log (truy vấn, ngày, tiêu chí chọn), bảng trạng thái nguồn và locator, claim ledger với Claim ID `A02-C01…` | 1 |
| `02-Alfred-Adler/moda/a02-slides.json` | Kịch bản 35–40 slide | 1 |
| `02-Alfred-Adler/references/a02-visual-sources.md` | Nguồn, credit, mức kiểm quyền của từng ảnh | 2 |
| `02-Alfred-Adler/moda/a02-report-v1.json` | Metadata Moda: canvas, trang, markup, tài nguyên, kiểm tra, link xuất, cảnh báo, giới hạn; cùng khoá với `02-Alfred-Adler/moda/a01-report-v1.json` | 2 |
| `02-Alfred-Adler/visuals/` | PPTX/PDF chỉ khi tải về thật sự thành công; không tạo file giả | 2 |
| file lệnh này | Chỉ front matter và mục "Nhật ký" ở cuối | 1–2 |
| `02-Alfred-Adler/README.md` | Tuỳ chọn: thêm đúng một dòng liên kết tới bài khi file bài đã tồn tại | 1 |

## 5. Giai đoạn 1 — nghiên cứu, viết bài, kịch bản slide

**Đọc trước (một lượt):** `psychology-knowledge/STANDARDS.md`, `DESIGN-SYSTEM.md`, dòng của A02 trong `PROGRAM.md` và `02-Alfred-Adler/curriculum.md`, `02-Alfred-Adler/references/sources.md`, bài mẫu F01 (đã được chủ repo duyệt) và A01 (cùng tuyến, cùng chuẩn) làm mẫu về độ sâu và giọng văn. Không sao chép nội dung bài khác.

**Nghiên cứu:** dùng web thật; ưu tiên văn bản gốc, rồi nghiên cứu peer-reviewed, review/meta-analysis, sách học thuật; tìm cả nguồn trái chiều. Ghi mức truy cập thực tế của từng nguồn (`metadata-verified`, `abstract-read`, `full-text-read`, `locator-verified`) và không nâng mức khi chưa đọc. Điền claim ledger cho mỗi khẳng định quan trọng trước khi chốt bài.

**Bài học:** `## Lưu ý` (tài liệu giáo dục, không tự chẩn đoán) trước mục A; rồi A–L đúng STANDARDS: A mục tiêu quan sát được; B bối cảnh và năm tác phẩm gốc; C lý thuyết cốt lõi và điều khái niệm không cho phép suy ra; D cơ chế từng bước, gắn nhãn mô hình đề xuất; E **ít nhất ba** ví dụ từ đơn giản đến phức tạp, mỗi ví dụ có phân tích và giải thích thay thế; F **một** ca giả định phân tích từng bước (ghi rõ giả định, điều còn thiếu, cách kiểm tra); G bằng chứng hỗ trợ **và** trái chiều, thiết kế nghiên cứu, giới hạn đo lường; H ứng dụng có điều kiện; I mô tả hình, caption, alt text và nguồn (chưa có canvas thì `visual_status: not-started`, không link giả); J 5–10 điểm ghi nhớ gồm cả giới hạn khoa học; K **đúng 5** câu hỏi, đáp án giải thích lập luận và lỗi hiểu thường gặp, có câu vận dụng và câu đánh giá bằng chứng; L mỗi nguồn một dòng `[S1] tác giả, tên, năm, ấn bản/DOI/URL, locator`. `[S1]` đặt sát khẳng định. Tiếng Việt có dấu; thuật ngữ tiếng Anh ở lần xuất hiện đầu. Có liên kết "đọc trước/đọc tiếp".

**Kịch bản slide** `a02-slides.json`, cùng lược đồ với `02-Alfred-Adler/moda/a01-slides.json`: khoá cấp cao `title`, `subtitle`, `status`, `review_status`, `visual_status`, `design_system`, `source_lesson`, `slides`, `canvas_ref`, `canvas_url`, `exports`, `presentation_status`, `production_notes`; mỗi slide có `title`, `section`, `body`, `nodes`, `layout`, `source`, `note`, `visual_brief`. 35–40 slide (không ép số nếu làm giảm chiều sâu), đi theo bài: bìa, lộ trình, các mục A–L, nguồn, kết. `body` là đoạn giải thích hiện trên slide, đủ ý; `nodes` là sơ đồ hỗ trợ, không rút nội dung thành nhãn rời. Không thêm ý không có trong bài. Layout lấy từ bộ đã dùng ở F01 v4 và A01 (cover, roadmap, lead, comparison, timeline, flow, mechanism, matrix, balance, ledger, example, dialogue, decision, takeaways, question, references, closing…).

Kết giai đoạn 1: commit, push, cập nhật `heartbeat_at`, chuyển sang giai đoạn 2 cùng phiên.

## 6. Giai đoạn 2 — Moda, PPTX/PDF

- **Chuẩn thiết kế:** F01 v4 đã duyệt. Canvas https://moda.app/canvas/53a95d71-d2f0-4013-ad6c-7d526ff19027?source=agent và `01-Sigmund-Freud/moda/f01-report-v4.json`; canvas của A01 (https://moda.app/canvas/c53e3ca8-b9de-4fb8-8506-65caf8644eed?source=agent) là bản cùng tuyến. Đọc hai canvas làm tham chiếu, không sao chép nội dung.
- **Thông số:** trang 1920×1080; không brand kit (bỏ qua theo quyết định của chủ repo); chữ tiêu đề Bricolage Grotesque, chữ thân Be Vietnam Pro; Teal `#14695F`, teal đậm `#123D3A`, teal nhạt `#A6D6C6`, kem `#F5F0E6`, mực `#182B2B`; tiêu đề mục A–L có emoji 🎯 🕰️ 🧠 ⚙️ 💬 📋 🔬 🧭 🗺️ 💡 ❓ 📚; icon nét mảnh 56 px ở góc trên phải trang nội dung; sơ đồ dùng connector neo vào node, đường đứt và nhãn "giả thuyết" cho cơ chế chưa xác nhận.
- **Ảnh tư liệu:** chỉ ảnh có nguồn và quyền kiểm được (ưu tiên Wikimedia Commons miền công cộng); credit ngay trên trang dùng; `fit=contain`, không cắt; ảnh chưa rõ quyền thì bỏ, ghi vào `excluded_assets`. Không dùng ảnh người thật làm đại diện cho ca giả định. Ghi tất cả vào `a02-visual-sources.md`.
- **Trình tự (ít lệnh nhất):** `moda_bootstrap` một lần; nạp skill markup đúng theo catalog; `canvas_search` "A02"; tạo canvas với toàn bộ trang; ghi `canvas_url` vào front matter, push; chụp tất cả trang theo nhóm ba trang một lệnh, sửa **một lần**; xuất **PPTX và PDF** (không PNG); thử tải vào `02-Alfred-Adler/visuals/` đúng một lần, bị chặn thì ghi lý do và dừng, không tạo file giả.
- **Ghi lại:** `a02-report-v1.json`, `a02-visual-sources.md`; cập nhật mục I của bài (link canvas, PPTX, PDF, metadata, nguồn ảnh), `visual_status` (`exported` / `canvas-only` / `blocked`) trong bài, và `canvas_url`, `exports`, `presentation_status` trong `a02-slides.json`. Cảnh báo xuất (ví dụ trang PDF bị rasterize) ghi nguyên văn.
- Không dựng thêm canvas hay bản xuất khi đã có bản đúng; lỗi công cụ thì ghi `blocked` cùng nguyên nhân, không giả làm đã xong.

## 7. Kiểm trước khi báo xong (chạy một lần)

- Bài đủ A–L; ít nhất 3 ví dụ và 1 ca có phân tích; 5–10 điểm ghi nhớ; đúng 5 câu hỏi có giải thích; mọi khẳng định chính có `[S#]` truy được tới mục L; không có trích dẫn, trang hay số liệu chưa kiểm.
- Trạng thái trung thực: `status: drafted`, `review_status: pending` (không tự ghi đã review), `visual_status` đúng thực tế. Không viết "complete".
- Mọi file JSON đọc được bằng `python3 -m json.tool`; mọi liên kết tương đối tới file có thật.
- Phạm vi: `git diff --name-only origin/psychology/batch-02-three-decks...HEAD` chỉ gồm file ở mục 4 (cộng `COORDINATION.md` từ commit điều phối); `git diff --check` sạch.
- `python3 -m unittest discover -s tests` và `python3 scripts/claims.py check --merge-ready` thoát 0 (CI chạy hai lệnh này).

## 8. Báo cáo cuối (một lần, đúng khuôn)

```text
A02 — status: drafted · review: pending · visual: <exported|canvas-only|blocked>
Nhánh/commit: <nhánh> @ <sha>
File: <danh sách đường dẫn>
Slide: <số> · Canvas: <URL> · PPTX: <URL> · PDF: <URL> · cảnh báo xuất: <nguyên văn hoặc không>
Nguồn: <số nguồn> · full-text <n> / abstract <n> / metadata <n> · claim phải thu hẹp: <danh sách>
Hạn chế và việc còn mở: <ngắn>
Câu hỏi cho chủ repo (tối đa một): <hoặc không>
```

## Nhật ký (chủ bài ghi, mỗi dòng một mốc)

- 2026-10-24 — điều phối giao bài; chưa ai nhận.

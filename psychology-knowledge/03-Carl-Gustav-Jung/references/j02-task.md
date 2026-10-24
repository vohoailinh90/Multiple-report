---
task_id: PSY-LESSON-J02-V1
lesson: J02
status: chờ phản biện
claimed_by: j02_ppt_production
claimed_at: 2026-10-24T15:15:45Z
heartbeat_at: 2026-10-24T15:47:05Z
requested_from: Codex (yêu cầu comment trên PR của bài; task PSY-LESSON-J02-V1 vòng 1)
requested_at: 2026-10-24T07:26:01Z
canvas_url: https://moda.app/canvas/835be034-4ca5-49f9-bf5d-64f12a43478d?source=agent
branch: psychology/lesson-j02
base: psychology/batch-02-three-decks
assigned: 2026-10-24
---
# Lệnh giao việc J02 — Analytical Psychology

Hợp đồng giao việc cho **một** phiên thực thi (Codex; nếu dùng sub-agent thì mỗi bài một sub-agent), do phiên điều phối (Claude) soạn ngày 2026-10-24. Sổ chung: [COORDINATION.md](../../COORDINATION.md), mục "Batch 3". Chủ repo cho phép Codex viết bài và dùng Moda trong phạm vi bài này (ngoại lệ batch 3 so với quy trình "Codex chỉ review"); không mở rộng sang bài khác.

## 1. Nhận bài và chống trùng (làm đúng thứ tự, không hỏi ai)

1. `git fetch origin`. Làm việc trong worktree riêng của nhánh `psychology/lesson-j02` (PR nháp đã có sẵn, base `psychology/batch-02-three-decks`). Kiểm: `git branch -r | grep -i j02` chỉ ra đúng `origin/psychology/lesson-j02`, và không có PR nào khác mang mã J02 trong tiêu đề. Thấy khác đi thì dừng và báo.
2. Đọc front matter ở đầu file này. `status: giao` thì bạn nhận được. `status: đang làm` bởi chủ khác mà `heartbeat_at` chưa quá 24 giờ thì **dừng và báo**, không đoạt bài.
3. Sửa front matter: `status: đang làm`, `claimed_by` (tên agent hoặc phiên), `claimed_at` và `heartbeat_at` (UTC, dạng `2026-10-24T08:00:00Z`). Commit `claim: J02` và **push trước khi viết**.
4. Mỗi lần push về sau cập nhật `heartbeat_at`. Khi chuyển giai đoạn hoặc xong, đổi `status` (`chờ phản biện` khi đã push đủ).
5. Moda: `canvas_search` theo "J02" trước khi dựng. Thấy canvas của chính bài này thì dùng tiếp; không dựng canvas thứ hai. Tạo xong ghi ngay `canvas_url` vào front matter và push.
6. Không đụng F02, A01, J01 (đã xong ở PR #38) hay bài nào khác. Không tạo nhánh, PR hay canvas thứ hai cho J02.

## 2. Luật tự chủ (áp dụng cho phiên chính và mọi sub-agent)

- Chủ repo đã cho phép trước: nghiên cứu web, viết các file ở mục 4, Moda, commit và push lên đúng nhánh `psychology/lesson-j02`. Không xin xác nhận từng bước.
- Không xin nâng quyền hay duyệt mạng. Lệnh nào bị sandbox chặn (tải file, mạng ngoài) thì ghi hạn chế vào metadata, **không chờ duyệt**, làm tiếp, không thử lại quá một lần.
- Hỏi chủ repo **tối đa một lần cho cả bài**, gộp mọi vấn đề vào một câu, và chỉ khi (a) quyết định nội dung vượt phạm vi mục 3, hoặc (b) công cụ từ chối mà không có đường khác. Sau câu hỏi vẫn làm tiếp phần không bị chặn.
- Gộp lệnh: đọc nhiều file trong một lệnh, ghi mỗi file một lần, dựng deck bằng ít lệnh Moda nhất; chụp màn hình mỗi trang tối đa một lần ở bản cuối (ba trang một lệnh chụp).
- Sub-agent không dùng git, không gọi sub-agent con, không ghi ngoài mục 4. Phiên chính commit và push.
- Không bịa nguồn, số liệu, trang, ngày hay câu trích. Thiếu thì thu hẹp claim, ghi `chưa đánh giá` và giới hạn. Không tự xin review, không đánh dấu PR sẵn sàng, không merge: điều phối làm.

## 3. Phạm vi bài

**Dòng curriculum:** Hiểu nguyên tắc đối lập, bù trừ và cách dùng biểu tượng trong hệ thống Jung. Ý tưởng hình: *bản đồ hệ thống có nhãn lý thuyết*.

**Đọc trước:** [J01](../lessons/01-cuoc-doi-va-quan-he-voi-freud.md). Không lặp lại tiểu sử và quan hệ với Freud, chỉ dẫn link khi cần. **Đọc tiếp:** J03 (Conscious Ego). J02 là **bản đồ tổng quan**: mỗi khái niệm (J03 Conscious Ego, J04 Personal Unconscious, J05 Collective Unconscious, J06 Archetypes, J07 Persona, J08 Shadow, J09 Anima và Animus, J10 Self, J11 Individuation, J12 Types, J15 giấc mơ, J20 Transcendent Function, J21 Libido và compensation) chỉ được định vị trong một đoạn ngắn kèm "sẽ học kỹ ở J0x", không giải trước.

**Trọng tâm cần dạy**

1. Tên và vị trí của Analytical Psychology so với psychoanalysis: kiểm năm và cách chính Jung dùng tên này từ nguồn đọc được; phân biệt với "Jungian" trong đời sống phổ thông và với MBTI.
2. Ba nguyên lý nền của mô hình: đối lập (opposites), bù trừ (compensation), tự điều hòa của tâm lý (psyche as self-regulating). Trình bày như **mô hình khái niệm của Jung**, dẫn định nghĩa của chính Jung và nêu nguồn.
3. Biểu tượng (symbol) trong hệ thống Jung: khác "dấu hiệu" (sign), khác từ điển biểu tượng cố định; vì sao đọc biểu tượng cần bối cảnh liên tưởng (nối sang J15, không dạy giải mộng).
4. Bản đồ hệ thống: ý thức/ego, vô thức cá nhân, vô thức tập thể (giả thuyết), persona, shadow, anima/animus, Self, individuation. Mỗi nút mang nhãn "Jung đề xuất" hoặc "giả thuyết" và trỏ tới bài sau.
5. Hai cách nhìn một triệu chứng hay giấc mơ, nhân quả–quá khứ và hướng đích–tương lai (prospective), chỉ khi đọc được nguồn của chính Jung.

**Phải phân biệt:** *compensation* của Jung ≠ *compensation* của Adler (A06): chỉ một câu cảnh báo, không so sánh sâu; libido theo Jung để J21; tư tưởng Jung thay đổi theo giai đoạn, không gộp thành hệ thống bất biến; mô hình lý thuyết ≠ cơ chế đã kiểm chứng.

**Giới hạn bắt buộc (STANDARDS và ngoài đó):** collective unconscious, archetypes và synchronicity không được trình bày như cơ chế thực nghiệm đã xác nhận; kết quả nghiên cứu trị liệu theo Jung không xác nhận cơ chế; không giải mộng bằng từ điển biểu tượng; không đưa bài tập active imagination tự thực hành; ghi rõ bản dịch Collected Works (Bollingen) và năm bản gốc của từng văn bản được dùng.

**Nguồn gợi ý (tự kiểm tra tồn tại, tập, ấn bản và trang trước khi dùng; không phải nguồn đã đọc):**
- Jung, C. G., *Psychological Types*, Collected Works tập 6 (bản Đức 1921). Đã có mục J-SRC01 trong [sources.md](sources.md), mới ở mức metadata; kiểm phần định nghĩa thuật ngữ như symbol.
- Jung, C. G., *Two Essays on Analytical Psychology*, Collected Works tập 7, và *The Structure and Dynamics of the Psyche*, Collected Works tập 8 (kiểm mục lục từng tập trước khi gán một bài cho tập đó, ví dụ các bài về năng lượng tâm lý, chức năng siêu việt, tâm lý học giấc mơ).
- Roesler, C. (2013), "Evidence for the Effectiveness of Jungian Psychotherapy: A Review of Empirical Studies", *Behavioral Sciences*. Đã có mục J-SRC04 trong [sources.md](sources.md); dùng ở mục G để tách kết quả trị liệu khỏi cơ chế lý thuyết, đọc đúng phạm vi.
- Nguồn đã dùng ở J01 (xem [j01-research.md](j01-research.md)) khi nhắc lại bối cảnh.

**Ví dụ gợi ý (viết lại, có phân tích và giải thích thay thế):** một người luôn "vui vẻ" ở nơi làm việc rồi kiệt sức khi về nhà; một hình ảnh lặp lại trong giấc mơ được đọc theo hai cách (liên tưởng cá nhân so với nghĩa cố định); một xung đột giữa hai lựa chọn đối lập. Ca giả định phức tạp hơn do bạn thiết kế, không phải ca công bố.

## 4. Sản phẩm và quyền ghi

Chỉ ghi các file sau (thư mục tác giả `03-Carl-Gustav-Jung`). `COORDINATION.md` và mọi file dùng chung ở gốc `psychology-knowledge/` chỉ điều phối sửa.

| File | Nội dung | Giai đoạn |
|---|---|---|
| `03-Carl-Gustav-Jung/lessons/02-analytical-psychology.md` | Bài đủ A–L; front matter `id`, `title`, `topic: khac`, `date` (ngày sửa thực tế), `status: drafted`, `review_status: pending`, `visual_status` | 1 |
| `03-Carl-Gustav-Jung/references/j02-research.md` | Search log (truy vấn, ngày, tiêu chí chọn), bảng trạng thái nguồn và locator, claim ledger với Claim ID `J02-C01…` | 1 |
| `03-Carl-Gustav-Jung/moda/j02-slides.json` | Kịch bản 35–40 slide | 1 |
| `03-Carl-Gustav-Jung/references/j02-visual-sources.md` | Nguồn, credit, mức kiểm quyền của từng ảnh | 2 |
| `03-Carl-Gustav-Jung/moda/j02-report-v1.json` | Metadata Moda: canvas, trang, markup, tài nguyên, kiểm tra, link xuất, cảnh báo, giới hạn; cùng khoá với `03-Carl-Gustav-Jung/moda/j01-report-v1.json` | 2 |
| `03-Carl-Gustav-Jung/visuals/` | PPTX/PDF chỉ khi tải về thật sự thành công; không tạo file giả | 2 |
| file lệnh này | Chỉ front matter và mục "Nhật ký" ở cuối | 1–2 |
| `03-Carl-Gustav-Jung/README.md` | Tuỳ chọn: thêm đúng một dòng liên kết tới bài khi file bài đã tồn tại | 1 |

## 5. Giai đoạn 1 — nghiên cứu, viết bài, kịch bản slide

**Đọc trước (một lượt):** `psychology-knowledge/STANDARDS.md`, `DESIGN-SYSTEM.md`, dòng của J02 trong `PROGRAM.md` và `03-Carl-Gustav-Jung/curriculum.md`, `03-Carl-Gustav-Jung/references/sources.md`, bài mẫu F01 (đã được chủ repo duyệt) và J01 (cùng tuyến, cùng chuẩn) làm mẫu về độ sâu và giọng văn. Không sao chép nội dung bài khác.

**Nghiên cứu:** dùng web thật; ưu tiên văn bản gốc, rồi nghiên cứu peer-reviewed, review/meta-analysis, sách học thuật; tìm cả nguồn trái chiều. Ghi mức truy cập thực tế của từng nguồn (`metadata-verified`, `abstract-read`, `full-text-read`, `locator-verified`) và không nâng mức khi chưa đọc. Điền claim ledger cho mỗi khẳng định quan trọng trước khi chốt bài.

**Bài học:** `## Lưu ý` (tài liệu giáo dục, không tự chẩn đoán) trước mục A; rồi A–L đúng STANDARDS: A mục tiêu quan sát được; B bối cảnh và năm tác phẩm gốc; C lý thuyết cốt lõi và điều khái niệm không cho phép suy ra; D cơ chế từng bước, gắn nhãn mô hình đề xuất; E **ít nhất ba** ví dụ từ đơn giản đến phức tạp, mỗi ví dụ có phân tích và giải thích thay thế; F **một** ca giả định phân tích từng bước (ghi rõ giả định, điều còn thiếu, cách kiểm tra); G bằng chứng hỗ trợ **và** trái chiều, thiết kế nghiên cứu, giới hạn đo lường; H ứng dụng có điều kiện; I mô tả hình, caption, alt text và nguồn (chưa có canvas thì `visual_status: not-started`, không link giả); J 5–10 điểm ghi nhớ gồm cả giới hạn khoa học; K **đúng 5** câu hỏi, đáp án giải thích lập luận và lỗi hiểu thường gặp, có câu vận dụng và câu đánh giá bằng chứng; L mỗi nguồn một dòng `[S1] tác giả, tên, năm, ấn bản/DOI/URL, locator`. `[S1]` đặt sát khẳng định. Tiếng Việt có dấu; thuật ngữ tiếng Anh ở lần xuất hiện đầu. Có liên kết "đọc trước/đọc tiếp".

**Kịch bản slide** `j02-slides.json`, cùng lược đồ với `03-Carl-Gustav-Jung/moda/j01-slides.json`: khoá cấp cao `title`, `subtitle`, `status`, `review_status`, `visual_status`, `design_system`, `source_lesson`, `slides`, `canvas_ref`, `canvas_url`, `exports`, `presentation_status`, `production_notes`; mỗi slide có `title`, `section`, `body`, `nodes`, `layout`, `source`, `note`, `visual_brief`. 35–40 slide (không ép số nếu làm giảm chiều sâu), đi theo bài: bìa, lộ trình, các mục A–L, nguồn, kết. `body` là đoạn giải thích hiện trên slide, đủ ý; `nodes` là sơ đồ hỗ trợ, không rút nội dung thành nhãn rời. Không thêm ý không có trong bài. Layout lấy từ bộ đã dùng ở F01 v4 và J01 (cover, roadmap, lead, comparison, timeline, flow, mechanism, matrix, balance, ledger, example, dialogue, decision, takeaways, question, references, closing…).

Kết giai đoạn 1: commit, push, cập nhật `heartbeat_at`, chuyển sang giai đoạn 2 cùng phiên.

## 6. Giai đoạn 2 — Moda, PPTX/PDF

- **Chuẩn thiết kế:** F01 v4 đã duyệt. Canvas https://moda.app/canvas/53a95d71-d2f0-4013-ad6c-7d526ff19027?source=agent và `01-Sigmund-Freud/moda/f01-report-v4.json`; canvas của J01 (https://moda.app/canvas/6ee47b5e-532d-454e-b480-3f5cfc87fa7e?source=agent) là bản cùng tuyến. Đọc hai canvas làm tham chiếu, không sao chép nội dung.
- **Thông số:** trang 1920×1080; không brand kit (bỏ qua theo quyết định của chủ repo); chữ tiêu đề Bricolage Grotesque, chữ thân Be Vietnam Pro; Indigo `#493C89`, tím phụ `#6B59B5`, nền tối `#241F39`, giấy `#FAF8F4`, tím nhạt `#C8BDEE`, icon `#8874BF`; tiêu đề mục A–L có emoji 🎯 🕰️ 🧠 ⚙️ 💬 📋 🔬 🧭 🗺️ 💡 ❓ 📚; icon nét mảnh 56 px ở góc trên phải trang nội dung; sơ đồ dùng connector neo vào node, đường đứt và nhãn "giả thuyết" cho cơ chế chưa xác nhận.
- **Ảnh tư liệu:** chỉ ảnh có nguồn và quyền kiểm được (ưu tiên Wikimedia Commons miền công cộng); credit ngay trên trang dùng; `fit=contain`, không cắt; ảnh chưa rõ quyền thì bỏ, ghi vào `excluded_assets`. Không dùng ảnh người thật làm đại diện cho ca giả định. Ghi tất cả vào `j02-visual-sources.md`.
- **Trình tự (ít lệnh nhất):** `moda_bootstrap` một lần; nạp skill markup đúng theo catalog; `canvas_search` "J02"; tạo canvas với toàn bộ trang; ghi `canvas_url` vào front matter, push; chụp tất cả trang theo nhóm ba trang một lệnh, sửa **một lần**; xuất **PPTX và PDF** (không PNG); thử tải vào `03-Carl-Gustav-Jung/visuals/` đúng một lần, bị chặn thì ghi lý do và dừng, không tạo file giả.
- **Ghi lại:** `j02-report-v1.json`, `j02-visual-sources.md`; cập nhật mục I của bài (link canvas, PPTX, PDF, metadata, nguồn ảnh), `visual_status` (`exported` / `canvas-only` / `blocked`) trong bài, và `canvas_url`, `exports`, `presentation_status` trong `j02-slides.json`. Cảnh báo xuất (ví dụ trang PDF bị rasterize) ghi nguyên văn.
- Không dựng thêm canvas hay bản xuất khi đã có bản đúng; lỗi công cụ thì ghi `blocked` cùng nguyên nhân, không giả làm đã xong.

## 7. Kiểm trước khi báo xong (chạy một lần)

- Bài đủ A–L; ít nhất 3 ví dụ và 1 ca có phân tích; 5–10 điểm ghi nhớ; đúng 5 câu hỏi có giải thích; mọi khẳng định chính có `[S#]` truy được tới mục L; không có trích dẫn, trang hay số liệu chưa kiểm.
- Trạng thái trung thực: `status: drafted`, `review_status: pending` (không tự ghi đã review), `visual_status` đúng thực tế. Không viết "complete".
- Mọi file JSON đọc được bằng `python3 -m json.tool`; mọi liên kết tương đối tới file có thật.
- Phạm vi: `git diff --name-only origin/psychology/batch-02-three-decks...HEAD` chỉ gồm file ở mục 4 (cộng `COORDINATION.md` từ commit điều phối); `git diff --check` sạch.
- `python3 -m unittest discover -s tests` và `python3 scripts/claims.py check --merge-ready` thoát 0 (CI chạy hai lệnh này).

## 8. Báo cáo cuối (một lần, đúng khuôn)

```text
J02 — status: drafted · review: pending · visual: <exported|canvas-only|blocked>
Nhánh/commit: <nhánh> @ <sha>
File: <danh sách đường dẫn>
Slide: <số> · Canvas: <URL> · PPTX: <URL> · PDF: <URL> · cảnh báo xuất: <nguyên văn hoặc không>
Nguồn: <số nguồn> · full-text <n> / abstract <n> / metadata <n> · claim phải thu hẹp: <danh sách>
Hạn chế và việc còn mở: <ngắn>
Câu hỏi cho chủ repo (tối đa một): <hoặc không>
```

## Nhật ký (chủ bài ghi, mỗi dòng một mốc)

- 2026-10-24 — điều phối giao bài; chưa ai nhận.
- 2026-10-24T07:10:00Z — Claude (phiên điều phối) nhận bài theo lời chủ repo; sub-agent viết giai đoạn 1, Moda giai đoạn 2 do phiên điều phối dựng. Không giao lại.
- 2026-10-24T07:26:01Z — Claude trả quyền chủ bài về Codex theo lời chủ repo (Claude không tự viết); sub-agent của Claude đã dừng trước khi ghi file nào. Yêu cầu giao Codex gửi bằng một comment trên PR.

- 2026-10-24T15:15:45Z — Phiên có Moda tiếp nhận sau khi task Cloud đã kết thúc nhưng output chưa xuất bản (nhánh không có lesson/script). Không có canvas riêng của bài; kết quả search chỉ trúng bài trước do nhắc mã bài tiếp. Tiếp tục đúng PR/branch theo yêu cầu người dùng tạo PPT còn thiếu; nghiên cứu và ghi bản nội dung thực sự truy cập được, không nhận đã khôi phục commit Cloud thất lạc.

- 2026-10-24 15:35:06 UTC — Bàn giao36slide, canvas/PPTX/PDF thật, đã xem36/36render và sửa một vòng. Metadata/credits/lessonI/script cập nhật; local binary chưa tải theo chỉ dẫn điều phối, không xin quyền mạng. Review học thuật chờ điều phối.

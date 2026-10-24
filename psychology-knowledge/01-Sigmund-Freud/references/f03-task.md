---
task_id: PSY-LESSON-F03-V1
lesson: F03
status: giao
claimed_by: null
claimed_at: null
heartbeat_at: null
requested_from: Codex (yêu cầu comment trên PR của bài; task PSY-LESSON-F03-V1 vòng 1)
requested_at: 2026-10-24T07:26:01Z
canvas_url: null
branch: psychology/lesson-f03
base: psychology/batch-02-three-decks
assigned: 2026-10-24
---
# Lệnh giao việc F03 — Id, Ego và Superego

Hợp đồng giao việc cho **một** phiên thực thi (Codex; nếu dùng sub-agent thì mỗi bài một sub-agent), do phiên điều phối (Claude) soạn ngày 2026-10-24. Sổ chung: [COORDINATION.md](../../COORDINATION.md), mục "Batch 3". Chủ repo cho phép Codex viết bài và dùng Moda trong phạm vi bài này (ngoại lệ batch 3 so với quy trình "Codex chỉ review"); không mở rộng sang bài khác.

## 1. Nhận bài và chống trùng (làm đúng thứ tự, không hỏi ai)

1. `git fetch origin`. Làm việc trong worktree riêng của nhánh `psychology/lesson-f03` (PR nháp đã có sẵn, base `psychology/batch-02-three-decks`). Kiểm: `git branch -r | grep -i f03` chỉ ra đúng `origin/psychology/lesson-f03`, và không có PR nào khác mang mã F03 trong tiêu đề. Thấy khác đi thì dừng và báo.
2. Đọc front matter ở đầu file này. `status: giao` thì bạn nhận được. `status: đang làm` bởi chủ khác mà `heartbeat_at` chưa quá 24 giờ thì **dừng và báo**, không đoạt bài.
3. Sửa front matter: `status: đang làm`, `claimed_by` (tên agent hoặc phiên), `claimed_at` và `heartbeat_at` (UTC, dạng `2026-10-24T08:00:00Z`). Commit `claim: F03` và **push trước khi viết**.
4. Mỗi lần push về sau cập nhật `heartbeat_at`. Khi chuyển giai đoạn hoặc xong, đổi `status` (`chờ phản biện` khi đã push đủ).
5. Moda: `canvas_search` theo "F03" trước khi dựng. Thấy canvas của chính bài này thì dùng tiếp; không dựng canvas thứ hai. Tạo xong ghi ngay `canvas_url` vào front matter và push.
6. Không đụng F02, A01, J01 (đã xong ở PR #38) hay bài nào khác. Không tạo nhánh, PR hay canvas thứ hai cho F03.

## 2. Luật tự chủ (áp dụng cho phiên chính và mọi sub-agent)

- Chủ repo đã cho phép trước: nghiên cứu web, viết các file ở mục 4, Moda, commit và push lên đúng nhánh `psychology/lesson-f03`. Không xin xác nhận từng bước.
- Không xin nâng quyền hay duyệt mạng. Lệnh nào bị sandbox chặn (tải file, mạng ngoài) thì ghi hạn chế vào metadata, **không chờ duyệt**, làm tiếp, không thử lại quá một lần.
- Hỏi chủ repo **tối đa một lần cho cả bài**, gộp mọi vấn đề vào một câu, và chỉ khi (a) quyết định nội dung vượt phạm vi mục 3, hoặc (b) công cụ từ chối mà không có đường khác. Sau câu hỏi vẫn làm tiếp phần không bị chặn.
- Gộp lệnh: đọc nhiều file trong một lệnh, ghi mỗi file một lần, dựng deck bằng ít lệnh Moda nhất; chụp màn hình mỗi trang tối đa một lần ở bản cuối (ba trang một lệnh chụp).
- Sub-agent không dùng git, không gọi sub-agent con, không ghi ngoài mục 4. Phiên chính commit và push.
- Không bịa nguồn, số liệu, trang, ngày hay câu trích. Thiếu thì thu hẹp claim, ghi `chưa đánh giá` và giới hạn. Không tự xin review, không đánh dấu PR sẵn sàng, không merge: điều phối làm.

## 3. Phạm vi bài

**Dòng curriculum:** Hiểu mô hình cấu trúc; ego không đồng nghĩa ý thức và các cấu trúc không phải vùng não. Ý tưởng hình: *hai mô hình giao nhau*.

**Đọc trước:** [F02](../lessons/02-conscious-preconscious-unconscious.md). Mục C của F02 đã hứa rằng F03 sẽ trả lời vì sao không ghép "conscious = ego, unconscious = id". **Đọc tiếp:** F04 (Pleasure Principle và Reality Principle) và F05 (xung đột nội tâm, cơ chế phòng vệ). F03 chỉ nối tới hai bài này, không giải trước.

**Trọng tâm cần dạy**

1. Mô hình cấu trúc (structural model) với id (*das Es*), ego (*das Ich*), superego (*das Über-Ich*): chức năng và quan hệ mà mô hình gán; ego đối diện đòi hỏi từ id, từ superego và từ thực tại bên ngoài.
2. Vì sao có thêm mô hình cấu trúc sau mô hình địa hình ở F02. Chỉ nêu lý do có trong văn bản đã đọc (*The Ego and the Id*, 1923).
3. Superego và ego-ideal: nguồn gốc giả định, vai trò trong mô hình, khác "lương tâm" theo nghĩa thông thường.
4. Đặt hai mô hình cạnh nhau: ba cấu trúc và ba miền truy cập (F02) **cắt chéo**, không thành bảng một–một.

**Phải phân biệt:** id ≠ "ham muốn xấu"; ego Freud ≠ "cái tôi" theo nghĩa tự trọng hay kiêu ngạo; superego ≠ mọi cảm giác tội lỗi; khái niệm của mô hình ≠ vùng não; thuật ngữ Đức gốc và bản dịch La-tinh *ego/id/superego* (chỉ viết về chuyện dịch thuật nếu đọc được nguồn bàn đúng điều đó, không thì bỏ).

**Giới hạn bắt buộc (ngoài STANDARDS):** không gán id/ego/superego vào vùng não; đối chiếu thần kinh–phân tâm chỉ là giả thuyết đối chiếu, không xác nhận mô hình; tương đồng với chức năng điều hành, xử lý hai hệ hay tự kiểm soát là loại suy có giới hạn, không đồng nhất; không dùng "ego yếu", "superego khắt khe" làm nhãn chẩn đoán về một người; ví dụ và ca là giả định, nêu giải thích thay thế không dùng khung Freud.

**Nguồn gợi ý (tự kiểm tra tồn tại, ấn bản và trang trước khi dùng; không phải nguồn đã đọc):**
- Freud, S. (1923), *Das Ich und das Es*; bản Anh *The Ego and the Id*, Standard Edition tập 19. Đã có mục F-SRC01 trong [sources.md](sources.md), mới ở mức metadata: chọn đúng bản dịch, đọc và ghi trang.
- Freud, S. (1933), *New Introductory Lectures on Psycho-Analysis*, bài giảng XXXI "The Dissection of the Psychical Personality", Standard Edition tập 22.
- Carhart-Harris, R. L. & Friston, K. J. (2010), "The default-mode, ego-functions and free-energy: a neurobiological account of Freudian ideas", *Brain* 133(4). Dùng làm ví dụ đối chiếu thần kinh–phân tâm: đọc phạm vi mà bài đề xuất, không trình bày như xác nhận mô hình.
- Bettelheim, B. (1983), *Freud and Man's Soul*: phê bình bản dịch; chỉ dùng nếu đọc được đoạn thích hợp.
- Nguồn đã dùng ở F02 (S1–S7, xem [f02-research.md](f02-research.md)) khi nhắc lại mô hình địa hình.

**Ví dụ gợi ý (viết lại, có phân tích và giải thích thay thế):** một người định nhắn tin riêng trong cuộc họp; mua sắm bốc đồng rồi áy náy; chọn nói thẳng hay giữ lịch sự với đồng nghiệp. Ca giả định phức tạp hơn do bạn thiết kế, không phải ca công bố.

## 4. Sản phẩm và quyền ghi

Chỉ ghi các file sau (thư mục tác giả `01-Sigmund-Freud`). `COORDINATION.md` và mọi file dùng chung ở gốc `psychology-knowledge/` chỉ điều phối sửa.

| File | Nội dung | Giai đoạn |
|---|---|---|
| `01-Sigmund-Freud/lessons/03-id-ego-superego.md` | Bài đủ A–L; front matter `id`, `title`, `topic: khac`, `date` (ngày sửa thực tế), `status: drafted`, `review_status: pending`, `visual_status` | 1 |
| `01-Sigmund-Freud/references/f03-research.md` | Search log (truy vấn, ngày, tiêu chí chọn), bảng trạng thái nguồn và locator, claim ledger với Claim ID `F03-C01…` | 1 |
| `01-Sigmund-Freud/moda/f03-slides.json` | Kịch bản 35–40 slide | 1 |
| `01-Sigmund-Freud/references/f03-visual-sources.md` | Nguồn, credit, mức kiểm quyền của từng ảnh | 2 |
| `01-Sigmund-Freud/moda/f03-report-v1.json` | Metadata Moda: canvas, trang, markup, tài nguyên, kiểm tra, link xuất, cảnh báo, giới hạn; cùng khoá với `01-Sigmund-Freud/moda/f02-report-v1.json` | 2 |
| `01-Sigmund-Freud/visuals/` | PPTX/PDF chỉ khi tải về thật sự thành công; không tạo file giả | 2 |
| file lệnh này | Chỉ front matter và mục "Nhật ký" ở cuối | 1–2 |
| `01-Sigmund-Freud/README.md` | Tuỳ chọn: thêm đúng một dòng liên kết tới bài khi file bài đã tồn tại | 1 |

## 5. Giai đoạn 1 — nghiên cứu, viết bài, kịch bản slide

**Đọc trước (một lượt):** `psychology-knowledge/STANDARDS.md`, `DESIGN-SYSTEM.md`, dòng của F03 trong `PROGRAM.md` và `01-Sigmund-Freud/curriculum.md`, `01-Sigmund-Freud/references/sources.md`, bài mẫu F01 (đã được chủ repo duyệt) và F02 (cùng tuyến, cùng chuẩn) làm mẫu về độ sâu và giọng văn. Không sao chép nội dung bài khác.

**Nghiên cứu:** dùng web thật; ưu tiên văn bản gốc, rồi nghiên cứu peer-reviewed, review/meta-analysis, sách học thuật; tìm cả nguồn trái chiều. Ghi mức truy cập thực tế của từng nguồn (`metadata-verified`, `abstract-read`, `full-text-read`, `locator-verified`) và không nâng mức khi chưa đọc. Điền claim ledger cho mỗi khẳng định quan trọng trước khi chốt bài.

**Bài học:** `## Lưu ý` (tài liệu giáo dục, không tự chẩn đoán) trước mục A; rồi A–L đúng STANDARDS: A mục tiêu quan sát được; B bối cảnh và năm tác phẩm gốc; C lý thuyết cốt lõi và điều khái niệm không cho phép suy ra; D cơ chế từng bước, gắn nhãn mô hình đề xuất; E **ít nhất ba** ví dụ từ đơn giản đến phức tạp, mỗi ví dụ có phân tích và giải thích thay thế; F **một** ca giả định phân tích từng bước (ghi rõ giả định, điều còn thiếu, cách kiểm tra); G bằng chứng hỗ trợ **và** trái chiều, thiết kế nghiên cứu, giới hạn đo lường; H ứng dụng có điều kiện; I mô tả hình, caption, alt text và nguồn (chưa có canvas thì `visual_status: not-started`, không link giả); J 5–10 điểm ghi nhớ gồm cả giới hạn khoa học; K **đúng 5** câu hỏi, đáp án giải thích lập luận và lỗi hiểu thường gặp, có câu vận dụng và câu đánh giá bằng chứng; L mỗi nguồn một dòng `[S1] tác giả, tên, năm, ấn bản/DOI/URL, locator`. `[S1]` đặt sát khẳng định. Tiếng Việt có dấu; thuật ngữ tiếng Anh ở lần xuất hiện đầu. Có liên kết "đọc trước/đọc tiếp".

**Kịch bản slide** `f03-slides.json`, cùng lược đồ với `01-Sigmund-Freud/moda/f02-slides.json`: khoá cấp cao `title`, `subtitle`, `status`, `review_status`, `visual_status`, `design_system`, `source_lesson`, `slides`, `canvas_ref`, `canvas_url`, `exports`, `presentation_status`, `production_notes`; mỗi slide có `title`, `section`, `body`, `nodes`, `layout`, `source`, `note`, `visual_brief`. 35–40 slide (không ép số nếu làm giảm chiều sâu), đi theo bài: bìa, lộ trình, các mục A–L, nguồn, kết. `body` là đoạn giải thích hiện trên slide, đủ ý; `nodes` là sơ đồ hỗ trợ, không rút nội dung thành nhãn rời. Không thêm ý không có trong bài. Layout lấy từ bộ đã dùng ở F01 v4 và F02 (cover, roadmap, lead, comparison, timeline, flow, mechanism, matrix, balance, ledger, example, dialogue, decision, takeaways, question, references, closing…).

Kết giai đoạn 1: commit, push, cập nhật `heartbeat_at`, chuyển sang giai đoạn 2 cùng phiên.

## 6. Giai đoạn 2 — Moda, PPTX/PDF

- **Chuẩn thiết kế:** F01 v4 đã duyệt. Canvas https://moda.app/canvas/53a95d71-d2f0-4013-ad6c-7d526ff19027?source=agent và `01-Sigmund-Freud/moda/f01-report-v4.json`; canvas của F02 (https://moda.app/canvas/6fc130f8-596c-4446-b9f8-3aaceb1bc64b?source=agent) là bản cùng tuyến. Đọc hai canvas làm tham chiếu, không sao chép nội dung.
- **Thông số:** trang 1920×1080; không brand kit (bỏ qua theo quyết định của chủ repo); chữ tiêu đề Bricolage Grotesque, chữ thân Be Vietnam Pro; Burgundy `#7A2038`, nền tối `#23191F`, giấy `#F5F0E6`, hồng nhạt `#EADDE0`, icon `#B56D84`; tiêu đề mục A–L có emoji 🎯 🕰️ 🧠 ⚙️ 💬 📋 🔬 🧭 🗺️ 💡 ❓ 📚; icon nét mảnh 56 px ở góc trên phải trang nội dung; sơ đồ dùng connector neo vào node, đường đứt và nhãn "giả thuyết" cho cơ chế chưa xác nhận.
- **Ảnh tư liệu:** chỉ ảnh có nguồn và quyền kiểm được (ưu tiên Wikimedia Commons miền công cộng); credit ngay trên trang dùng; `fit=contain`, không cắt; ảnh chưa rõ quyền thì bỏ, ghi vào `excluded_assets`. Không dùng ảnh người thật làm đại diện cho ca giả định. Ghi tất cả vào `f03-visual-sources.md`.
- **Trình tự (ít lệnh nhất):** `moda_bootstrap` một lần; nạp skill markup đúng theo catalog; `canvas_search` "F03"; tạo canvas với toàn bộ trang; ghi `canvas_url` vào front matter, push; chụp tất cả trang theo nhóm ba trang một lệnh, sửa **một lần**; xuất **PPTX và PDF** (không PNG); thử tải vào `01-Sigmund-Freud/visuals/` đúng một lần, bị chặn thì ghi lý do và dừng, không tạo file giả.
- **Ghi lại:** `f03-report-v1.json`, `f03-visual-sources.md`; cập nhật mục I của bài (link canvas, PPTX, PDF, metadata, nguồn ảnh), `visual_status` (`exported` / `canvas-only` / `blocked`) trong bài, và `canvas_url`, `exports`, `presentation_status` trong `f03-slides.json`. Cảnh báo xuất (ví dụ trang PDF bị rasterize) ghi nguyên văn.
- Không dựng thêm canvas hay bản xuất khi đã có bản đúng; lỗi công cụ thì ghi `blocked` cùng nguyên nhân, không giả làm đã xong.

## 7. Kiểm trước khi báo xong (chạy một lần)

- Bài đủ A–L; ít nhất 3 ví dụ và 1 ca có phân tích; 5–10 điểm ghi nhớ; đúng 5 câu hỏi có giải thích; mọi khẳng định chính có `[S#]` truy được tới mục L; không có trích dẫn, trang hay số liệu chưa kiểm.
- Trạng thái trung thực: `status: drafted`, `review_status: pending` (không tự ghi đã review), `visual_status` đúng thực tế. Không viết "complete".
- Mọi file JSON đọc được bằng `python3 -m json.tool`; mọi liên kết tương đối tới file có thật.
- Phạm vi: `git diff --name-only origin/psychology/batch-02-three-decks...HEAD` chỉ gồm file ở mục 4 (cộng `COORDINATION.md` từ commit điều phối); `git diff --check` sạch.
- `python3 -m unittest discover -s tests` và `python3 scripts/claims.py check --merge-ready` thoát 0 (CI chạy hai lệnh này).

## 8. Báo cáo cuối (một lần, đúng khuôn)

```text
F03 — status: drafted · review: pending · visual: <exported|canvas-only|blocked>
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

# Biên bản bàn giao: đào sâu bộ "Bộ não và tâm lý"

Gửi: phiên Claude **điều phối** (orchestrator) sẽ tiếp quản. Ngày lập: 2026-10-20. Người lập: phiên Claude đã dựng L01–L06.
Đọc kèm: `CLAUDE.md` (luật repo), `docs/ke-hoach-nao-bo-tam-ly.md` (kế hoạch gốc), `docs/deck-style.md` (phong cách deck).

## 1. Yêu cầu của chủ repo

Chủ repo (nói tiếng Việt) nhận xét: **nội dung các slide hiện tại hơi sơ sài**. Họ muốn:

1. Phân tích kỹ hơn **vai trò của từng bộ phận não**.
2. Phân tích kỹ hơn **các chất dẫn truyền thần kinh chi phối cảm xúc**.
3. Cho phép **nhiều chữ hơn trên một slide, hoặc nhiều slide hơn** (đã nói từ trước: không giới hạn số từ, slide nhiều cũng được, miễn dễ hiểu).
4. Một phiên Claude khác (bạn) **điều phối nhiều phiên Claude cùng viết bài**.

Các yêu cầu cũ vẫn còn hiệu lực: tiếng Việt, có nguồn, dễ hiểu, có hình minh họa từ sách miễn phí, mỗi bài một deck PowerPoint
dựng bằng Moda.

## 2. Hiện trạng (đã push, chưa có PR)

- Repo `vohoailinh90/Multiple-report`. Nhánh làm việc `claude/dreamy-johnson-xy3y2y` (commit `d8c9857` trở lên); `main` chưa có
  L01–L06 bản có hình. Chưa tạo PR. Việc đầu tiên của bạn: tạo nhánh của mình từ nhánh này hoặc hỏi chủ repo có merge không.
  *Cập nhật 2026-10-20:* nhánh điều phối là `claude/orchestrate-brain-series` (tách từ nhánh trên); chủ repo chọn **một PR vào `main` sau
  giai đoạn 1** (mục 11).
- 7 bài: `L00` (dopamine, bài mẫu cũ) và `L01`–`L06`. Mỗi bài có `lesson.md`, `slides.json`, `Lxx.pptx`, `deck.json`, `images/`.
- Công cụ đã chuyển vào repo ở `scripts/deckgen/` (trước đó nằm ngoài repo, sẽ mất): `gen.py` (sinh markup Moda từ `slides.json`),
  `check_lesson.py` (gate cấu trúc thay cho `lesson_gates.py` của repo template), `mk.py` (viết `slides.json` + `expected.json`),
  `opts/Lxx.json` (tuỳ chọn trang bìa, số lớn, tác nhân từng bài), `file_ids.json` (id ảnh đã tải lên Moda; nếu hết hạn thì tải lại).
- Số đo "sơ sài" (tính từ `slides.json` hiện tại):

| Bài | Slide | Gạch/slide | Chữ/gạch | Chữ `notes`/slide | Chữ `lesson.md` |
|---|---|---|---|---|---|
| L00 | 10 | 3,1 | 9,3 | 24 | 1.072 |
| L01 | 13 | 3,3 | 6,5 | 25 | 1.323 |
| L02 | 18 | 3,2 | 6,1 | 18 | 1.531 |
| L03 | 17 | 2,7 | 6,5 | 17 | 1.607 |
| L04 | 19 | 2,8 | 6,9 | 18 | 1.824 |
| L05 | 18 | 2,9 | 6,3 | 23 | 1.612 |
| L06 | 18 | 2,8 | 7,6 | 23 | 2.072 |

Ví dụ cụ thể: slide "Glutamate và GABA" (L03) chỉ có ba gạch ngắn và một dòng `notes`; dopamine, serotonin, noradrenaline mỗi chất
chiếm một slide ba gạch. Không có slide nào nói chất đó **được tạo ở đâu, đi theo đường nào, gắn vào thụ thể nào, làm gì ở từng vùng,
thuốc nào tác động, rối loạn nào liên quan**. Tương tự, mỗi bộ phận não (hạnh nhân, hải mã, đồi thị, vùng dưới đồi, hạch nền, đảo)
chỉ được nhắc một hai dòng trong L01. Nguyên nhân gốc: luật `CLAUDE.md` giới hạn gạch ≤ 160 ký tự, ≤ 6 gạch, "giải thích để trong
`notes`"; deck builder đọc gạch chứ không đọc `notes`, nên phần giải thích không bao giờ lên slide.

## 3. Mục tiêu chất lượng (đo được)

| Chỉ số | Hiện tại | Mục tiêu mỗi bài |
|---|---|---|
| Chữ trong `lesson.md` | 1.000–2.000 | **3.500–6.000** (bài tổng quan nhẹ có thể 3.000) |
| Slide | 10–19 | **30–50** |
| Mỗi mục `## ` | 1–2 slide | **≥ 3 slide** (định nghĩa, cơ chế, ví dụ/bằng chứng, hiểu lầm) |
| Chữ trên slide giải thích | ≤ 20 | **60–110 chữ** ở trường `body` |
| `notes` | một dòng | 80–200 chữ: lời giảng, ví dụ, chỗ dễ nhầm |
| Trích dẫn `[Sn]` | ≥ 5 | **≥ 12**, trong đó ≥ 4 nguồn gốc độc lập ngoài giáo trình |
| Hình | 1–3 | **≥ 4** mỗi bài khi có hình đủ giấy phép |

"Dễ hiểu" vẫn là ưu tiên một: mọi thuật ngữ kèm tiếng Anh ở lần đầu; mỗi đoạn một ý; ví dụ đời thường được ghi rõ
là "Ví dụ của người viết"; không kể một ý mà không nói nó **dùng để làm gì**.

## 4. Phạm vi nội dung

### 4.1 Thẻ hồ sơ bắt buộc

Mỗi **bộ phận não**, mỗi **chất dẫn truyền** và mỗi **cảm xúc** được viết theo một khung cố định (một đến ba slide, một mục `## `
hoặc tiểu mục `### `), để người đọc so sánh được:

- **Bộ phận:** (1) Ở đâu (vị trí, hình), (2) Gồm những phần nào, (3) Vai trò chính, có bằng chứng gì (người, động vật, bệnh nhân
  tổn thương, ảnh chụp não), (4) Kết nối với những vùng nào, (5) Chất dẫn truyền chính ở đó, (6) Điều gì xảy ra khi tổn thương
  hoặc rối loạn, (7) **Đừng hiểu nhầm** (ví dụ "hạnh nhân là trung tâm sợ hãi").
- **Chất dẫn truyền:** (1) Tên và loại hóa học, (2) Được tạo ở nhân nào, (3) Đường đi (nguồn → đích), (4) Các loại thụ thể và
  tác dụng kích thích/ức chế, (5) Vai trò theo từng vùng, (6) Liên hệ với cảm xúc/hành vi, mức bằng chứng, (7) Thuốc và chất tác
  động (rượu, caffeine, cần sa, opioid, thuốc điều trị), (8) Rối loạn liên quan, (9) **Đừng hiểu nhầm**.
- **Cảm xúc:** (1) Cảm xúc đó là gì (định nghĩa làm việc), (2) Mạch thần kinh chính, (3) Chất dẫn truyền và hormone liên quan,
  (4) Vai trò thích nghi, (5) Khi mất cân bằng, (6) Nó khác "cảm giác chủ quan" thế nào, (7) **Đừng hiểu nhầm**.

### 4.2 Gắn nhãn mức chắc chắn

Mỗi khẳng định về cơ chế thuộc một trong ba nhóm, và bài phải cho người đọc biết nhóm nào:
**giáo khoa** (nguồn đồng thuận), **giả thuyết/đang tranh luận** (có nguồn, nói rõ ai tranh luận), **suy luận của người viết**
(ghi "Suy luận của người viết", không gắn `[Sn]` như thể nguồn đã nói điều đó). Quy tắc có sẵn: "Ví dụ của người viết" cho ví dụ đời thường.
Không viết "một vùng, một cảm xúc" hay "một chất, một cảm xúc"; đã có bài L03 phản bác, đừng mâu thuẫn với nó.

### 4.3 Danh sách bài

Ghi chú về số hiệu: giữ nguyên `L00`–`L06` (đã có link, deck), bài mới đánh số tiếp từ `L07`. Thứ tự đọc khuyến nghị nằm ở bảng bên dưới,
cập nhật vào `docs/ke-hoach-nao-bo-tam-ly.md`. Mục lục `lessons/README.md` do `decks.py index` sinh (không sửa tay).

**Giai đoạn 1 (ưu tiên: đúng điều chủ repo vừa hỏi)**

| Thứ tự đọc | Bài | Việc | Nội dung chính | Chương giáo trình |
|---|---|---|---|---|
| 1 | L01 | **Viết lại** | Bản đồ tổng, hệ thần kinh trung ương/ngoại biên, hướng và mặt cắt, cách chụp não (rút gọn), **thân não** (cầu não, hành não, não giữa và các nhân nguồn chất dẫn truyền), **tiểu não** | 2.2–2.5, 2.6 (Brainstem, Cerebellum) |
| 2 | L02 | Giữ, đào sâu vừa phải ở giai đoạn 2 | nơron, xung, synapse | 3.2–3.4 |
| 3 | L07 | **Mới** | **Hệ viền và các nhân nằm sâu:** hạnh nhân, hải mã, đồi thị, vùng dưới đồi, hạch nền (nhân đuôi, bèo sẫm, nhân accumbens), đảo, vỏ vòng đai trước nếu giáo trình nêu. Mỗi bộ phận một thẻ hồ sơ | 2.6 (Limbic System, Basal Ganglia, Thalamus, Hypothalamus, Insula) |
| 4 | L03 | **Viết lại** | Chất dẫn truyền: mỗi chất một thẻ hồ sơ đầy đủ (glutamate, GABA, dopamine, serotonin, noradrenaline, acetylcholine, endorphin/opioid, **thêm oxytocin/vasopressin nếu có nguồn**); bản đồ nguồn → đích; thụ thể; thuốc; hiểu lầm | 5.5, 3.4, 12.3; NBK10795 (xem mục 5) |
| 5 | L09 | **Mới** | **Cảm xúc cơ bản và mạch thần kinh:** ham muốn (desire), thích (liking), sợ, giận, yêu thương/gắn bó, đau buồn/cô đơn; quy tắc "một cấu trúc nhiều chức năng"; kinh nghiệm làm đổi não | 10.1–10.4 |
| 6 | L10 | **Mới** | **Chất dẫn truyền và hormone × cảm xúc:** bảng ghép từng cảm xúc ↔ mạch ↔ chất ↔ hormone (cortisol, oxytocin, testosterone), nói rõ mức bằng chứng; chống hiểu lầm "hormone hạnh phúc" | 10.2, 6.4, 5.5 + nguồn gốc độc lập |
| 7 | L05 | **Viết lại** | Hệ thưởng, chú ý, căng thẳng (cảm xúc chi tiết chuyển sang L09, ở đây chỉ nhắc và dẫn) | 10.2, 8.3 (Amygdala), nguồn cũ |
| 8 | L04 | Giữ, đào sâu ở giai đoạn 2 | Thùy trán, bán cầu | 2.6 (Frontal Lobe) |
| 9 | L06 | Giữ, đào sâu ở giai đoạn 2 | Mạng xã hội | ngoài giáo trình |

**Giai đoạn 2:** đào sâu L02, L04, L06 (cùng thước đo mục 3) và viết **L08 Vỏ não và các thùy** (thùy thái dương, đỉnh, chẩm, đảo; L04 giữ phần
thùy trán và bán cầu, chỉ dẫn qua lại, không lặp).

**Giai đoạn 3 (hỏi chủ repo trước khi làm, xem mục 11):**
L11 Trí nhớ cảm xúc (hải mã, hạnh nhân, vỏ trước trán; Ch. 8), L12 Rối loạn tâm trạng, lo âu và PTSD ở mức cơ chế (Ch. 12; có `## Lưu ý` y tế),
L13 Thuốc và chất tác động lên chất dẫn truyền (rượu, caffeine, cần sa, opioid; 5.5; có `## Lưu ý`), L14 Não thay đổi theo tuổi và kinh nghiệm,
tuổi vị thành niên (Ch. 7; nối với L06).

### 4.4 Tránh lặp giữa các bài

Mỗi bài có một **chủ sở hữu** cho từng khái niệm; bài khác chỉ nhắc một dòng và dẫn "xem Lxx":

| Khái niệm | Bài sở hữu |
|---|---|
| nơron, xung điện, synapse, thụ thể | L02 |
| hạnh nhân, hải mã, đồi thị, vùng dưới đồi, hạch nền, đảo | L07 |
| từng chất dẫn truyền (hồ sơ đầy đủ) | L03 |
| từng cảm xúc cơ bản và mạch | L09 |
| ghép chất ↔ cảm xúc ↔ hormone | L10 |
| hệ thưởng, chú ý, căng thẳng | L05 (dopamine gốc ở L00) |
| vỏ não trước trán, bán cầu | L04 |

## 5. Nguồn

- **Giáo trình nền:** *Biological Psychology* (Hove & Martinez, CC BY-NC-SA 4.0), `https://rotel.pressbooks.pub/biologicalpsychology/`.
  Mục lục thật (đã đối chiếu 2026-10-20): Ch.1 Giới thiệu; Ch.2 Não và hệ thần kinh (2.2 hình ảnh, 2.3–2.5 hệ thần kinh, 2.6 Não: vỏ não, thùy trán,
  thái dương, đỉnh, chẩm, đảo, hệ viền, hạch nền, đồi thị, vùng dưới đồi, tiểu não, thân não); Ch.3 Nơron; Ch.4 Phương pháp; Ch.5 Dược lý tâm thần
  (5.5 thuốc tác động chất dẫn truyền: rượu, caffeine, cần sa, opioid); Ch.6 Hormone và hành vi; Ch.7 Phát triển não; Ch.8 Trí nhớ; Ch.9 Di truyền
  và biểu sinh; Ch.10 Cảm xúc (10.2: desire, liking, fear, rage, love, grief); Ch.11 Rối loạn thần kinh; Ch.12 Rối loạn tâm lý (12.3 tâm trạng,
  12.4 lo âu, 12.6 PTSD).
  Đường dẫn dạng `…/chapter/<slug>/`: `the-brain/`, `the-nervous-system/`, `communication-within-and-between-neurons/`, `how-drugs-affect-neurotransmitters/`,
  `basic-emotions/`, `parental-behaviors/` (6.4), `brain-structures-have-multiple-functions/` (10.4), `mood-disorders-depression-and-bipolar-disorder/`,
  `anxiety/`, `post-traumatic-stress-disorder/`, `8-3-brain-structures-in-memory/`.
  **Đây là giáo trình có sẵn trên mạng: phải đọc chương thật rồi mới viết, không viết từ trí nhớ.** Thẻ hình của sách ghi giấy phép riêng trong mục *Media Attributions*.
- **Nguồn gốc độc lập đã dùng trong repo** (tái sử dụng được, xem `## Nguồn tham khảo` trong từng `lesson.md`): Schultz 1997; Berridge & Robinson 1998; LeDoux 2000;
  McEwen 2007; Corbetta & Shulman 2002; Miller & Cohen 2001; NBK10795 (*Neuroscience*, Purves, NCBI Bookshelf); NINDS Know Your Brain; SfN Brain Facts 2018;
  Moncrieff và cộng sự 2022 (umbrella review serotonin, doi 10.1038/s41380-022-01661-0).
- **Gợi ý nguồn mới, phải tự kiểm DOI/URL và nội dung trước khi dùng, không bịa:** Panksepp, *Affective Neuroscience* (1998; nền của Ch.10.2);
  Berridge & Kringelbach 2015 về hệ thống khoái cảm (Neuron); Insel & Young 2001 về gắn bó và oxytocin (Nat Rev Neurosci);
  các chương Purves về chất dẫn truyền trong NBK10795 (nhân raphe, locus coeruleus, vùng mái bụng, liềm đen, nhân nền não trước).
  Nếu không kiểm được, viết ý đó **không kèm số liệu** và không gắn `[Sn]`.
- Mỗi nguồn một dòng `- [S1] tác giả, tên, năm, URL` (luật `CLAUDE.md`). Số liệu, năm, tên nghiên cứu, câu trích: không bịa.

## 6. Việc phải làm trước khi cho các phiên viết bắt đầu (Giai đoạn 0, do điều phối làm)

Luật hiện hành chặn nội dung dày, nên sửa luật trước, nếu không các phiên viết sẽ viết đúng luật cũ và lại sơ sài.

1. **`CLAUDE.md`:** thêm quy định cho trường `body` trong `slides.json` (xem 6.1). Sửa câu "Gạch đầu dòng là cụm từ ngắn ... phần giải thích để trong `notes`" thành:
   slide giải thích dùng `body` 60–110 chữ; slide sơ đồ vẫn dùng gạch ngắn.
2. **`slides.json`:** thêm hai trường tuỳ chọn: `body` (chuỗi, 60–110 chữ) và `facts` (mảng ≤ 6 cặp `{"label","text"}` cho `profile-card`).
3. **`scripts/deckgen/gen.py`:** viết ba layout mới (6.2). Cần chạy thử trên **một** canvas Moda và xem ảnh chụp trước khi giao cho đợt viết.
4. **`scripts/deckgen/check_lesson.py`:** nới `bullets` ≤ 160 ký tự cho layout cũ; layout mới kiểm `body` trong khoảng 40–130 chữ, `facts` ≤ 6; cảnh báo nếu slide
   giải thích không có `body`.
5. **`expected.json`:** `slides.max` nâng lên 60; `min_words` theo mục 3; `min_citations` 12. (File này của "tester": hiện tại phiên trước tự viết thay vai tester vì chưa có
   model VPS. Chủ repo biết điều đó; nêu lại khi báo cáo.)
6. **Gate của repo template:** `lesson_gates.py` nằm ở repo `claude-agent-routing-template`, nằm ngoài phạm vi truy cập của phiên này. Kiểm xem nó có giới hạn slide/độ dài không;
   nếu có, báo chủ repo.
   *Đã kiểm 2026-10-20 (bản `f80c4cc`):* có giới hạn. Nó chỉ nhận 7 trường slide (`title, bullets, notes, section, sources, layout, tone`), nên `images`, `body`, `facts`
   bị từ chối; chỉ nhận 12 layout (không có `figure` và 4 layout mới); `bullets` phải có ít nhất một gạch; khóa lạ trong `expected.json` bị từ chối (mã 3);
   `slides.max` mặc định 20; `sources` là danh sách cố định. Hệ quả: L01–L06 có hình đã không qua gate đó, và bài đào sâu cũng vậy. Repo này không sửa repo template;
   chủ repo quyết định có cập nhật nó không. Gate dùng ở đây là `scripts/deckgen/check_lesson.py` (có test).
7. Cập nhật `docs/deck-style.md` (bảng layout, cỡ chữ tối thiểu cho `body` là 30 chứ không phải 34–40).

### 6.1 Ví dụ slide giải thích

```json
{
  "title": "Hạnh nhân: bộ phận gắn nhãn 'đáng chú ý về cảm xúc'",
  "section": "Hạnh nhân",
  "sources": ["S1", "S5"],
  "layout": "explainer",
  "tone": "light",
  "body": "Hạnh nhân (amygdala) là hai khối nhỏ hình quả hạnh nằm sâu trong thùy thái dương, mỗi bên não một khối. ... (60–110 chữ, có [Sn] ở cuối câu)",
  "bullets": ["Ở đâu: sâu trong thùy thái dương", "Vai trò chính: ...", "Đừng hiểu nhầm: không phải 'trung tâm sợ hãi' duy nhất"],
  "notes": "Lời giảng 80–200 chữ ..."
}
```

### 6.2 Ba layout mới (bên cạnh 13 layout hiện có)

| layout | Vẽ thế nào |
|---|---|
| `explainer` | cột trái 60–70% chiều rộng là `body` (cỡ 30, giãn dòng 1,3, từ khoá tô màu khái niệm), cột phải 2–3 thẻ nhỏ "Ở đâu / Làm gì / Đừng hiểu nhầm" lấy từ `bullets` |
| `profile-card` | lưới 2×3 thẻ lấy từ `facts` (nhãn màu khái niệm, chữ ≥ 28), tiêu đề là tên bộ phận/chất; dùng cho thẻ hồ sơ mục 4.1 |
| `annotated-figure` | như `figure` nhưng thêm một khối `body` 40–70 chữ dưới hình hoặc thay một thẻ chú giải |
| `references` | *(thêm 2026-10-20)* slide nguồn: 1 cột đến 6 nguồn, 2 cột đến 18; mỗi gạch `S1: tên rút gọn` ≤ 110 ký tự. Bài ≥ 12 nguồn không nhét vừa `lookup-table` |

Ba layout này không được dùng hai lần liền nhau (gate vẫn cấm hai slide liền cùng kiểu); xen với `card-grid`, `flow`, `two-column-comparison`, `layers`, `figure`.
Một bài 40 slide cần đủ ≥ 8 kiểu để đỡ đơn điệu.

## 7. Phân công và quy trình đa phiên

### 7.1 Vai trò

| Vai | Số phiên | Làm gì | Không làm |
|---|---|---|---|
| **Điều phối** (bạn) | 1 | Giai đoạn 0; viết `lessons/Lxx.spec.md` cho từng bài (mục 7.2); giao việc; gộp nhánh; chạy gate; dựng deck; báo cáo | Không tự viết bài hàng loạt |
| **Phiên viết** | 1 phiên mỗi bài, chạy song song theo giai đoạn | Đọc chương giáo trình thật, tìm nguồn gốc, viết `lesson.md` rồi `slides.json`, tải hình (nếu có), chạy `check_lesson.py` | Không đụng bài khác, không sửa `expected.json`, không dùng Moda, không sửa `lessons/README.md` |
| **Phiên phản biện** | 2 mỗi bài (chỉ đọc) | (a) Kiểm chứng: đối chiếu từng khẳng định và số liệu với chương/nguồn thật, đánh dấu bịa, thổi phồng, hiểu sai, thiếu `[Sn]`, nhầm nhãn "giáo khoa/giả thuyết/suy luận". (b) Sư phạm và định dạng: dễ hiểu, thuật ngữ nhất quán, không lặp bài khác (bảng 4.4), `slides.json` khớp `lesson.md` | Không sửa file; chỉ trả danh sách lỗi có vị trí |
| **Phiên sửa** | có thể là chính phiên viết | Xử lý từng lỗi: sửa, hoặc ghi lý do không sửa | |
| **Dựng deck** | chính phiên điều phối, tuần tự | Mục 9 | **Không giao Moda cho subagent** (CLAUDE.md: mỗi lệnh Moda của subagent phải chờ chủ repo duyệt) |

Dùng `mcp__claude-code-remote__create_session` (có `source_url`, `prompt`, `title`) để tạo phiên viết. Mỗi phiên viết có nhánh riêng; vì các bài ở
thư mục riêng nên gộp không xung đột. Tệp dùng chung (`lessons/README.md`, `docs/*`, `scripts/*`) **chỉ điều phối sửa**.

### 7.2 Spec mỗi bài (điều phối viết trước khi giao)

`lessons/Lxx.spec.md` (không phải `expected.json`; file mới, nhỏ) gồm: tiêu đề và `topic`; danh sách mục `## ` (tên chính xác, để làm `sections` trong `expected.json`);
mục tiêu chữ/slide; thẻ hồ sơ nào phải có (mục 4.1) và bộ phận/chất/cảm xúc nào thuộc bài này (mục 4.4); URL chương giáo trình phải đọc; nguồn gốc gợi ý (đánh dấu "phải kiểm");
khái niệm bài khác sở hữu (chỉ được dẫn); `key_terms`; có cần `## Lưu ý` y tế không; ý tưởng hình ảnh; hình dự kiến (chương nào, hình nào).

### 7.3 Prompt giao việc cho phiên viết (dán nguyên, điền ngoặc)

```text
Bạn viết bài <Lxx> "<tiêu đề>" cho repo vohoailinh90/Multiple-report (nhánh cơ sở: <nhánh>).
Đọc theo thứ tự: CLAUDE.md, docs/ban-giao-mo-rong-noi-dung.md (mục 3, 4, 5, 6), lessons/<Lxx>.spec.md,
lessons/L03/lesson.md (mẫu văn phong và cách gắn [Sn]).
Việc:
1. Đọc ĐÚNG các chương giáo trình trong spec (tải bằng curl với User-Agent trình duyệt; xem mục 10). Ghi lại điều mỗi chương nói.
2. Tìm nguồn gốc độc lập; kiểm DOI/URL có thật và nội dung đúng. Không kiểm được thì không dùng số liệu đó.
3. Viết lessons/<Lxx>/lesson.md: ≥ <N> chữ, mỗi bộ phận/chất/cảm xúc theo thẻ hồ sơ (mục 4.1), gắn nhãn mức chắc chắn (4.2),
   thuật ngữ kèm tiếng Anh ở lần đầu, [S1] ngay sau ý, mục cuối ## Nguồn tham khảo.
4. Viết lessons/<Lxx>/slides.json: mỗi mục ## ≥ 3 slide; slide giải thích có "body" 60–110 chữ, slide thẻ hồ sơ có "facts"; "notes" 80–200 chữ;
   đa dạng layout, không trùng hai slide liền, không quá 3 slide liền cùng tone.
5. Hình: chỉ dùng hình mà mục Media Attributions của chương ghi giấy phép cho phép; đặt vào lessons/<Lxx>/images/, khai trong slides.json khóa "images".
6. Chạy: python3 scripts/deckgen/check_lesson.py . <Lxx>   (phải OK)  và  python3 -m unittest discover -s tests.
7. Commit (thông điệp "lesson: <Lxx> viết lại/thêm") và push lên nhánh của phiên này. KHÔNG tạo PR. KHÔNG sửa file ngoài lessons/<Lxx>/.
Không dùng Moda. Không bịa nguồn, số liệu, năm, câu trích. Điều chưa chắc: viết "chưa rõ" thay vì đoán.
Báo lại: số chữ, số slide, danh sách nguồn đã kiểm, điều bạn không kiểm được.
```

### 7.4 Prompt phiên phản biện (chỉ đọc)

```text
Phản biện bài <Lxx> trên nhánh <nhánh viết>. Chỉ đọc, không sửa file. Mục: <(a) kiểm chứng | (b) sư phạm và định dạng>.
(a) Với mỗi khẳng định về cơ chế, số liệu, tên nghiên cứu: mở chương giáo trình/nguồn thật và đối chiếu. Trả danh sách: vị trí (file:dòng), câu bị nghi,
    điều nguồn thật nói, mức nghiêm trọng (sai / thổi phồng / thiếu nguồn / nhãn sai). Đặc biệt soát: "một vùng một cảm xúc", "hormone hạnh phúc",
    số liệu không nguồn, Gage/não trái-phải thổi phồng, suy luận trình bày như bằng chứng.
(b) Đọc như người mới: chỗ nào khó hiểu, thuật ngữ nào chưa giải thích, đoạn nào lặp bài khác (bảng 4.4 trong docs/ban-giao-mo-rong-noi-dung.md),
    slides.json có khớp lesson.md không, có vi phạm CLAUDE.md không. Trả danh sách có vị trí, không viết lại bài.
```

## 8. Kiểm tra và tiêu chí hoàn thành

Một bài **xong** khi:
- `python3 scripts/deckgen/check_lesson.py . <Lxx>` in `OK` (cảnh báo được giải thích, không bỏ qua);
- `python3 -m unittest discover -s tests` OK (CI chạy lệnh này);
- hai phiên phản biện không còn lỗi mức "sai" hoặc "thổi phồng"; lỗi khác đã sửa hoặc có lý do ghi lại;
- mọi `[Sn]` mở được và đúng nội dung (điều phối lấy mẫu ít nhất 3 nguồn mỗi bài và tự kiểm);
- `python3 scripts/decks.py todo` không in gì sau khi dựng deck; `python3 scripts/decks.py index` đã chạy.

Cả đợt xong khi mọi bài giai đoạn 1 xong và chủ repo đã nhận được: danh sách bài mới/viết lại, link canvas từng bài, các điều chưa kiểm được, các quyết định còn chờ họ.

## 9. Dựng deck (điều phối, tuần tự, trong phiên chính)

Mỗi bài 30–50 slide thành ~35–55 lệnh Moda, nên đừng dựng deck trước khi bài qua phản biện. Quy trình đã chạy được:

1. `canvas_create` (`name` = `Multiple-report · Lxx · <tiêu đề>`, `skip_brand_kit=true`, `page_count` = số slide + 1) để có sẵn mọi trang.
2. Với mỗi trang: `python3 scripts/deckgen/gen.py Lxx <i> --opts scripts/deckgen/opts/Lxx.json` (`i = 0` là bìa) rồi `canvas_apply_markup` vào đúng mã trang
   (`p_a` = trang 0, `p_b` = trang 1...). Gọi nhiều `canvas_apply_markup` song song trong một lượt được.
3. Chụp màn hình mọi slide ba trang một lệnh, sửa một lần, xuất `export` PPTX (`fresh=true`), tải về `lessons/<id>/<id>.pptx` bằng `curl`, rồi
   `python3 scripts/decks.py record <id> --canvas <URL>`.
4. Ảnh: `upload` với `url=` (Moda tự tải về) trả về `file_...`; ghi vào `scripts/deckgen/file_ids.json` (khoá là tên file). Markup dùng `<image src="file_..." fit="contain">`.

**Bẫy đã gặp, đừng lặp:**
- `canvas_apply_markup` vào trang **đã có nội dung** thì **thêm chồng**, không thay thế. Muốn sửa trang: `canvas_delete(ids=[...])` bằng id các nút cũ rồi áp lại, hoặc dùng `canvas_edit`.
  `canvas_edit` không xoá nút (`remove()` bị chặn) và không xoá trang.
- Chèn slide vào giữa làm lệch chân trang (chấm tiến độ và `NN/TT`) của mọi slide sau; sau khi đổi dàn ý, dựng lại cả canvas mới thay vì chèn.
- Cảnh báo `text_auto_shrunk`: cỡ chữ 110 trong ô cao 124 bị co; dùng ô cao 135 hoặc sửa theo gợi ý trong cảnh báo.
- Trang bìa L06 từng có hình thẻ giả đè lên tiêu đề; đã sửa trong `gen.py` (motif `feed`: dịch sang phải, độ mờ 0,55) và canvas L06 hiện hành đã khớp. Soát bìa mỗi bài.
- Máy chủ Moda MCP có lúc ngắt kết nối giữa phiên rồi tự nối lại; chạy lại `ToolSearch` để nạp công cụ, đừng báo "không dùng được" ngay.
- Link tải PPTX có hạn ngắn; tải về ngay sau `export`.
- Các canvas bản cũ (trước khi có hình) vẫn còn trên Moda; canvas thử `test-figure-layout` (`cvs_35Y3WY2WMC9XTB7SQV2P557MHA`) có thể xoá. Hỏi chủ repo trước khi xoá canvas khác.

## 10. Mạng và hình

- Mạng mở ở môi trường cloud `env_01FLRVzUuF7HzUtxGKMRQJrt`. *Cập nhật 2026-10-20:* môi trường còn lại (`env_016xkeasTxqB1STnoRvbnVgg`, nơi phiên điều phối
  chạy) chặn `rotel.pressbooks.pub`, NCBI, doi.org, Wikimedia (proxy trả 403, WebFetch không phân giải tên miền). Vì vậy phiên viết, phản biện và phiên phụ
  đọc nguồn được tạo bằng `create_session(environment_id="env_01FLRVzUuF7HzUtxGKMRQJrt")`; điều phối kiểm nguồn qua bản ghi lệnh `curl` của các phiên đó.
  `rotel.pressbooks.pub` trả 403 nếu không có `User-Agent` trình duyệt; có thì tải được:
  `curl -sS -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" -H "Accept: text/html" -L <URL>`.
  Có lúc phải thử lần hai.
- API Wikimedia Commons hay trả 429; đối chiếu giấy phép hình thì chờ rồi thử lại. Hiện chỉ hình Blausen (CC BY 3.0) và Gage (CC BY 2.5) đã đối chiếu tận gốc, các hình còn lại ghi giấy phép "theo sách";
  việc đối chiếu nốt còn treo.
- Điều kiện dùng hình: trang nguồn ghi rõ giấy phép cho dùng lại (CC BY, CC BY-SA, CC0, public domain, hoặc CC BY-NC-SA của chính giáo trình khi mục đích phi thương mại).
  Ghi tác giả, giấy phép, URL ở `images` trong `slides.json`, chú thích dưới hình trong `lesson.md`, dòng `Hình:` trên slide. `.gitignore` đã mở cho `lessons/*/images/*.png`.
- Hình sách (Noba, Wikipedia, Blausen...) thường có nhãn tiếng Anh; slide `figure` đã có cách xử lý: nhãn Anh màu nhấn + nghĩa Việt.

## 11. Quyết định thuộc về chủ repo (hỏi một lần, trước khi làm phần liên quan)

1. **Giai đoạn 3 (L11–L14) có làm không?** Mặc định đề xuất: làm sau khi giai đoạn 1–2 xong, hỏi lại.
2. **Có bỏ giới hạn "một slide đọc trong 5 giây"** trong `docs/deck-style.md` cho slide giải thích không? Mặc định: có, chỉ cho layout `explainer`, `profile-card`, `annotated-figure`;
   các layout khác giữ nguyên.
3. **Chương Ch.12 (rối loạn tâm lý) và L13 (thuốc/chất):** nội dung y tế, cần `## Lưu ý`; có đưa tên thuốc điều trị không? Mặc định: chỉ nhóm thuốc và cơ chế, không liều, không khuyến nghị.
4. **Merge:** nhánh `claude/dreamy-johnson-xy3y2y` chưa có PR; muốn gộp vào `main` bằng PR nào, lúc nào?

Những điều khác (cách viết, cấu trúc, nguồn) điều phối tự quyết theo văn bản này.

**Chủ repo đã trả lời (2026-10-20):** (1) giai đoạn 3 hỏi lại sau khi xong giai đoạn 1–2; (2) **bỏ luật "đọc trong 5 giây" cho mọi layout**, không chỉ
3 layout mới (đã ghi vào `docs/deck-style.md`); (3) thuốc: chỉ nêu nhóm thuốc và cơ chế, không liều, không khuyến nghị; (4) một PR từ nhánh điều phối vào
`main` sau giai đoạn 1.

## 12. Thứ tự làm việc gợi ý

1. Giai đoạn 0 (mục 6): sửa luật và công cụ, dựng thử **một** slide mỗi layout mới, chụp ảnh. Commit.
2. Viết spec cho giai đoạn 1; hỏi chủ repo các quyết định 11.2–11.4 nếu cần.
3. Tạo 6 phiên viết song song (L01, L03, L05 viết lại; L07, L09, L10 mới). Mỗi phiên theo prompt 7.3.
4. Khi phiên viết báo xong: tạo 2 phiên phản biện mỗi bài (12 phiên, chỉ đọc), rồi giao lỗi lại cho phiên viết sửa.
5. Gộp nhánh vào nhánh của điều phối, chạy gate và test, tự kiểm mẫu nguồn.
6. Dựng deck từng bài (mục 9); `decks.py todo` rỗng; `decks.py index`; cập nhật `docs/ke-hoach-nao-bo-tam-ly.md` (bảng bài, thứ tự đọc).
7. Giai đoạn 2, rồi hỏi chủ repo về giai đoạn 3.
8. Báo cáo: link canvas từng bài, số chữ/slide trước và sau, điều chưa kiểm được, quyết định đang chờ.

## 13. Nhật ký điều phối

**2026-10-20, giai đoạn 0 xong** (nhánh `claude/orchestrate-brain-series`):
- `CLAUDE.md`: thêm `body`, `facts`, `lessons/<id>.spec.md`; gạch ngắn chỉ cho slide sơ đồ; ghi rõ giới hạn của gate template.
- `scripts/deckgen/check_lesson.py` viết lại thành hàm `check()` có test (`tests/test_check_lesson.py`). Khóa mới của `expected.json` (đều tuỳ chọn, bài cũ giữ
  kiểm tra cũ): `required_urls` (thay `sources` cố định, vì phiên viết tự tìm nguồn), `min_independent_sources`, `min_layouts`, `section_min_slides` +
  `section_min_exempt`, `notes_words` (cảnh báo), `min_images` (cảnh báo). Trích dẫn giờ chỉ đếm phần trước `## Nguồn tham khảo` (trước đây đếm cả danh sách nguồn).
  Kiểm thêm: `body` chỉ trên layout vẽ nó, `facts` 3–6, nguồn của slide phải có trong danh sách, hình khai báo phải tồn tại. Bỏ cảnh báo "gạch > 10 chữ" (quyết định 11.2).
- `scripts/deckgen/gen.py`: 4 layout mới (`explainer`, `profile-card`, `annotated-figure`, `references`); hàm `fit` tự hạ cỡ chữ theo độ dài cho mọi layout
  (deck cũ L01–L06 sinh ra đúng cỡ chữ và nội dung như trước); footer co chấm khi deck > 40 trang (deck 51 trang trước đây đẩy nhãn ra ngoài khổ);
  `--slides` để dựng deck mẫu. Test: `tests/test_deckgen.py`.
- Dựng thử 6 trang (bìa + 4 layout mới + `card-grid` gạch dài) trên canvas `Multiple-report · T00 · Mẫu ba layout mới`
  (https://moda.app/canvas/6b00067f-f69e-4200-b090-1e660bcb271a), không cảnh báo co chữ, ảnh chụp đạt. Nội dung lấy từ L01/L03/L05.
- `docs/deck-style.md`: bảng 17 layout, cỡ chữ `body` 30–38, bỏ luật 5 giây, lệnh `gen.py` trong quy trình.
- `expected.json` của các bài giai đoạn 1 do phiên điều phối viết thay vai "tester" (chưa có model VPS), theo `scripts/deckgen/mk.py` `deep_expected`.

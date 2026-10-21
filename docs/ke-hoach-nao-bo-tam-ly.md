# Kế hoạch: bộ tài liệu "Bộ não và tâm lý"

Bộ tài liệu giải thích đại khái cách não vận hành và ảnh hưởng đến tâm lý, rồi dùng nó để hiểu mạng xã hội và truyền thông
tác động lên con người thế nào. Giáo trình nền: **Biological Psychology** (Hove & Martinez, CC BY-NC-SA 4.0,
[bản Rotel Pressbooks](https://rotel.pressbooks.pub/biologicalpsychology/)). Mục tiêu là hiểu ý chính, không đi sâu;
mỗi bài một file PowerPoint. Chủ repo cho phép bài dài và nhiều slide, miễn là dễ hiểu (không giới hạn số từ; `expected.json` đặt
tối đa 30000 từ và 40 slide).

## Quy mô

3 phần, 6 bài (`L01`–`L06`), mỗi bài khoảng 12–25 slide sau khi mở rộng. Bài `L00` (Dopamine và động lực) đã có, được dùng như bài tham chiếu
cho chất dẫn truyền dopamine; các bài mới không lặp lại nội dung của nó mà dẫn về nó.

| Phần | Bài | Tiêu đề | Chủ đề (`topic`) | Chương giáo trình |
|---|---|---|---|---|
| A. Nền tảng | L01 | Bản đồ não: các bộ phận lớn làm gì | `nao-bo` | Ch. 2 The Brain and Nervous System |
| A. Nền tảng | L02 | Nơron và synapse: não truyền tin thế nào | `nao-bo` | Ch. 3 Neurons |
| B. Hóa học và vỏ não | L03 | Chất dẫn truyền thần kinh và tâm lý | `than-kinh` | Ch. 5 Psychopharmacology |
| B. Hóa học và vỏ não | L04 | Thùy trán, não trái và não phải | `nao-bo` | Ch. 2 và các chương về chức năng cao cấp |
| C. Ứng dụng | L05 | Hệ thưởng, chú ý và cảm xúc | `than-kinh` | Ch. 5, Ch. 11 |
| C. Ứng dụng | L06 | Mạng xã hội và truyền thông tác động lên não | `khac` | ngoài giáo trình (xem dưới) |

Hạn chế đã biết: máy chủ của phiên này không mở được trang giáo trình, nên mục lục chương lấy từ kết quả tìm kiếm
(chắc chắn: Ch. 1 Introduction, Ch. 2 The Brain and Nervous System, Ch. 3 Neurons, Ch. 5 Psychopharmacology,
Ch. 11 Biopsychology of Psychological Disorders). Bài nào nêu chương nào thì nhóm phản biện kiểm lại trước khi giữ.
L06 không có trong giáo trình, nên dùng nghiên cứu gốc, và chỉ viết những điều có nguồn.

## Nội dung từng bài

- **L01 Bản đồ não.** Thân não, tiểu não, hệ viền, vỏ não; bốn thùy; hệ thần kinh trung ương và ngoại biên.
  Câu hỏi mở bài: "Phần nào của não quyết định bạn làm gì ngay lúc này?"
- **L02 Nơron và synapse.** Nơron, xung điện, synapse hóa học, thụ thể; vì sao tín hiệu hóa học là điểm các thuốc tác động.
- **L03 Chất dẫn truyền và tâm lý.** Glutamate và GABA (kích thích, ức chế), dopamine, serotonin, noradrenaline,
  acetylcholine, endorphin. Mỗi chất: vai trò chính, điều không nên hiểu quá đà ("hormone hạnh phúc" là cách gọi sai).
- **L04 Thùy trán, não trái và não phải.** Thùy trán và kiểm soát bản thân, kế hoạch; chuyên biệt hóa bán cầu
  (ngôn ngữ thường nghiêng trái) và vì sao "người não trái / não phải" là hiểu lầm.
- **L05 Hệ thưởng, chú ý và cảm xúc.** Vòng thưởng, hạnh nhân (amygdala) và phản ứng căng thẳng, chú ý bị kéo đi;
  liên hệ L00. Có `## Lưu ý` (nội dung liên quan trầm cảm, lo âu, nghiện).
- **L06 Mạng xã hội và truyền thông.** Các tính năng thiết kế (thông báo, lượt thích, cuộn vô tận, phần thưởng
  thất thường) khớp với cơ chế nào ở L00, L03, L05; cái đã có bằng chứng và cái còn tranh cãi; cách tự bảo vệ.
  Giữ giọng cân bằng: không khẳng định "nghiện mạng xã hội" như chẩn đoán, không bịa số liệu.

## Cấu trúc và kiểm tra mỗi bài

Theo `CLAUDE.md`: `lessons/Lxx.expected.json`, `lessons/Lxx/lesson.md`, `slides.json` (ít nhất 8 slide, ít nhất 5 kiểu
layout, không trùng kiểu ở hai slide liền nhau, không quá 3 slide liền cùng tone), rồi `Lxx.pptx` và `deck.json`.
Bài có nội dung y tế (L03, L05, L06) có `## Lưu ý`; mục cuối là `## Nguồn tham khảo`.
Mỗi bài có tối thiểu 5 trích dẫn `[Sn]`, gồm giáo trình (kèm chương) và ít nhất một nguồn gốc độc lập.

## Quy trình điều phối

1. **Viết mẫu (phiên chính).** Claude viết L01 trọn bộ: `lesson.md`, `slides.json`, `expected.json`. Tôi tự viết
   `expected.json` thay vai "tester" vì không có model VPS (ghi rõ để chủ repo biết).
2. **Phản biện mẫu (2 agent, chỉ đọc, song song).** Một agent kiểm chứng: đối chiếu từng khẳng định với nguồn, tìm lại
   nguồn bằng web, đánh dấu chỗ bịa, thổi phồng, hiểu sai, thiếu `[Sn]`. Một agent kiểm sư phạm và định dạng: đúng
   "đại khái, không sâu", thuật ngữ nhất quán, tuân thủ `CLAUDE.md`, `slides.json` khớp `lesson.md`. Chúng chỉ trả danh
   sách lỗi có vị trí, không sửa file. Tôi sửa L01 theo đó; những lỗi hay gặp được ghi lại để L02–L06 tránh.
3. **Viết L02–L06, rồi phản biện cả đợt (6 agent, song song).** 5 agent kiểm chứng, mỗi agent một bài, và 1 agent
   kiểm sư phạm/định dạng cho cả 5 bài (có đọc L00 và L01 để kiểm sự lặp và liên kết giữa các bài).
4. **Sửa (phiên chính).** Tôi xử lý từng lỗi: sửa, hoặc ghi lý do không sửa. Chạy
   `python3 -m unittest discover -s tests`.
5. **Deck (phiên chính, tuần tự).** Mỗi bài một canvas Moda theo `docs/deck-style.md`, xuất PPTX,
   `python3 scripts/decks.py record Lxx --canvas <URL>`. Việc Moda **không** giao cho subagent, vì `CLAUDE.md`
   quy định lệnh Moda của subagent phải chờ chủ repo duyệt từng lệnh.
6. **Hoàn tất.** `python3 scripts/decks.py todo` không in gì; `python3 scripts/decks.py index`; commit
   `decks: L01..L06` và push; báo link canvas từng bài kèm ý tưởng hình ảnh.

## Thứ tự và cam kết

L01 → L02 → L03 → L04 → L05 → L06 (bài sau dẫn về bài trước). L01 làm mẫu và qua phản biện trước, để lỗi không lặp
6 lần. Tổng cộng 8 agent phản biện. Không dùng số liệu, nghiên cứu hay câu trích
mà không có nguồn đã kiểm lại.

## Hình minh họa từ sách miễn phí (yêu cầu của chủ repo)

Mỗi bài có hình lấy từ giáo trình mở hoặc Wikimedia Commons, để bài sinh động và dễ hiểu.

- **Trạng thái:** đã làm. 13 hình từ giáo trình *Biological Psychology* (Hove & Martinez, ROTEL Pressbooks) nằm trong L01–L06
  (L01 3, L02 3, L03 1, L04 3, L05 1, L06 2), mỗi hình có slide `figure` và đoạn trong `lesson.md`.
- **Điều kiện dùng một hình:** trang nguồn ghi rõ giấy phép cho phép dùng lại (CC BY, CC BY-SA, CC0, public domain, hoặc
  CC BY-NC-SA của chính giáo trình nếu mục đích phi thương mại). Ghi tác giả, giấy phép và URL trang ảnh; đặt vào `notes` của
  slide và ở chân slide.
- **Nơi lưu:** `lessons/<id>/images/`, kèm bảng tác giả/giấy phép trong `slides.json` (khóa `images`) để nhóm phản biện kiểm lại.
- **Phản biện:** thêm một agent kiểm hình: giấy phép có đúng không, hình có minh họa đúng ý slide không, có hình nào sai
  khoa học hay lỗi thời không.
- **Còn lại:** đối chiếu giấy phép riêng của hình còn ghi "theo sách" trên Wikimedia Commons khi API hết giới hạn tốc độ (chỉ Blausen và Gage đã kiểm).

## Đợt đào sâu (2026-10-20)

Chủ repo thấy slide sơ sài; đợt này đào sâu vai trò từng bộ phận não và các chất dẫn truyền chi phối cảm xúc. Kế hoạch chi tiết, thước đo và quy trình đa phiên:
`docs/ban-giao-mo-rong-noi-dung.md`. Mỗi bài có `lessons/<id>.spec.md`. Số hiệu cũ giữ nguyên; bài mới đánh số từ L07.

| Thứ tự đọc | Bài | Tiêu đề | Đợt | Việc |
|---|---|---|---|---|
| 1 | L01 | Bản đồ não: các bộ phận lớn làm gì | giai đoạn 1 | viết lại: thêm hướng và mặt cắt, cách chụp não, thân não và tiểu não theo thẻ hồ sơ |
| 2 | L02 | Nơron và synapse: não truyền tin thế nào | giai đoạn 2 | đào sâu |
| 3 | L07 | Hệ viền và các nhân nằm sâu của não | giai đoạn 1 | mới: hạnh nhân, hải mã, đồi thị, vùng dưới đồi, hạch nền, thùy đảo, hồi đai |
| 4 | L03 | Chất dẫn truyền thần kinh và tâm lý | giai đoạn 1 | viết lại: mỗi chất một thẻ hồ sơ, thụ thể, đường đi, thuốc (nhóm và cơ chế) |
| 5 | L09 | Cảm xúc cơ bản và mạch thần kinh | giai đoạn 1 | mới: ham muốn, thích, sợ, giận, yêu thương, đau buồn |
| 6 | L10 | Chất dẫn truyền, hormone và cảm xúc | giai đoạn 1 | mới: bảng ghép cảm xúc ↔ mạch ↔ chất ↔ hormone, mức bằng chứng |
| 7 | L05 | Hệ thưởng, chú ý và căng thẳng | giai đoạn 1 | viết lại (đổi tên; cảm xúc chuyển sang L09) |
| 8 | L04 | Thùy trán, não trái và não phải | giai đoạn 2 | đào sâu |
| 9 | L08 | Vỏ não và các thùy | giai đoạn 2 | mới |
| 10 | L06 | Mạng xã hội và truyền thông tác động lên não | giai đoạn 2 | đào sâu |
| | L00 | Dopamine và động lực | | bài tham chiếu cũ, giữ nguyên |

Giai đoạn 3 (L11 Trí nhớ cảm xúc, L12 Rối loạn tâm trạng, lo âu và PTSD, L13 Thuốc và chất tác động, L14 Não thay đổi theo tuổi): chủ repo quyết định sau
giai đoạn 1–2. Nội dung thuốc ở mọi bài: chỉ nhóm thuốc và cơ chế, không tên hoạt chất, không liều, không khuyến nghị (chủ repo, 2026-10-20).

Ghi chú về các phần trên: mục "Hạn chế đã biết" (không mở được trang giáo trình) đã lỗi thời. Mục lục thật của giáo trình đã đối chiếu ngày 2026-10-20
(biên bản, mục 5). Giới hạn "tối đa 40 slide" và "12–25 slide mỗi bài" chỉ còn áp dụng cho L00, L02, L04, L06 cho tới khi chúng được đào sâu.

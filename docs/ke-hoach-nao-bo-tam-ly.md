# Kế hoạch: bộ tài liệu "Bộ não và tâm lý"

Bộ tài liệu giải thích đại khái cách não vận hành và ảnh hưởng đến tâm lý, rồi dùng nó để hiểu mạng xã hội và truyền thông
tác động lên con người thế nào. Giáo trình nền: **Biological Psychology** (Hove & Martinez, CC BY-NC-SA 4.0,
[bản Rotel Pressbooks](https://rotel.pressbooks.pub/biologicalpsychology/)). Mục tiêu là hiểu ý chính, không đi sâu;
mỗi bài một file PowerPoint 9–12 slide.

## Quy mô

3 phần, 6 bài (`L01`–`L06`), khoảng 63 slide. Bài `L00` (Dopamine và động lực) đã có, được dùng như bài tham chiếu
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

Theo `CLAUDE.md`: `lessons/Lxx.expected.json`, `lessons/Lxx/lesson.md`, `slides.json` (9–12 slide, ít nhất 5 kiểu
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

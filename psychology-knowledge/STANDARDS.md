# Chuẩn bài học và kiểm chứng

## Phạm vi và quy ước

Một bài là một chương nhỏ độc lập, giải thích khái niệm bằng lập luận, cơ chế, ví dụ, phản biện và câu hỏi có đáp án. Không dùng số từ làm đại diện cho chất lượng. Ngôn ngữ Việt có dấu; thuật ngữ tiếng Anh ở lần xuất hiện đầu. Không biến thuật ngữ lịch sử thành nhãn chẩn đoán hiện đại.

Mã: F01–F18, A01–A18, J01–J24. File `lessons/01-<slug-khong-dau>.md` trong từng tác giả; giữ mã khi đổi tên bài. Đổi phạm vi/thêm bài cần PR cập nhật curriculum, coverage và liên kết; không tái dùng mã đã xuất bản. Nếu tách/gộp bài, giữ ghi chú chuyển hướng từ mã cũ và review lại các bài phụ thuộc. Front matter gồm `id`, `title`, `topic: khac`, `date` (ngày sửa thực tế), `status`, `review_status`, `visual_status`. Không dùng số L của hệ thống cũ. Heading H1 là tên bài, H2 cho A–L; dùng bảng có header, link và ảnh tương đối, không phụ thuộc HTML riêng. Chú thích nguồn `[S1]` đặt sát khẳng định; ID nguồn ánh xạ tới L của chính bài.

## Cấu trúc A–L bắt buộc

| Mục | Nội dung cần đạt | Câu hỏi reviewer phải trả lời |
|---|---|---|
| A. Learning Objectives | 3–5 mục tiêu quan sát được: giải thích, so sánh, đánh giá, phân tích | Bài và câu hỏi có kiểm tra các mục tiêu không? |
| B. Historical Background | Bối cảnh vấn đề, tác phẩm gốc, năm đầu và lần sửa học thuyết | Có phân biệt niên đại tác phẩm và bản dịch đang dùng không? |
| C. Core Theory | Định nghĩa, giả định, quan hệ khái niệm, điều khái niệm không cho phép suy ra | Có tránh diễn giải phổ thông sai nghĩa không? |
| D. Psychological Mechanism | Từng bước từ điều kiện tới diễn biến và hệ quả, gắn nhãn mô hình đề xuất | Có tách cơ chế giả định khỏi kết quả quan sát không? |
| E. Real-Life Examples | Ít nhất 3 tình huống từ đơn giản tới phức tạp, có phân tích và giải thích thay thế | Có tránh suy động cơ từ một hành vi không? |
| F. Case Study | Một ca giả định có dữ kiện, giả thuyết, phân tích từng bước, điều còn thiếu và cách kiểm tra | Có ghi rõ giả định; không giả làm ca công bố không? |
| G. Modern Scientific Perspective | Bằng chứng hỗ trợ/trái chiều, phương pháp, giới hạn đo lường, ngoại suy và quan hệ nhân quả | Có phân biệt không có bằng chứng và bằng chứng chống lại không? |
| H. Practical Applications | Ứng dụng có điều kiện trong giao tiếp/giáo dục/tự phản tư/nghiên cứu | Có vượt bằng chứng hoặc thành hướng dẫn tự trị liệu không? |
| I. Visual Explanation | Ít nhất một hình Moda có caption, alt text, nguồn, link canvas; ngoại lệ ghi rõ trở ngại | Mũi tên, tầng và nhãn có đúng nghĩa không? |
| J. Key Takeaways | 5–10 ý trọng tâm, gồm giới hạn khoa học | Có nhắc lại một suy đoán như sự thật không? |
| K. Knowledge Check | Đúng 5 câu hỏi, đáp án giải thích lập luận và lỗi hiểu thường gặp | Có câu vận dụng và câu đánh giá bằng chứng không? |
| L. References — Nguồn tham khảo | Mỗi nguồn một dòng: `[S1]` tác giả, tên, năm, ấn bản/DOI/URL, locator khi cần | Tất cả claim chính có truy được tới phần nguồn phù hợp không? |

Thêm `## Lưu ý` trước A khi bài có nội dung y tế: tài liệu giáo dục, không tự chẩn đoán hoặc thay thế chăm sóc chuyên môn. Giữ L là mục cuối. Ví dụ giả định không mang dữ liệu nhận dạng; ca lịch sử trích nguồn, nêu giới hạn báo cáo và tiếng nói người bệnh. Không hướng dẫn gợi nhớ ký ức bị cho là dồn nén, không dùng giải mộng hay active imagination làm công cụ chẩn đoán.

## Nghiên cứu và nguồn

1. Tìm văn bản gốc cho định nghĩa và sự phát triển học thuyết; ghi tác phẩm, năm gốc, tập/ấn bản và trang/đoạn thực sự đọc. Không lấy mô tả nhà xuất bản thay văn bản gốc.
2. Tìm nghiên cứu thực nghiệm, systematic review/meta-analysis, sách học thuật và nghiên cứu phản biện; kiểm thiết kế, mẫu, độ đo, sai lệch, độ bất định và khả năng khái quát. Không chỉ chọn nguồn ủng hộ trường phái.
3. Ghi truy vấn, ngày tìm và tiêu chí chọn vào `references/<id>-search-log.md`. Đây là tổng quan phục vụ giảng dạy, không tự xưng systematic review nếu chưa đáp ứng phương pháp.
4. Phân biệt `metadata-verified`, `abstract-read`, `full-text-read`, `locator-verified`. Metadata khớp không có nghĩa nội dung claim đã kiểm. Với paywall, ghi giới hạn, tìm bản tác giả hợp pháp hoặc thu hẹp claim; không bịa trang.
5. Điền claim ledger cho mỗi khẳng định quan trọng trước khi chốt bài: định nghĩa, lịch sử then chốt, cơ chế, kết quả và khuyến nghị ứng dụng. Theo mẫu trong từng `references/evidence-ledger.md`.
6. Ưu tiên DOI, nhà xuất bản, thư viện và cơ sở dữ liệu khoa học; kiểm đính chính/rút bài khi có. Không đưa bản sách vi phạm bản quyền vào repo. Dịch lại bằng lời riêng, ghi người dịch khi trích bản dịch; không bịa trích dẫn trực tiếp.

## Đánh giá bằng chứng theo claim

Các nhãn sau là quy ước biên tập, **không phải GRADE**. Ghi loại nguồn, mức hỗ trợ và lý do riêng. Lịch sử được tư liệu gốc xác nhận không nhận nhãn “cơ chế mạnh”.

- **Chưa đánh giá:** chưa đọc nguồn thích hợp; không xuất bản claim như kết luận.
- **Chưa đủ:** chưa có phép kiểm phù hợp hoặc dữ liệu không phân biệt được các giải thích cạnh tranh.
- **Hạn chế:** ca bệnh, nghiên cứu nhỏ/quan sát hoặc phép đo gián tiếp với rủi ro sai lệch rõ.
- **Vừa:** nhiều nghiên cứu phù hợp có một mức hội tụ nhưng còn giới hạn về thiết kế, tái lập hay khái quát.
- **Mạnh:** nguồn chất lượng cao, hội tụ và tái lập phù hợp đúng claim; vẫn nêu phạm vi áp dụng và độ bất định.

Bằng chứng trái chiều cần mô tả chiều và độ chính xác, không chỉ gắn một nhãn thấp. Mức hỗ trợ của điều trị không tự chuyển sang cơ chế hoặc toàn bộ hệ thống lý thuyết.

Các giới hạn bắt buộc: vô thức nhận thức không xác nhận toàn bộ vô thức Freud; hiệu quả trị liệu tâm động học không chứng minh Oedipus hoặc death drive; thứ tự sinh không phải định mệnh nhân cách; nghiên cứu Jungian psychotherapy không xác nhận collective unconscious, archetypes hay synchronicity. Đọc khái niệm giới trong lịch sử, không áp khuôn nam/nữ lên mọi người.

## Definition of Done và review

Trạng thái bài: `planned → researching → drafted → reviewed → complete`; chưa tạo file bài ở `planned`. Visual riêng: `not-started`, `canvas-only`, `exported`, `verified`, `blocked`. Khi công cụ cản trở, có thể `complete-with-visual-exception` nếu toàn bộ phần học thuật đã đạt và reviewer chấp thuận ngoại lệ được ghi rõ; không tính là complete không điều kiện.

- [ ] A–L đủ sâu, các mục tiêu được bao phủ; 3 ví dụ và một case có phân tích.
- [ ] Cơ chế, giới hạn và ứng dụng thống nhất; 5–10 takeaways, 5 câu có giải thích.
- [ ] Nguồn và locator cho claim chính đã đọc/kiểm, không còn `unassessed` claim trình bày như kết luận.
- [ ] Hình Moda, bản xuất, caption/alt, nguồn và metadata khớp; hoặc ngoại lệ công cụ cụ thể.
- [ ] Markdown/link/ảnh được kiểm ở GitHub; kiểm tiếng Việt và thuật ngữ.
- [ ] Reviewer độc lập đọc nội dung, nguồn, ví dụ, sơ đồ, cấu trúc, liên kết và tính nhất quán; findings có vị trí, mức độ, bằng chứng và cách sửa.
- [ ] Finding nghiêm trọng/major được sửa và review lại; không còn finding chưa xử lý. Finding bác bỏ phải có lý do và phản hồi reviewer. Nếu không có reviewer độc lập, ghi self-review và giới hạn, không giả nhận đã review độc lập.

Folder chỉ hoàn thành khi mọi bài trong curriculum đạt checklist; ngoại lệ hình phải liệt kê riêng. Toàn dự án chỉ hoàn thành sau cross-theory review. Không dùng số lượng file hay CI xanh thay phản biện học thuật.

# Hệ thống thiết kế trực quan — Moda

## Ngôn ngữ thiết kế

Academic Editorial Design, Psychology Textbook, Scientific Infographics, Modern Minimalism. Khoảng trắng rộng; một câu hỏi trung tâm cho mỗi hình. Bố cục gồm tiêu đề, nội dung chính, chú giải mức bằng chứng và footer nguồn. Typography đề xuất Noto Sans hỗ trợ tiếng Việt; title 48px, node 28px, chú thích 24px trên 1600×1000. Lưới 8px, lề 64px, khoảng cách khối 32px; kiểm lại theo độ dài tiếng Việt và độ đọc khi thu nhỏ.

| Trường phái | Accent | Vai trò |
|---|---|---|
| Freud | Burgundy `#7A2038` | Điểm nhấn và nhãn tác giả |
| Adler | Teal `#126B60` | Điểm nhấn và nhãn tác giả |
| Jung | Indigo `#493C89` | Điểm nhấn và nhãn tác giả |

Nền `#FAF8F4`, chữ `#20242A`, nền thẻ trắng. Dùng đường liền cho quan hệ định nghĩa, đường đứt và nhãn “giả thuyết” cho cơ chế chưa xác nhận; chú giải bắt buộc. Icon tối giản có nhãn chữ; không dùng hình não để ám chỉ vị trí sinh học của id, ego, archetype. So sánh ba trường phái dùng cùng lưới và tiêu chí, không biểu diễn khác biệt như bảng xếp hạng đúng/sai.

## Khả năng đã xác nhận và giới hạn

Ngày 2026-10-24 đã gọi bootstrap Moda thành công và đọc `moda-diagram`. Connector cung cấp tạo/đọc/sửa canvas, markup có connector neo, screenshot và export PNG/JPEG/PDF/PPTX. Đây là xác nhận kết nối và giao diện công cụ; **chưa tạo canvas, chưa thử export/tải file**, không khẳng định toàn chuỗi đã chạy. Không có hình ở Phase 1.

Trước khi thiết kế: đọc `moda-core`, `diagram`, `markup`, `design-quality` và hướng dẫn export liên quan theo skill; kiểm brand list. Áp palette người dùng đã yêu cầu, giải quyết brand kit theo quy tắc Moda tại thời điểm tạo canvas. Chỉ phiên chính thực hiện Moda; reviewer chỉ đọc và phản biện.

Quy trình cho mỗi bài: nội dung được nghiên cứu → brief xác định điểm khó và bằng chứng → nodes/edges/nhãn → tạo canvas → đối chiếu học thuật → xem screenshot cuối → sửa nếu có lỗi → xuất và tải → kiểm bản xuất → nhúng vào bài → ghi metadata. Mỗi bài tối thiểu một hình; bài có nhiều mô hình bổ sung hình đối chiếu. Dùng connector neo, không ghép mũi tên thủ công có thể lệch khi sửa.

Nếu xuất không được, giữ URL canvas thật và trạng thái canvas-only; nếu chưa có canvas ghi blocked cùng nguyên nhân. Không thay bằng ảnh tự dựng rồi ghi là Moda. Ngày và trạng thái review chỉ ghi khi đã thực hiện. Các bản xuất lưu trong `visuals/` của đúng tác giả, metadata trong `moda/` tương ứng.

## Cập nhật bài mẫu 2026-10-24

F01 đã tạo canvas, áp markup, xem screenshot và export PNG thành công trên Moda. Người dùng chọn không tạo brand kit, dùng palette hiện có. Workspace không kết nối được proxy để tải PNG; đã lưu screenshot JPEG thật làm preview, xem metadata F01. Nhận định “chưa tạo canvas” ở đoạn kiểm tra Phase 1 phía trên chỉ ghi trạng thái lịch sử lúc PR #35 được lập.

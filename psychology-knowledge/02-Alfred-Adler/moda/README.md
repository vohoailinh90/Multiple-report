# Moda — Alfred Adler

**Trạng thái: chưa tạo canvas, chưa xuất hình.** Connector đã kết nối và đọc skill `moda-diagram` ngày 2026-10-24; việc export thực tế chưa được thử. Không có link giả.

Mỗi bài có `a01-visual.json` khi bắt đầu thiết kế, ghi: lesson_id, visual_id, canvas_url, canvas_ref, page_ref, skill, source_ids, source_locators, lesson_commit, revision, export_path, exported_at, academic_review, visual_review, status, blocker. Các giá trị chưa biết dùng null và nêu lý do; không ghi completed khi chưa kiểm tra.

Trình tự: đọc bài và nguồn → chọn khái niệm khó → nodes/edges hoặc cấu trúc thông tin → đọc skill Moda đúng định dạng và brand setup → tạo canvas → đối chiếu học thuật → screenshot cuối → export PNG/PDF → tải vào `visuals/` → kiểm bản xuất → ghi metadata và nhúng vào bài.

Nếu export không được: giữ URL canvas thật, ghi `status: canvas-only` và lỗi cụ thể; ghi ngoại lệ trong checklist bài. Nếu không tạo được canvas: `status: blocked`, không tự nhận đã dùng Moda để tạo hình.

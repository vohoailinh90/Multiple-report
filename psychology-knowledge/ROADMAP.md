# Roadmap và tích hợp repository

## Kiểm tra ban đầu — 2026-10-24

Repository được gắn: `vohoailinh90/Multiple-report`; default branch `main` xác nhận qua GitHub API. HEAD ban đầu `c57505e91e0d2db63e320f47001c606ffad576b3` khớp main tại lúc kiểm. Working tree ban đầu sạch, nhánh local `work`. Đã đọc AGENTS.md, CLAUDE.md, docs/TEAM.md, docs/dieu-phoi.md, README và CI. Có bài tổng quan L15; không chuyển hoặc ghi đè bài đó.

Yêu cầu trực tiếp hiện tại của người dùng giao thiết kế/viết kiến trúc và PR cho phiên này, được áp dụng trong phạm vi dự án mới thay cho phân vai Claude viết/Codex chỉ review trong hướng dẫn cũ. Không sửa các file hướng dẫn, không khởi động VPS team đang tạm dừng. Không tự merge: yêu cầu hiện tại giữ quyền phê duyệt cho người dùng.

Kho mới là `psychology-knowledge/` với ba thư mục tác giả; file quản trị nằm ở root của kho mới. Các folder con dùng README có nội dung quy ước hoặc `.gitkeep` để Git lưu thư mục lessons; không tạo hàng chục bài placeholder. ID F/A/J độc lập với ID L. Không đưa file mới vào mục lục sinh tự động `lessons/README.md`, không cấp claim L vì Phase 1 chưa viết bài trong pipeline cũ. Root README thêm một liên kết để tìm kho mới.

Chuẩn A–L và ảnh PNG/PDF theo yêu cầu dự án mới; hệ thống lesson.md/slides.json/PPTX của kho cũ giữ nguyên. Script gate/deck hiện tại chỉ kiểm cây lessons cũ, không được dùng để tuyên bố bài mới đã đạt chuẩn. Khi triển khai nội dung, dùng checklist STANDARDS và reviewer; nếu cần tích hợp gate tự động thì làm một PR riêng trước, không tự nhận CI đã bao phủ A–L.

## Các phase và điểm duyệt

| Phase | Kết quả kiểm tra trên GitHub | Điều kiện chuyển tiếp |
|---|---|---|
| 1 — Knowledge Architecture | PR curriculum 60 bài, chuẩn A–L, nguồn nền, claim ledger, thiết kế và review | Người dùng phê duyệt kiến trúc; PR không tự merge |
| 2 — Freud | Các PR 2–3 bài, nguồn và Moda đúng bài; tổng 18 bài đạt chuẩn | Mỗi batch hết finding chưa xử lý; tổng kết folder |
| 3 — Adler | Các PR tương tự cho 18 bài, kiểm định kiến thứ tự sinh | Mọi bài đạt checklist, ghi ngoại lệ hình riêng |
| 4 — Jung | Các PR tương tự cho 24 bài, kiểm khẳng định archetype/synchronicity | Mọi bài đạt checklist, ghi ngoại lệ hình riêng |
| 5 — Cross-Theory Review | PR rà soát thuật ngữ, nguồn, bảng đối chiếu trong bài phù hợp và liên kết chéo | Review toàn kho và kiểm các link; không có chương thứ tư |

Sau duyệt Phase 1 mới nghiên cứu/viết batch Freud F01–F03. Mỗi PR ghi bài hoàn thành, sơ đồ và canvas thật, nguồn chính, findings đã sửa, kiểm tra đã chạy, vấn đề mở và bước tiếp. Branch riêng cho batch, commit phạm vi hẹp; không sửa main, không auto-merge. Không lên lịch chạy tự động hoặc gửi thông báo bên ngoài.

## Điều kiện duyệt kiến trúc

- Đúng ba thư mục, curriculum bao phủ yêu cầu và phần thiếu có lý do.
- Chuẩn bài, kiểm chứng, định nghĩa hoàn thành và xử lý giới hạn công cụ rõ ràng.
- Nguồn nền có trạng thái truy cập trung thực; chưa coi metadata là đọc toàn văn.
- Reviewer độc lập kiểm kiến trúc và phản hồi findings; kiểm repo bình thường vẫn chạy.
- PR để mở cho người dùng, chưa bắt đầu Phase 2.

## Yêu cầu tiếp theo sau PR kiến trúc

Người dùng đã yêu cầu ghi toàn bộ chương trình, một bài mẫu rồi ba phiên Codex đồng thời. Đang thực hiện theo [PROGRAM](PROGRAM.md) và [COORDINATION](COORDINATION.md), thay điểm chờ Phase 2 trong phạm vi batch mẫu/ba bản nháp này. PR #35 vẫn chưa merge; không suy yêu cầu mới thành quyền tự merge hoặc duyệt chất lượng mẫu.

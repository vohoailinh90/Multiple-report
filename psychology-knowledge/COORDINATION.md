# Điều phối ba phiên Codex

## Ủy quyền và phạm vi

Ngày 2026-10-24 người dùng yêu cầu: ghi lại chương trình, làm một bài mẫu, sau đó điều phối ba phiên Codex đồng thời. Bài mẫu F01 đã được phiên chính viết A–L và có canvas/preview Moda trước khi khởi động ba phiên. Đây là ba subagent Codex trong cùng môi trường dùng chung filesystem, không phải ba cửa sổ ứng dụng hoặc ba tiến trình VPS. Không khởi động team/team-codex/team-lesson đang tạm dừng.

Yêu cầu mới thay phân vai Claude-only và giới hạn hai phiên cũ trong phạm vi dự án này. Không sửa AGENTS.md/CLAUDE.md, hệ thống L/claims cũ hoặc main; không tự merge. Mỗi lần chỉ giao một bài để kiểm độ sâu, không giao tạo hàng chục placeholder.

## Phân công hiện hành

| Phiên | Agent | Bài | File được ghi | Trạng thái khi khởi động |
|---|---|---|---|---|
| Freud | freud_session | F02: Conscious, Preconscious, Unconscious | Freud/lessons/02-conscious-preconscious-unconscious.md và references/f02-research.md | Đã khởi động song song |
| Adler | adler_session | A01: Cuộc đời và khác biệt Freud | Adler/lessons/01-cuoc-doi-va-khac-biet-voi-freud.md và references/a01-research.md | Đã khởi động song song |
| Jung | jung_session | J01: Cuộc đời và quan hệ Freud | Jung/lessons/01-cuoc-doi-va-quan-he-voi-freud.md và references/j01-research.md | Đã khởi động song song |

Các đường dẫn rút gọn Freud/Adler/Jung tương ứng ba thư mục học thuật có số đầu. Phiên chính giữ PROGRAM, COORDINATION, README, trạng thái chung, bài mẫu F01, Moda, commit và PR. Agent không đổi branch/commit/push trên checkout dùng chung; phiên chính đóng gói diff theo đúng file được giao. Branch tích hợp hiện tại: psychology/sample-and-coordination.

## Hợp đồng bàn giao

Mỗi phiên đọc PROGRAM/STANDARDS/curriculum và mẫu F01; nghiên cứu nguồn thật, ghi mức truy cập/locator/claim ledger; viết A–L, 3 ví dụ, case, 5–10 takeaways và 5 câu có giải thích. Bản bàn giao là drafted, review pending, visual not-started. Mục I có brief để phiên chính làm Moda, không link hình/canvas giả. Không ghi complete.

Sau bàn giao: phiên chính kiểm phạm vi, thuật ngữ và nguồn → reviewer độc lập → sửa findings → Moda tuần tự ở phiên chính → kiểm ảnh/xuất/nhúng → PR theo batch. Không tự nhận bản nháp đã đạt Definition of Done. Lưu kết quả thực tế bên dưới; agent kết thúc turn không có nghĩa tự tiếp tục chạy nền.

## Trạng thái bài mẫu

F01 là bản để người dùng xem thử, chưa tự coi mẫu đã được người dùng duyệt. Có một canvas và preview JPEG thật; PNG export đã tạo trên Moda nhưng workspace không tải được vì proxy không kết nối. Review độc lập và giới hạn được ghi tại references/f01-review.md khi có kết quả.

## Kết quả thực tế của vòng điều phối đầu

Ba phiên đã chạy đồng thời và đã bàn giao đủ hai file/phiên, không sửa ngoài phạm vi, không thao tác Git/Moda. Cả ba hiện đã kết thúc lượt, không đang chạy nền:

- Freud: [F02](01-Sigmund-Freud/lessons/02-conscious-preconscious-unconscious.md) và [research](01-Sigmund-Freud/references/f02-research.md). Cần cập nhật thêm nghiên cứu hiện đại ngoài bộ nguồn đã đọc.
- Adler: [A01](02-Alfred-Adler/lessons/01-cuoc-doi-va-khac-biet-voi-freud.md) và [research](02-Alfred-Adler/references/a01-research.md). Phân biệt văn bản Adler qua trung gian với nguồn gốc.
- Jung: [J01](03-Carl-Gustav-Jung/lessons/01-cuoc-doi-va-quan-he-voi-freud.md) và [research](03-Carl-Gustav-Jung/references/j01-research.md). Phân biệt quan hệ 1913 với tổ chức 1914; review 2025 chỉ truy cập một phần.

Tự kiểm A–L và link của các phiên đã đạt; đây chưa là review độc lập. Ba bài vẫn drafted/pending/not-started, chưa đủ Definition of Done. Chưa sản xuất đại trà theo mẫu chưa được người dùng phản hồi. Bước tiếp sau phản hồi mẫu: sửa chuẩn nếu cần, review độc lập ba draft, bổ sung nguồn còn thiếu và Moda tuần tự; chỉ giao tiếp batch kế khi chất lượng đã kiểm.

Review mẫu F01 đã hoàn tất hai vòng trong phạm vi đã nêu, không còn finding chưa xử lý; giữ drafted/reviewed-with-limitations, chờ người dùng xem. Xem [biên bản](01-Sigmund-Freud/references/f01-review.md).

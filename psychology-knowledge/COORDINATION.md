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


## Batch 2 — sau khi duyệt mẫu v4 (2026-10-24)

Người dùng xác nhận “file mẫu này ok rồi” và yêu cầu điều phối ba phiên làm các bài tiếp theo. Mẫu thiết kế hiện hành là F01 v4, canvas https://moda.app/canvas/53a95d71-d2f0-4013-ad6c-7d526ff19027?source=agent. Đây là duyệt mẫu, không phải duyệt merge PR hoặc công nhận toàn bộ curriculum hoàn thành.

Ba phiên được kích hoạt lại đồng thời, mỗi phiên hoàn thiện bài đã có từ vòng đầu và tạo kịch bản slide để tránh bỏ dở draft:

| Phiên | Bài | Phạm vi ghi bổ sung | Bàn giao cần có |
|---|---|---|---|
| freud_session | F02 — Conscious, Preconscious, Unconscious | Hai file F02 nêu trên và Freud/moda/f02-slides.json | Bài A–L, research ledger, kịch bản khoảng 30–40 slide |
| adler_session | A01 — Cuộc đời Adler và khác biệt Freud | Hai file A01 nêu trên và Adler/moda/a01-slides.json | Bài A–L, research ledger, kịch bản khoảng 30–40 slide |
| jung_session | J01 — Cuộc đời Jung và quan hệ Freud | Hai file J01 nêu trên và Jung/moda/j01-slides.json | Bài A–L, research ledger, kịch bản khoảng 30–40 slide |

Mỗi phiên chỉ ghi ba file được giao; không Git/commit/branch/push, không dùng Moda. Kịch bản cần body giải thích, cấu trúc sơ đồ, nguồn và visual brief theo từng slide; ảnh tìm được phải có URL/credit/trạng thái giấy phép, không gán quyền chưa kiểm. Freud Burgundy, Adler Teal, Jung Indigo; emoji và icon theo mẫu vừa duyệt. Không ép số slide nếu làm giảm chiều sâu.

Phiên chính phụ trách tích hợp, review độc lập, xử lý findings, dựng Moda tuần tự và xuất PDF/PPTX. Trạng thái tại lúc giao: cả ba đã được gửi tác vụ; chưa có kết quả batch 2. Bài vẫn drafted/review pending/visual not-started cho đến khi kiểm xong. Agent kết thúc lượt không đồng nghĩa tự chạy nền liên tục. Không merge.


## Giao sản xuất deck cho phiên khác — 2026-10-24

Theo yêu cầu trực tiếp mới của người dùng, phiên `presentation_production` được khởi động để dùng Moda dựng và xuất đủ PPTX/PDF cho F02, A01, J01. Yêu cầu này ủy quyền riêng cho phiên đó dùng Moda, thay quy tắc chỉ phiên chính dùng Moda trong phạm vi ba deck; không sửa AGENTS/CLAUDE và không khởi động VPS team.

Đầu vào: ba kịch bản 37/38/40 slide và bài học/research tương ứng; chuẩn F01 v4 đã duyệt. Không brand kit; màu Burgundy/Teal/Indigo. Đầu ra: ba canvas mới, sáu bản xuất thật, metadata `<id>-report-v1.json` và nguồn ảnh `<id>-visual-sources.md`; lưu visual chỉ khi tải thật thành công. Giữ nội dung đầy đủ, nguồn, sơ đồ đa dạng, ảnh tư liệu đúng ngữ cảnh, emoji/icon như mẫu. Phải xem render, sửa lỗi và nêu cảnh báo xuất.

Phiên sản xuất không Git/branch/commit/push, không sửa bài học, tài liệu nghiên cứu hoặc file chung. Phiên chính giữ tích hợp và PR. Trạng thái lúc giao: đã kích hoạt agent, chưa có bản xuất; không coi là đã hoàn thành.


### Cập nhật phân công: một phiên cho một bài

Người dùng yêu cầu tách ba bài thành ba phiên. Đã tạm dừng phiên sản xuất chung và đổi phạm vi; phiên đó xác nhận chưa tạo canvas/task/file A01 hoặc J01 nên không có việc trùng.

| Agent | Phạm vi duy nhất | Đầu ra |
|---|---|---|
| presentation_production | F02 — Freud | Canvas, PPTX, PDF; f02-report-v1.json và nguồn ảnh |
| adler_presentation | A01 — Adler | Canvas, PPTX, PDF; a01-report-v1.json và nguồn ảnh |
| jung_presentation | J01 — Jung | Canvas, PPTX, PDF; j01-report-v1.json và nguồn ảnh |

Ba phiên được phép dùng Moda cho canvas riêng theo yêu cầu mới, không ghi chéo file, không thao tác Git. Phiên chính giữ tích hợp/review/PR. Các phân công một phiên làm ba deck phía trên được thay thế bởi bảng này.


## Sổ giữ việc chống trùng — batch deck F02/A01/J01

Nguồn quy trình đã đọc ngày 2026-10-24:
- Template: https://github.com/vohoailinh90/claude-agent-routing-template/blob/main/.claude/skills/codex-lane/SKILL.md
- Giao thức chống yêu cầu trùng, một yêu cầu đang chạy và xác minh đầu ra: https://github.com/vohoailinh90/claude-agent-routing-template/blob/main/docs/claude-to-codex.md (mục 6, 11, 14, 16).
- Điều phối nội bộ repo: ../docs/dieu-phoi.md. Công cụ claims.py dành cho hệ L cũ; bảng này giữ mã F/A/J trong psychology-knowledge, không giả nhận đã có khóa máy hay khóa liên phiên trên remote.

Các agent ở đây là subagent Codex nội bộ do người dùng chỉ định, không phải yêu cầu Codex Cloud qua GitHub. Không tạo thêm yêu cầu Cloud IMPLEMENT cho cùng ba deck. Quy tắc marker/round Cloud chỉ áp dụng khi thực sự gửi lệnh Cloud; kiểm tra request đang chờ và head trước khi xin review PR. Quyền ba phiên dùng Moda là chỉ định mới; không tự merge.

| Task ID | Bài | Chủ duy nhất | Trạng thái gần nhất | Canvas giữ chỗ | File bàn giao |
|---|---|---|---|---|---|
| PSY-DECK-F02-V1 | F02 | presentation_production | Đã xuất PPTX/PDF, đủ 37 trang; chờ tích hợp PR | https://moda.app/canvas/6fc130f8-596c-4446-b9f8-3aaceb1bc64b?source=agent | 01-Sigmund-Freud/moda/f02-report-v1.json |
| PSY-DECK-A01-V1 | A01 | adler_presentation | Đã xuất PPTX/PDF, đủ 38 trang; chờ tích hợp PR | https://moda.app/canvas/c53e3ca8-b9de-4fb8-8506-65caf8644eed?source=agent | 02-Alfred-Adler/moda/a01-report-v1.json |
| PSY-DECK-J01-V1 | J01 | jung_presentation | Đã xuất PPTX/PDF, đủ 40 trang; chờ tích hợp PR | https://moda.app/canvas/6ee47b5e-532d-454e-b480-3f5cfc87fa7e?source=agent | 03-Carl-Gustav-Jung/moda/j01-report-v1.json |

Chỉ phiên chính sửa sổ này. Không nhận lại bài có chủ đang làm. Khi gián đoạn, kiểm trạng thái agent, file bàn giao, canvas và task export trước khi khởi động lại; tiếp tục trên canvas đã ghi. Ghi rõ bàn giao/blocked/done và chứng cứ trước khi đổi chủ. Chỉ bàn giao xong khi có hai URL xuất thật hoặc lỗi công cụ được ghi rõ. Không coi agent biến mất là bài đã xong.

Sau khi đủ ba bàn giao: phiên chính tích hợp, review độc lập, chạy kiểm tra nội dung/JSON/link và kiểm tra repo; mở một PR batch mới trên branch riêng với base là branch mẫu hiện hành nếu PR mẫu chưa merge. PR phải ghi 3 bài, canvas, nguồn, kết quả review, giới hạn và việc tiếp theo; không tạo PR trùng nếu batch đã có PR. Trước khi review Cloud kiểm comment/head để tránh yêu cầu trùng. PR không được tự merge.


### Bàn giao batch và trạng thái hiện hành

Cả ba task PSY-DECK-F02-V1, PSY-DECK-A01-V1, PSY-DECK-J01-V1 đã bàn giao hai bản xuất complete và metadata; không giao lại hoặc tạo canvas mới. F02 37 trang, A01 38 trang, J01 40 trang. Mỗi phiên đã xem toàn bộ render. A01 đã loại ảnh phù điêu chưa đối chiếu provenance. Link tải nằm tại [DELIVERABLES.md](DELIVERABLES.md); các URL canvas trong bảng giữ việc là bản hiện hành.

Reviewer độc lập không thấy finding học thuật nghiêm trọng; ghi nhận và sửa trạng thái trước sản xuất trong mục I/front matter/research. Xem [biên bản review](BATCH-02-REVIEW.md). Giữ drafted/reviewed-with-limitations/exported, không tính hoàn thành toàn bộ Definition of Done. Chưa lưu binary cục bộ vì download bị chặn; không có file giả. Mỗi PDF có một trang rasterized, PPTX không cảnh báo.

Kiểm tích hợp: đủ A–L/37–38–40 slide/markup/export URLs/link nội bộ và trạng thái; 122 unit tests pass; claims.py check --merge-ready pass (hệ cũ, không chứng nhận học thuật); git diff --check pass. Branch PR: psychology/batch-02-three-decks, base psychology/sample-and-coordination (PR #36 chưa merge). Chỉ phiên chính tạo/cập nhật PR của batch, kiểm PR đang có trước mỗi lần tạo. Không tự merge.


PR batch đã tạo: [#38](https://github.com/vohoailinh90/Multiple-report/pull/38), branch psychology/batch-02-three-decks. Đây là PR duy nhất của batch PSY-DECK-F02/A01/J01-V1; cập nhật PR này khi sửa, không mở yêu cầu sản xuất hoặc PR trùng. Ba phiên sản xuất đã kết thúc lượt sau bàn giao.

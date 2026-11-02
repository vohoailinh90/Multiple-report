# Ghi chú bằng chứng cho báo cáo thành tích (2026-11-02)

Nguồn: 2 file macro (đọc trực tiếp) + 5 agent đọc 9 repo (chỉ đọc) + số liệu git do script tính.
Mọi con số trong deck đều truy được về một dòng bên dưới. Phần "CẦN XỬ LÝ TRƯỚC KHI GỬI" quan trọng nhất.

## CẦN XỬ LÝ TRƯỚC KHI GỬI MANAGER

1. **Ai viết code.** Git log: phần lớn commit mang tác giả "Claude" (DocumentAIEditor 598/692, Outlook-RSVP 134/155,
   Excel-to-planner 152/181, doc-tools 324/388, Test-order-tracker 334/374, Shipping_Inspection 968/1287,
   Temperature_validation 12/14). Manager có thể mở git log. Deck đã viết đúng: "Most of the code is written by AI agents
   under my direction. I own the requirements, the rules and the acceptance." Đừng nói "tự code X dòng".
2. **Repo Outlook-RSVP là CÔNG KHAI** và lịch sử git vẫn còn file DB và PDF chứa tên/email/số tiền thật của đồng nghiệp
   (`git log --all --oneline -- rsvp_data.db RSVP_tool.pdf` ra 3 commit; `docs/PURGE_HISTORY.md` mới là hướng dẫn, chưa thực hiện).
   **Đừng gửi link repo này cho ai trước khi xử lý.** DocumentAIEditor (private) có 1 email NT-ID thật ở commit đầu (OUTSTANDING mục 8).
3. **Shipping Inspection chưa tự so với bản vẽ để ra OK/NG.** Mọi dòng xuất ra là NEEDS_HUMAN_CHECK (si_copilot_marking.py:1146).
   Tool tự phát hiện: lỗi thứ tự ảnh, thiếu/lệch bản ghi, lỗi parse. "Sai khác với bản vẽ tự phát hiện (再発防止)" mới là mục tiêu
   (ROADMAP Phase S5 chưa mở). Deck nói đúng điều này.
4. **Temperature_validation**: repo là bộ phân tích/audit/sửa lỗi cho workbook có sẵn, không phải "tool do team CIP xây". Leader-CIP,
   3 thành viên, bằng khen, database xu hướng nhiệt độ: **không có trong repo** (deck ghi theo lời bạn). Đừng đưa workbook/VBA cho
   người ngoài: có tên khách hàng, model, giới hạn nhiệt độ; Module2 hard-code mật khẩu sheet.
5. **Con số 1.000+ giờ (NIKK).** File chứng minh: mẫu 108 từ, 199,3 phút (thủ công, 18/04/2023) so với 47 phút (có tool, 19/04/2023)
   = giảm 76%. Ô `P30 = P29*18000/60` = 423 là **giờ** cho dự án giả định **18.000 từ** (nhãn trong file ghi nhầm "minutes", nên sửa).
   "1.000+ giờ" là ước tính của bạn cộng dồn các dự án (~2,4 dự án cỡ 18.000 từ). Nên chuẩn bị bảng tính gốc nếu manager hỏi.
6. **Check_PDF_paper_size.xlsm**: metadata gốc của file ghi tác giả "Tomoya Kubo" (tạo 2018); phần liệt kê bản vẽ (`MakeDrawingList`, comment
   tiếng Nhật, nhắc SolidWorks) là mã có sẵn. Phần của bạn: module `Check_Paper_Size` (khổ A0–A5, hướng, số trang qua Acrobat),
   cột so sánh JP/EN, hướng dẫn tiếng Việt. Deck ghi "Extended from an existing drawing-list workbook".
7. **Excel-to-planner**: repo không xác nhận Bosch IT/ACM đã duyệt quyền `Tasks.ReadWrite`; nếu chưa duyệt thì chặn đăng nhập mọi người.
   Hỏi IT trước khi nói với manager. Quyền Responsible (người phụ trách) đã gỡ 2026-10-16 vì ACM từ chối `User.ReadBasic.All`.
   "Hoạt động Digital" và lộ trình báo giá → ECR không có trong repo (là định hướng, deck ghi "Next").
8. **Test-order-tracker**: chưa có bằng chứng dùng hằng ngày với dữ liệu thật; README vẫn ghi phần Windows/Outlook "needs manual verification";
   nút Approve/Reject chỉ có qua helper Outlook COM; ADR 0002 còn "proposed". Chỉ nên nói "theo dõi tiến độ", không nói "đang dùng rộng".
9. **DocumentAIEditor**: bước LLM là copy-paste với Copilot (bmf_client.py không được GUI import). Deck giới thiệu của chính repo
   (`docs/presentation/DocumentAIEditor_紹介.pptx`) còn ghi "qua Bosch Model Farm" nên mâu thuẫn: sửa trước khi dùng.
   Một sổ tay Word thật 679 đoạn: 453 ghi được, 121 không có run, 105 bị từ chối (OUTSTANDING mục 46). XLSX chỉ đọc. EXE v1.1 chưa build.
   Từ "TCD" không xuất hiện trong repo.
10. **Outlook-RSVP**: không có nhắc tự động (Task Scheduler chưa làm); COM "verified by reading", chưa có biên bản chạy end-to-end; app thật là fork riêng đã gộp.
11. **FTA / doc-tools**: toàn bộ 32 mục I1–I26 của docs/windows-verification.md còn `[ ]`; ADR 024 ghi bạn chạy thật trên Windows và báo "ổn".
    Bối cảnh Hino / task-force không có trong repo (do bạn cung cấp). CLAUDE.md của doc-tools ghi FTA "~2100 dòng" là cũ (thật 8.189).
12. **Moda**: tài khoản free, canvas có logo Moda ở góc dưới phải khi xuất; nếu cần bản sạch thì nâng gói hoặc che bằng tay.

## SỐ LIỆU ĐÃ KIỂM CHỨNG (nguồn)

| Hạng mục | Con số | Nguồn |
|---|---|---|
| NIKK: mẫu 108 từ | 199,3 → 47 phút, −76% | sheet ẩn "Time estimate_*" (K21, P28) |
| NIKK: mô hình dự án | ≈423 giờ / 18.000 từ | ô P30 |
| NIKK: VBA | ~1.236 dòng, 17 module; 8 phiên bản 22/02–05/04/2023; lưu lần cuối 06/11/2025 | History, core.xml |
| TEF paper size | ~304 dòng VBA; lô mẫu 50/50 khớp (38 A4 + 12 A3) | Check_Paper_Size, sheet General |
| Test tự động (đếm tĩnh `def test_`) | DocAI 1.691; RSVP 329; Planner 601; doc-tools 2.853; Tracker 1.551; Shipping 950; Temperature 75 → ~8.050 | các agent, kèm lệnh |
| Khung routing (framework) | 62 manifest, 1.782 mutation; 2.092 test; 727 commit | routing-template |
| Multiple-report | 19 bài, 24 deck pptx, 777 slide, 119k từ, 122 test OK | agent + unittest |
| Temperature audit | gốc: exit 1, 2 lỗi dữ liệu (EF10, ET36) + 7 ô ghép sai; bản vá: exit 0 | `python3 -m dnox.audit` |

## NHỮNG ĐIỀU DO BẠN CUNG CẤP (không kiểm chứng được từ file/repo)
- Khoảng thời gian 02/2023–08/2024 và 09/2024–11/2026; đảm nhiệm 3 khách hàng JOEM về kỹ thuật.
- Đàm phán với team Platform để họ nhường hơn 25.000 euro giờ công cho EET1.
- Buổi sharing compliance (Procodex) cho RBJP (EET1 + project manager).
- Leader-CIP với 3 thành viên EET1, tool báo cáo nhiệt độ highlight OK/NG, database nhiệt độ, bằng khen.
- Hoạt động Digital ở EET, lộ trình tự động hóa báo giá → ECR; task force Hino (production line, QC).
Nên chuẩn bị chứng cứ độc lập (email, quyết định phân bổ giờ công, bằng khen bản scan) cho những mục này.

## KHÔNG đưa vào deck (có dữ liệu nhạy cảm)
Đường dẫn mạng nội bộ trong ô C3 / B4 / B5 của hai macro, tên khách hàng trong VBA/Workbook, mật khẩu sheet, tenant/ID Azure,
tên và email thật trong DB cũ của RSVP.

## Cập nhật 2026-11-02
Slide 10 nêu đề xuất cụ thể: nâng từ level 52 lên level 53 (do chủ repo cung cấp).

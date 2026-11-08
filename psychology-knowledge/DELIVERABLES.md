# Bản trình bày — batch F02/A01/J01

Bản xuất thật từ Moda; mẫu F01 v4 đã được người dùng duyệt. Mỗi bài do một phiên riêng dựng. Chưa tự nhận toàn bộ giáo trình hoàn thành.

| Bài | Slide | PowerPoint | PDF | Moda |
|---|---:|---|---|---|
| F02 | 37 | [PPTX](https://assets-cdn.moda.app/mcp-exports/6fc130f8-596c-4446-b9f8-3aaceb1bc64b/vcrdt-198d7ebd445879f015eeff7785be5240/pptx-r2-f0-w1-all.pptx?Expires=1824358837&KeyName=mpwa&Signature=rQWtiGYYEnVApo9ZzZih1neRfQg) | [PDF](https://assets-cdn.moda.app/mcp-exports/6fc130f8-596c-4446-b9f8-3aaceb1bc64b/vcrdt-198d7ebd445879f015eeff7785be5240/pdf-r3-f0-w1-all.pdf?Expires=1824358811&KeyName=mpwa&Signature=5fEFgUJy6JKocj9PPBzEQjaz2PM) | [Canvas](https://moda.app/canvas/6fc130f8-596c-4446-b9f8-3aaceb1bc64b?source=agent) |
| A01 | 38 | [PPTX](https://assets-cdn.moda.app/mcp-exports/c53e3ca8-b9de-4fb8-8506-65caf8644eed/vcrdt-1cab8c3a19b9006a32dd192e06cecfb6/pptx-r2-f0-w1-all.pptx?Expires=1824358987&KeyName=mpwa&Signature=1EMrL2RsF2q9djOQ55JFjVBCWY4) | [PDF](https://assets-cdn.moda.app/mcp-exports/c53e3ca8-b9de-4fb8-8506-65caf8644eed/vcrdt-1cab8c3a19b9006a32dd192e06cecfb6/pdf-r3-f0-w1-all.pdf?Expires=1824359008&KeyName=mpwa&Signature=FdK4qswR1OGRzUrfbAdUWz1t3Ws) | [Canvas](https://moda.app/canvas/c53e3ca8-b9de-4fb8-8506-65caf8644eed?source=agent) |
| J01 | 40 | [PPTX](https://assets-cdn.moda.app/mcp-exports/6ee47b5e-532d-454e-b480-3f5cfc87fa7e/vcrdt-65eca1d0612270c60f7ffce3b219a3dc/pptx-r2-f0-w1-all.pptx?Expires=1824358833&KeyName=mpwa&Signature=bP-aoWak7ujXnTlebsdpvU6rGdQ) | [PDF](https://assets-cdn.moda.app/mcp-exports/6ee47b5e-532d-454e-b480-3f5cfc87fa7e/vcrdt-65eca1d0612270c60f7ffce3b219a3dc/pdf-r3-f0-w1-all.pdf?Expires=1824358855&KeyName=mpwa&Signature=ZTFEnODda4ORIMdf-9hYaBT68eA) | [Canvas](https://moda.app/canvas/6ee47b5e-532d-454e-b480-3f5cfc87fa7e?source=agent) |

Mỗi PDF có một trang rasterized; chữ trang đó không chọn/tìm kiếm được, hình vẫn hiển thị và link vẫn dùng được. Chưa lưu binary cục bộ. Link export có thể hết hạn; tiếp tục dùng đúng canvas ghi trên để xuất lại.

Xem [sổ giữ việc](COORDINATION.md) trước khi nhận bài và [review](BATCH-02-REVIEW.md) để biết phạm vi kiểm chứng.


## Bản PowerPoint lưu trong repo (kiểm 2026-10-24)

Bốn file PPTX dưới đây được tải từ đúng link xuất Moda của từng bài (F01 từ `01-Sigmund-Freud/moda/f01-report-v4.json`, ba bài còn lại từ bảng phía trên) rồi lưu vào `visuals/` của tác giả. Đã mở từng file: zip hợp lệ và đếm slide trong file khớp số slide đã ghi. Đây là kiểm tra bản xuất, không phải review nội dung; trạng thái học thuật của từng bài giữ như đã ghi trong bài và `BATCH-02-REVIEW.md`.

| Bài | File trong repo | Slide trong file | Dung lượng | SHA-256 |
|---|---|---:|---:|---|
| F01 | [f01.pptx](01-Sigmund-Freud/visuals/f01.pptx) | 35 | 9,7 MB | `a9d9ace04060e0005b857545d0631edb268fcda153c2c8be2bb28c1b3065346c` |
| F02 | [f02.pptx](01-Sigmund-Freud/visuals/f02.pptx) | 37 | 5,8 MB | `314158908684a4837e900d164b4f3474fa2fc7715630a598ae623dac21045e4b` |
| A01 | [a01.pptx](02-Alfred-Adler/visuals/a01.pptx) | 38 | 6,4 MB | `0f48cce014591e61ca6d1bc90c959a31e2f8f1254dfe1554822207ea4fb2ce8d` |
| J01 | [j01.pptx](03-Carl-Gustav-Jung/visuals/j01.pptx) | 40 | 10,1 MB | `54a56b4557e6a39ac65d059cdfa2e5596377f6df6c2c91f65973c582fa6f6a4f` |

**PDF không lưu vào repo.** Bản PDF xuất từ Moda là bản ảnh, nặng 25–28 MB mỗi bài (khoảng 107 MB cho bốn bài), sẽ làm lịch sử git nặng vĩnh viễn. Chúng vẫn mở được qua link xuất ở bảng phía trên và trong metadata; đã kiểm số trang: F01 35, F02 37, A01 38, J01 40. Link xuất có hạn; khi hết hạn, xuất lại từ đúng canvas ghi ở `COORDINATION.md`. Nếu chủ repo muốn PDF trong repo, nên xuất bản có chữ chọn được (`flatten=false`) nhẹ hơn rồi mới lưu.

Giới hạn: PPTX mới được kiểm cấu trúc (zip, số slide), chưa mở bằng PowerPoint để xem lại từng trang; ảnh tư liệu vẫn theo ghi chú giấy phép trong các file `*-visual-sources.md`.

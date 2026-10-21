# Điều phối nhiều phiên Claude: học từ tool-marketing-studio

Ngày lập: 2026-10-21, nhánh `claude/tool-marketing-studio-coordination-vl6acx`. Nguồn: đọc `CLAUDE.md`, `AGENTS.md`, `docs/sd101-*.md`,
`docs/session-budget.md`, `docs/agent-team.md` và `scripts/sd101_claims.py`, `scripts/sd101_slides.py` của repo
`vohoailinh90/tool-marketing-studio` (commit `ebc733c`, bản sao nông). **Chỉ đọc mã và tài liệu; chưa chạy test hay script của họ.**
Bảng "đang có gì" ở mục 2 là mô tả của chính tài liệu họ; chưa kiểm GitHub issue mà họ nói có phản chiếu bảng điều phối.

## 1. Tóm tắt

Repo kia có tới 404 bài và hai tài khoản Claude, nhiều phiên chạy cùng lúc, nên họ dựng **ba lớp**:

1. **Khoá có thể đọc từ xa** (claim): mỗi phiên ghi vào git "tôi đang làm bài X" và đẩy lên nhánh của mình; phiên khác chạy `git fetch` rồi đọc
   được, không cần máy chủ riêng.
2. **Bảng phân công theo dải** (assignments): điều phối viên đặt trước cả dải bài cho từng phiên; công cụ đọc bảng này và tự bỏ qua dải đã giữ.
3. **Quy ước cho phiên chết**: nhịp tim (heartbeat), hạn 72 giờ, nhận lại bài của phiên chết bằng một lệnh.

Phần còn lại là luật cứng bằng máy (CI chặn, test chạy trên repo git thật) chứ không dựa vào việc phiên "nhớ" đọc tài liệu.

Repo này **đã có** nửa đầu của lối làm đó (mỗi bài một thư mục riêng, file dùng chung chỉ điều phối sửa, Moda chỉ chạy trong phiên điều phối).
Nó **chưa có** phần khoá: ai đang giữ bài nào chỉ thấy được bằng cách liệt kê nhánh. Đã có một lần đụng nhau thật (mục 3).

## 2. Họ làm gì, và mỗi thứ chặn kiểu chồng chéo nào

| # | Cơ chế | Cách chạy | Chặn cái gì |
|---|---|---|---|
| 1 | **Claim trước khi làm** | `sd101_claims.py claim --next N --publish` (bài viết) và `sd101_slides.py claim ...` (deck). Cấm lấy số tiếp theo trong `progress.json`. | Hai phiên cùng viết một bài |
| 2 | **Chủ khoá là tên nhánh** | `owner` = tên nhánh; trên nhánh khác chỉ tính bản ghi có `owner` đúng bằng tên nhánh đó. | Bản sao khoá cũ nằm trong nhánh cắt ra từ nhánh khác bị tính nhầm là khoá thật |
| 3 | **`--publish` chỉ đẩy nhánh của mình** | Commit đúng file khoá rồi đẩy nhánh hiện tại, từ chối `main`/`master`. Khoá chưa đẩy thì `verify` thất bại. | "Khoá" chỉ nằm trên máy, người khác không thấy |
| 4 | **Đọc mọi nhánh remote** | `git fetch` rồi `git cat-file --batch` đọc `deck.yaml` trên từng nhánh. Không đọc được remote thì thoát mã 2, không đoán. | Quyết định dựa trên thông tin cũ |
| 5 | **Phân xử khi đua** | Không có compare-and-swap trên git, nên: `claimed_at` sớm hơn thắng, hoà thì tên nhánh nhỏ hơn; bên thua thấy `verify` hỏng, phải `release` và lấy bài khác. | Hai khoá đẩy cùng lúc |
| 6 | **Hạn thuê 72 giờ** | `touch --publish` gia hạn; quá 72 giờ là "stale", nhận lại bằng `claim <id> --take-stale`. Nhịp tim ghi giờ tương lai quá 1 giờ thì coi như hết hạn. | Bài kẹt mãi vì phiên chết; đồng hồ sai |
| 7 | **Một file khoá mỗi đơn vị, hoặc dòng cách nhau** | Deck: một `deck.yaml` mỗi bài. Bài viết: `claims.jsonl` có dòng trống giữa hai bản ghi. | Hai phiên khoá hai bài khác nhau mà vẫn bị conflict khi merge |
| 8 | **Bảng phân công đọc được bằng máy** | `docs/sd101-assignments.md`: bảng `Range / Work / Branch / Status`. `board_reservations()` đọc bảng, `claim --next` bỏ qua dải đã giữ; bảng sai cú pháp thì **từ chối** thay vì đọc thiếu. Có test giữ cho bảng thật luôn đọc được. | Phiên mới nhảy vào dải mà phiên khác sắp lấy ở lượt kế |
| 9 | **Bảng điều phối viết tay** | `docs/sd101-slides-coordination.md`: ai giữ dải nào, thứ tự được đánh thức, phần việc không có khoá riêng (xuất PPTX). Nó cố ý **không ghi số đếm**; số liệu luôn lấy từ `status`. | Số trên bảng lệch số thật |
| 10 | **Giới hạn đồng thời** | Chủ repo đặt: tối đa 2 phiên của tài khoản A chạy cùng lúc; điều phối viên đánh thức từng phiên một. | Quá tải Moda và hàng đợi merge |
| 11 | **Cổng CI** | `sd101_check.py` fail nhánh có sổ khoá không khớp bài thật; hai nhánh viết cùng bài thì conflict khi merge. | Cái lọt qua mọi lớp trên không vào được `main` |
| 12 | **Tài khoản Moda** | Canvas thuộc tài khoản tạo ra nó; tài khoản kia gọi `canvas_read` ra `canvas_not_found`. Quy tắc: thấy `canvas_not_found` thì ghi vào issue cho tài khoản kia, **không dựng canvas thứ hai**. Phiên chết giữa chừng: `canvas_search` theo id bài trước rồi mới tạo. | Hai canvas cho cùng một bài |
| 13 | **Việc xác định thì để script** | `sd101_slide_brief.py` cắt bài thành vai slide, gán màu khái niệm theo số bài; `finish` kiểm bảng layout. Phiên chỉ làm phần cần phán đoán. | Hai phiên cùng một bài làm ra hai kiểu khác nhau |
| 14 | **Tự bảo vệ phiên khỏi chết giữa chừng** | Hook theo dõi ngữ cảnh: ~70% nhắc cập nhật file bàn giao, ~85% nhắc kết thúc; `SESSION-HANDOFF.md` có phần máy tự sinh và phần phiên tự viết; phát lại ở `SessionStart`. Ngân sách subagent (`route.py --record`, hook từ chối khi quá trần). | Mất việc làm dở, tốn gấp nhiều lần khi làm lại |

Quy trình PR và Codex phản biện của họ là cùng một văn bản `AGENTS.md` với repo này, nên không phải chỗ khác biệt.

Quy mô để cân nhắc việc sao chép: hai công cụ khoá dài khoảng 2.900 dòng, kèm khoảng 4.300 dòng test, thêm `sd101_check.py` 1.566 dòng. Phần lớn
là xử lý ca hiếm của 404 bài (hai bài chung nguồn, đếm thế hệ khi nhận lại, kiểm PNG/PPTX, huy hiệu Moda). Repo này không cần những phần đó.

## 3. Repo này đang ở đâu (đo ngày 2026-10-21)

Đã có, đúng hướng:
- Mỗi bài một thư mục `lessons/<id>/`, nên các phiên viết gộp nhánh không conflict.
- File dùng chung (`lessons/README.md`, `docs/*`, `scripts/*`) chỉ điều phối sửa; Moda chỉ chạy trong phiên điều phối, tuần tự
  (`docs/ban-giao-mo-rong-noi-dung.md`, mục 7 và 9).
- `lessons/<id>.spec.md` + bảng "chủ sở hữu khái niệm" (mục 4.4) chống lặp **nội dung** giữa các bài.
- `decks.py todo` tính "thiếu hoặc cũ" bằng băm `slides.json`, nên khỏi cãi nhau bài nào cần dựng lại.

Chưa có, và bằng chứng trong git:
- **Đụng số hiệu.** Nhánh `claude/awesome-curie-uuh5vu` (10 commit, chưa merge) viết "Freud, Jung và Adler" thành `L01` ngày 2026-10-20, trong khi `L01` trên
  `main` là "Bản đồ não". Cùng một số hiệu cho hai bài khác nhau; về sau bài kia được đánh lại thành `L15`. Đây đúng là lỗi mà bước 1 và 2 của mục 2 chặn.
- **Không có chỗ đọc "ai đang giữ bài nào".** Lúc lập tài liệu, `origin` có 37 nhánh; muốn biết nhánh nào còn việc chưa gộp phải so từng nhánh với `main`
  (`git rev-list --count origin/main..origin/<nhánh>`). Kết quả: 4 nhánh đang bay (`claude/lesson-L11` đến `L14`, mỗi nhánh một commit, chưa có PR, chưa phản biện),
  6 nhánh `review-*` (L01, L03, L07, mỗi bài hai nhánh a/b) còn mở, `awesome-curie-uuh5vu` (mục trên), và `lesson-L08`: nhánh này và `main` đều thêm
  `lessons/L08/L08.pptx` sau một gốc chung, tức hai lần dựng deck L08 độc lập. Không file nào trong repo nói phiên nào đang giữ chúng.
- **Nhánh đã gộp không bị xoá**, nên danh sách nhánh là tín hiệu nhiễu. Quy ước "chủ khoá là tên nhánh" của họ chỉ chạy tốt khi nhánh xong thì biến mất.
- **Không có luật phiên chết.** Phiên viết chết giữa chừng thì không ai biết bài đó còn trống hay không.
- **`docs/ban-giao-mo-rong-noi-dung.md` mục 13 là nhật ký văn xuôi.** Muốn biết ai giữ gì phải đọc cả đoạn.
- **Lịch sử deck.** Nhiều bài có nhiều hơn một commit `decks: <id>` (L16 bốn lần; L02, L04, L05, L06 hai lần). Phần lớn có thể là dựng lại hợp lệ sau khi
  `slides.json` đổi; chỉ nhìn log thì không phân biệt được với trùng việc (cặp L08 ở trên thì chắc chắn là trùng). Một bảng điều phối sẽ làm việc này rõ ràng.

## 4. Đề xuất: bản nhẹ cho repo này

**Đã làm cả hai tầng (chủ repo chọn, 2026-10-21).** Luật và bảng giữ bài: `docs/dieu-phoi.md`. Công cụ: `scripts/claims.py`, test: `tests/test_claims.py`
(repo git thật, 37 test). Chỗ khác với đề xuất bên dưới:
- Giới hạn đồng thời do công cụ ép, không chỉ ghi trong luật: 2 phiên (chủ repo). Phiên thứ ba bị từ chối khi `claim`; nếu đẩy lách thì `verify` báo thua theo thứ tự thời gian.
- Hạn thuê 24 giờ như đề xuất; chưa được chủ repo xác nhận riêng.
- Kiểm phạm vi ghi là lệnh `claims.py scope`, không phải script riêng.
- Bảng giữ bài **có** được máy đọc ở mức nhẹ (`claims.py check`: tên cột, giá trị cho phép, không quá 2 nhánh viết cùng lúc), chạy trong test và CI. Không dùng để tự động bỏ qua dải
  bài như bảng của họ; ở quy mô này `next` và `claim` đã đủ.
- Thêm ba chốt họ không có: `claim` từ chối bài đang có việc dở trên nhánh khác (bắt được `L11` đến `L14` ngay trên repo thật), từ chối bài đã viết khi thiếu `--rewrite`,
  và `check --merge-ready` trong CI chặn khoá `doing` lọt vào `main`.
- Bản chạy thử trên repo thật (chỉ đọc) mất khoảng 1 giây với 37 nhánh.

Nguyên tắc: chỉ lấy cái chống đúng lỗi đã xảy ra, đi từ rẻ đến đắt, và dừng khi hết va chạm.

### Tầng 1: luật và bảng, không thêm mã (làm ngay)

1. **`docs/dieu-phoi.md`: bảng giữ bài**, cột `Bài | Việc | Nhánh | Phiên | Trạng thái | Cập nhật`. `Việc` là một trong: viết, phản biện (a), phản biện (b), sửa,
   deck. `Trạng thái`: giao, đang làm, chờ PR, xong. Chỉ phiên điều phối sửa; phiên viết **đọc trước khi làm** và báo điều phối khi đổi trạng thái.
   Giống mục 9 của họ: **không ghi số đếm**, số liệu luôn lấy từ `decks.py todo` và `git`.
2. **Cấp số hiệu tập trung.** Chỉ điều phối cấp `L<nn>` và tạo `lessons/<id>.spec.md` **trước** khi có phiên nào viết. Phiên viết không tự chọn số; trước khi
   push, `git ls-remote --heads origin 'claude/lesson-<id>*'` và `git ls-tree` `main` không được cho thấy ai khác đã có số đó. Spec tồn tại nghĩa là bài có chủ.
3. **Quy ước nhánh = chủ khoá**: `claude/lesson-<id>` (một bài một nhánh), `claude/review-<id>-a` và `-b`, `claude/decks-<ids>`. Điều phối xoá nhánh ngay sau khi
   gộp, để danh sách nhánh phản ánh việc đang chạy.
4. **Giới hạn đồng thời**: chủ repo đặt N phiên viết cùng lúc (xem mục 5). Phản biện chạy khi bài đã đẩy; deck chỉ dựng sau khi bài qua phản biện và gộp.
5. **Luật phiên chết**: phiên viết ghi nhánh vào bảng khi nhận việc; quá 24 giờ không có commit mới thì điều phối coi là chết, mở lại bằng `create_session` trên chính
   nhánh đó (không tạo nhánh mới cho cùng một bài).
6. **Moda**: giữ nguyên "chỉ phiên điều phối, tuần tự". Thêm đúng một việc từ họ: trước khi dựng hoặc dựng lại, `canvas_search` theo id bài; thấy `canvas_not_found`
   thì hỏi chủ repo, không dựng canvas thứ hai.
7. **Kiểm phạm vi ghi bằng máy**: một script nhỏ so `git diff --name-only origin/main...HEAD` với `lessons/<id>/**`, chạy trước khi gộp nhánh viết.
   Hiện "đừng sửa file ngoài thư mục bài" chỉ nằm trong prompt, nên một phiên lỡ tay sửa `lessons/README.md` hay `scripts/` sẽ làm conflict mà không ai báo.

### Tầng 2: công cụ khoá nhỏ (làm khi tầng 1 vẫn va nhau)

`scripts/claims.py`, khoảng 200 dòng, lấy đúng cái cốt lõi của họ:
- một file `lessons/<id>/claim.json` mỗi bài (bài kia không bao giờ conflict với nó), có `owner` (tên nhánh), `claimed_at`, `heartbeat_at`, `status` (`doing`, `written`);
- `claim <id> --publish`, `touch --publish`, `release`, `status`, `verify`; `--publish` chỉ đẩy nhánh của mình, từ chối `main`;
- đọc mọi nhánh remote bằng `git fetch` + `git cat-file --batch`; không đọc được remote thì thoát mã 2;
- hạn thuê (đề xuất 24 giờ, con số của họ là 72 giờ; chủ repo chỉnh), `claim --take-stale` để nhận lại;
- đua nhau thì `claimed_at` sớm hơn thắng, hoà thì tên nhánh nhỏ hơn;
- `claim --new` cấp số tiếp theo bằng cách đọc `lessons/*.spec.md` trên `main` và mọi nhánh, nên chấm dứt đụng số hiệu;
- test chạy trên repo git thật (như `tests/test_sd101_claims.py` của họ), nối vào `python3 -m unittest discover -s tests`.

Không lấy: bài chung nguồn, chuỗi `taken_from`/`generation`, kiểm PNG/PPTX, bảng phân công đọc bằng máy. Với khoảng 20 bài và một điều phối viên, bảng
Markdown ở tầng 1 đủ; bảng đọc bằng máy chỉ đáng khi có nhiều điều phối viên.

Việc nằm trong `scripts/`, `tests/`, `docs/` và `CLAUDE.md` đi theo quy trình PR + Codex phản biện của repo (không đẩy thẳng).

## 5. Quyết định và việc còn mở

Đã trả lời (2026-10-21): tối đa **2** phiên viết cùng lúc; làm **cả hai tầng**.

Còn mở:
1. Bốn nhánh `lesson-L11..L14` đang bay: phiên điều phối nào đang giữ chúng? Bảng giữ bài ghi "chưa rõ". Phiên này **chưa đụng** tới chúng.
2. Xoá 23 nhánh đã gộp, và quyết định số phận `awesome-curie-uuh5vu` và `lesson-L08` (liệt kê trong `docs/dieu-phoi.md`).
3. Hạn thuê 24 giờ có hợp không.

# Điều phối nhiều phiên: ai giữ bài nào

Nhiều phiên Claude cùng làm trong repo này, mỗi phiên trong một container riêng và trên một nhánh riêng. Chúng chỉ nhìn thấy nhau qua remote git.
Tài liệu này là luật và bảng giữ bài; công cụ là `scripts/claims.py`. Nghiên cứu nguồn gốc (cách tool-marketing-studio làm) nằm ở
`docs/dieu-phoi-nhieu-phien.md`.

**Quyết định của chủ repo (2026-10-21): tối đa 2 phiên viết chạy cùng lúc.** Phiên phản biện (chỉ đọc) không tính. Deck chỉ phiên điều phối dựng.

## Luật

1. **Chỉ điều phối cấp số hiệu.** Số bài mới lấy bằng `python3 scripts/claims.py next`; điều phối tạo `lessons/<id>.spec.md` và
   `lessons/<id>.expected.json`, đưa lên `main` bằng PR, **rồi** mới giao cho phiên viết. Phiên viết không tự chọn số. (Lần `L01` bị hai phiên
   dùng cho hai bài khác nhau, 2026-10-20, là lỗi mà luật này chặn.)
2. **Claim trước khi viết.** Phiên viết tạo nhánh `claude/lesson-<id>` từ `main` mới nhất, chạy `claims.py claim <id> --publish`. Bị từ chối (thoát 1) thì
   **dừng và báo điều phối**, không đổi sang cách khác để lách. Thoát 2 là không đọc được remote: sửa mạng, không đoán.
3. **Một bài một nhánh một chủ.** Tên nhánh là chủ khoá. Nhánh: `claude/lesson-<id>` (viết, sửa), `claude/review-<id>-a` và `-b` (phản biện, chỉ đọc),
   `claude/decks-<ids>` (điều phối dựng deck). Đừng đổi tên nhánh đang giữ khoá (khoá mồ côi): `release` trước.
4. **Phiên viết chỉ ghi trong `lessons/<id>/`** (và file khoá `lessons/<id>.claim.json`). Không sửa `expected.json`, `lessons/README.md`, `docs/`, `scripts/`,
   `CLAUDE.md`. Trước khi báo xong: `claims.py scope <id>` phải thoát 0.
5. **Giữ nhịp tim.** Mỗi vài giờ và trước mỗi lần push: `claims.py touch --publish`. Khoá im quá **24 giờ** là "stale": ai cũng nhận lại được bằng
   `claim <id> --take-stale`, và phiên cũ nếu tỉnh dậy thì thua (`verify` báo). Khoá của chính mình đã quá hạn thì `touch` không gia hạn được: `claim <id> --publish` lại, và chỉ được khi còn chỗ trong 2 phiên. Hạn 24 giờ do chủ repo chốt (2026-10-21); đổi `LEASE_HOURS` trong script nếu cần.
6. **Xong thì `finish`.** `claims.py finish <id> --publish` (cần `lessons/<id>/lesson.md`), commit file khoá cùng bài. PR mang khoá `doing` sẽ bị
   `claims.py check --merge-ready` chặn (CI chạy lệnh này).
7. **Bài đã viết xong muốn viết lại hoặc sửa** cần cờ `--rewrite` (điều phối bảo thì mới dùng). Bài đang có việc dở trên nhánh khác bị từ chối trừ khi
   điều phối bảo dùng `--ignore-drafts`.
8. **Moda chỉ trong phiên điều phối, tuần tự.** Trước khi dựng hay dựng lại, `canvas_search` theo id bài; thấy `canvas_not_found` (canvas của tài khoản Moda
   khác) thì hỏi chủ repo, không dựng canvas thứ hai.
9. **Gộp xong thì xoá nhánh.** Điều phối xoá nhánh đã gộp để danh sách nhánh chỉ còn việc đang chạy.

## Bảng giữ bài

Chỉ phiên điều phối sửa. Không ghi số đếm (số liệu lấy từ `claims.py status` và `decks.py todo`). `claims.py check` đọc bảng này: cột đúng tên, giá trị
trong tập cho phép, và không quá 2 nhánh cùng ở `viết`/`sửa` với trạng thái `giao` hoặc `đang làm`.

Việc: `viết`, `phản biện a`, `phản biện b`, `sửa`, `deck`. Trạng thái: `giao`, `đang làm`, `chờ phản biện`, `chờ PR`, `xong`.

| Bài | Việc | Nhánh | Phiên | Trạng thái | Cập nhật |
|---|---|---|---|---|---|
| L11 | sửa | `claude/lesson-L11` | session_01G8FY… | xong | 2026-10-22 |
| L12 | sửa | `claude/lesson-L12` | session_01APRS… | đang làm | 2026-10-22 |
| L13 | viết | `claude/lesson-L13` | session_013hwz… | chờ phản biện | 2026-10-22 |
| L14 | viết | `claude/lesson-L14` | session_012AtG… | chờ phản biện | 2026-10-22 |

Ghi chú về bốn dòng trên: nhánh đã đẩy một commit `lesson: <id> thêm bài` mỗi nhánh, chưa có PR, chưa có nhánh phản biện. Phiên nào viết chúng chưa
được xác nhận, nên cột Phiên ghi "chưa rõ". Chúng viết trước khi có công cụ này nên không có file khoá; `claims.py claim` vẫn từ chối các id này vì thấy
việc dở trên nhánh (`unmerged work`).

### Nhánh tồn đọng (chủ repo để xoá sau, 2026-10-21: chưa xoá nhánh nào)

- 23 nhánh đã gộp vào `main` (`git branch -r --merged origin/main`): xoá được không mất việc.
- `claude/awesome-curie-uuh5vu` (10 commit): bài Freud, Jung và Adler đánh số `L01`; trên `main` bài này là `L15`, `L01` là bản đồ não. Nhánh này không gộp được
  mà không đè `L01`.
- `claude/lesson-L08` (3 commit): dựng deck L08 lần thứ hai; `main` đã có `L08.pptx` từ PR #10.
- `claude/review-L01-a/b`, `review-L03-a/b`, `review-L07-a/b`: phản biện đã đẩy, chưa gộp; chưa kiểm xem còn khớp bản bài hiện tại không.

## Lệnh

Phiên viết:

```bash
git fetch origin && git checkout -b claude/lesson-L17 origin/main
python3 scripts/claims.py status                  # ai đang viết gì (tối đa 2), số kế tiếp
python3 scripts/claims.py claim L17 --publish     # thoát 0 mới được viết
# ... viết lessons/L17/ ...
python3 scripts/claims.py touch --publish         # mỗi vài giờ và trước mỗi push
python3 scripts/claims.py verify                  # thoát 0 = khoá còn của mình và đã đẩy
python3 scripts/claims.py scope L17               # chỉ đụng lessons/L17/ và khoá của nó
python3 scripts/claims.py finish L17 --publish    # xong; commit khoá cùng bài
python3 scripts/claims.py release L17 --publish   # bỏ không viết nữa
```

Điều phối:

```bash
python3 scripts/claims.py next                    # số mới; tạo spec + expected.json rồi PR vào main
python3 scripts/claims.py status                  # ai giữ gì, bài dở trên nhánh nào
python3 scripts/claims.py check --merge-ready     # trước khi gộp một nhánh viết
python3 scripts/claims.py claim L17 --take-stale --publish   # nhận lại bài của phiên đã chết
```

## Cái công cụ chặn, và cái nó không chặn

Chặn: hai phiên viết cùng một bài; phiên thứ ba khi đã có hai phiên viết; cấp trùng số hiệu; viết đè bài đã có hoặc bài đang dở trên nhánh khác; khoá của
phiên chết giữ bài mãi; phiên viết sửa file ngoài bài của nó; khoá `doing` lọt vào `main`.

Không chặn: git không có compare-and-swap, nên hai phiên claim cùng lúc vẫn có thể cùng đẩy. Khi đó khoá có `claimed_at` sớm hơn thắng (hoà thì tên nhánh
nhỏ hơn) và phiên thua thấy `verify` thoát 1: bỏ bài đó, `release`, không đẩy bản nháp. Việc thua chỉ mất việc của phiên thua, không bao giờ có hai bài
trùng trên `main`. Công cụ cũng không giữ chỗ cho phản biện và deck (đã tách theo nhánh và theo luật 8); giới hạn 2 đếm theo nhánh có khoá `doing`, không
đếm theo phiên.

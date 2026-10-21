# Multiple-report: bài học đa ngành

Kho lưu những gì chủ repo đã hỏi Claude (thần kinh, não bộ, triết học, sức khỏe, quản lý dự án, kỹ thuật...),
mỗi chủ đề thành một bài học tiếng Việt có nguồn và một file PowerPoint, để đọc lại thay vì hỏi lại.

Quy trình hiện tại (chủ repo đặt, tạm thời): Claude thiết kế và tự viết bài trong phiên chính, Codex phản biện mỗi pull
request, Claude làm deck bằng Moda sau khi merge. Quy trình `team-lesson` của
[claude-agent-routing-template](https://github.com/vohoailinh90/claude-agent-routing-template/blob/main/docs/vps-team-lesson.md)
(model miễn phí trên VPS viết) tạm dừng cho đến khi chủ repo bật lại.

## Làm việc tự chủ

Chủ repo đã cho phép trước mọi việc trong repo này: tạo, sửa bài học, làm deck bằng Moda, xuất PPTX, commit và
push. Làm đến hết việc được giao, không dừng để xin xác nhận từng bước. Chỉ hỏi khi một quyết định về nội dung
thật sự thuộc về chủ repo (bài nói về điều gì), hoặc khi một công cụ từ chối và không có cách khác.

- Không giao việc Moda cho subagent: mỗi lệnh của subagent lại chờ chủ repo duyệt. Mọi lệnh Moda chạy trong
  phiên chính.
- Gộp lệnh: dựng mỗi deck bằng ít lệnh nhất có thể; không chụp màn hình sau mỗi lần sửa (tối đa một lần cuối).
- Quyền tool đã có trong `.claude/settings.json`. Nếu vẫn bị hỏi duyệt, báo một lần tên tool cần thêm, rồi làm tiếp.

## Cấu trúc một bài

```text
lessons/<id>.expected.json   các kiểm tra của gate (Claude viết khi thiết kế bài, trước khi viết lesson.md; không sửa để gate qua)
lessons/<id>/lesson.md       bài học
lessons/<id>/slides.json     dàn ý slide đã duyệt
lessons/<id>/<id>.pptx       deck Moda (chỉ PPTX; không PNG, không PDF)
lessons/<id>/deck.json       hash của slides.json mà deck được dựng từ đó (scripts/decks.py record)
lessons/README.md            mục lục, sinh bởi scripts/decks.py index
```

`lesson.md`:
- front matter `---` với `id`, `title`, `topic`, `date` (YYYY-MM-DD), rồi `# <title>`;
- `topic` là một trong `than-kinh`, `nao-bo`, `triet-hoc`, `suc-khoe`, `quan-ly-du-an`, `ky-thuat`, `khac`;
- các mục `## ` theo spec; bài sức khỏe (hoặc có nội dung y tế) có `## Lưu ý` (không phải lời khuyên y tế);
  mục cuối luôn là `## Nguồn tham khảo` với mỗi nguồn một dòng `- [S1] tác giả, tên, năm, URL`;
- tiếng Việt có dấu; thuật ngữ kèm tiếng Anh trong ngoặc lần đầu; trích dẫn `[S1]` ngay sau ý;
- không bịa nguồn, số liệu, nghiên cứu, ngày tháng hay câu trích. Thiếu nguồn thì viết ý không kèm số liệu.

`slides.json`: `{"title", "subtitle", "slides": [{"title", "bullets", "notes", "section", "sources", "layout", "tone"}]}`,
thêm hai trường tuỳ chọn:
- `body`: đoạn giải thích hiện **trên slide**, 60–110 chữ (gate nhận 40–130), `[S1]` ngay sau ý, `**từ khoá**` được tô màu khái niệm.
  Chỉ dùng cho layout `explainer` (bắt buộc ở đó) và `annotated-figure` (40–70 chữ).
- `facts`: mảng 3–6 cặp `{"label", "text"}` (nhãn ≤ 40, chữ ≤ 160 ký tự) cho layout `profile-card` (thẻ hồ sơ của một bộ phận,
  chất dẫn truyền hay cảm xúc).

Slide giải thích dùng `body`; slide sơ đồ (`flow`, `card-grid`, `layers`...) vẫn dùng gạch ngắn (≤ 160 ký tự, ≤ 6 gạch; layout
`references` ≤ 18 nguồn). `notes` là lời giảng 80–200 chữ: ví dụ, chỗ dễ nhầm. Mỗi mục `## ` có ít nhất một slide; bài theo chuẩn
đào sâu (`docs/ban-giao-mo-rong-noi-dung.md`, mục 3) có ít nhất ba slide mỗi mục nội dung. `lessons/<id>.spec.md` là spec của bài
(điều phối viết, phiên viết đọc). Kiểm: `python3 scripts/deckgen/check_lesson.py . <id>`.

## Làm deck (PPTX) bằng Moda

Phong cách và quy trình: **`docs/deck-style.md`** (font, màu, footer, cách vẽ 17 kiểu layout, màu của từng khái niệm),
lấy từ deck System Design của tool-marketing-studio. Markup từng trang sinh bằng `scripts/deckgen/gen.py`.

1. `git pull`, rồi `python3 scripts/decks.py todo`: danh sách bài thiếu deck hoặc deck cũ. Làm tất cả.
2. Mỗi bài: đọc `slides.json` (không thêm ý mới). Một canvas, bìa tối rồi mỗi phần tử một slide theo đúng `layout` và
   `tone` của nó; nguồn `[S1]` ở chân slide. Logo Moda trên slide là chấp nhận được.
3. Xem mọi slide (ba trang một lệnh chụp), sửa một lần. Xuất **PPTX** (không PNG), tải về `lessons/<id>/<id>.pptx`,
   rồi `python3 scripts/decks.py record <id> --canvas <URL>`.
4. Hết bài: `python3 scripts/decks.py todo` không in gì; `python3 scripts/decks.py index`; commit
   (`decks: <ids>`) và push; báo link canvas của từng bài.

## Kiểm tra

`python3 -m unittest discover -s tests` (CI chạy lệnh này). Gate cấu trúc trong repo: `scripts/deckgen/check_lesson.py`
(có test). Gate `lesson_gates.py` của pipeline `team-lesson` nằm ở repo template; bản `f80c4cc` (2026-10-20) chỉ nhận 7 trường
slide (không `images`, `body`, `facts`), 12 layout (không `figure` và 4 layout mới), không nhận khóa lạ trong `expected.json` và mặc định
tối đa 20 slide, nên các bài có hình hoặc theo chuẩn đào sâu chưa chạy được qua pipeline đó cho đến khi repo template được cập nhật.
Claude chạy gate đó bằng tay khi viết bài (`team-lesson` đang tạm dừng).

<!-- team-onboarding:start -->
## Team agent process

`vohoailinh90/Multiple-report` is registered with the free-model team: `team` (Claude leads) and `team-codex` (Codex leads), with free models writing the tests, the code and a pre-review. The details are in `docs/TEAM.md`; the settings that differ per repository live in `repos.conf` on the VPS, not here.

**Paused:** The free-model VPS team (team, team-codex, team-lesson) is paused for this repository by the owner. Do not run team new, team run, team push or team-lesson new here. Claude designs and writes in the main session and Codex reviews each pull request until the owner turns the team back on.

- Base branch `main`; sensitivity `private`; gates setup none (nothing to install); suggested test commands `python3 -m unittest discover -s tests`.
- If you are a team worker (tester, coder or reviewer), follow the handoff files you are given and touch only the files the task names. Never edit CI (`.github/`), agent instructions (`CLAUDE.md`, `AGENTS.md`, `.claude/`, `.codex/`), lockfiles or `repos.conf` unless the task says so.

If you are Claude Code or Codex working on this repository directly (a spec, an audit or an ordinary change), this is the pull-request process:

- When your work here is ready to ship, open the pull request yourself; do not wait to be asked, unless the user asked for a local change only or this repository's own rules say a pull request is opened only on request.
- As soon as it is open, ask Codex for a review with one comment on the PR: `@codex review` (add `@codex security review` where this repository's rules, or the change itself, call for one: authentication, authorization, secrets, payments, personal data). Codex never reviews on its own here. Ask once per head commit for each review command, never while a request is unanswered, and never mention Codex in the PR description or a commit message. Where the repository has `scripts/codex_round_count.py`, run it before each request.
- Check each finding against the code. Confirmed: fix it, with a regression test where the defect has testable behavior (a prose-only fix keeps the repository's normal checks instead), push, and ask again on the new head. Wrong: answer on its thread with the evidence. There is no cap on rounds; a rejected P2/P3 stands and blocks nothing; a P0/P1 you cannot settle goes to the repository owner and the PR is not merged.
- Merge it yourself, without waiting for approval, once all of these hold on the current head: every review this change requires (the standard review, plus the security review where it touches authentication, authorization, secrets, payments or personal data) has been requested of that exact commit and has no finding left (a bare thumbs-up is not a review, unless this repository's own rules accept one for that exact request), CI is green, there is no merge conflict, and the base branch's protection (or a merge queue) requires branches to be up to date and applies to admins, and the identity that merges has no bypass of it (ruleset bypass list, custom role or app privilege). Immediately before merging, re-read the PR head and the base head: if the PR head moved, review it again; if the base moved, merge it in and re-validate. Merge scoped to the validated head SHA. If that protection is missing, do not merge: leave the PR open, say it is clean and why it was not merged, and tell the owner.
- If Codex gives no sign of life within 10 minutes, retry once per head; an explicit error or usage-limit reply needs no wait before that one retry. If it acknowledges but never delivers a review, or its task fails, do not retry: the PR is BLOCKED. The PR is also BLOCKED when the retry gets no answer. A BLOCKED PR stays open and is reported once; never merge it unreviewed, and never use another route (API, CLI, Action) to get a review.

Exceptions in this repository, which replace the matching rule above:

- Current process (set by the owner, temporary): Claude designs and writes the code or the lesson in the main session, Codex critiques every pull request (`@codex review` on each head, as the review step above says).
- Claude scores the requirement with scripts/route.py of the template repo and keeps to the agent budget of its tier; Codex never designs or edits here, it only reviews, and a finding is checked against the code before it is fixed or answered.
- Claude writes lessons/<id>.expected.json itself when it designs a lesson (the tester that used to write it is not running), from its own outline and sources and before writing lesson.md; after that it is not edited to make the gate pass. Claude then runs the structure gate by hand: `python3 <template>/scripts/team/lesson/lesson_gates.py lessons/<id> --expect lessons/<id>.expected.json` (lesson_gates.py is in the template repo, scripts/team/lesson/).
- The deck (lessons/<id>/<id>.pptx) is built by Claude with Moda in the main session, never by a subagent; record it with `python3 scripts/decks.py record`.
- A new or changed lesson (lesson.md, slides.json, expected.json) goes through the pull-request process above like any other change. Only deck commits (`decks: <ids>`, the pptx and its deck.json) are pushed straight to the branch, as CLAUDE.md "Lam viec tu chu" allows; the pull-request process also covers scripts/, tests/, docs/ and the agent files.

Where this repository documents its own rule for one of these steps elsewhere (who merges, what gates a merge, how the review is requested, a cap on rounds), that rule governs that step; this process covers whatever the repository leaves unsaid.
<!-- team-onboarding:end -->

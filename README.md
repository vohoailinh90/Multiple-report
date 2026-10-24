# Multiple-report

Bài học và report đa ngành: thần kinh, não bộ, triết học, sức khỏe, quản lý dự án, kỹ thuật... Mỗi bài là một
câu hỏi mình từng hỏi Claude, được tổng hợp thành bài học tiếng Việt có nguồn và một file PowerPoint, để sau
này đọc lại thay vì hỏi lại.

Mục lục: [`lessons/README.md`](lessons/README.md).

## Một bài được làm ra thế nào

Hiện tại (chủ repo đặt, tạm thời): Claude thiết kế và tự viết bài trong phiên chính, Codex phản biện mỗi pull request,
rồi Claude + Moda dựng deck. Team model miễn phí trên VPS (`team-lesson`) tạm dừng, xem mục cuối.

```text
mình hỏi Claude  →  Claude (kiến trúc sư) viết dàn ý, nguồn, slide plan
                 →  Claude viết lesson.md + slides.json, tự chạy gate cấu trúc (lesson_gates.py)
                 →  PR → Codex review → sửa đến khi sạch → merge
                 →  Claude + Moda dựng lessons/<id>/<id>.pptx
```

Quy trình và quy tắc PR: [`docs/TEAM.md`](docs/TEAM.md).

### Quy trình VPS `team-lesson` (tạm dừng, không dùng khi quy trình hiện tại còn hiệu lực)

Luồng cũ: Claude viết spec, model miễn phí trên VPS viết `lesson.md` + `slides.json` và phản biện, script kiểm cấu trúc,
Claude audit. Chi tiết cài đặt và lệnh: [`docs/vps-team-lesson.md`](https://github.com/vohoailinh90/claude-agent-routing-template/blob/main/docs/vps-team-lesson.md)
trong repo template. Chỉ chạy lại khi chủ repo bật lại:

```bash
team-lesson new L02 --repo git@github.com:vohoailinh90/Multiple-report.git
nano /srv/team-lesson/work/L02/request.md
cd /srv/team-lesson/work/L02 && claude          # dán: team-lesson prompt lesson-spec L02
team-lesson run L02 --detach
team-lesson prompt lesson-audit L02             # Claude audit → verdict.md
team-lesson push L02                            # rồi mở PR và merge
cd ~/Multiple-report && git pull && claude      # dán: team-lesson prompt lesson-deck L02
```

### Làm deck không bị hỏi duyệt từng bước

`.claude/settings.json` đã cho phép mọi tool Moda trong Claude Code. Trên ứng dụng Claude / claude.ai: Settings →
Connectors → Moda, đặt các tool thành luôn cho phép. `CLAUDE.md` dặn Claude tự làm đến hết, không dùng subagent.

## Cấu trúc

```text
lessons/<id>/lesson.md     bài học
lessons/<id>/slides.json   dàn ý slide
lessons/<id>/<id>.pptx     file PowerPoint (Moda)
lessons/<id>/deck.json     deck được dựng từ slides.json nào
scripts/decks.py           bài nào còn thiếu deck, mục lục
```

## Kho tâm lý học chuyên sâu

[Psychology Knowledge — Freud, Adler, Jung](psychology-knowledge/README.md): kiến trúc và curriculum đề xuất cho 60 bài, triển khai theo phase sau phê duyệt; hiện chưa có bài mới hoàn thành.

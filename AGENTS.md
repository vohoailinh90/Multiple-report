# AGENTS.md

This repository's working rules are in `CLAUDE.md`; read it as well as this file.

<!-- team-onboarding:start -->
## Team agent process

`vohoailinh90/Multiple-report` is registered with the free-model team: `team` (Claude leads) and `team-codex` (Codex leads), with free models writing the tests, the code and a pre-review. The details are in `docs/TEAM.md`; the settings that differ per repository live in `repos.conf` on the VPS, not here.

- Base branch `main`; sensitivity `private`; gates setup none (nothing to install); suggested test commands `python3 -m unittest discover -s tests`.
- If you are a team worker (tester, coder or reviewer), follow the handoff files you are given and touch only the files the task names. Never edit CI (`.github/`), agent instructions (`CLAUDE.md`, `AGENTS.md`, `.claude/`, `.codex/`), lockfiles or `repos.conf` unless the task says so.

If you are Claude Code or Codex working on this repository directly (a spec, an audit or an ordinary change), this is the pull-request process:

- When your work here is ready to ship, open the pull request yourself; do not wait to be asked, unless the user asked for a local change only or this repository's own rules say a pull request is opened only on request.
- As soon as it is open, ask Codex for a review with one comment on the PR: `@codex review` (add `@codex security review` where this repository's rules, or the change itself, call for one: authentication, authorization, secrets, payments, personal data). Codex never reviews on its own here. Ask once per head commit for each review command, never while a request is unanswered, and never mention Codex in the PR description or a commit message. Where the repository has `scripts/codex_round_count.py`, run it before each request.
- Check each finding against the code. Confirmed: fix it, with a regression test where the defect has testable behavior (a prose-only fix keeps the repository's normal checks instead), push, and ask again on the new head. Wrong: answer on its thread with the evidence. There is no cap on rounds; a rejected P2/P3 stands and blocks nothing; a P0/P1 you cannot settle goes to the repository owner and the PR is not merged.
- Merge it yourself, without waiting for approval, once all of these hold on the current head: every review this change requires (the standard review, plus the security review where it touches authentication, authorization, secrets, payments or personal data) has been requested of that exact commit and has no finding left (a bare thumbs-up is not a review, unless this repository's own rules accept one for that exact request), CI is green, there is no merge conflict, and the base branch's protection (or a merge queue) requires branches to be up to date and applies to admins, and the identity that merges has no bypass of it (ruleset bypass list, custom role or app privilege). Immediately before merging, re-read the PR head and the base head: if the PR head moved, review it again; if the base moved, merge it in and re-validate. Merge scoped to the validated head SHA. If that protection is missing, do not merge: leave the PR open, say it is clean and why it was not merged, and tell the owner.
- If Codex gives no sign of life within 10 minutes, retry once per head; an explicit error or usage-limit reply needs no wait before that one retry. If it acknowledges but never delivers a review, or its task fails, do not retry: the PR is BLOCKED. The PR is also BLOCKED when the retry gets no answer. A BLOCKED PR stays open and is reported once; never merge it unreviewed, and never use another route (API, CLI, Action) to get a review.

Exceptions in this repository, which replace the matching rule above:

- Current process (set by the owner, temporary): Claude designs and writes the code or the lesson in the main session, Codex critiques every pull request (`@codex review` on each head, as the review step above says). The free-model VPS team (`team-lesson`, docs/vps-team-lesson.md in the template repo) is not used while this holds; no `team new` or `team-lesson new` run is started.
- Claude scores the requirement with scripts/route.py of the template repo and keeps to the agent budget of its tier; Codex never designs or edits here, it only reviews, and a finding is checked against the code before it is fixed or answered.
- A lesson's structure is judged by lesson_gates.py (template repo, scripts/team/lesson/) against lessons/<id>.expected.json, which Claude runs by hand when it writes a lesson: `python3 <template>/scripts/team/lesson/lesson_gates.py lessons/<id> --expect lessons/<id>.expected.json`.
- The deck (lessons/<id>/<id>.pptx) is built by Claude with Moda in the main session, never by a subagent; record it with `python3 scripts/decks.py record`.
- Lessons and decks are personal notes and are committed and pushed as CLAUDE.md "Lam viec tu chu" allows; the pull-request process above applies to changes to scripts/, tests/, docs/ and the agent files.

Where this repository documents its own rule for one of these steps elsewhere (who merges, what gates a merge, how the review is requested, a cap on rounds), that rule governs that step; this process covers whatever the repository leaves unsaid.
<!-- team-onboarding:end -->

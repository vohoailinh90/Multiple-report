"""scripts/claims.py: sessions are real git clones of one bare remote, so what one session pushes is what the others read."""

from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("claims", ROOT / "scripts" / "claims.py")
claims = importlib.util.module_from_spec(spec)
sys.modules["claims"] = claims  # @dataclass looks its module up
spec.loader.exec_module(claims)

START = dt.datetime(2026, 10, 21, 8, 0, 0, tzinfo=dt.timezone.utc)
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@example.com", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


def run(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True).stdout


class Sessions(unittest.TestCase):
    """origin.git holds main with L01 written and the specs of L02..L04; every session is a clone on its own branch."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        patcher = mock.patch.dict(os.environ, GIT_ENV)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.clock = START
        clock = mock.patch.object(claims, "now", lambda: self.clock)
        clock.start()
        self.addCleanup(clock.stop)
        self.origin = self.tmp / "origin.git"
        run(self.tmp, "init", "-q", "--bare", "-b", "main", str(self.origin))
        seed = self.clone("seed")
        (seed / "lessons" / "L01").mkdir(parents=True)
        (seed / "lessons" / "L01" / "lesson.md").write_text("# L01\n", encoding="utf-8")
        for number in (1, 2, 3, 4):
            (seed / "lessons" / f"L0{number}.spec.md").write_text("spec\n", encoding="utf-8")
        run(seed, "add", "-A")
        run(seed, "commit", "-q", "-m", "seed")
        run(seed, "push", "-q", "origin", "HEAD:main")
        self.seed = seed

    def clone(self, name: str) -> Path:
        path = self.tmp / name
        run(self.tmp, "clone", "-q", str(self.origin), str(path))
        return path

    def session(self, name: str, base: str = "main") -> Path:
        path = self.clone(name)
        run(path, "checkout", "-q", "-B", f"claude/{name}", f"origin/{base}")
        return path

    def cli(self, where: Path, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = claims.main(list(args), root=where)
        return code, out.getvalue()

    def push_file(self, where: Path, name: str, text: str, branch: str | None = None) -> None:
        path = where / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        run(where, "add", "-A")
        run(where, "commit", "-q", "-m", "add " + name)
        run(where, "push", "-q", "origin", f"HEAD:refs/heads/{branch or run(where, 'branch', '--show-current').strip()}")

    def rival_claim(self, where: Path, lesson: str, minutes: int = 1) -> None:
        """A claim another session pushed before it could see ours: written by hand, as a lost race leaves it."""
        moment = claims.stamp(self.clock + dt.timedelta(minutes=minutes))
        owner = run(where, "branch", "--show-current").strip()
        record = {"id": lesson, "status": "doing", "owner": owner, "claimed_at": moment, "heartbeat_at": moment}
        self.push_file(where, f"lessons/{lesson}.claim.json", claims.render(record))


class ClaimTests(Sessions):
    def test_a_claim_is_one_commit_on_my_branch_and_the_others_read_it(self):
        a, b = self.session("a"), self.session("b")
        code, out = self.cli(a, "claim", "L02", "--publish")
        self.assertEqual(code, 0, out)
        self.assertEqual(run(a, "show", "--name-only", "--format=", "HEAD").split(), ["lessons/L02.claim.json"])
        self.assertIn("lessons/L02.claim.json", run(self.origin, "ls-tree", "-r", "--name-only", "claude/a"))
        self.assertNotIn("L02.claim.json", run(self.origin, "ls-tree", "-r", "--name-only", "main"))
        self.assertIn("L02\tdoing\tclaude/a", self.cli(b, "status")[1])

    def test_a_held_lesson_is_refused(self):
        a, b = self.session("a"), self.session("b")
        self.cli(a, "claim", "L02", "--publish")
        code, out = self.cli(b, "claim", "L02", "--publish")
        self.assertEqual(code, 1)
        self.assertIn("held by claude/a", out)
        self.assertFalse((b / "lessons" / "L02.claim.json").exists())

    def test_the_third_session_is_refused_while_two_write(self):
        a, b, c = self.session("a"), self.session("b"), self.session("c")
        self.cli(a, "claim", "L02", "--publish")
        self.cli(b, "claim", "L03", "--publish")
        code, out = self.cli(c, "claim", "L04", "--publish")
        self.assertEqual(code, 1)
        self.assertIn("limit is 2", out)
        self.assertIn("writing now: 2 of 2", self.cli(c, "status")[1])

    def test_a_session_may_hold_several_lessons_and_still_counts_once(self):
        a, b = self.session("a"), self.session("b")
        self.assertEqual(self.cli(a, "claim", "L02", "L03", "--publish")[0], 0)
        self.assertEqual(self.cli(b, "claim", "L04", "--publish")[0], 0)

    def test_the_session_that_pushed_over_the_limit_loses_on_verify(self):
        a, b, c = self.session("a"), self.session("b"), self.session("c")
        self.cli(a, "claim", "L02", "--publish")
        self.clock += dt.timedelta(minutes=1)
        self.cli(b, "claim", "L03", "--publish")
        self.rival_claim(c, "L04", minutes=1)
        run(c, "reset", "-q", "--hard")  # keep the working tree as the push left it
        code, out = self.cli(c, "verify")
        self.assertEqual(code, 1)
        self.assertIn("were writing before you", out)
        self.assertEqual(self.cli(a, "verify")[0], 0)
        self.assertEqual(self.cli(b, "verify")[0], 0)

    def test_the_earlier_claim_wins_a_race_for_one_lesson(self):
        a, b = self.session("a"), self.session("b")
        self.cli(a, "claim", "L02", "--publish")
        self.rival_claim(b, "L02", minutes=1)
        code, out = self.cli(b, "verify")
        self.assertEqual(code, 1)
        self.assertIn("held by claude/a", out)
        self.assertEqual(self.cli(a, "verify")[0], 0)

    def test_an_unknown_id_is_refused_and_new_takes_the_next_free_one(self):
        a = self.session("a")
        code, out = self.cli(a, "claim", "L40")
        self.assertEqual(code, 1)
        self.assertIn("no file or folder", out)
        self.assertEqual(self.cli(a, "claim", "--new", "--publish")[0], 0)
        self.assertTrue((a / "lessons" / "L05.claim.json").is_file())

    def test_the_next_id_counts_files_on_every_branch(self):
        d = self.session("d")
        self.push_file(d, "lessons/L07.spec.md", "spec\n")
        self.assertEqual(self.cli(self.session("a"), "next")[1].strip(), "L08")

    def test_an_id_from_a_malformed_name_is_refused(self):
        code, out = self.cli(self.session("a"), "claim", "17")
        self.assertEqual(code, 1)
        self.assertIn("not a lesson id", out)

    def test_a_claim_nobody_pushed_does_not_verify(self):
        a = self.session("a")
        self.assertEqual(self.cli(a, "claim", "L02")[0], 1)
        code, out = self.cli(a, "verify")
        self.assertEqual(code, 1)
        self.assertIn("only in your working tree", out)

    def test_the_default_branch_is_never_claimed_on(self):
        code, out = self.cli(self.clone("m"), "claim", "L02", "--publish")
        self.assertEqual(code, 1)
        self.assertIn("work branch", out)

    def test_an_unreadable_remote_is_exit_2(self):
        a = self.session("a")
        run(a, "remote", "set-url", "origin", str(self.tmp / "missing.git"))
        self.assertEqual(self.cli(a, "claim", "L02")[0], 2)
        self.assertEqual(self.cli(a, "status")[0], 2)

    def test_release_gives_the_lesson_back(self):
        a, b = self.session("a"), self.session("b")
        self.cli(a, "claim", "L02", "--publish")
        self.assertEqual(self.cli(a, "release", "L02", "--publish")[0], 0)
        self.assertEqual(self.cli(b, "claim", "L02", "--publish")[0], 0)

    def test_releasing_a_claim_that_was_never_committed_is_clean(self):
        a = self.session("a")
        self.cli(a, "claim", "L02")
        self.assertEqual(self.cli(a, "release", "L02", "--publish")[0], 0)
        self.assertFalse((a / "lessons" / "L02.claim.json").exists())

    def test_a_copy_of_a_claim_on_someone_elses_branch_is_not_a_claim(self):
        a = self.session("a")
        self.cli(a, "claim", "L02", "--publish")
        c = self.clone("c")
        run(c, "checkout", "-q", "-b", "claude/c", "origin/claude/a")  # cut from a's branch: its file names a as owner
        run(c, "push", "-q", "origin", "claude/c")
        out = self.cli(self.session("b"), "status")[1]
        self.assertIn("origin/claude/a", out)
        self.assertNotIn("origin/claude/c", out)

    def test_a_written_lesson_needs_rewrite(self):
        a = self.session("a")
        code, out = self.cli(a, "claim", "L01")
        self.assertEqual(code, 1)
        self.assertIn("--rewrite", out)
        self.assertEqual(self.cli(a, "claim", "L01", "--rewrite", "--publish")[0], 0)

    def test_unmerged_work_on_a_lesson_by_another_branch_blocks_the_claim(self):
        d = self.session("d")
        self.push_file(d, "lessons/L03/lesson.md", "draft\n")
        a = self.session("a")
        code, out = self.cli(a, "claim", "L03")
        self.assertEqual(code, 1)
        self.assertIn("claude/d already carries unmerged work", out)
        self.assertIn("unmerged work on lessons/L03/: claude/d", self.cli(a, "status")[1])
        self.assertEqual(self.cli(a, "claim", "L03", "--ignore-drafts", "--publish")[0], 0)

    def test_a_merged_branch_is_not_unmerged_work(self):
        d = self.session("d")
        self.push_file(d, "lessons/L03/lesson.md", "draft\n")
        run(self.seed, "fetch", "-q", "origin")
        run(self.seed, "merge", "-q", "--ff-only", "origin/claude/d")
        run(self.seed, "push", "-q", "origin", "HEAD:main")
        a = self.session("a")
        code, out = self.cli(a, "claim", "L03")
        self.assertEqual(code, 1)
        self.assertIn("already written", out)  # on main now, so a rewrite, not someone's draft


class StaleTests(Sessions):
    def test_a_silent_claim_blocks_until_taken_and_the_taker_wins(self):
        a, b = self.session("a"), self.session("b")
        self.cli(a, "claim", "L02", "--publish")
        self.clock += dt.timedelta(hours=25)
        code, out = self.cli(b, "claim", "L02", "--publish")
        self.assertEqual((code, "--take-stale" in out), (1, True))
        self.assertEqual(self.cli(b, "claim", "L02", "--take-stale", "--publish")[0], 0)
        self.assertIn('"taken_from"', (b / "lessons" / "L02.claim.json").read_text(encoding="utf-8"))
        self.cli(a, "touch", "--publish")  # the dead session wakes up
        code, out = self.cli(a, "verify")
        self.assertEqual(code, 1)
        self.assertIn("held by claude/b", out)
        self.assertEqual(self.cli(b, "verify")[0], 0)

    def test_an_expired_claim_does_not_use_up_a_place(self):
        a, b, c = self.session("a"), self.session("b"), self.session("c")
        self.cli(a, "claim", "L02", "--publish")
        self.clock += dt.timedelta(hours=25)
        self.assertEqual(self.cli(b, "claim", "L03", "--publish")[0], 0)
        self.assertEqual(self.cli(c, "claim", "L04", "--publish")[0], 0)

    def test_touch_keeps_a_claim_alive(self):
        a, b = self.session("a"), self.session("b")
        self.cli(a, "claim", "L02", "--publish")
        self.clock += dt.timedelta(hours=20)
        self.assertEqual(self.cli(a, "touch", "--publish")[0], 0)
        self.clock += dt.timedelta(hours=20)
        self.assertIn("held by claude/a", self.cli(b, "claim", "L02", "--take-stale")[1])

    def test_a_published_claim_that_expired_is_reported(self):
        a = self.session("a")
        self.cli(a, "claim", "L02", "--publish")
        self.clock += dt.timedelta(hours=25)
        code, out = self.cli(a, "verify")
        self.assertEqual(code, 1)
        self.assertIn("has expired; run touch --publish", out)

    def test_a_heartbeat_from_the_future_is_not_proof_of_life(self):
        moment = claims.stamp(START + dt.timedelta(hours=3))
        future = claims.holding("L02", claims.render({"id": "L02", "status": "doing", "owner": "x", "claimed_at": moment,
                                                      "heartbeat_at": moment}), "origin/x")
        self.assertTrue(claims.is_stale(future, START))
        self.assertFalse(claims.is_stale(future, START + dt.timedelta(hours=3)))


class FinishTests(Sessions):
    def test_finish_needs_the_text_then_records_done(self):
        a = self.session("a")
        self.cli(a, "claim", "L02", "--publish")
        code, out = self.cli(a, "finish", "L02")
        self.assertEqual(code, 1)
        self.assertIn("lesson.md does not exist", out)
        (a / "lessons" / "L02").mkdir()
        (a / "lessons" / "L02" / "lesson.md").write_text("# L02\n", encoding="utf-8")
        self.assertEqual(self.cli(a, "finish", "L02", "--publish")[0], 0)
        self.assertIn('"status": "done"', (a / "lessons" / "L02.claim.json").read_text(encoding="utf-8"))
        self.assertEqual(self.cli(a, "check", "--merge-ready")[0], 0)
        self.assertIn("L02\tdone", self.cli(self.session("b"), "status")[1])

    def test_finish_refuses_a_lost_claim(self):
        a, b = self.session("a"), self.session("b")
        self.cli(a, "claim", "L02", "--publish")
        self.rival_claim(b, "L02", minutes=1)
        (b / "lessons" / "L02").mkdir()
        (b / "lessons" / "L02" / "lesson.md").write_text("# L02\n", encoding="utf-8")
        code, out = self.cli(b, "finish", "L02")
        self.assertEqual(code, 1)
        self.assertIn("held by claude/a", out)

    def test_a_claim_in_progress_is_not_merge_ready(self):
        a = self.session("a")
        self.cli(a, "claim", "L02")
        code, out = self.cli(a, "check", "--merge-ready")
        self.assertEqual(code, 1)
        self.assertIn("still in progress", out)
        self.assertEqual(self.cli(a, "check")[0], 0)


class ScopeTests(Sessions):
    def test_changes_inside_the_lesson_and_its_claim_file_pass(self):
        a = self.session("a")
        self.cli(a, "claim", "L02")
        (a / "lessons" / "L02").mkdir()
        (a / "lessons" / "L02" / "lesson.md").write_text("x\n", encoding="utf-8")
        run(a, "add", "-A")
        run(a, "commit", "-q", "-m", "x")
        self.assertEqual(self.cli(a, "scope", "L02")[0], 0)

    def test_a_file_outside_the_lesson_fails_whether_committed_edited_or_new(self):
        a = self.session("a")
        (a / "lessons" / "L01" / "lesson.md").write_text("edited\n", encoding="utf-8")
        (a / "scripts").mkdir()
        (a / "scripts" / "new.py").write_text("x\n", encoding="utf-8")
        self.push_file(a, "lessons/L03/lesson.md", "other lesson\n")
        (a / "docs.md").write_text("untracked\n", encoding="utf-8")
        code, out = self.cli(a, "scope", "L02")
        self.assertEqual(code, 1)
        for name in ("lessons/L01/lesson.md", "lessons/L03/lesson.md", "scripts/new.py", "docs.md"):
            self.assertIn(f"outside lessons/L02/: {name}", out)


class RecordTests(unittest.TestCase):
    def test_a_record_is_checked_field_by_field(self):
        good = {"id": "L02", "status": "doing", "owner": "b", "claimed_at": "2026-10-21T08:00:00Z",
                "heartbeat_at": "2026-10-21T08:00:00Z"}
        self.assertEqual(claims.record_problems(good, "L02"), [])
        for bad, word in (({**good, "extra": 1}, "unknown key"), ({**good, "id": "L03"}, "id is"),
                          ({**good, "status": "idle"}, "status must"), ({**good, "owner": ""}, "owner"),
                          ({**good, "claimed_at": "yesterday"}, "claimed_at"), ({**good, "status": "done"}, "done_at"),
                          ({**good, "taken_from": "a"}, "taken_from")):
            self.assertTrue(any(word in text for text in claims.record_problems(bad, "L02")), bad)

    def test_an_unreadable_claim_blocks_its_lesson(self):
        broken = claims.holding("L02", "{not json", "origin/x")
        self.assertEqual(claims.standing([broken], START)[0], "invalid")
        self.assertEqual(claims.holding("L02", None, "origin/x").status, "invalid")

    def test_exactly_one_of_two_claims_wins(self):
        def make(owner: str, at: str, taken: tuple[str, ...] = ()):
            return claims.Holding("L02", "doing", owner, at, at, taken, "origin/" + owner)
        early, late = make("a", "2026-10-21T08:00:00Z"), make("b", "2026-10-21T09:00:00Z")
        self.assertTrue(claims.beats(early, late) and not claims.beats(late, early))
        same_a, same_b = make("a", early.claimed_at), make("b", early.claimed_at)
        self.assertTrue(claims.beats(same_a, same_b) and not claims.beats(same_b, same_a))
        taker = make("b", "2026-10-22T08:00:00Z", ("a",))
        self.assertTrue(claims.beats(taker, early) and not claims.beats(early, taker))

    def test_ids_are_numbered_after_the_highest_seen(self):
        self.assertEqual(claims.next_id({"L00", "L03", "L16"}), "L17")
        self.assertEqual(claims.next_id(set()), "L00")


GOOD_BOARD = """# Bảng

| Bài | Việc | Nhánh | Phiên | Trạng thái | Cập nhật |
|---|---|---|---|---|---|
| L11 | viết | `claude/lesson-L11` | chưa rõ | giao | 2026-10-21 |
| L12 | viết | `claude/lesson-L12` | chưa rõ | đang làm | 2026-10-21 |
| L13 | phản biện a | `claude/review-L13-a` | chưa rõ | chờ PR | 2026-10-21 |

| Other | table |
|---|---|
| x | y |
"""


class BoardTests(unittest.TestCase):
    def test_a_good_board_reads(self):
        self.assertEqual(claims.board_problems(GOOD_BOARD), [])

    def test_bad_rows_are_named(self):
        for bad, word in ((GOOD_BOARD.replace("| giao |", "| xong rồi |"), "Trạng thái"),
                          (GOOD_BOARD.replace("| L11 |", "| 11 |"), "Bài"),
                          (GOOD_BOARD.replace("| viết | `claude/lesson-L11`", "| code | `claude/lesson-L11`"), "Việc"),
                          (GOOD_BOARD.replace("2026-10-21 |\n| L12", "21/10 |\n| L12"), "Cập nhật"),
                          ("no table here\n", "no table")):
            self.assertTrue(any(word in text for text in claims.board_problems(bad)), word)

    def test_a_row_with_a_missing_cell_is_reported_not_a_crash(self):
        short = GOOD_BOARD.replace("| L11 | viết | `claude/lesson-L11` | chưa rõ | giao | 2026-10-21 |", "| L11 | viết | giao |")
        self.assertTrue(any("3 cells" in text for text in claims.board_problems(short)))

    def test_more_than_two_branches_writing_at_once_is_refused(self):
        three = GOOD_BOARD.replace("chờ PR", "đang làm").replace("phản biện a", "viết")
        self.assertTrue(any("limit is 2" in text for text in claims.board_problems(three)))

    def test_the_real_repository_passes_its_own_check(self):
        self.assertEqual(claims.check_problems(ROOT), [])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Who is writing which lesson, so that two sessions never write the same one.

Sessions share only the git remote. A session claims a lesson by committing lessons/<id>.claim.json on its own branch and
pushing that branch; every command that decides something first fetches all branches and reads the claims on each. The
owner of a claim is the branch name. At most MAX_ACTIVE sessions write at once (owner decision 2026-10-24, was 2).

    python3 scripts/claims.py status                       # who holds what, who is writing, the next free id
    python3 scripts/claims.py claim L17 --publish          # or: claim --new --publish (takes the next free L id); F03, A02, J02 for the course
    python3 scripts/claims.py verify                       # exit 0 = every claim of mine is still mine and pushed
    python3 scripts/claims.py touch --publish              # renew the heartbeat; one silent for LEASE_HOURS is stale: claim it again
    python3 scripts/claims.py finish L17 --publish         # the lesson is written (lessons/<id>/lesson.md must exist)
    python3 scripts/claims.py release L17 --publish        # give back a lesson you will not write
    python3 scripts/claims.py scope L17                    # exit 1 if this branch changes files outside the lesson
    python3 scripts/claims.py check [--merge-ready]        # claim files and docs/dieu-phoi.md are well formed

Exit 0 = done, 1 = refused or lost, 2 = the remote could not be read (fix the network; nothing is guessed).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTE = "origin"
LEASE_HOURS = 24
SKEW_HOURS = 1  # a heartbeat further ahead of the clock than this is not proof of life
MAX_ACTIVE = 3
STAMP = "%Y-%m-%dT%H:%M:%SZ"
# L = the general series; F, A, J = the Freud, Adler and Jung course (owner decision 2026-10-24)
LESSON_ID = re.compile(r"[LFAJ]\d{2}")
LESSON_NAME = re.compile(r"([LFAJ]\d{2})(?:\.|$)")
STATUSES = ("doing", "done")
RECORD_KEYS = {"id", "status", "owner", "claimed_at", "heartbeat_at", "done_at", "session", "taken_from"}
BOARD = "docs/dieu-phoi.md"
BOARD_COLUMNS = ["bài", "việc", "nhánh", "phiên", "trạng thái", "cập nhật"]
BOARD_WORK = ("viết", "phản biện a", "phản biện b", "sửa", "deck")
BOARD_STATUS = ("giao", "đang làm", "chờ phản biện", "chờ pr", "xong")


class ClaimsError(Exception):
    """Exit 1: a refusal."""


class RemoteError(ClaimsError):
    """Exit 2: the remote could not be read or written."""


def now() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)


def stamp(moment: _dt.datetime) -> str:
    return moment.strftime(STAMP)


def parse_stamp(value: object) -> _dt.datetime | None:
    try:
        return _dt.datetime.strptime(value, STAMP).replace(tzinfo=_dt.timezone.utc)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def git(root: Path, *args: str, check: bool = True, data: bytes | None = None) -> subprocess.CompletedProcess:
    done = subprocess.run(["git", "-C", str(root), *args], input=data, capture_output=True)
    if check and done.returncode:
        raise ClaimsError(f"git {' '.join(args)} failed: {done.stderr.decode(errors='replace').strip()}")
    return done


def git_text(root: Path, *args: str) -> str:
    return git(root, *args).stdout.decode(errors="replace").strip()


@dataclass(frozen=True)
class Holding:
    lesson: str
    status: str  # doing | done | invalid
    owner: str
    claimed_at: str | None
    heartbeat_at: str | None
    taken_from: tuple[str, ...]
    where: str  # "origin/<branch>" or "local"
    problems: tuple[str, ...] = ()
    done_at: str | None = None


def record_problems(record: object, lesson: str) -> list[str]:
    if not isinstance(record, dict):
        return ["is not a JSON object"]
    problems = [f"unknown key {key!r}" for key in sorted(set(record) - RECORD_KEYS)]
    if record.get("id") != lesson:
        problems.append(f"id is {record.get('id')!r}, the file is for {lesson}")
    if record.get("status") not in STATUSES:
        problems.append(f"status must be one of {', '.join(STATUSES)}")
    if not isinstance(record.get("owner"), str) or not record.get("owner"):
        problems.append("owner (the branch name) is missing")
    for key in ("claimed_at", "heartbeat_at") + (("done_at",) if record.get("status") == "done" else ()):
        if parse_stamp(record.get(key)) is None:
            problems.append(f"{key} must look like 2026-10-21T08:00:00Z")
    taken = record.get("taken_from", [])
    if not isinstance(taken, list) or not all(isinstance(item, str) and item for item in taken):
        problems.append("taken_from must be a list of branch names")
    return problems


def holding(lesson: str, text: str | None, where: str) -> Holding:
    """What a claim file says, read leniently: one that cannot be used is `invalid` and blocks its lesson until fixed."""
    try:
        record = json.loads(text) if text is not None else None
    except ValueError:
        record = None
    if not isinstance(record, dict):
        return Holding(lesson, "invalid", "", None, None, (), where, ("does not parse as a JSON object",))
    problems = tuple(record_problems(record, lesson))
    taken = record.get("taken_from") if isinstance(record.get("taken_from"), list) else []
    return Holding(lesson, "invalid" if problems else record["status"],
                   record["owner"] if isinstance(record.get("owner"), str) else "",
                   record.get("claimed_at") if isinstance(record.get("claimed_at"), str) else None,
                   record.get("heartbeat_at") if isinstance(record.get("heartbeat_at"), str) else None,
                   tuple(item for item in taken if isinstance(item, str)), where, problems,
                   record.get("done_at") if isinstance(record.get("done_at"), str) else None)


def claim_name(lesson: str) -> str:
    return f"lessons/{lesson}.claim.json"


def render(record: dict) -> str:
    return json.dumps(record, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def is_stale(found: Holding, moment: _dt.datetime) -> bool:
    if found.status != "doing":
        return False
    beat = parse_stamp(found.heartbeat_at)
    if beat is None or beat - moment > _dt.timedelta(hours=SKEW_HOURS):
        return True
    return moment - beat > _dt.timedelta(hours=LEASE_HOURS)


def beats(first: Holding, second: Holding) -> bool:
    """Whether first wins the lesson over second: a takeover over the claim it took, else the earlier claim, else the
    smaller owner. Exactly one of beats(a, b) and beats(b, a) is true for two different claims."""
    first_took, second_took = second.owner in first.taken_from, first.owner in second.taken_from
    if first_took != second_took:
        return first_took
    return (first.claimed_at or "", first.owner) < (second.claimed_at or "", second.owner)


def best(found: list[Holding]) -> Holding:
    winner = found[0]
    for other in found[1:]:
        if beats(other, winner):
            winner = other
    return winner


def standing(found: list[Holding], moment: _dt.datetime) -> tuple[str, Holding | None]:
    """invalid (a record nobody can use) | doing (the live winner) | done (the latest finished record) | stale (only
    expired claims) | free. A claim in progress beats a finished record only when it was made after the lesson was
    finished (a rewrite); one made before it lost the race for the lesson, and finishing does not hand it the win."""
    broken = [item for item in found if item.status == "invalid"]
    if broken:
        return "invalid", broken[0]
    done = [item for item in found if item.status == "done"]
    finished = max(done, key=lambda item: (item.done_at or "", item.owner)) if done else None
    live = [item for item in found if item.status == "doing" and not is_stale(item, moment)
            and (finished is None or (item.claimed_at or "") > (finished.done_at or ""))]
    if live:
        return "doing", best(live)
    if finished is not None:
        return "done", finished
    stale = [item for item in found if item.status == "doing"]
    if stale:
        return "stale", min(stale, key=lambda item: (item.claimed_at or "", item.owner))
    return "free", None


def active_owners(holdings: dict[str, list[Holding]], moment: _dt.datetime) -> list[str]:
    """The owners with a live claim on some lesson, the one that started first at the front. Only the first MAX_ACTIVE
    of them may write; a later one that pushed anyway loses on verify, like the loser of a race for one lesson."""
    first: dict[str, str] = {}
    for found in holdings.values():
        state, winner = standing(found, moment)
        if state == "doing" and winner is not None:
            first[winner.owner] = min(first.get(winner.owner, winner.claimed_at or ""), winner.claimed_at or "")
    return [owner for _, owner in sorted((at, owner) for owner, at in first.items())]


@dataclass
class Context:
    root: Path
    offline: bool = False
    me: str = ""


@dataclass
class Board:
    holdings: dict[str, list[Holding]]
    seen: set[str]  # every lesson id that has a file or folder under lessons/ anywhere
    base: str | None
    drafts: dict[str, list[str]]  # lesson id -> other branches that carry unmerged work on lessons/<id>/


def remote_branches(root: Path) -> list[str]:
    out = git_text(root, "for-each-ref", "--format=%(refname:lstrip=3)", f"refs/remotes/{REMOTE}")
    return [name for name in out.splitlines() if name and name != "HEAD"]


def default_branch(root: Path, branches: list[str]) -> str | None:
    shown = git(root, "symbolic-ref", "--short", "-q", f"refs/remotes/{REMOTE}/HEAD", check=False)
    if shown.returncode == 0:
        return shown.stdout.decode().strip().split("/", 1)[-1]
    return next((name for name in ("main", "master") if name in branches), None)


def fetch(root: Path) -> None:
    done = git(root, "fetch", "--prune", "--quiet", REMOTE, f"+refs/heads/*:refs/remotes/{REMOTE}/*", check=False)
    if done.returncode:
        raise RemoteError(f"the remote could not be read ({done.stderr.decode(errors='replace').strip()}); "
                          "pass --offline to decide without it")


def read_blobs(root: Path, specs: list[str]) -> dict[str, str | None]:
    """git object spec -> text; None where the object is missing or is not UTF-8."""
    if not specs:
        return {}
    out = git(root, "cat-file", "--batch", data="".join(f"{spec}\n" for spec in specs).encode()).stdout
    found: dict[str, str | None] = {}
    position = 0
    for spec in specs:
        end = out.index(b"\n", position)
        fields = out[position:end].split(b" ")
        position = end + 1
        found[spec] = None
        if len(fields) == 3:
            size = int(fields[2])
            if fields[1] == b"blob":
                try:
                    found[spec] = out[position:position + size].decode("utf-8")
                except UnicodeDecodeError:
                    pass
            position += size + 1
    return found


def lesson_of(name: str) -> str | None:
    match = LESSON_NAME.match(name)
    return match.group(1) if match else None


def gather(ctx: Context) -> Board:
    """Every claim as the remote and this checkout show it. A claim counts on the default branch always, and on any other
    branch only when its owner is that branch (a branch cut from someone's branch holds a stale copy, which is not a claim)."""
    holdings: dict[str, list[Holding]] = {}
    seen: set[str] = set()
    base: str | None = None
    drafts: dict[str, list[str]] = {}
    if not ctx.offline:
        fetch(ctx.root)
        branches = remote_branches(ctx.root)
        base = default_branch(ctx.root, branches)
        wanted: list[tuple[str, str]] = []
        for name in branches:
            listing = git(ctx.root, "ls-tree", "--name-only", f"refs/remotes/{REMOTE}/{name}", "lessons/", check=False)
            for line in listing.stdout.decode(errors="replace").splitlines():
                leaf = line.rsplit("/", 1)[-1]
                lesson = lesson_of(leaf)
                if lesson is not None:
                    seen.add(lesson)
                    if leaf == f"{lesson}.claim.json":
                        wanted.append((name, lesson))
        texts = read_blobs(ctx.root, [f"refs/remotes/{REMOTE}/{name}:{claim_name(lesson)}" for name, lesson in wanted])
        for name, lesson in wanted:
            found = holding(lesson, texts[f"refs/remotes/{REMOTE}/{name}:{claim_name(lesson)}"], f"{REMOTE}/{name}")
            if found.problems:  # a malformed record blocks, whoever it names
                holdings.setdefault(lesson, []).append(found)
            elif name == base:
                if found.status == "doing" and found.owner in branches and found.owner != base:
                    continue  # a claim in progress belongs to its owner's branch, which says whether it still stands
                holdings.setdefault(lesson, []).append(found)
            elif found.owner == name:
                holdings.setdefault(lesson, []).append(found)
        if base is not None:
            for name in branches:
                if name in (base, ctx.me):
                    continue
                changed = git(ctx.root, "diff", "--name-only", f"refs/remotes/{REMOTE}/{base}...refs/remotes/{REMOTE}/{name}",
                              "--", "lessons/", check=False)
                for path in changed.stdout.decode(errors="replace").splitlines():
                    parts = path.split("/")
                    if len(parts) >= 3 and LESSON_ID.fullmatch(parts[1]) and name not in drafts.setdefault(parts[1], []):
                        drafts[parts[1]].append(name)
    lessons = ctx.root / "lessons"
    if lessons.is_dir():
        for path in sorted(lessons.iterdir()):
            lesson = lesson_of(path.name)
            if lesson is None:
                continue
            seen.add(lesson)
            if path.name == f"{lesson}.claim.json":
                found = holding(lesson, path.read_text(encoding="utf-8"), "local")
                if found.owner == ctx.me or ctx.offline or found.problems:
                    holdings.setdefault(lesson, []).append(found)
    return Board(holdings, seen, base, drafts)


def next_id(seen: set[str]) -> str:
    return f"L{max((int(item[1:]) for item in seen if item[0] == 'L'), default=-1) + 1:02d}"


def require_branch(ctx: Context) -> str:
    """My owner name: the branch I am on. Never the default branch: a claim counts only on the branch its owner names."""
    shown = git(ctx.root, "symbolic-ref", "--short", "-q", "HEAD", check=False)
    branch = shown.stdout.decode().strip() if shown.returncode == 0 else ""
    if not branch:
        raise ClaimsError("HEAD is detached; check out a work branch (claude/lesson-<id>) first")
    if branch in ("main", "master", default_branch(ctx.root, remote_branches(ctx.root))):
        raise ClaimsError(f"you are on {branch}; claims are made on a work branch of your own (claude/lesson-<id>)")
    return branch


def publish(ctx: Context, paths: list[Path], message: str) -> None:
    """Commit only these paths and push my own branch (anything else already committed on it goes with it)."""
    branch = require_branch(ctx)
    relative = [str(path.relative_to(ctx.root)) for path in paths]
    # a released claim that was never committed is nothing to stage
    relative = [name for name in relative if (ctx.root / name).exists() or git(ctx.root, "ls-files", "--", name).stdout.strip()]
    if relative:
        git(ctx.root, "add", "-A", "--", *relative)
        if git(ctx.root, "diff", "--cached", "--quiet", "--", *relative, check=False).returncode:
            git(ctx.root, "commit", "-q", "-m", message, "--", *relative)
    pushed = git(ctx.root, "push", "-q", "-u", REMOTE, f"HEAD:refs/heads/{branch}", check=False)
    if pushed.returncode:
        raise RemoteError(f"git push failed: {pushed.stderr.decode(errors='replace').strip()}")


def mine(board: Board, ctx: Context, statuses: tuple[str, ...] = ("doing",)) -> list[str]:
    return sorted(lesson for lesson, found in board.holdings.items()
                  if any(item.where == "local" and item.owner == ctx.me and item.status in statuses for item in found))


def check_ids(ids: list[str]) -> list[str]:
    for lesson in ids:
        if not LESSON_ID.fullmatch(lesson):
            raise ClaimsError(f"{lesson!r} is not a lesson id (L00 to L99, F00 to F99, A00 to A99 or J00 to J99)")
    return ids


def lost_reason(lesson: str, board: Board, ctx: Context, moment: _dt.datetime) -> str | None:
    """Why my claim on this lesson does not stand, or None."""
    found = board.holdings.get(lesson, [])
    local = [item for item in found if item.where == "local" and item.owner == ctx.me]
    if not local:
        return f"{lesson}: you hold no claim on it"
    state, winner = standing(found, moment)
    if state == "invalid":
        return f"{lesson}: {winner.where} has a claim file that cannot be used ({'; '.join(winner.problems)})"
    if winner is None or winner.owner != ctx.me:
        return f"{lesson}: held by {winner.owner if winner else 'nobody (your claim expired)'}; stop, release it and take another"
    owners = active_owners(board.holdings, moment)
    if state == "doing" and ctx.me not in owners[:MAX_ACTIVE]:
        return (f"{lesson}: {MAX_ACTIVE} sessions were writing before you ({', '.join(owners[:MAX_ACTIVE])}); "
                "release it and wait")
    if ctx.offline:
        return None
    published = [item for item in found if item.where == f"{REMOTE}/{ctx.me}" and item.owner == ctx.me]
    if not published:
        return f"{lesson}: your claim is only in your working tree; claim or touch with --publish"
    if published[0].claimed_at != local[0].claimed_at or published[0].taken_from != local[0].taken_from:
        return f"{lesson}: the claim on {published[0].where} differs from your working tree (claimed_at or taken_from)"
    if is_stale(published[0], moment):
        return f"{lesson}: the claim on {published[0].where} has expired; claim it again (touch cannot renew it)"
    return None


def report(ctx: Context, lessons: list[str]) -> int:
    """Look again at the remote and say whether each of these claims (default: all of mine) stands."""
    moment = now()
    board = gather(ctx)
    lessons = lessons or mine(board, ctx)
    problems = [text for lesson in lessons if (text := lost_reason(lesson, board, ctx, moment))]
    for text in problems:
        print(text, file=sys.stderr)
    if not problems:
        print(f"{', '.join(lessons) or 'no claim of yours'}: " + ("yours" if ctx.offline else "yours and pushed"))
    return 1 if problems else 0


def cmd_status(ctx: Context, args) -> int:
    moment = now()
    board = gather(ctx)
    for lesson in sorted(board.holdings):
        state, winner = standing(board.holdings[lesson], moment)
        who = f"{winner.owner} ({winner.where})" if winner else "-"
        beat = parse_stamp(winner.heartbeat_at) if winner and state in ("doing", "stale") else None
        age = f", heartbeat {int((moment - beat).total_seconds() // 3600)} h ago" if beat else ""
        print(f"{lesson}\t{state}\t{who}{age}")
    owners = active_owners(board.holdings, moment)
    print(f"writing now: {len(owners)} of {MAX_ACTIVE}" + (f" ({', '.join(owners)})" if owners else ""))
    for lesson, names in sorted(board.drafts.items()):
        print(f"unmerged work on lessons/{lesson}/: {', '.join(names)} (ahead of {board.base})")
    print(f"next free id: {next_id(board.seen)}")
    return 0


def cmd_next(ctx: Context, args) -> int:
    print(next_id(gather(ctx).seen))
    return 0


def is_written(ctx: Context, board: Board, lesson: str) -> bool:
    """Whether the default branch (the checkout, offline) already has this lesson's text."""
    if ctx.offline or board.base is None:
        return (ctx.root / "lessons" / lesson / "lesson.md").is_file()
    spec = f"refs/remotes/{REMOTE}/{board.base}:lessons/{lesson}/lesson.md"
    return git(ctx.root, "cat-file", "-e", spec, check=False).returncode == 0


def cmd_claim(ctx: Context, args) -> int:
    moment = now()
    ctx.me = require_branch(ctx)
    board = gather(ctx)
    ids = [next_id(board.seen)] if args.new else check_ids(args.ids)
    if not ids:
        raise ClaimsError("name the lessons to claim, or pass --new for the next free id")
    owners = active_owners(board.holdings, moment)
    if ctx.me not in owners and len(owners) >= MAX_ACTIVE:
        raise ClaimsError(f"{len(owners)} sessions are already writing ({', '.join(owners)}); the limit is {MAX_ACTIVE}. "
                          "Wait for one to finish or release")
    lessons = ctx.root / "lessons"
    written: list[Path] = []
    for lesson in ids:
        if not args.new and lesson not in board.seen:
            raise ClaimsError(f"{lesson}: no file or folder of that id exists; the orchestrator creates lessons/{lesson}.spec.md "
                              "first (or use --new)")
        found = board.holdings.get(lesson, [])
        state, winner = standing(found, moment)
        if state == "invalid":
            raise ClaimsError(f"{lesson}: {winner.where} has a claim file that cannot be used ({'; '.join(winner.problems)})")
        if state == "doing" and winner.owner != ctx.me:
            raise ClaimsError(f"{lesson}: held by {winner.owner} ({winner.where})")
        if state == "doing":
            continue  # already mine; touch renews it
        taken: list[str] = []
        if state == "stale" and winner.owner != ctx.me:
            if not args.take_stale:
                raise ClaimsError(f"{lesson}: {winner.owner} has been silent for over {LEASE_HOURS} h; take it with --take-stale")
            taken = sorted({item.owner for item in found if item.status == "doing" and item.owner != ctx.me}
                           | {name for item in found for name in item.taken_from if name != ctx.me})
        if (state == "done" or is_written(ctx, board, lesson)) and not args.rewrite:
            raise ClaimsError(f"{lesson}: already written; claim it with --rewrite when the orchestrator asked for a rewrite or a fix")
        others = [name for name in board.drafts.get(lesson, []) if name != ctx.me]
        if others and not args.ignore_drafts:
            raise ClaimsError(f"{lesson}: branch {', '.join(others)} already carries unmerged work on it; ask the orchestrator "
                              "who holds it (--ignore-drafts if it is yours to take)")
        record = {"id": lesson, "status": "doing", "owner": ctx.me, "claimed_at": stamp(moment), "heartbeat_at": stamp(moment)}
        if taken:
            record["taken_from"] = taken
        if args.session:
            record["session"] = args.session
        lessons.mkdir(exist_ok=True)
        path = lessons / f"{lesson}.claim.json"
        path.write_text(render(record), encoding="utf-8")
        written.append(path)
    if args.publish and written:
        publish(ctx, written, f"claim: {', '.join(path.name.split('.')[0] for path in written)}")
    return report(ctx, ids)


def cmd_verify(ctx: Context, args) -> int:
    ctx.me = require_branch(ctx)
    return report(ctx, check_ids(args.ids))


def cmd_touch(ctx: Context, args) -> int:
    moment = now()
    ctx.me = require_branch(ctx)
    board = gather(ctx)
    ids = check_ids(args.ids) or mine(board, ctx)
    paths = []
    for lesson in ids:
        found = [item for item in board.holdings.get(lesson, []) if item.where == "local" and item.owner == ctx.me]
        if not found or found[0].status != "doing":
            raise ClaimsError(f"{lesson}: you hold no claim in progress on it")
        copies = [item for item in board.holdings.get(lesson, []) if item.owner == ctx.me and item.status == "doing"]
        if any(is_stale(item, moment) for item in copies):
            raise ClaimsError(f"{lesson}: your claim expired (silent over {LEASE_HOURS} h) and its place may have been taken; "
                              f"claim it again: claims.py claim {lesson} --publish")
        path = ctx.root / "lessons" / f"{lesson}.claim.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record["heartbeat_at"] = stamp(moment)
        path.write_text(render(record), encoding="utf-8")
        paths.append(path)
    if args.publish and paths:
        publish(ctx, paths, f"claim: heartbeat {', '.join(ids)}")
    return report(ctx, ids)


def cmd_finish(ctx: Context, args) -> int:
    moment = now()
    ctx.me = require_branch(ctx)
    board = gather(ctx)
    ids = check_ids(args.ids) or mine(board, ctx)
    if not ids:
        raise ClaimsError("name the lessons to finish")
    problems = [text for lesson in ids if (text := lost_reason(lesson, board, ctx, moment))]
    problems += [f"{lesson}: lessons/{lesson}/lesson.md does not exist; a lesson is finished when it is written"
                 for lesson in ids if not (ctx.root / "lessons" / lesson / "lesson.md").is_file()]
    if problems:
        raise ClaimsError("\n".join(problems))
    paths = []
    for lesson in ids:
        path = ctx.root / "lessons" / f"{lesson}.claim.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record.update(status="done", heartbeat_at=stamp(moment), done_at=stamp(moment))
        path.write_text(render(record), encoding="utf-8")
        paths.append(path)
    if args.publish:
        publish(ctx, paths, f"claim: finished {', '.join(ids)}")
    print(f"{', '.join(ids)}: done; commit the claim file with the lesson")
    return 0


def cmd_release(ctx: Context, args) -> int:
    ctx.me = require_branch(ctx)
    board = gather(ctx)
    ids = check_ids(args.ids) or mine(board, ctx)
    paths = []
    for lesson in ids:
        if not any(item.where == "local" and item.owner == ctx.me for item in board.holdings.get(lesson, [])):
            raise ClaimsError(f"{lesson}: you hold no claim on it")
        path = ctx.root / "lessons" / f"{lesson}.claim.json"
        path.unlink()
        paths.append(path)
    if args.publish and paths:
        publish(ctx, paths, f"claim: release {', '.join(ids)}")
    print(f"released {', '.join(ids) or 'nothing'}")
    return 0


def changed_files(root: Path, base: str) -> list[str]:
    """Paths this branch changes against its base: committed since the merge base, edited, or not yet tracked."""
    names = set(git_text(root, "diff", "--name-only", f"{base}...HEAD").splitlines())
    names |= set(git_text(root, "diff", "--name-only", "HEAD").splitlines())
    names |= set(git_text(root, "ls-files", "--others", "--exclude-standard").splitlines())
    return sorted(name for name in names if name)


def cmd_scope(ctx: Context, args) -> int:
    lesson = check_ids([args.id])[0]
    base = args.base or f"{REMOTE}/{default_branch(ctx.root, remote_branches(ctx.root)) or 'main'}"
    outside = [name for name in changed_files(ctx.root, base)
               if not name.startswith(f"lessons/{lesson}/") and name != claim_name(lesson)]
    for name in outside:
        print(f"outside lessons/{lesson}/: {name}", file=sys.stderr)
    if not outside:
        print(f"{lesson}: every change is inside lessons/{lesson}/ (or its claim file)")
    return 1 if outside else 0


def board_problems(text: str) -> list[str]:
    """Rows of docs/dieu-phoi.md that cannot be read, and a board that gives more than MAX_ACTIVE branches writing at once."""
    problems: list[str] = []
    header: list[str] | None = None
    writers: set[str] = set()
    rows = 0
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            header = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            header = [cell.lower() for cell in cells]
            continue
        if all(set(cell) <= set("-: ") for cell in cells) or header != BOARD_COLUMNS:
            continue  # the |---|---| line, or some other table
        rows += 1
        label = f"row {line.strip()!r}"
        if len(cells) != len(header):
            problems.append(f"{label}: has {len(cells)} cells, the header has {len(header)}")
            continue
        row = dict(zip(header, cells))
        if not LESSON_ID.fullmatch(row["bài"]):
            problems.append(f"{label}: Bài must look like L17, F03, A02 or J02")
        if row["việc"].lower() not in BOARD_WORK:
            problems.append(f"{label}: Việc must be one of {', '.join(BOARD_WORK)}")
        if row["trạng thái"].lower() not in BOARD_STATUS:
            problems.append(f"{label}: Trạng thái must be one of {', '.join(BOARD_STATUS)}")
        if parse_stamp(row["cập nhật"] + "T00:00:00Z") is None:
            problems.append(f"{label}: Cập nhật must be a date like 2026-10-21")
        if row["việc"].lower() in ("viết", "sửa") and row["trạng thái"].lower() in ("giao", "đang làm"):
            writers.add(row["nhánh"].strip("`"))
    if not rows:
        problems.append("no table with the columns " + " | ".join(BOARD_COLUMNS))
    if len(writers) > MAX_ACTIVE:
        problems.append(f"{len(writers)} branches are writing or fixing at once; the limit is {MAX_ACTIVE}")
    return problems


def check_problems(root: Path, merge_ready: bool = False) -> list[str]:
    problems: list[str] = []
    lessons = root / "lessons"
    for path in sorted(lessons.glob("L*.claim.json")) if lessons.is_dir() else []:
        lesson, name = path.name.split(".", 1)[0], str(path.relative_to(root))
        found = holding(lesson, path.read_text(encoding="utf-8"), "local")
        problems += [f"{name}: {item}" for item in found.problems]
        if found.status == "done" and not (lessons / lesson / "lesson.md").is_file():
            problems.append(f"{name}: status done but lessons/{lesson}/lesson.md does not exist")
        if merge_ready and found.status == "doing":
            problems.append(f"{name}: still in progress; finish or release it before merging")
    board = root / BOARD
    if board.is_file():
        problems += [f"{BOARD}: {item}" for item in board_problems(board.read_text(encoding="utf-8"))]
    return problems


def cmd_check(ctx: Context, args) -> int:
    problems = check_problems(ctx.root, args.merge_ready)
    for item in problems:
        print(item, file=sys.stderr)
    return 1 if problems else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--offline", action="store_true", help="decide from this checkout alone (tests, no remote)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="who holds what, how many are writing, the next free id")
    sub.add_parser("next", help="print the next free lesson id")
    claim = sub.add_parser("claim", help="claim lessons before writing them")
    claim.add_argument("ids", nargs="*")
    claim.add_argument("--new", action="store_true", help="claim the next free id")
    claim.add_argument("--publish", action="store_true", help="commit the claim file and push my own branch")
    claim.add_argument("--take-stale", action="store_true", help="take over a claim silent for over %d h" % LEASE_HOURS)
    claim.add_argument("--rewrite", action="store_true", help="the lesson is already written; the orchestrator asked for a rewrite or fix")
    claim.add_argument("--ignore-drafts", action="store_true", help="claim although another branch has unmerged work on it")
    claim.add_argument("--session", help="the session link, kept in the record")
    verify = sub.add_parser("verify", help="exit 0 when every claim of mine is still mine and pushed")
    verify.add_argument("ids", nargs="*")
    for name, helptext in (("touch", "renew the heartbeat of my claims"), ("finish", "mark lessons written"),
                           ("release", "give back lessons I will not write")):
        command = sub.add_parser(name, help=helptext)
        command.add_argument("ids", nargs="*")
        command.add_argument("--publish", action="store_true")
    scope = sub.add_parser("scope", help="exit 1 when this branch changes files outside the lesson")
    scope.add_argument("id")
    scope.add_argument("--base", help="default: the remote's default branch")
    check = sub.add_parser("check", help="claim files and the board are well formed (no network)")
    check.add_argument("--merge-ready", action="store_true", help="also fail on a claim still in progress")
    return parser


COMMANDS = {"status": cmd_status, "next": cmd_next, "claim": cmd_claim, "verify": cmd_verify, "touch": cmd_touch,
            "finish": cmd_finish, "release": cmd_release, "scope": cmd_scope, "check": cmd_check}


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    args = build_parser().parse_args(argv)
    ctx = Context(root, args.offline)
    try:
        return COMMANDS[args.command](ctx, args)
    except RemoteError as error:
        print(f"claims.py: {error}", file=sys.stderr)
        return 2
    except ClaimsError as error:
        print(f"claims.py: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

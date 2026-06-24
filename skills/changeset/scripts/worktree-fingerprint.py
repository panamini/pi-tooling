#!/usr/bin/env python3
"""Compute read-only, baseline-aware fingerprints for a Git change set.

The tool hashes Git-reported tracked changes and non-ignored untracked state
relative to HEAD without printing file contents. Ignored paths are excluded.
It reports three digests, each bound to the baseline HEAD:

- worktree_sha256: tracked changes and non-ignored untracked filesystem state;
- index_sha256: index entries for changed paths plus visibility flags that can hide changes;
- state_sha256: status, index, and filesystem state together.

It performs a stability recheck before returning. Exit codes: 0 complete,
2 usage/not-a-repository, 3 incomplete or unstable fingerprint.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Iterable

SCHEMA = "changeset/worktree-fingerprint/v2"
SCOPE = "HEAD plus index/worktree state for paths reported by git status --untracked-files=all; ignored paths excluded"

# Ambient repository-local Git variables can redirect `git -C <repo>` to a
# different worktree, index, object database, or ref namespace. Remove them so
# --repo identifies the repository actually inspected. Ordinary repository and
# user configuration still apply unless explicitly overridden per command.
REPOSITORY_LOCAL_GIT_ENV = {
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_CEILING_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_CONFIG",
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_PARAMETERS",
    "GIT_DIR",
    "GIT_DISCOVERY_ACROSS_FILESYSTEM",
    "GIT_GRAFT_FILE",
    "GIT_IMPLICIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_NAMESPACE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_PREFIX",
    "GIT_QUARANTINE_PATH",
    "GIT_REPLACE_REF_BASE",
    "GIT_SHALLOW_FILE",
    "GIT_WORK_TREE",
}


class GitError(RuntimeError):
    pass


def escape_control_text(value: str) -> str:
    """Escape control characters for one-line terminal output."""
    return json.dumps(value, ensure_ascii=True)[1:-1]


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    for key in tuple(env):
        if (
            key in REPOSITORY_LOCAL_GIT_ENV
            or key.startswith("GIT_CONFIG_KEY_")
            or key.startswith("GIT_CONFIG_VALUE_")
        ):
            env.pop(key, None)
    env.update(
        {
            # Keep inspection non-interactive and avoid optional index writes or
            # on-demand network fetches where the installed Git supports them.
            "GIT_LITERAL_PATHSPECS": "1",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_PAGER": "cat",
            "GIT_TERMINAL_PROMPT": "0",
            "LC_ALL": "C",
        }
    )
    proc = subprocess.run(
        ["git", "-C", os.fspath(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=env,
    )
    if check and proc.returncode != 0:
        message = escape_control_text(proc.stderr.decode("utf-8", "replace").strip())
        rendered = " ".join(json.dumps(arg, ensure_ascii=True) for arg in args)
        raise GitError(f"git {rendered} failed: {message or proc.returncode}")
    return proc


def feed(hasher: Any, label: bytes, value: bytes) -> None:
    hasher.update(len(label).to_bytes(4, "big"))
    hasher.update(label)
    hasher.update(len(value).to_bytes(8, "big"))
    hasher.update(value)


def display_path(raw: bytes) -> str:
    return raw.decode("utf-8", "backslashreplace")


def safe_display_path(raw: bytes) -> str:
    """Render a repository path without emitting terminal control characters."""
    return escape_control_text(display_path(raw))


def decode_git_path_line(raw: bytes, label: str) -> Path:
    """Decode a single newline-terminated path emitted by Git."""
    if not raw.endswith(b"\n"):
        raise GitError(f"{label} returned an unterminated path")
    path_bytes = raw[:-1]
    if os.name == "nt" and path_bytes.endswith(b"\r"):
        path_bytes = path_bytes[:-1]
    return Path(os.fsdecode(path_bytes)).resolve()


def parse_status_z(data: bytes) -> list[tuple[bytes, bytes, bytes | None]]:
    """Parse porcelain v1 -z records as (XY, path, original_path)."""
    records: list[tuple[bytes, bytes, bytes | None]] = []
    pos = 0
    while pos < len(data):
        end = data.find(b"\0", pos)
        if end < 0:
            raise GitError("unterminated git status record")
        record = data[pos:end]
        pos = end + 1
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            raise GitError(f"unexpected git status record: {record!r}")
        xy = record[:2]
        path = record[3:]
        original: bytes | None = None
        if b"R" in xy or b"C" in xy:
            end = data.find(b"\0", pos)
            if end < 0:
                raise GitError("unterminated rename/copy status record")
            original = data[pos:end]
            pos = end + 1
        records.append((xy, path, original))
    return records


def stat_signature(info: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def hash_file(path: bytes, expected: os.stat_result) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with open(path, "rb", buffering=0) as handle:
        before = os.fstat(handle.fileno())
        if stat_signature(before) != stat_signature(expected):
            raise OSError("path changed before hashing")
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
        after = os.fstat(handle.fileno())
    if stat_signature(before) != stat_signature(after) or size != after.st_size:
        raise OSError("file changed while hashing")
    current = os.lstat(path)
    if stat_signature(current) != stat_signature(after):
        raise OSError("path changed while hashing")
    return digest.hexdigest(), size


def canonical_snapshot_bytes(snapshot: dict[str, Any]) -> bytes:
    return json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def snapshot_path(
    repo: Path,
    raw_path: bytes,
    seen_repos: set[Path],
) -> tuple[dict[str, Any], list[str]]:
    limitations: list[str] = []
    root_b = os.fsencode(repo)
    full = os.path.join(root_b, raw_path)
    try:
        info = os.lstat(full)
    except FileNotFoundError:
        return {"kind": "absent"}, limitations
    except OSError as exc:
        return {"kind": "unreadable", "error": str(exc)}, [
            f"cannot stat {safe_display_path(raw_path)}: {exc}"
        ]

    mode = stat.S_IMODE(info.st_mode)
    if stat.S_ISLNK(info.st_mode):
        try:
            target = os.readlink(full)
            target_b = os.fsencode(target) if isinstance(target, str) else target
            current = os.lstat(full)
            if stat_signature(current) != stat_signature(info):
                raise OSError("symlink changed while reading")
            return {
                "kind": "symlink",
                "mode": f"{mode:04o}",
                "size": len(target_b),
                "sha256": hashlib.sha256(target_b).hexdigest(),
            }, limitations
        except OSError as exc:
            return {"kind": "unreadable-symlink", "mode": f"{mode:04o}", "error": str(exc)}, [
                f"cannot read symlink {safe_display_path(raw_path)}: {exc}"
            ]

    if stat.S_ISREG(info.st_mode):
        try:
            digest, size = hash_file(full, info)
            return {
                "kind": "file",
                "mode": f"{mode:04o}",
                "size": size,
                "sha256": digest,
            }, limitations
        except OSError as exc:
            return {"kind": "unreadable-file", "mode": f"{mode:04o}", "error": str(exc)}, [
                f"cannot read {safe_display_path(raw_path)}: {exc}"
            ]

    if stat.S_ISDIR(info.st_mode):
        nested = Path(os.fsdecode(full)).resolve()
        probe = run_git(nested, "rev-parse", "--show-toplevel", check=False)
        nested_root: Path | None = None
        if probe.returncode == 0:
            try:
                nested_root = decode_git_path_line(probe.stdout, "nested git rev-parse --show-toplevel")
            except GitError as exc:
                return {"kind": "directory", "mode": f"{mode:04o}"}, [
                    f"cannot identify nested repository {safe_display_path(raw_path)}: {exc}"
                ]
        # `git -C ordinary/subdir rev-parse` also discovers the parent repository.
        # Treat the directory as a nested repository only when it is itself the root.
        if nested_root == nested:
            if nested_root in seen_repos:
                return {"kind": "git-directory", "mode": f"{mode:04o}", "cycle": True}, [
                    f"recursive Git directory at {safe_display_path(raw_path)}"
                ]
            child = fingerprint_repo(nested_root, seen_repos | {nested_root}, include_entries=False)
            if not child["complete"]:
                limitations.extend(
                    f"{safe_display_path(raw_path)}: {item}" for item in child.get("limitations", [])
                )
            return {
                "kind": "git-directory",
                "mode": f"{mode:04o}",
                "head": child["head"],
                "worktree_sha256": child["worktree_sha256"],
                "index_sha256": child["index_sha256"],
                "state_sha256": child["state_sha256"],
                "complete": child["complete"],
            }, limitations
        return {"kind": "directory", "mode": f"{mode:04o}"}, [
            f"untracked or special directory cannot be fingerprinted exactly: {safe_display_path(raw_path)}"
        ]

    return {
        "kind": "special",
        "mode": f"{mode:04o}",
        "size": info.st_size,
    }, [f"special file cannot be fingerprinted exactly: {safe_display_path(raw_path)}"]


def index_snapshot(repo: Path) -> tuple[dict[bytes, bytes], bytes]:
    """Return exact stage records keyed by path plus the canonical raw output."""
    raw = run_git(repo, "ls-files", "--stage", "-z", "--full-name").stdout
    by_path: dict[bytes, bytes] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        tab = record.find(b"\t")
        if tab < 0:
            raise GitError(f"unexpected git ls-files --stage record: {record!r}")
        path = record[tab + 1 :]
        by_path[path] = by_path.get(path, b"") + record + b"\0"
    return by_path, raw


def status_bytes(repo: Path) -> bytes:
    return run_git(
        repo,
        "-c",
        "core.fsmonitor=false",
        "-c",
        "core.untrackedCache=false",
        "-c",
        "status.renames=false",
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--ignore-submodules=none",
    ).stdout


def index_visibility_flags(repo: Path) -> tuple[list[dict[str, Any]], bytes]:
    """Return index flags that can make Git status omit worktree differences."""
    raw = run_git(repo, "ls-files", "-v", "-z", "--full-name").stdout
    records: list[tuple[bytes, bytes, bool, bool]] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        if len(record) < 3 or record[1:2] != b" ":
            raise GitError(f"unexpected git ls-files -v record: {record!r}")
        tag = record[:1]
        path = record[2:]
        assume_unchanged = tag.islower()
        skip_worktree = tag.upper() == b"S"
        if assume_unchanged or skip_worktree:
            records.append((tag, path, assume_unchanged, skip_worktree))

    records.sort(key=lambda item: (item[1], item[0]))
    canonical = b"\0".join(tag + b" " + path for tag, path, _assume, _skip in records)
    entries = [
        {
            "tag": tag.decode("ascii", "replace"),
            "path": display_path(path),
            "path_b64": base64.b64encode(path).decode("ascii"),
            "assume_unchanged": assume_unchanged,
            "skip_worktree": skip_worktree,
        }
        for tag, path, assume_unchanged, skip_worktree in records
    ]
    return entries, canonical


def fingerprint_repo(
    repo: Path,
    seen_repos: set[Path] | None = None,
    *,
    include_entries: bool = True,
) -> dict[str, Any]:
    repo = repo.resolve()

    inside = run_git(repo, "rev-parse", "--is-inside-work-tree", check=False)
    if inside.returncode != 0 or inside.stdout.strip() != b"true":
        raise GitError(f"not a Git worktree: {repo}")

    root_raw = run_git(repo, "rev-parse", "--show-toplevel").stdout
    root = decode_git_path_line(root_raw, "git rev-parse --show-toplevel")
    repo = root
    seen_repos = {item.resolve() for item in (seen_repos or set())}
    seen_repos.add(root)

    head_proc = run_git(repo, "rev-parse", "--verify", "HEAD", check=False)
    head = head_proc.stdout.strip().decode("ascii") if head_proc.returncode == 0 else "UNBORN"
    branch_proc = run_git(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    branch = branch_proc.stdout.strip().decode("utf-8", "replace") if branch_proc.returncode == 0 else "DETACHED"

    status_raw = status_bytes(repo)
    index_by_path, index_raw = index_snapshot(repo)
    hidden_index_flags, hidden_index_flags_raw = index_visibility_flags(repo)
    records = parse_status_z(status_raw)
    records.sort(key=lambda item: (item[1], item[2] or b"", item[0]))

    worktree_hasher = hashlib.sha256()
    index_hasher = hashlib.sha256()
    state_hasher = hashlib.sha256()
    for hasher, kind in (
        (worktree_hasher, b"worktree"),
        (index_hasher, b"index"),
        (state_hasher, b"state"),
    ):
        feed(hasher, b"schema", SCHEMA.encode("ascii"))
        feed(hasher, b"scope", SCOPE.encode("ascii"))
        feed(hasher, b"kind", kind)
        feed(hasher, b"head", head.encode("ascii"))

    entries: list[dict[str, Any]] = []
    limitations: list[str] = []
    if hidden_index_flags:
        limitations.append(
            f"{len(hidden_index_flags)} index visibility flag(s) can hide worktree changes; "
            "inspect hidden_index_flags in JSON output"
        )
    observations: list[tuple[bytes, bytes, bytes | None, bytes, bytes]] = []

    feed(index_hasher, b"hidden-index-flags", hidden_index_flags_raw)
    feed(state_hasher, b"hidden-index-flags", hidden_index_flags_raw)

    for xy, path, original in records:
        snapshot, path_limits = snapshot_path(repo, path, seen_repos)
        limitations.extend(path_limits)
        idx = index_by_path.get(path, b"")
        snapshot_bytes = canonical_snapshot_bytes(snapshot)
        observations.append((xy, path, original, snapshot_bytes, idx))

        for hasher in (worktree_hasher, index_hasher, state_hasher):
            feed(hasher, b"path", path)
            feed(hasher, b"original", original or b"")
        feed(worktree_hasher, b"worktree", snapshot_bytes)
        feed(index_hasher, b"index", idx)
        feed(state_hasher, b"xy", xy)
        feed(state_hasher, b"index", idx)
        feed(state_hasher, b"worktree", snapshot_bytes)

        if include_entries:
            entries.append(
                {
                    "xy": xy.decode("ascii", "replace"),
                    "path": display_path(path),
                    "path_b64": base64.b64encode(path).decode("ascii"),
                    "original_path": display_path(original) if original is not None else None,
                    "original_path_b64": base64.b64encode(original).decode("ascii") if original is not None else None,
                    "index_sha256": hashlib.sha256(idx).hexdigest(),
                    "worktree": snapshot,
                }
            )

    # Recheck repository and path state so the digest is not presented as complete
    # when files, index entries, branch, or HEAD moved during the pass.
    head_after_proc = run_git(repo, "rev-parse", "--verify", "HEAD", check=False)
    head_after = head_after_proc.stdout.strip().decode("ascii") if head_after_proc.returncode == 0 else "UNBORN"
    branch_after_proc = run_git(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    branch_after = (
        branch_after_proc.stdout.strip().decode("utf-8", "replace")
        if branch_after_proc.returncode == 0
        else "DETACHED"
    )
    status_after = status_bytes(repo)
    index_after_by_path, index_after_raw = index_snapshot(repo)
    if head_after != head:
        limitations.append("HEAD changed while fingerprinting")
    if branch_after != branch:
        limitations.append("branch state changed while fingerprinting")
    if status_after != status_raw:
        limitations.append("Git status changed while fingerprinting")
    if index_after_raw != index_raw:
        limitations.append("Git index entries changed while fingerprinting")

    for _xy, path, _original, snapshot_before, index_before in observations:
        snapshot_after, recheck_limits = snapshot_path(repo, path, seen_repos)
        limitations.extend(f"stability recheck: {item}" for item in recheck_limits)
        if canonical_snapshot_bytes(snapshot_after) != snapshot_before:
            limitations.append(f"worktree path changed while fingerprinting: {safe_display_path(path)}")
        if index_after_by_path.get(path, b"") != index_before:
            limitations.append(f"index entry changed while fingerprinting: {safe_display_path(path)}")

    _hidden_after, hidden_index_flags_after = index_visibility_flags(repo)
    if hidden_index_flags_after != hidden_index_flags_raw:
        limitations.append("index visibility flags changed while fingerprinting")

    # Preserve first occurrence order while avoiding duplicate nested limitations.
    limitations = list(dict.fromkeys(limitations))

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "scope": SCOPE,
        "ignored_paths_included": False,
        "repository": os.fspath(repo),
        "branch": branch,
        "head": head,
        "complete": not limitations,
        "entries_count": len(records),
        "hidden_index_flags_count": len(hidden_index_flags),
        "hidden_index_flags_sha256": hashlib.sha256(hidden_index_flags_raw).hexdigest(),
        "worktree_sha256": worktree_hasher.hexdigest(),
        "index_sha256": index_hasher.hexdigest(),
        "state_sha256": state_hasher.hexdigest(),
        "limitations": limitations,
    }
    if include_entries:
        result["entries"] = entries
        result["hidden_index_flags"] = hidden_index_flags
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo", default=".", help="Git worktree to fingerprint (default: current directory)")
    parser.add_argument("--json", action="store_true", help="emit the full JSON manifest")
    return parser


def render_line_value(value: Any) -> str:
    """Render one control-character-safe JSON scalar for key=value output."""
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = fingerprint_repo(Path(args.repo))
    except (GitError, OSError) as exc:
        # Keep diagnostics on one terminal-safe line even when a path or Git
        # message contains control characters.
        print(f"error: {escape_control_text(str(exc))}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True))
    else:
        for key in (
            "schema",
            "scope",
            "ignored_paths_included",
            "repository",
            "branch",
            "head",
            "complete",
            "entries_count",
            "hidden_index_flags_count",
            "hidden_index_flags_sha256",
            "worktree_sha256",
            "index_sha256",
            "state_sha256",
        ):
            print(f"{key}={render_line_value(result[key])}")
        for limitation in result["limitations"]:
            print(f"limitation={render_line_value(limitation)}")

    return 0 if result["complete"] else 3


if __name__ == "__main__":
    raise SystemExit(main())

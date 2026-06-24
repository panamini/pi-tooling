from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "worktree-fingerprint.py"
spec = importlib.util.spec_from_file_location("worktree_fingerprint", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout


def git_bytes(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


class FingerprintTests(unittest.TestCase):
    def make_repo(self) -> Path:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        repo = Path(self.tempdir.name)
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "Test User")
        git(repo, "config", "user.email", "test@example.invalid")
        (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
        git(repo, "add", "tracked.txt")
        git(repo, "commit", "-qm", "base")
        return repo

    def test_terminal_output_escapes_control_characters(self) -> None:
        rendered = module.escape_control_text('line\nbreak\t"quoted"')
        self.assertEqual(rendered, r'line\nbreak\t\"quoted\"')
        self.assertNotIn("\n", rendered)
        self.assertNotIn("\t", rendered)

    def test_cli_error_escapes_control_characters(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        path = Path(self.tempdir.name) / "not\na-repository"
        path.mkdir()
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = module.main(["--repo", str(path)])
        rendered = stderr.getvalue()
        self.assertEqual(exit_code, 2)
        self.assertEqual(len(rendered.splitlines()), 1)
        self.assertIn(r"not\na-repository", rendered)

    def test_clean_fingerprint_is_deterministic_and_read_only(self) -> None:
        repo = self.make_repo()
        before = git(repo, "status", "--porcelain=v1", "-uall")
        first = module.fingerprint_repo(repo)
        second = module.fingerprint_repo(repo)
        after = git(repo, "status", "--porcelain=v1", "-uall")
        self.assertTrue(first["complete"])
        self.assertEqual(first["state_sha256"], second["state_sha256"])
        self.assertEqual(first["entries_count"], 0)
        self.assertEqual(before, after)

    def test_tracked_and_untracked_content_changes_fingerprint(self) -> None:
        repo = self.make_repo()
        clean = module.fingerprint_repo(repo)
        (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
        changed = module.fingerprint_repo(repo)
        self.assertNotEqual(clean["worktree_sha256"], changed["worktree_sha256"])
        (repo / "new file.txt").write_text("untracked\n", encoding="utf-8")
        untracked = module.fingerprint_repo(repo)
        self.assertNotEqual(changed["state_sha256"], untracked["state_sha256"])
        self.assertEqual(untracked["entries_count"], 2)

    def test_ignored_paths_are_explicitly_out_of_scope(self) -> None:
        repo = self.make_repo()
        (repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
        git(repo, "add", ".gitignore")
        git(repo, "commit", "-qm", "ignore local file")
        before = module.fingerprint_repo(repo)
        (repo / "ignored.txt").write_text("local-only\n", encoding="utf-8")
        after = module.fingerprint_repo(repo)
        self.assertFalse(after["ignored_paths_included"])
        self.assertIn("ignored paths excluded", after["scope"])
        self.assertEqual(before["state_sha256"], after["state_sha256"])

    def test_index_digest_changes_when_staging_changes(self) -> None:
        repo = self.make_repo()
        (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
        unstaged = module.fingerprint_repo(repo)
        git(repo, "add", "tracked.txt")
        staged = module.fingerprint_repo(repo)
        self.assertEqual(unstaged["worktree_sha256"], staged["worktree_sha256"])
        self.assertNotEqual(unstaged["index_sha256"], staged["index_sha256"])
        self.assertNotEqual(unstaged["state_sha256"], staged["state_sha256"])

    def test_deleted_file_is_recorded(self) -> None:
        repo = self.make_repo()
        (repo / "tracked.txt").unlink()
        result = module.fingerprint_repo(repo)
        self.assertEqual(result["entries_count"], 1)
        self.assertEqual(result["entries"][0]["worktree"]["kind"], "absent")

    def test_subdirectory_invocation_reports_repository_root(self) -> None:
        repo = self.make_repo()
        nested = repo / "a directory" / "child"
        nested.mkdir(parents=True)
        result = module.fingerprint_repo(nested)
        self.assertEqual(Path(result["repository"]), repo.resolve())
        self.assertTrue(result["complete"])

    def test_unborn_repository_with_untracked_file_is_supported(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        repo = Path(self.tempdir.name)
        git(repo, "init", "-q")
        (repo / "new.txt").write_text("new\n", encoding="utf-8")
        result = module.fingerprint_repo(repo)
        self.assertEqual(result["head"], "UNBORN")
        self.assertEqual(result["entries_count"], 1)
        self.assertTrue(result["complete"])

    def test_status_parser_handles_rename_record(self) -> None:
        records = module.parse_status_z(b"R  new name.txt\0old name.txt\0")
        self.assertEqual(records, [(b"R ", b"new name.txt", b"old name.txt")])

    def test_unusual_untracked_filename_is_stable(self) -> None:
        repo = self.make_repo()
        unusual = repo / "line\nbreak-µ.txt"
        unusual.write_text("content\n", encoding="utf-8")
        first = module.fingerprint_repo(repo)
        second = module.fingerprint_repo(repo)
        self.assertTrue(first["complete"])
        self.assertEqual(first["state_sha256"], second["state_sha256"])
        self.assertIn("line\nbreak-µ.txt", [entry["path"] for entry in first["entries"]])

    def test_fingerprint_does_not_refresh_git_index(self) -> None:
        repo = self.make_repo()
        index = Path(git(repo, "rev-parse", "--git-path", "index").strip())
        if not index.is_absolute():
            index = repo / index
        before_bytes = index.read_bytes()
        before_mtime = index.stat().st_mtime_ns
        result = module.fingerprint_repo(repo)
        self.assertTrue(result["complete"])
        self.assertEqual(before_bytes, index.read_bytes())
        self.assertEqual(before_mtime, index.stat().st_mtime_ns)

    def test_empty_unborn_repository_is_supported(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        repo = Path(self.tempdir.name)
        git(repo, "init", "-q")
        result = module.fingerprint_repo(repo)
        self.assertTrue(result["complete"])
        self.assertEqual(result["head"], "UNBORN")
        self.assertEqual(result["entries_count"], 0)

    def test_repository_path_preserves_trailing_space(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        repo = Path(self.tempdir.name) / "repo-with-space "
        repo.mkdir()
        git(repo, "init", "-q")
        result = module.fingerprint_repo(repo)
        self.assertEqual(result["repository"], str(repo.resolve()))
        self.assertTrue(result["complete"])

    def test_plain_directory_is_not_misclassified_as_nested_repository(self) -> None:
        repo = self.make_repo()
        ordinary = repo / "ordinary"
        ordinary.mkdir()
        snapshot, limitations = module.snapshot_path(repo, b"ordinary", {repo.resolve()})
        self.assertEqual(snapshot["kind"], "directory")
        self.assertTrue(any("cannot be fingerprinted exactly" in item for item in limitations))

    def test_embedded_repository_is_fingerprinted_as_nested_state(self) -> None:
        repo = self.make_repo()
        embedded = repo / "embedded"
        embedded.mkdir()
        git(embedded, "init", "-q")
        git(embedded, "config", "user.name", "Nested User")
        git(embedded, "config", "user.email", "nested@example.invalid")
        (embedded / "nested.txt").write_text("nested\n", encoding="utf-8")
        git(embedded, "add", "nested.txt")
        git(embedded, "commit", "-qm", "nested base")

        result = module.fingerprint_repo(repo)
        embedded_entries = [entry for entry in result["entries"] if entry["path"].rstrip("/") == "embedded"]
        self.assertEqual(len(embedded_entries), 1)
        self.assertEqual(embedded_entries[0]["worktree"]["kind"], "git-directory")
        self.assertTrue(embedded_entries[0]["worktree"]["complete"])

    def test_assume_unchanged_flag_makes_fingerprint_incomplete(self) -> None:
        repo = self.make_repo()
        git(repo, "update-index", "--assume-unchanged", "tracked.txt")
        (repo / "tracked.txt").write_text("hidden change\n", encoding="utf-8")

        result = module.fingerprint_repo(repo)
        self.assertFalse(result["complete"])
        self.assertEqual(result["entries_count"], 0)
        self.assertEqual(result["hidden_index_flags_count"], 1)
        self.assertTrue(result["hidden_index_flags"][0]["assume_unchanged"])
        self.assertTrue(any("can hide worktree changes" in item for item in result["limitations"]))

    def test_skip_worktree_flag_is_reported(self) -> None:
        repo = self.make_repo()
        git(repo, "update-index", "--skip-worktree", "tracked.txt")

        result = module.fingerprint_repo(repo)
        self.assertFalse(result["complete"])
        self.assertEqual(result["hidden_index_flags_count"], 1)
        self.assertTrue(result["hidden_index_flags"][0]["skip_worktree"])

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable")
    def test_symlink_target_changes_worktree_fingerprint(self) -> None:
        repo = self.make_repo()
        link = repo / "link"
        os.symlink("first-target", link)
        first = module.fingerprint_repo(repo)
        link.unlink()
        os.symlink("second-target", link)
        second = module.fingerprint_repo(repo)
        self.assertTrue(first["complete"])
        self.assertTrue(second["complete"])
        self.assertNotEqual(first["worktree_sha256"], second["worktree_sha256"])

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFOs are unavailable")
    def test_encountered_special_file_reports_limitation(self) -> None:
        repo = self.make_repo()
        os.mkfifo(repo / "named-pipe")
        snapshot, limitations = module.snapshot_path(repo, b"named-pipe", {repo.resolve()})
        self.assertEqual(snapshot["kind"], "special")
        self.assertTrue(any("special file" in item for item in limitations))

    def test_stability_recheck_detects_mid_pass_change(self) -> None:
        repo = self.make_repo()
        target = repo / "tracked.txt"
        target.write_text("first change\n", encoding="utf-8")
        original = module.snapshot_path
        calls = 0

        def changing_snapshot(repo_arg, raw_path, seen_repos):
            nonlocal calls
            result = original(repo_arg, raw_path, seen_repos)
            calls += 1
            if calls == 1:
                target.write_text("second change\n", encoding="utf-8")
            return result

        module.snapshot_path = changing_snapshot
        self.addCleanup(setattr, module, "snapshot_path", original)
        result = module.fingerprint_repo(repo)
        self.assertFalse(result["complete"])
        self.assertTrue(
            any("changed while fingerprinting" in item for item in result["limitations"]),
            result["limitations"],
        )

    def test_ambient_git_routing_environment_is_ignored(self) -> None:
        repo = self.make_repo()
        expected_head = git(repo, "rev-parse", "HEAD").strip()

        other_tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(other_tempdir.cleanup)
        other = Path(other_tempdir.name)
        git(other, "init", "-q")

        hostile_env = {
            "GIT_DIR": str(other / ".git"),
            "GIT_WORK_TREE": str(other),
            "GIT_INDEX_FILE": str(other / ".git" / "index"),
            "GIT_NAMESPACE": "redirected",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.bare",
            "GIT_CONFIG_VALUE_0": "true",
        }
        with mock.patch.dict(os.environ, hostile_env, clear=False):
            result = module.fingerprint_repo(repo)

        self.assertEqual(Path(result["repository"]), repo.resolve())
        self.assertEqual(result["head"], expected_head)
        self.assertTrue(result["complete"])

    def test_index_snapshot_keeps_pathspec_like_names_literal(self) -> None:
        repo = self.make_repo()
        literal = repo / "*.txt"
        other = repo / "other.txt"
        literal.write_text("literal base\n", encoding="utf-8")
        other.write_text("other base\n", encoding="utf-8")
        git(repo, "add", "--", "*.txt", "other.txt")
        git(repo, "commit", "-qm", "add pathspec-like names")

        literal.write_text("literal changed\n", encoding="utf-8")
        other.write_text("other changed\n", encoding="utf-8")
        result = module.fingerprint_repo(repo)
        entries = {entry["path"]: entry for entry in result["entries"]}

        records = git_bytes(repo, "ls-files", "--stage", "-z", "--full-name").split(b"\0")
        expected_record = next(record + b"\0" for record in records if record.endswith(b"\t*.txt"))
        expected_hash = hashlib.sha256(expected_record).hexdigest()

        self.assertEqual(entries["*.txt"]["index_sha256"], expected_hash)
        self.assertNotEqual(entries["*.txt"]["index_sha256"], entries["other.txt"]["index_sha256"])

    def test_default_cli_output_escapes_repository_control_characters(self) -> None:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        repo = Path(tempdir.name) / "repo\nname"
        repo.mkdir()
        git(repo, "init", "-q")

        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(repo)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        self.assertEqual(proc.returncode, 0, proc.stderr)
        repository_lines = [line for line in proc.stdout.splitlines() if line.startswith("repository=")]
        self.assertEqual(len(repository_lines), 1)
        self.assertEqual(json.loads(repository_lines[0].split("=", 1)[1]), str(repo.resolve()))
        self.assertIn(r"\n", repository_lines[0])


if __name__ == "__main__":
    unittest.main()

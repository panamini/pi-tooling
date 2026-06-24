from __future__ import annotations

import os
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"

EXPECTED_FILES = {
    ".gitignore",
    "README.md",
    "SKILL.md",
    "agents/openai.yaml",
    "references/change-contract.md",
    "references/code-review.md",
    "references/evaluation-cases.md",
    "references/git-safety.md",
    "references/verification.md",
    "scripts/worktree-fingerprint.py",
    "tests/test_skill_package.py",
    "tests/test_worktree_fingerprint.py",
}

EXPECTED_MAIN_STATUSES = {
    "TARGET_CLEAR",
    "NEEDS_TARGET",
    "READY_FOR_APPROVAL",
    "AUTHORIZED_TO_IMPLEMENT",
    "NEEDS_DECISION",
    "LOCAL_PASS",
    "LOCAL_PASS_WITH_LIMITATIONS",
    "LOCAL_FAIL",
    "LOCAL_BLOCKED",
    "STALE_CONTRACT",
    "VERIFIED",
    "VERIFIED_WITH_LIMITATIONS",
    "VERIFICATION_FAILED",
    "VERIFICATION_BLOCKED",
    "LOCAL_REVIEW_CLEAR",
    "LOCAL_REVIEW_NOTES",
    "LOCAL_REVIEW_CHANGES_REQUIRED",
    "STAGED",
    "COMMIT_CREATED",
    "PUSHED",
    "PR_CREATED_DRAFT",
    "PR_CREATED_READY",
    "PR_MARKED_READY",
    "PR_UPDATED",
    "REMOTE_REVIEW_SUBMITTED",
    "MERGE_READY",
    "MERGE_BLOCKED",
    "MERGE_READINESS_UNKNOWN",
    "MERGED",
    "PUBLISH_BLOCKED",
    "BLOCKED",
}


class SkillPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = SKILL_PATH.read_text(encoding="utf-8")
        cls.skill_lines = cls.skill_text.splitlines()

    def parse_frontmatter(self) -> dict[str, str]:
        self.assertGreaterEqual(len(self.skill_lines), 4)
        self.assertEqual(self.skill_lines[0], "---")
        try:
            end = self.skill_lines.index("---", 1)
        except ValueError as exc:  # pragma: no cover - assertion path
            self.fail(f"SKILL.md frontmatter is not closed: {exc}")

        metadata: dict[str, str] = {}
        for line in self.skill_lines[1:end]:
            self.assertRegex(line, r"^[a-z][a-z0-9-]*: .+$")
            key, value = line.split(":", 1)
            self.assertNotIn(key, metadata)
            metadata[key] = value.strip()
        return metadata

    def test_frontmatter_is_minimal_and_spec_conformant(self) -> None:
        metadata = self.parse_frontmatter()
        self.assertEqual(set(metadata), {"name", "description"})

        name = metadata["name"]
        self.assertLessEqual(len(name), 64)
        self.assertRegex(name, r"^(?!.*--)[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertEqual(name, ROOT.name)

        description = metadata["description"]
        self.assertGreaterEqual(len(description), 1)
        self.assertLessEqual(len(description), 1024)
        self.assertIn("Use for", description)
        self.assertIn("Do not use", description)
        self.assertIn("file triage", description)
        self.assertIn("pure code explanation", description)

    def test_main_skill_uses_progressive_disclosure(self) -> None:
        self.assertLessEqual(len(self.skill_lines), 500)
        self.assertIn("## Load only the reference needed", self.skill_text)
        self.assertIn("Do not load every reference by default.", self.skill_text)

    def test_main_skill_links_exist_and_are_shallow(self) -> None:
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", self.skill_text)
        self.assertGreaterEqual(len(links), 6)
        for target in links:
            self.assertFalse(target.startswith(("http://", "https://", "#")))
            relative = Path(target)
            self.assertNotIn("..", relative.parts)
            self.assertEqual(len(relative.parts), 2, target)
            self.assertTrue((ROOT / relative).is_file(), target)

    def test_bundle_contains_only_intentional_files(self) -> None:
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(actual, EXPECTED_FILES)
        self.assertTrue((ROOT / "README.md").is_file())

    def test_long_references_have_contents_sections(self) -> None:
        for path in sorted((ROOT / "references").glob("*.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            if len(lines) > 100:
                self.assertIn("## Contents", lines[:20], path.name)

    def test_evaluation_case_numbering_and_contents_match(self) -> None:
        text = (ROOT / "references/evaluation-cases.md").read_text(encoding="utf-8")
        headings = [
            (int(number), title)
            for number, title in re.findall(r"^## (\d+)\. (.+)$", text, re.MULTILINE)
        ]
        self.assertGreaterEqual(len(headings), 40)
        self.assertEqual([number for number, _ in headings], list(range(1, len(headings) + 1)))

        contents_match = re.search(
            r"^## Contents\n\n(?P<body>(?:- .+\n)+)\n## 1\.",
            text,
            re.MULTILINE,
        )
        self.assertIsNotNone(contents_match)
        toc = [
            (int(number), title)
            for number, title in re.findall(
                r"^- (\d+)\. (.+)$",
                contents_match.group("body"),
                re.MULTILINE,
            )
        ]
        self.assertEqual(toc, headings)

    def test_markdown_is_utf8_clean_and_fences_are_balanced(self) -> None:
        for path in sorted(ROOT.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for number, line in enumerate(text.splitlines(), 1):
                self.assertEqual(line, line.rstrip(), f"trailing whitespace: {path}:{number}")

            active: tuple[str, int] | None = None
            for number, line in enumerate(text.splitlines(), 1):
                match = re.match(r"^\s*(`{3,}|~{3,})", line)
                if not match:
                    continue
                marker = match.group(1)
                token = marker[0]
                if active is None:
                    active = (token, len(marker))
                elif active[0] == token and len(marker) >= active[1]:
                    active = None
            self.assertIsNone(active, f"unclosed Markdown fence in {path}")

    def test_openai_interface_metadata_is_complete(self) -> None:
        text = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertRegex(text, r'(?m)^interface:\n')
        self.assertRegex(text, r'(?m)^  display_name: "[^"\n]+"$')
        short = re.search(r'(?m)^  short_description: "([^"\n]+)"$', text)
        self.assertIsNotNone(short)
        self.assertGreaterEqual(len(short.group(1)), 25)
        self.assertLessEqual(len(short.group(1)), 64)
        prompt = re.search(r'(?m)^  default_prompt: "([^"\n]+)"$', text)
        self.assertIsNotNone(prompt)
        self.assertIn("$changeset", prompt.group(1))

    def test_status_vocabulary_is_defined_and_non_provider_like(self) -> None:
        for token in EXPECTED_MAIN_STATUSES:
            self.assertIn(f"`{token}`", self.skill_text, token)

        for obsolete in ("REVIEW_APPROVE", "REVIEW_COMMENT", "REVIEW_REQUEST_CHANGES"):
            self.assertNotIn(obsolete, self.skill_text)
            for path in (ROOT / "references").glob("*.md"):
                self.assertNotIn(obsolete, path.read_text(encoding="utf-8"), path.name)

        review = (ROOT / "references/code-review.md").read_text(encoding="utf-8")
        for token in ("LOCAL_REVIEW_CLEAR", "LOCAL_REVIEW_NOTES", "LOCAL_REVIEW_CHANGES_REQUIRED"):
            self.assertIn(f"`{token}`", review)

        git_safety = (ROOT / "references/git-safety.md").read_text(encoding="utf-8")
        self.assertIn("`MERGE_READINESS_UNKNOWN`", git_safety)

    def test_readme_validation_commands_are_current_and_offline_safe(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("skills-ref validate ./changeset", text)
        self.assertIn("python3 -m unittest discover -v", text)
        self.assertNotIn("uvx --from skills-ref", text)

    def test_git_diff_and_shell_safety_guards_are_present(self) -> None:
        git_safety = (ROOT / "references/git-safety.md").read_text(encoding="utf-8")
        self.assertIn("--no-ext-diff", self.skill_text)
        self.assertIn("--no-textconv", self.skill_text)
        self.assertIn("GIT_LITERAL_PATHSPECS=1", git_safety)
        self.assertIn("never use `eval`", git_safety)

    def test_helper_is_executable_and_syntax_valid(self) -> None:
        helper = ROOT / "scripts/worktree-fingerprint.py"
        self.assertTrue(os.access(helper, os.X_OK))
        source = helper.read_text(encoding="utf-8")
        self.assertTrue(source.startswith("#!/usr/bin/env python3\n"))
        compile(source, os.fspath(helper), "exec")


if __name__ == "__main__":
    unittest.main()

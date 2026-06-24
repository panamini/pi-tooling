# Changeset

A portable Agent Skill for planning, implementing, verifying, reviewing, and publishing one scoped repository change without overwriting unrelated work or overstating evidence.

## Install

Use the shared Agent Skills location supported by Codex and Pi:

```bash
mkdir -p ~/.agents/skills/changeset
cp -R changeset/. ~/.agents/skills/changeset/
```

For a repository-scoped installation:

```bash
mkdir -p .agents/skills/changeset
cp -R changeset/. .agents/skills/changeset/
```

Invoke explicitly as `$changeset` in Codex or `/skill:changeset` in Pi. Both can also select it from its description.

Bundled references and scripts are resolved relative to this skill directory, not the repository being changed. For broader distribution, keep this portable skill folder as the shared source and wrap it in a Codex plugin or Pi package only when a registry/installable package is needed.

## Structure

```text
changeset/
├── .gitignore
├── README.md
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── change-contract.md
│   ├── code-review.md
│   ├── evaluation-cases.md
│   ├── git-safety.md
│   └── verification.md
├── scripts/worktree-fingerprint.py
└── tests/
    ├── test_skill_package.py
    └── test_worktree_fingerprint.py
```

The optional Python 3.10+ helper is read-only by design. It produces separate baseline-aware worktree, index, and combined change-state SHA-256 fingerprints without printing file contents; compare two consecutive complete runs when high-confidence uncommitted identity matters.

It covers paths reported by Git status, including non-ignored untracked files. Ignored paths and external environment state remain outside the fingerprint. Its output still contains repository/path metadata and content hashes. Review and redact that metadata before placing raw output in a public issue, PR, or log.

## Validate

```bash
skills-ref validate ./changeset
python3 -m unittest discover -v -s ./changeset/tests -p 'test_*.py'
```

`skills-ref` is the reference validator named by the Agent Skills specification. The bundled tests provide offline structural and helper checks; the skill remains usable when that validator is not installed.

## Security

Review the skill and helper before installation. Repository tests, package scripts, Git hooks, diff/textconv helpers, and hosting commands may execute code or contact external systems; the workflow therefore inspects and authorizes them according to scope and risk.

## Operational principle

A plan is not approval, implementation is not publication, a PR ready for review is not merge-ready, local checks are not remote CI, and reproducibility is not reviewer independence.

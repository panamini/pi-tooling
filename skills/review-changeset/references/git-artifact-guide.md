# Safe Git artifact guide

Use these as command shapes, not as permission to bypass repository wrappers. Prefix
or route every command through the wrapper required by active instructions.

Do not fetch, switch branches, alter the index, or mutate history.

## Repository and state

```sh
git rev-parse --show-toplevel
git branch --show-current
git rev-parse --verify HEAD
git status --short
git diff --check
git ls-files --others --exclude-standard
```

When the repository requires a before/after fingerprint, capture the exact
`git status --short` output and resolved `HEAD` before verification, then repeat it
afterward.

## Staged only

```sh
git diff --cached --name-status
git diff --cached --stat
git diff --cached --check
git diff --cached
```

Scope is `HEAD` versus the index. Exclude unstaged and untracked content.

## Unstaged only

```sh
git diff --name-status
git diff --stat
git diff --check
git diff
```

Scope is index versus worktree. Exclude staged and untracked content.

## Complete current worktree

```sh
git diff HEAD --name-status
git diff HEAD --stat
git diff HEAD --check
git diff HEAD
git ls-files --others --exclude-standard
```

`git diff HEAD` includes staged and unstaged tracked changes but not untracked files.
Read relevant untracked files separately. Never treat ignored files as part of scope
unless the user explicitly names them.

## Branch against base

Resolve and show the base ref before review.

Useful local evidence:

```sh
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git symbolic-ref --quiet --short refs/remotes/origin/HEAD
git show-ref --verify --quiet refs/remotes/origin/main
git show-ref --verify --quiet refs/remotes/origin/master
git show-ref --verify --quiet refs/heads/main
git show-ref --verify --quiet refs/heads/master
```

After selecting a defensible base:

```sh
git merge-base <base> HEAD
git diff <base>...HEAD --name-status
git diff <base>...HEAD --stat
git diff <base>...HEAD --check
git diff <base>...HEAD
git log --oneline --decorate <base>..HEAD
```

Three-dot diff compares `HEAD` with the merge base. Do not replace it with a two-dot
diff unless the user explicitly requested endpoint-to-endpoint comparison.

A configured upstream is not automatically the integration base. For example, a
feature branch may track its same-named remote branch. Use repository/PR context and
local default-branch evidence.

## Commit

```sh
git show --stat --oneline --decorate <commit>
git show --format=fuller --find-renames --find-copies <commit>
git diff-tree --no-commit-id --name-status -r <commit>
```

For a root commit, use `git show`; do not assume `<commit>^` exists.

## Commit range

Clarify whether the user supplied endpoint (`A..B`) or merge-base (`A...B`) semantics.
Do not silently change one into the other.

```sh
git diff A..B --name-status
git diff A..B --stat
git diff A..B --check
git diff A..B
```

or:

```sh
git diff A...B --name-status
git diff A...B --stat
git diff A...B --check
git diff A...B
```

## Path-level context

Use narrow search and history only when needed to prove a candidate:

```sh
git grep -n -- <symbol-or-literal>
git log -p -- <path>
git blame -L <start>,<end> -- <path>
```

Do not treat blame or commit messages as authoritative requirements. They are context
only.

## Renames, submodules, and binaries

- Use rename-aware diff output when a move could hide semantic changes.
- For submodule pointer changes, identify the old/new commit locally; do not fetch.
- Mark binaries as not directly reviewable and inspect the code/config that consumes
  them when relevant.
- For lockfiles, inspect the matching manifest and meaningful package/version/source
  changes rather than reviewing raw lockfile noise.

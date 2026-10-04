# Harmonic Composition

A portable Agent Skill by Norma for composing interfaces, pages, HUDs, and frames with measurable proportions.

It gives Codex, Claude Code, and other Agent Skills-compatible tools a practical workflow for:

- choosing a frame and one governing proportional family;
- deriving positions, grids, type scales, and spacing tokens;
- separating exact, strong, approximate, and speculative readings;
- verifying the rendered result for legibility and platform constraints.

## Install

Copy the `skills/harmonic-composition` directory into the skill directory used by your agent.

### Codex

~~~bash
mkdir -p ~/.codex/skills
git clone --depth 1 https://github.com/panamini/pi-tooling.git /tmp/pi-tooling
cp -R /tmp/pi-tooling/skills/harmonic-composition ~/.codex/skills/
~~~

### Claude Code

~~~bash
mkdir -p .claude/skills
git clone --depth 1 https://github.com/panamini/pi-tooling.git /tmp/pi-tooling
cp -R /tmp/pi-tooling/skills/harmonic-composition .claude/skills/
~~~

The folder follows the open Agent Skills shape: one `SKILL.md` plus optional `references/` files. Read the source before enabling it in a project.

## Example prompts

- “Use harmonic composition to audit this landing page’s proportions.”
- “Build this dashboard with one rational grid and verify the rendered spacing.”
- “Derive a type scale and spacing tokens for this editorial interface.”
- “Show which ratios are exact, approximate, or speculative in this layout.”

## Scope

This skill provides design reasoning and implementation guidance. It does not claim that a ratio guarantees beauty, and it never overrides legibility, safe areas, accessibility, content hierarchy, or platform rules.

## License

The files in this directory are available under the [PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0).

Noncommercial study, teaching, research, and personal use are permitted under that license. Any commercial use requires a separate written license from the rights holder.

This license applies only to this skill directory; other resources in `pi-tooling` retain their own licenses.

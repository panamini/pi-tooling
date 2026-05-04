import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { join, relative } from "node:path";
import type { ExtensionAPI, ExtensionCommandContext } from "@mariozechner/pi-coding-agent";

type SkillInfo = {
	name: string;
	description: string;
	path: string;
	bytes: number;
	mtimeMs: number;
};

type Skin = {
	name: string;
	description: string;
	instructions: string;
};

const SKINS: Record<string, Skin> = {
	builder: {
		name: "builder",
		description: "Practical implementation mode: concise, makes changes, verifies.",
		instructions:
			"Prefer direct implementation. Keep explanations short. Before editing, identify the minimum viable change. After editing, run the smallest useful verification and summarize changed files.",
	},
	reviewer: {
		name: "reviewer",
		description: "Adversarial review mode: risks, regressions, missing tests.",
		instructions:
			"Act as a skeptical reviewer. Look for regressions, missing tests, security issues, ambiguous requirements, and UX edge cases. Prioritize concrete findings over praise.",
	},
	researcher: {
		name: "researcher",
		description: "Evidence-first mode: sources, comparisons, uncertainty.",
		instructions:
			"Prefer gathering evidence before deciding. Use web/code search when current external knowledge matters. Separate facts, assumptions, and recommendations.",
	},
	minimal: {
		name: "minimal",
		description: "Low-chatter mode: minimal questions, compact output.",
		instructions:
			"Be extremely concise. Ask only blocking questions. Avoid long tables unless requested. Prefer action over explanation.",
	},
	planner: {
		name: "planner",
		description: "Blueprint-style mode: break work into safe steps and gates.",
		instructions:
			"Plan before implementing. Break work into small reversible steps with dependencies, verification commands, and exit criteria. Flag parallelizable work.",
	},
};

function slugify(input: string): string {
	return input
		.trim()
		.toLowerCase()
		.replace(/[^a-z0-9]+/g, "-")
		.replace(/^-+|-+$/g, "")
		.slice(0, 64);
}

function titleCase(slug: string): string {
	return slug
		.split("-")
		.filter(Boolean)
		.map((part) => part.charAt(0).toUpperCase() + part.slice(1))
		.join(" ");
}

function ensurePiDir(cwd: string): string {
	const dir = join(cwd, ".pi");
	mkdirSync(dir, { recursive: true });
	return dir;
}

function activeSkinPath(cwd: string): string {
	return join(ensurePiDir(cwd), "active-skin.json");
}

function nudgeConfigPath(cwd: string): string {
	return join(ensurePiDir(cwd), "auto-nudge.json");
}

function isNudgeEnabled(cwd: string): boolean {
	const file = nudgeConfigPath(cwd);
	if (!existsSync(file)) return true;
	try {
		const parsed = JSON.parse(readFileSync(file, "utf-8"));
		return parsed.enabled !== false;
	} catch {
		return true;
	}
}

function setNudgeEnabled(cwd: string, enabled: boolean): void {
	writeFileSync(nudgeConfigPath(cwd), `${JSON.stringify({ enabled }, null, 2)}\n`, "utf-8");
}

function readActiveSkin(cwd: string): Skin | null {
	const file = activeSkinPath(cwd);
	if (!existsSync(file)) return null;
	try {
		const parsed = JSON.parse(readFileSync(file, "utf-8"));
		const name = typeof parsed.name === "string" ? parsed.name : "";
		return SKINS[name] ?? null;
	} catch {
		return null;
	}
}

function setActiveSkin(cwd: string, name: string | null): void {
	if (!name) {
		writeFileSync(activeSkinPath(cwd), `${JSON.stringify({ name: null }, null, 2)}\n`, "utf-8");
		return;
	}
	writeFileSync(activeSkinPath(cwd), `${JSON.stringify({ name }, null, 2)}\n`, "utf-8");
}

function walkSkillFiles(root: string, files: string[] = []): string[] {
	if (!existsSync(root)) return files;
	for (const entry of readdirSync(root)) {
		if (entry === "node_modules" || entry === ".git" || entry === ".archive") continue;
		const path = join(root, entry);
		let stat;
		try {
			stat = statSync(path);
		} catch {
			continue;
		}
		if (stat.isDirectory()) walkSkillFiles(path, files);
		else if (entry === "SKILL.md") files.push(path);
	}
	return files;
}

function parseSkill(file: string): SkillInfo {
	const content = readFileSync(file, "utf-8");
	const stat = statSync(file);
	const frontmatter = content.match(/^---\n([\s\S]*?)\n---/);
	const fm = frontmatter?.[1] ?? "";
	const name = fm.match(/^name:\s*["']?([^"'\n]+)["']?/m)?.[1]?.trim() || slugify(file.split("/").slice(-2, -1)[0] || "skill");
	const description = fm.match(/^description:\s*(?:>-\s*)?["']?([^"'\n]+)["']?/m)?.[1]?.trim() || "";
	return { name, description, path: file, bytes: stat.size, mtimeMs: stat.mtimeMs };
}

function collectSkills(cwd: string): SkillInfo[] {
	const paths = new Set<string>();
	for (const root of [join(cwd, "skills"), join(cwd, "extensions")]) {
		for (const file of walkSkillFiles(root)) paths.add(file);
	}
	return [...paths].sort().map(parseSkill);
}

function duplicateGroups(skills: SkillInfo[]): SkillInfo[][] {
	const groups = new Map<string, SkillInfo[]>();
	for (const skill of skills) {
		const key = skill.name.toLowerCase().replace(/[^a-z0-9]/g, "");
		const list = groups.get(key) ?? [];
		list.push(skill);
		groups.set(key, list);
	}
	return [...groups.values()].filter((group) => group.length > 1);
}

function buildCuratorReport(cwd: string): string {
	const skills = collectSkills(cwd);
	const duplicates = duplicateGroups(skills);
	const now = Date.now();
	const stale = skills.filter((skill) => now - skill.mtimeMs > 180 * 24 * 60 * 60 * 1000);
	const tiny = skills.filter((skill) => skill.bytes < 500);
	const missingDescriptions = skills.filter((skill) => !skill.description);

	const lines = [
		"# Skill Curator Report",
		"",
		`Generated: ${new Date().toISOString()}`,
		`Root: ${cwd}`,
		"",
		"## Summary",
		`- Skills found: ${skills.length}`,
		`- Duplicate-name groups: ${duplicates.length}`,
		`- Missing descriptions: ${missingDescriptions.length}`,
		`- Very small skills (<500 bytes): ${tiny.length}`,
		`- Stale skills (>180 days): ${stale.length}`,
		"",
		"## Recommended actions",
	];

	if (duplicates.length === 0 && missingDescriptions.length === 0 && tiny.length === 0 && stale.length === 0) {
		lines.push("- No obvious cleanup actions found.");
	} else {
		if (duplicates.length) lines.push("- Review duplicate-name groups and consolidate where they overlap.");
		if (missingDescriptions.length) lines.push("- Add descriptions to skills with missing frontmatter descriptions.");
		if (tiny.length) lines.push("- Expand tiny skills or merge them into broader workflow skills.");
		if (stale.length) lines.push("- Re-test stale skills before relying on them in routing.");
	}

	lines.push("", "## Duplicate-name groups");
	if (!duplicates.length) lines.push("- None");
	for (const group of duplicates) {
		lines.push(`- ${group[0].name}`);
		for (const skill of group) lines.push(`  - ${relative(cwd, skill.path)}`);
	}

	lines.push("", "## Missing descriptions");
	if (!missingDescriptions.length) lines.push("- None");
	for (const skill of missingDescriptions) lines.push(`- ${skill.name} — ${relative(cwd, skill.path)}`);

	lines.push("", "## Tiny skills");
	if (!tiny.length) lines.push("- None");
	for (const skill of tiny) lines.push(`- ${skill.name} (${skill.bytes} bytes) — ${relative(cwd, skill.path)}`);

	lines.push("", "## Stale skills");
	if (!stale.length) lines.push("- None");
	for (const skill of stale) lines.push(`- ${skill.name} — ${relative(cwd, skill.path)}`);

	return `${lines.join("\n")}\n`;
}

function handleSkillDraft(args: string, ctx: ExtensionCommandContext): void {
	const [rawName, ...rest] = args.trim().split(/\s+/).filter(Boolean);
	if (!rawName) {
		ctx.ui.notify("Usage: /skill-draft <name> [short description]", "error");
		return;
	}

	const slug = slugify(rawName);
	const description = rest.join(" ") || `Reusable workflow for ${titleCase(slug)}.`;
	const skillDir = join(ctx.cwd, "skills", slug);
	const skillPath = join(skillDir, "SKILL.md");
	if (existsSync(skillPath)) {
		ctx.ui.notify(`Skill already exists: ${skillPath}`, "warning");
		return;
	}

	mkdirSync(skillDir, { recursive: true });
	writeFileSync(
		skillPath,
		`---\nname: ${slug}\ndescription: ${description}\ndisable-model-invocation: true\n---\n\n# ${titleCase(slug)}\n\n## When to use\n\nUse this skill when the user asks for ${description.toLowerCase()}\n\n## Workflow\n\n1. Confirm the task scope if it is ambiguous.\n2. Inspect the relevant files, inputs, or external references.\n3. Execute the smallest safe workflow that satisfies the request.\n4. Verify the output and summarize changed files or delivered artifacts.\n\n## Notes\n\n- Keep this skill focused. Split broader behavior into separate skills.\n- Update this file after using it successfully 2-3 times.\n`,
		"utf-8",
	);
	ctx.ui.notify(`Drafted skill: ${skillPath}`, "info");
}

function handleCurator(ctx: ExtensionCommandContext): void {
	const report = buildCuratorReport(ctx.cwd);
	const out = join(ensurePiDir(ctx.cwd), "SKILL_CURATOR_REPORT.md");
	writeFileSync(out, report, "utf-8");
	ctx.ui.notify(`Wrote skill curator report: ${out}`, "info");
}

function handleSkin(args: string, ctx: ExtensionCommandContext): void {
	const arg = args.trim().toLowerCase();
	if (!arg || arg === "status") {
		const active = readActiveSkin(ctx.cwd);
		ctx.ui.notify(active ? `Active skin: ${active.name} — ${active.description}` : "No active skin", "info");
		return;
	}
	if (arg === "list") {
		ctx.ui.notify(Object.values(SKINS).map((skin) => `${skin.name}: ${skin.description}`).join("\n"), "info");
		return;
	}
	if (arg === "off" || arg === "none" || arg === "clear") {
		setActiveSkin(ctx.cwd, null);
		ctx.ui.notify("Personality skin disabled", "info");
		return;
	}
	const skin = SKINS[arg];
	if (!skin) {
		ctx.ui.notify(`Unknown skin '${arg}'. Use /skin list`, "error");
		return;
	}
	setActiveSkin(ctx.cwd, skin.name);
	ctx.ui.notify(`Active skin: ${skin.name} — ${skin.description}`, "info");
}

function handleNudge(args: string, ctx: ExtensionCommandContext): void {
	const arg = args.trim().toLowerCase();
	if (!arg || arg === "status") {
		ctx.ui.notify(`Auto-nudge is ${isNudgeEnabled(ctx.cwd) ? "on" : "off"}`, "info");
		return;
	}
	if (arg === "on" || arg === "enable") {
		setNudgeEnabled(ctx.cwd, true);
		ctx.ui.notify("Auto-nudge enabled", "info");
		return;
	}
	if (arg === "off" || arg === "disable") {
		setNudgeEnabled(ctx.cwd, false);
		ctx.ui.notify("Auto-nudge disabled", "info");
		return;
	}
	ctx.ui.notify("Usage: /nudge [on|off|status]", "error");
}

function detectNudge(prompt: string): string | null {
	const text = prompt.toLowerCase();
	if (/\b(again|repeat|same workflow|every time|often|reuse|reusable)\b/.test(text)) {
		return "Repeated workflow detected: consider `/skill-draft <name>` after this turn if the steps become reusable.";
	}
	if (/\b(big refactor|migration|multi[- ]?step|roadmap|large project|many files)\b/.test(text)) {
		return "Large task detected: consider `/skill:blueprint` or `pi_messenger({ action: \"plan\" })` before implementation.";
	}
	if (/\b(done|finished|implemented|ready to ship|before shipping)\b/.test(text) && /\b(review|check|verify|safe|bugs?)\b/.test(text)) {
		return "Shipping checkpoint detected: consider `/review-start` for an automated review loop.";
	}
	return null;
}

export default function piSelfImprovement(pi: ExtensionAPI) {
	pi.registerCommand("skill-draft", {
		description: "Draft a new local SKILL.md from a reusable workflow idea",
		handler: async (args, ctx) => handleSkillDraft(args, ctx),
	});

	pi.registerCommand("skill-curator", {
		description: "Scan local skills and write .pi/SKILL_CURATOR_REPORT.md",
		handler: async (_args, ctx) => handleCurator(ctx),
	});

	pi.registerCommand("skin", {
		description: "Set/list/clear a behavior skin: /skin list, /skin builder, /skin off",
		handler: async (args, ctx) => handleSkin(args, ctx),
	});

	pi.registerCommand("nudge", {
		description: "Toggle lightweight workflow nudges: /nudge on|off|status",
		handler: async (args, ctx) => handleNudge(args, ctx),
	});

	pi.on("before_agent_start", async (event) => {
		const cwd = event.systemPromptOptions?.cwd || process.cwd();
		const additions: string[] = [];

		const skin = readActiveSkin(cwd);
		if (skin) {
			additions.push(`\n# Active Personality Skin: ${skin.name}\n${skin.instructions}\n`);
		}

		if (event.prompt && !/^\s*\//.test(event.prompt) && isNudgeEnabled(cwd)) {
			const nudge = detectNudge(event.prompt);
			if (nudge) {
				return {
					systemPrompt: additions.length ? `${event.systemPrompt}\n${additions.join("\n")}` : event.systemPrompt,
					message: {
						customType: "auto-nudge",
						content: `💡 Auto-nudge: ${nudge}`,
						display: false,
					},
				};
			}
		}

		if (additions.length) return { systemPrompt: `${event.systemPrompt}\n${additions.join("\n")}` };
		return undefined;
	});
}

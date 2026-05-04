import type { BuildSystemPromptOptions, ExtensionAPI, Skill } from "@mariozechner/pi-coding-agent";

type Intent = {
	title: string;
	suggestion: string;
};

const DEFAULT_HINT =
	"Use plain-language routing: pick the most relevant skill/command from what is currently available and run it directly.";

const STOP_WORDS = new Set([
	"le",
	"la",
	"les",
	"de",
	"du",
	"des",
	"un",
	"une",
	"une",
	"et",
	"ou",
	"en",
	"à",
	"au",
	"avec",
	"pour",
	"qui",
	"que",
	"quoi",
	"comment",
	"faire",
	"faire",
	"sur",
	"dans",
	"je",
	"tu",
	"il",
	"elle",
	"nous",
	"vous",
	"ils",
	"elles",
	"mon",
	"ma",
	"mes",
	"tes",
	"ses",
	"notre",
	"votre",
	"ton",
	"ta",
	"si",
	"est",
	"sont",
	"sera",
	"a",
	"the",
	"a",
	"an",
	"and",
	"or",
	"to",
	"for",
	"how",
	"what",
	"when",
	"where",
	"why",
]);

function normalize(text: string): string {
	return (text || "").toLowerCase();
}

function tokenize(text: string): string[] {
	return normalize(text)
		.split(/[^a-z0-9-]+/gi)
		.filter((w) => w.length >= 3 && !STOP_WORDS.has(w));
}

function detectNeysan(prompt: string, cwd: string): boolean {
	const combined = `${cwd} ${prompt}`.toLowerCase();
	return combined.includes("neysan") || combined.includes("neyssan");
}

function detectExplicitIntent(prompt: string, cwd: string): Intent | null {
	const text = normalize(prompt);

	const explicit = [
		{
			terms: ["pdf", "paper", "lecture", "equation", "document"],
			suggestion: "Use `pdf-reader` for read/extract/search flow.",
		},
		{
			terms: ["diagram", "architecture", "visual", "flow", "mermaid", "table", "slide", "slide deck"],
			suggestion:
				"Use visual-explainer templates for structured output (`/generate-web-diagram` or `/generate-visual-plan`).",
		},
		{
			terms: ["diff", "review", "change", "pr", "pull request", "commit", "patch"],
			suggestion: "Use visual-explainer `/diff-review` for structured architectural diff review.",
		},
		{
			terms: ["plan", "spec", "roadmap", "proposal", "design", "migration"],
			suggestion: "Use visual-explainer `/plan-review` for plan-vs-codebase analysis.",
		},
		{
			terms: ["search web", "web research", "find on web", "online", "reference", "youtube", "video"],
			suggestion: "Use web-access (`/websearch`, `web_search`, `fetch_content`) for web lookup and content extraction.",
		},
		{
			terms: ["delegate", "ask opinion", "second opinion", "parallel review", "who should", "multi-step"],
			suggestion: "Use subagent flow (scout → planner → worker → reviewer) for multi-step work.",
		},
		{
			terms: ["scout", "researcher", "worker", "reviewer", "planner", "oracle", "implement and review", "background"],
			suggestion: "Use full subagent orchestration (scout/researcher/planner/worker/reviewer) when available.",
		},
	];

	const hit = explicit.find((entry) => entry.terms.some((term) => text.includes(term)));
	if (hit) {
		const neysanBoost =
			detectNeysan(text, cwd) &&
			(text.includes("impl") || text.includes("refactor") || text.includes("bug") || text.includes("review"));

		if (neysanBoost && !hit.suggestion.includes("subagent")) {
			return {
				title: "Neyssan or complex flow",
				suggestion:
					"Neyssan/app-grade workflow: run scout/context first, then planner, then worker, then reviewer before final summary.",
			};
		}

		return {
			title: "Auto-route",
			suggestion: hit.suggestion,
		};
	}

	return null;
}

function getLoadedSkills(systemPromptOptions?: BuildSystemPromptOptions): Skill[] {
	return systemPromptOptions?.skills?.filter((skill) => !!skill.name) ?? [];
}

function scoreByTokens(textTokens: string[], skillTextTokens: string[]): number {
	let score = 0;

	for (const token of textTokens) {
		if (skillTextTokens.includes(token)) score += 2;
		else {
			// Light partial match for compound names like `pdf-reader`
			for (const skillToken of skillTextTokens) {
				if (skillToken.startsWith(token) || token.startsWith(skillToken)) {
					score += 1;
					break;
				}
			}
		}
	}

	return score;
}

function pickBestSkill(prompt: string, skills: Skill[]): Skill | null {
	const promptTokens = tokenize(prompt);
	let best: { skill: Skill; score: number } | null = null;

	for (const skill of skills) {
		const skillTokens = tokenize(`${skill.name} ${skill.description || ""}`);
		const score = scoreByTokens(promptTokens, skillTokens);
		if (!best || score > best.score) {
			best = { skill, score };
		}
	}

	if (!best || best.score < 2) return null;
	return best.skill;
}

export default function (pi: ExtensionAPI) {
	pi.on("before_agent_start", async (event, _ctx) => {
		if (!event?.prompt) return;

		const prompt = event.prompt.trim();
		if (!prompt) return;

		// Don't interfere when user already typed a slash command.
		if (/^\s*\//.test(prompt)) return;

		const cwd = event.systemPromptOptions?.cwd || process.cwd();
		const explicit = detectExplicitIntent(prompt, cwd);
		if (explicit) {
			const message = [
				`🧭 Auto workflow hint: ${explicit.title}`,
				explicit.suggestion,
				"If context is ambiguous, run the minimal path first and escalate only when needed.",
			].join("\n");
			return {
				message: {
					customType: "workflow-router",
					content: message,
					display: false,
				},
			};
		}

		const loadedSkills = getLoadedSkills(event.systemPromptOptions);
		const skillMatch = pickBestSkill(prompt, loadedSkills);
		if (skillMatch) {
			const skillHint = `Use /skill:${skillMatch.name}`;
			const message = [
				`🧭 Auto workflow hint: Dynamic match`,
				skillHint,
				`(best match: ${skillMatch.name} — ${skillMatch.description || "no description"}).`,
				"If this is wrong, proceed with standard tool flow.",
			].join("\n");
			return {
				message: {
					customType: "workflow-router",
					content: message,
					display: false,
				},
			};
		}

		return {
			message: {
				customType: "workflow-router",
				content: `🧭 Auto workflow hint: ${DEFAULT_HINT}`,
				display: false,
			},
		};
	});
}

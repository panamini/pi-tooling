import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

type Intent = {
  title: string;
  suggestion: string;
};

const DEFAULT_HINT = "Use plain-language routing: pick the most relevant skill/command for the requested task.";

function detectNeysan(prompt: string, cwd: string): boolean {
  const combined = `${cwd} ${prompt}`.toLowerCase();
  return combined.includes("neysan") || combined.includes("neyssan");
}

function scoreIntent(prompt: string, options: { cwd: string }): Intent {
  const text = (prompt || "").toLowerCase();

  // Don't interfere with direct slash/manual commands
  if (/^\s*\//.test(text)) {
    return {
      title: "Manual",
      suggestion: "",
    };
  }

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
      terms: ["search web", "web research", "find on web", "online", "reference"],
      suggestion: "Use web-search/web-fetch for external lookup.",
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
      detectNeysan(text, options.cwd) &&
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

  return {
    title: "General",
    suggestion: DEFAULT_HINT,
  };
}

export default function (pi: ExtensionAPI) {
  pi.on("before_agent_start", async (event: any, ctx: any) => {
    if (!event?.prompt || !ctx) {
      return;
    }

    const prompt = event.prompt.trim();
    if (!prompt) {
      return;
    }

    const intent = scoreIntent(prompt, { cwd: event.systemPromptOptions?.cwd || process.cwd() });
    if (!intent.suggestion) {
      return;
    }

    const message = [
      `🧭 Auto workflow hint: ${intent.title}`,
      intent.suggestion,
      "If context is ambiguous, run the minimal path first and escalate only when needed.",
    ].join("\n");

    return {
      message: {
        customType: "workflow-router",
        content: message,
        display: false,
      },
    };
  });
}

import { appendFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import type { ExtensionAPI, ExtensionCommandContext } from "@mariozechner/pi-coding-agent";

const NOTES_FILE = "hub-notes.md";

function addHubNote(text: string, ctx: ExtensionCommandContext) {
  const note = text.trim();
  if (!note) {
    ctx.ui.notify("Usage: /hub-note <text>", "error");
    return;
  }

  const hubDir = join(ctx.cwd, ".pi");
  const notesPath = join(hubDir, NOTES_FILE);

  mkdirSync(hubDir, { recursive: true });
  appendFileSync(
    notesPath,
    `[${new Date().toISOString()}] ${note}\n`,
    "utf-8"
  );

  ctx.ui.notify(`Saved note to ${notesPath}`, "info");
}

export default function (pi: ExtensionAPI) {
  pi.registerCommand("hub-note", {
    description: "Append a dated note to .pi/hub-notes.md",
    handler: async (args, ctx) => {
      addHubNote(args, ctx);
    },
  });
}

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import type { ExtensionAPI, ExtensionContext, ExtensionCommandContext } from "@mariozechner/pi-coding-agent";

const STATE_FILE = join(homedir(), ".pi", "agent", "pi-tooling-reminder.json");
const REMINDER_INTERVAL_MS = 12 * 60 * 60 * 1000;
const SYNC_COMMAND = "cd /Users/pana/pi-tooling && ./scripts/sync-upstream.sh --commit --push";
const PI_UPDATE_COMMAND = "pi update git:github.com/panamini/pi-tooling";

interface ReminderState {
  lastRemindedAt?: number;
}

function readState(): ReminderState {
  try {
    if (!existsSync(STATE_FILE)) {
      return {};
    }

    const raw = readFileSync(STATE_FILE, "utf-8");
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? (parsed as ReminderState) : {};
  } catch {
    return {};
  }
}

function saveState(state: ReminderState): void {
  const dir = dirname(STATE_FILE);
  mkdirSync(dir, { recursive: true });
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), "utf-8");
}

function shouldShowReminder(force: boolean): boolean {
  if (force) return true;

  const state = readState();
  if (!state.lastRemindedAt) {
    return true;
  }

  const now = Date.now();
  return now - state.lastRemindedAt >= REMINDER_INTERVAL_MS;
}

function remind(ctx: ExtensionContext | ExtensionCommandContext, force = false): void {
  if (!ctx.hasUI || !shouldShowReminder(force)) {
    return;
  }

  const message = [
    "💡 Pi Tooling sync reminder:",
    "Run this when connected to pull upstream skill/extension updates:",
    `  1) ${SYNC_COMMAND}`,
    `  2) ${PI_UPDATE_COMMAND}   # (if you only changed in GitHub package)` ,
    "",
    "Tip: this check is repeated every 12h to avoid noise.",
  ].join("\n");

  ctx.ui.notify(message, "info");
  saveState({ lastRemindedAt: Date.now() });
}

export default function (pi: ExtensionAPI) {
  pi.registerCommand("sync-pi-tooling", {
    description: "Show quick commands to refresh pi-tooling skills/extensions",
    handler: async (_args, ctx) => {
      remind(ctx, true);
      ctx.ui.notify("If you want, run the command above manually in your terminal.", "info");
    },
  });

  const sendReminder = (ctx: ExtensionContext, force = false) => {
    remind(ctx, force);
  };

  pi.on("session_start", (_event, ctx) => {
    sendReminder(ctx);
  });

  pi.on("session_switch", (_event, ctx) => {
    sendReminder(ctx);
  });
}

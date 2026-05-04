import { spawnSync } from "node:child_process";
import { resolve } from "node:path";
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

function isGitWorktree(cwd: string): boolean {
  const result = spawnSync("git", ["rev-parse", "--is-inside-worktree"], {
    cwd,
    stdio: ["ignore", "ignore", "ignore"],
  });
  return result.status === 0;
}

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    if (!ctx.hasUI) return;

    const cwd = resolve(ctx.cwd ?? process.cwd());
    if (!isGitWorktree(cwd)) {
      ctx.ui.notify(
        "No git repo detected in current folder. '/powerbar' git-branch will be empty. Start pi from a git folder (e.g. /Users/pana/pi-tooling) and run /reload.",
        "warning",
      );
    }
  });
}

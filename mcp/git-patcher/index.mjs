import { Tool } from "@modelcontextprotocol/sdk";
import { exec } from "child_process";
import { promisify } from "util";

const run = promisify(exec);

export const gitPatcher = new Tool({
  name: "git-patcher",
  description: "Apply unified diffs to the local repo using git apply",
  methods: {
    apply_patch: {
      description: "Apply a unified diff patch to the repo",
      input: { type: "object", properties: { diff: { type: "string" } }, required: ["diff"] },
      output: { type: "object", properties: { ok: { type: "boolean" }, message: { type: "string" } } },
      async execute({ diff }) {
        try {
          const { stdout, stderr } = await run("git apply -", { input: diff });
          return { ok: true, message: stdout || stderr || "applied cleanly" };
        } catch (err) {
          return { ok: false, message: err.stderr || err.message };
        }
      }
    }
  }
});

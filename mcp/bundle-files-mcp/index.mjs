#!/usr/bin/env node
/**
 * MCP quick primer (concise):
 * - Transport: MCP servers speak JSON-RPC over stdio. Keep stdout for protocol
 *   only; write logs to stderr. Codex reads stdout and ignores stderr.
 * - Handshake: create a Server with capabilities, then connect via
 *   StdioServerTransport(). Register request handlers.
 * - Tools: clients discover tools via ListTools and invoke them via CallTool.
 *   Many clients hide tools without schemas, so we advertise BOTH
 *   `inputSchema` (camelCase) and `input_schema` (snake_case).
 * - This server exposes two tools that call a Python CLI (cli.py) to do the
 *   real work. We spawn it, enforce timeouts, cap output, and limit
 *   concurrency.
 * - Useful env overrides:
 *     BUNDLE_PY_CLI, BUNDLE_PYTHON, BUNDLE_TIMEOUT_MS,
 *     BUNDLE_MAX_BUFFER, BUNDLE_MAX_CONCURRENCY, BUNDLE_LOG.
 */

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

/* ──────────────── Config ──────────────── */
const here = dirname(fileURLToPath(import.meta.url));
const DEFAULT_PY_CLI = resolve(here, "../../src/shared_dev_tools/cli.py");
const PY_CLI = (process.env.BUNDLE_PY_CLI && existsSync(process.env.BUNDLE_PY_CLI))
  ? process.env.BUNDLE_PY_CLI
  : DEFAULT_PY_CLI;

const PYTHON = process.env.BUNDLE_PYTHON || "python3"; // fallback handled in runner
const TIMEOUT_MS = parseInt(process.env.BUNDLE_TIMEOUT_MS || "60000", 10);
const MAX_OUTPUT = parseInt(process.env.BUNDLE_MAX_BUFFER || `${64 * 1024 * 1024}`, 10); // 64MB
const LOG = process.env.BUNDLE_LOG === "1";

const MAX_CONCURRENCY = parseInt(process.env.BUNDLE_MAX_CONCURRENCY || "4", 10);
let inFlight = 0;
const waiters = [];

function log(...a){ if (LOG) console.error("[bundle-files]", ...a); }

/* ───────────── Response normalizer ───────────── */
function toTextContent(v) {
  // Always return a valid "text" content item; pretty-print JSON
  const s = typeof v === "string" ? v : JSON.stringify(v, null, 2);
  return { type: "text", text: s };
}

function toResourceContent(uri, mimeType) {
  return { type: "resource", resource: { uri, mimeType } };
}

function normalizeContent(items) {
  // Defense-in-depth: coerce any accidental {type:"json"} or raw objects to text
  const allowed = new Set(["text", "image", "audio", "resource"]);
  return (items || []).map((it) => {
    if (!it || typeof it !== "object") return toTextContent(String(it ?? ""));
    if (!("type" in it)) return toTextContent(it);
    if (!allowed.has(it.type)) {
      // e.g., {type:"json"} → stringify as text
      return toTextContent(it);
    }
    // Validate minimal required fields for resource
    if (it.type === "resource") {
      const r = it.resource || {};
      if (typeof r.uri !== "string" || typeof r.mimeType !== "string") {
        // Fall back to text if resource is malformed
        return toTextContent(it);
      }
    }
    // image/audio branches could be validated here too if you ever emit them
    return it;
  });
}

/* ───────────── Promise pool ───────────── */
async function withSlot(fn){
  if (inFlight >= MAX_CONCURRENCY) {
    await new Promise(r => waiters.push(r));
  }
  inFlight++;
  try { return await fn(); }
  finally {
    inFlight--;
    const r = waiters.shift();
    if (r) r();
  }
}

/* ───────────── Runner (spawn) ───────────── */
function parseJSON(s){ try { return JSON.parse(s); } catch { return null; } }

function runCli(args, { cwd, timeoutMs = TIMEOUT_MS, signal } = {}){
  return new Promise((resolve, reject) => {
    let stdout = "";
    let stderr = "";
    let truncatedOut = false, truncatedErr = false;

    function start(bin){
      log("spawn", bin, PY_CLI, args.join(" "), "cwd=", cwd || process.cwd());
      const child = spawn(bin, [PY_CLI, ...args], {
        cwd: cwd || process.cwd(),
        env: process.env,
        stdio: ["ignore", "pipe", "pipe"]
      });

      const timer = setTimeout(() => {
        try { child.kill("SIGTERM"); } catch {}
        setTimeout(() => { try { child.kill("SIGKILL"); } catch {} }, 2000);
      }, timeoutMs);

      if (signal && typeof signal.addEventListener === "function") {
        signal.addEventListener("abort", () => {
          try { child.kill("SIGTERM"); } catch {}
          setTimeout(() => { try { child.kill("SIGKILL"); } catch {} }, 2000);
          clearTimeout(timer);
          reject(new Error("bundle-files call canceled by client"));
        }, { once: true });
      }

      child.stdout.on("data", d => {
        stdout += d.toString();
        if (stdout.length > MAX_OUTPUT) {
          stdout = stdout.slice(0, MAX_OUTPUT);
          truncatedOut = true;
        }
      });
      child.stderr.on("data", d => {
        stderr += d.toString();
        if (stderr.length > MAX_OUTPUT) {
          stderr = stderr.slice(0, MAX_OUTPUT);
          truncatedErr = true;
        }
      });

      child.on("error", e => {
        if (/ENOENT/.test(String(e?.message)) && bin === "python3") {
          // retry with 'python'
          return start("python");
        }
        clearTimeout(timer);
        reject(new Error(`spawn failed: ${e?.message || String(e)}`));
      });

      child.on("close", (code, sig) => {
        clearTimeout(timer);
        if (sig === "SIGTERM" || sig === "SIGKILL") {
          const parsed = parseJSON(stdout);
          if (parsed) {
            return resolve({ ok: false, timeout: true, parsed, stdout, stderr, truncatedOut, truncatedErr });
          }
          return reject(new Error(`bundle-files timed out after ${timeoutMs}ms`));
        }
        if (code === 0) {
          return resolve({ ok: true, stdout, stderr, truncatedOut, truncatedErr });
        }
        const maybe = parseJSON(stdout);
        if (maybe) {
          return resolve({ ok: false, parsed: maybe, exit: code, stdout, stderr, truncatedOut, truncatedErr });
        }
        reject(new Error(`bundle-files failed (exit ${code})\n${stderr || stdout}`));
      });
    }

    start(PYTHON);
  });
}

/* ───────────── Tools ───────────── */
const tools = [
  {
    name: "bundle_list",
    description: "Preview which files would be included in a code-review bundle. Keywords: prepare for code review, review scope, list files, bundle preview, PR review preparation.",
    inputSchema: {
      type: "object",
      properties: {
        root: { type: "string", description: "Project root to scan" },
        include_ext: { type: "string", description: "Comma-separated includes for --include-ext" },
        extra_exclude_paths: { type: "string", description: "Comma-separated excludes" },
        include_ignored: { type: "boolean", default: false },
        no_respect_gitignore: { type: "boolean", default: false },
        changed_since: { type: "string", description: "Git revision for incremental bundling" },
        strict: { type: "boolean", default: false }
      },
      required: ["root"],
      additionalProperties: false
    },
    async run(args, req){
      const {
        root,
        include_ext,
        extra_exclude_paths,
        include_ignored = false,
        no_respect_gitignore = false,
        changed_since,
        strict = false
      } = args || {};

      const cli = ["--root", root, "--list", "--json"];
      if (strict) cli.push("--strict");
      if (include_ext) cli.push("--include-ext", include_ext);
      if (extra_exclude_paths) cli.push("--extra-exclude-paths", extra_exclude_paths);
      if (include_ignored) cli.push("--include-ignored");
      if (no_respect_gitignore) cli.push("--no-respect-gitignore");
      if (changed_since) cli.push("--changed-since", changed_since);

      const res = await runCli(cli, { cwd: root, signal: req?.signal });
      if (res.ok) {
        const parsed = parseJSON(res.stdout);
        if (!parsed) {
          return { content: normalizeContent([toTextContent("bundle-files returned invalid JSON")]) };
        }
        const filesAbs = (parsed.files || []).map(rel => resolve(root, rel));
        const payload = { root, files: filesAbs, raw: parsed };
        return { content: normalizeContent([toTextContent(payload)]) };
      }
      if (res.timeout) {
        return { content: normalizeContent([toTextContent(`bundle-files timed out after ${TIMEOUT_MS}ms`)]) };
      }
      if (res.parsed) {
        const payload = { ...res.parsed, strict_failed: true };
        return { content: normalizeContent([toTextContent(payload)]) };
      }
      return { content: normalizeContent([toTextContent("bundle-files ended unexpectedly.")]) };
    }
  },
  {
    name: "bundle_generate",
    description: "Generate chunked Markdown bundle(s) for code review and return JSON + file links. Use when someone says things like: \"prepare for code review\", \"create a code review bundle\", \"package files for PR review\", or \"bundle for reviewers\".",
    inputSchema: {
      type: "object",
      properties: {
        root: { type: "string" },
        output: { type: "string", description: "Output file path (parts derive from this)" },
        manifest: { type: "string", description: "Write manifest.json here (optional)" },
        archive: { type: "string", enum: ["zip","tar"], description: "Package parts + index + manifest" },
        archive_files: { type: "string", enum: ["zip","tar"], description: "Package ORIGINAL selected files preserving relative paths, plus BUNDLE_INSTRUCTIONS.md; includes index/manifest if present" },
        index: { type: "string", description: "Write JSON summary to this path; MCP returns a link" },
        output_dir: { type: "string", description: "Directory for outputs (overrides directory of output)" },
        output_base: { type: "string", description: "Base filename used with output_dir" },
        context_length: { type: "integer", default: 400000 },
        max_total_bytes: { type: "integer", default: 10000000 },
        encoding: { type: "string", default: "utf-8" },
        token_estimator: { type: "string", description: "'char' or 'tiktoken:<model>'" },
        include_ext: { type: "string" },
        extra_exclude_paths: { type: "string" },
        include_ignored: { type: "boolean", default: false },
        no_respect_gitignore: { type: "boolean", default: false },
        changed_since: { type: "string", description: "Git revision for incremental bundling" },
        strict: { type: "boolean", default: false },
        return_links: { type: "boolean", default: false, description: "Include resource link content entries to artifacts; set false for JSON-only" }
      },
      required: ["root", "output"],
      additionalProperties: false
    },
    async run(args, req){
      const {
        root, output, manifest, archive, archive_files, index, output_dir, output_base,
        context_length = 400000, max_total_bytes = 10_000_000, encoding = "utf-8",
        token_estimator, include_ext, extra_exclude_paths,
        include_ignored = false, no_respect_gitignore = false, changed_since,
        strict = false, return_links = false
      } = args || {};
 
      const cli = ["--root", root, "--output", output, "--context-length", String(context_length), "--max-total-bytes", String(max_total_bytes), "--encoding", encoding, "--json"];
      if (strict) cli.push("--strict");
      if (include_ext) cli.push("--include-ext", include_ext);
      if (extra_exclude_paths) cli.push("--extra-exclude-paths", extra_exclude_paths);
      if (include_ignored) cli.push("--include-ignored");
      if (no_respect_gitignore) cli.push("--no-respect-gitignore");
      if (changed_since) cli.push("--changed-since", changed_since);
      if (index) cli.push("--index", index);
      if (manifest) cli.push("--manifest", manifest);
      if (archive) cli.push("--archive", archive);
      if (archive_files) cli.push("--archive-files", archive_files);
      if (output_dir) cli.push("--output-dir", output_dir);
      if (output_base) cli.push("--output-base", output_base);
      if (token_estimator) cli.push("--token-estimator", token_estimator);

      const res = await runCli(cli, { cwd: root, timeoutMs: TIMEOUT_MS, signal: req?.signal });
      const parsed = res.parsed || parseJSON(res.stdout);

      // Build file:// links if we have parsed JSON
      const links = [];
      const toAbs = (p) => (!p ? null : (p.startsWith("/") ? p : resolve(root, p)));

      if (parsed?.parts?.length) {
        for (const p of parsed.parts) {
          if (p?.path) {
            const abs = toAbs(String(p.path));
            if (abs) {
              links.push(toResourceContent("file://" + abs, "text/markdown"));
            }
          }
        }
      }
      if (index) {
        const abs = toAbs(String(index));
        if (abs) {
          links.unshift(toResourceContent("file://" + abs, "application/json"));
        }
      }
      const mp = parsed?.manifest_path || manifest;
      if (mp) {
        const abs = toAbs(String(mp));
        if (abs) {
          links.unshift(toResourceContent("file://" + abs, "application/json"));
        }
      }
      if (parsed?.archive_path) {
        const abs = toAbs(String(parsed.archive_path));
        if (abs) {
          links.unshift(toResourceContent("file://" + abs, "application/octet-stream"));
        }
      }
      if (parsed?.files_archive_path) {
        const abs = toAbs(String(parsed.files_archive_path));
        if (abs) {
          links.unshift(toResourceContent("file://" + abs, "application/octet-stream"));
        }
      }

      // Always include an artifacts listing inside the JSON payload for compatibility
      const artifacts = [];
      if (parsed?.parts?.length) {
        for (const p of parsed.parts) {
          if (p?.path) {
            const abs = toAbs(String(p.path));
            if (abs) artifacts.push({ path: abs, mimeType: "text/markdown", kind: "part" });
          }
        }
      }
      if (index) {
        const abs = toAbs(String(index));
        if (abs) artifacts.unshift({ path: abs, mimeType: "application/json", kind: "index" });
      }
      if (mp) {
        const abs = toAbs(String(mp));
        if (abs) artifacts.unshift({ path: abs, mimeType: "application/json", kind: "manifest" });
      }
      if (parsed?.archive_path) {
        const abs = toAbs(String(parsed.archive_path));
        if (abs) artifacts.unshift({ path: abs, mimeType: "application/octet-stream", kind: "archive" });
      }
      if (parsed?.files_archive_path) {
        const abs = toAbs(String(parsed.files_archive_path));
        if (abs) artifacts.unshift({ path: abs, mimeType: "application/octet-stream", kind: "files_archive" });
      }

      const withArtifacts = (obj) => ({ ...obj, artifacts });

      if (res.ok) {
        if (!parsed) {
          return { content: normalizeContent([toTextContent("bundle-files returned invalid JSON")]) };
        }
        if (return_links) {
          return { content: normalizeContent([toTextContent(withArtifacts(parsed)), ...links]) };
        }
        return { content: normalizeContent([toTextContent(withArtifacts(parsed))]) };
      }
      if (res.timeout) {
        if (parsed) {
          if (return_links) {
            return { content: normalizeContent([toTextContent(withArtifacts({ ...parsed, timed_out: true })), ...links]) };
          }
          return { content: normalizeContent([toTextContent(withArtifacts({ ...parsed, timed_out: true }))]) };
        }
        return { content: normalizeContent([toTextContent(`bundle-files timed out after ${TIMEOUT_MS}ms`)]) };
      }
      if (parsed) {
        if (return_links) {
          return { content: normalizeContent([toTextContent(withArtifacts({ ...parsed, strict_failed: true })), ...links]) };
        }
        return { content: normalizeContent([toTextContent(withArtifacts({ ...parsed, strict_failed: true }))]) };
      }
      return { content: normalizeContent([toTextContent("bundle-files ended unexpectedly.")]) };
    }
  }
];

// Advertise dotted-name aliases for compatibility with clients expecting "bundle.*"
const baseList = tools.find(t => t.name === "bundle_list");
const baseGen = tools.find(t => t.name === "bundle_generate");
if (baseList) tools.push({ ...baseList, name: "bundle.list" });
if (baseGen) tools.push({ ...baseGen, name: "bundle.generate" });
// Intent-friendly aliases to improve NL routing from phrases like "prepare for code review"
if (baseGen) tools.push({ ...baseGen, name: "prepare_code_review" });
if (baseGen) tools.push({ ...baseGen, name: "code_review.prepare" });

/* ───────────── MCP server setup ───────────── */
const server = new Server(
  { name: "bundle-files-mcp", version: "0.3.0" },
  { capabilities: { tools: {} } }
);

// Advertise with both camelCase and snake_case keys for max compatibility
server.setRequestHandler(ListToolsRequestSchema, async () => {
  const advertised = tools.map(t => ({
    name: t.name,
    description: t.description,
    inputSchema: t.inputSchema,
    input_schema: t.inputSchema
  }));
  try { console.error(JSON.stringify({ ev: "advertise_tools", tools: advertised.map(x => x.name) })); } catch {}
  return { tools: advertised };
});

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const t = tools.find(x => x.name === req.params.name);
  if (!t) {
    return { isError: true, content: normalizeContent([toTextContent(`Unknown tool '${req.params.name}'. Available: ${tools.map(x => x.name).join(", ")}`)]) };
  }
  return withSlot(() => t.run(req.params.arguments || {}, req));
});

/* ───────────── Transport start ───────────── */
const transport = new StdioServerTransport();
await server.connect(transport);
try { console.error(JSON.stringify({ ev: "server_ready", tools: tools.map(t => t.name) })); } catch {}

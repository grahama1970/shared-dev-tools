# MCP Usage — bundle-files MCP Server

This server wraps the Python `bundle-files` CLI and exposes two tools over MCP.

Tools
- bundle.list
  - Input: `{ root, include_ext?, extra_exclude_paths?, include_ignored?, no_respect_gitignore?, changed_since?, strict? }`
  - Output: JSON `{ root, files[] }` plus raw selection metadata.
- bundle.generate
  - Input: `{ root, output, index?, manifest?, archive? ('zip'|'tar'), archive_files? ('zip'|'tar'), output_dir?, output_base?, context_length?, max_total_bytes?, encoding?, token_estimator?, include_ext?, extra_exclude_paths?, include_ignored?, no_respect_gitignore?, changed_since?, strict? }`
  - Output: JSON index with `schema_version`, `tool_name`, `tool_version`, `parts[]`, and optional `manifest_path`, `archive_path`, `files_archive_path`.
  - Also returns `resource_link` entries for parts and any `index`/`manifest`/`archive`/`files_archive` artifacts.

Strict behavior
- When `strict: true`, the CLI exits non‑zero if any part exceeded the limits or unreadables were skipped, but it still emits the JSON index.
- The wrapper surfaces this as JSON and adds `strict_failed: true` and `exit_code`.

Aliases and intent routing
- Tools are advertised under multiple names to improve agent intent matching:
  - bundle_list and bundle.list
  - bundle_generate and bundle.generate
  - prepare_code_review (alias of bundle.generate)
  - code_review.prepare (alias of bundle.generate)
- Natural language mapping guidance:
  - Phrases like "prepare for code review", "create a code review bundle", "package files for PR review", or "bundle for reviewers" → prefer prepare_code_review or bundle.generate.
  - Phrases like "list files to include", "what would be bundled", "preview selection" → prefer bundle.list.

Client compatibility: return_links
- Some MCP clients (including certain VS Code integrations) strictly validate tool content items and may reject "resource" entries.
- Default behavior in this project: keep return_links=false so the tool returns a single JSON payload that includes an "artifacts" array with absolute file paths and MIME types for generated outputs.
- When your client supports resource content correctly, you can set return_links=true to also receive resource link items (file:// URIs) alongside the JSON payload.

Additional examples
```jsonc
// Generate bundles with JSON-only payload (recommended default for broad client compatibility)
{
  "tool": "bundle.generate",
  "arguments": {
    "root": "/abs/project",
    "output": "bundle.md",
    "context_length": 400000,
    "strict": true,
    "index": "/abs/project/artifacts/bundle.index.json",
    "manifest": "/abs/project/artifacts/manifest.json",
    "return_links": false
  }
}

// Generate bundles and include resource link entries (only if your client supports resource content items)
{
  "tool": "prepare_code_review", // alias of bundle.generate
  "arguments": {
    "root": "/abs/project",
    "output": "bundle.md",
    "return_links": true
  }
}
```
Examples
```jsonc
// List files without writing outputs
{"tool":"bundle.list","arguments":{"root":"/abs/project"}}

// Generate bundles with a 400k budget + index + manifest + zip of parts
{
  "tool": "bundle.generate",
  "arguments": {
    "root": "/abs/project",
    "output": "bundle.md",
    "context_length": 400000,
    "strict": true,
    "index": "/abs/project/artifacts/bundle.index.json",
    "manifest": "/abs/project/artifacts/manifest.json",
    "archive": "zip"
  }
}

// Generate ORIGINAL files archive (preserving directory structure) + instructions
{
  "tool": "bundle.generate",
  "arguments": {
    "root": "/abs/project",
    "output": "bundle.md",
    "archive_files": "zip", // or "tar"
    "index": "/abs/project/artifacts/bundle.index.json",
    "manifest": "/abs/project/artifacts/manifest.json"
  }
}
```

Behavior notes
- `archive`: packages the generated Markdown bundle parts (basenames only) plus optional `index` and `manifest`. Entries in the archive have no path separators.
- `archive_files`: packages the ORIGINAL selected files preserving their repo‑relative paths, plus an instruction document `BUNDLE_INSTRUCTIONS.md`. Also includes `index` and `manifest` sidecars when provided.

Notes
- Paths in JSON are POSIX‑relative to `root` where applicable; `resource_link` URIs use `file://` absolute paths.
- The wrapper never parses human‑friendly text; it only processes `--json` outputs from the CLI.
- Token estimator options:
  - `char` (default, ~4 chars/token)
  - `tiktoken:<model>` (optional install; silently falls back to `char` if unavailable)

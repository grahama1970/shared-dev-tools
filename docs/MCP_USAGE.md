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

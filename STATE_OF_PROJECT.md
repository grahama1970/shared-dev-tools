Prompt: Generate/Update This Report Reliably

You are an operator agent asked to produce a fresh “State of Shared Dev Tools (Bundler + MCP)” report. Follow these exact steps and write your answer to STATE_OF_PROJECT.md:

1) Validate repo + env
   - Confirm working dir contains this project (shared-dev-tools). Run:
     - uv pip install -e .[dev]
     - ruff check . && black --check . && mypy src && pytest -q
   - If any tooling is missing, install with: uv pip install ruff black mypy pytest

2) Verify CLI basics
   - Dry list in JSON:
     - python src/shared_dev_tools/cli.py --root . --output artifacts/bundle.md --list --json
   - Generate a small bundle with headroom and JSON index:
     - python src/shared_dev_tools/cli.py \
       --root . --output artifacts/bundle.md \
       --context-length 360000 --json --index artifacts/bundle.index.json

3) Verify new features (quick checks)
   - Strict mode error (non-zero exit but prints JSON):
     - python src/shared_dev_tools/cli.py --root . --output artifacts/strict.md --strict --json || echo ok
   - Incremental selection (Git only):
     - python src/shared_dev_tools/cli.py --root . --output artifacts/inc.md --changed-since HEAD~1 --json
   - Token estimator switch:
     - python src/shared_dev_tools/cli.py --root . --output artifacts/tok.md --token-estimator char --json
     - python src/shared_dev_tools/cli.py --root . --output artifacts/tok.md --token-estimator tiktoken:gpt-4o --json
   - Preamble injection:
     - echo "# Operator Notes" > PREAMBLE.md
     - python src/shared_dev_tools/cli.py --root . --output artifacts/pre.md --prefix-file PREAMBLE.md --json
   - Token cache (optional):
     - python src/shared_dev_tools/cli.py --root . --output artifacts/cache.md --cache-dir .cache --json

4) Verify MCP wrapper
   - Ensure ~/.codex/config.toml includes [mcp_servers.bundle-files] pointing to mcp/bundle-files-mcp/index.mjs.
   - From an MCP client, call:
     - tool bundle.list → { root: "<abs/project>" }
     - tool bundle.generate → { root, output: "bundle.md", context_length: 400000, strict: true }
   - Expect JSON and resource_link entries (file://… for parts and optional index).

5) Optional competitor scan (use research tools; cite URLs)
   - Perplexity: “open-source CLI bundlers/packagers for LLM codebases 2024–2025; MCP file servers; what features matter?”
   - Brave: search “code repository bundler LLM”, “MCP server bundler”.
   - Context7: modelcontextprotocol/typescript-sdk server docs for tool schemas/links.

6) Write the report with sections:
   - Executive Summary, Capabilities, Validation Status, Competitor Landscape,
     Gaps vs. Market, Recommendations/Roadmap (Now/Next/Later), Metrics & SLIs,
     Risks & Mitigations, References.

7) Keep it operator‑friendly
   - Terse bullets, copy‑paste commands (wrapped ~400px), minimal fluff.

---

# State of Shared Dev Tools (Bundler + MCP) — September 19, 2025

Executive Summary
- The bundle-files CLI supports context-aware chunking (~token budget), JSON output, strict mode, incremental selection (Git), token estimator switching (char or tiktoken:<model>), preamble injection, and an optional token cache. Artifacts can be routed via --output-dir/--output-base and indexed with --index.
- A Node-based MCP wrapper exposes two tools (bundle.list, bundle.generate), returns structured JSON and resource_link entries, and provides usage/profile resources. Strict failures propagate as JSON (strict_failed with exit_code) so automations never lose diagnostics.
- Local quality gates and smokes are passing (ruff, black, mypy, pytest). The design keeps dependencies minimal by default and adds model tokenizers only if requested.

Capabilities
- Selection & filtering
  - Respects .gitignore (authoritative via Git) with best-effort fallback walk; default dir excludes and binary detection.
  - --include-ext, --extra-exclude-paths; --include-ignored and --no-respect-gitignore.
  - Incremental mode: --changed-since <rev>.
- Bundling & formatting
  - Markdown fences with BEGIN/END markers; language fences by extension.
  - Context-length chunking (default 400k); per-part header with Git rev, file count, and budget.
  - --output-dir / --output-base for controlled artifact paths; .partN naming.
  - --prefix-file to inject operator preamble into each part.
- Token accounting
  - Estimators: char (~4 chars/token) or tiktoken:<model> (fallback safe).
  - Optional cache (--cache-dir) stores tokens keyed by path+size+mtime+estimator.
- Output modes & robustness
  - --json prints single JSON object; --index writes same JSON to file.
  - --strict exits non-zero if any part exceeds limits or if unreadables were skipped (still prints JSON).
- MCP wrapper (TypeScript, @modelcontextprotocol/sdk)
  - Tools: bundle.list (dry run) and bundle.generate (chunk & write). Returns JSON + resource_link entries (file:// parts, optional index).
  - Resources: bundle-files://usage (guide), bundle-files://profile (capability snapshot).
  - Flags forwarded: context_length, max_total_bytes, encoding, include/exclude, include_ignored/no_respect_gitignore, changed_since, token_estimator, strict, output_dir/base, index.

Validation Status (local) — 2025-09-19T14:57:21Z
- Tooling gates
  - ruff: PASS
  - black --check: PASS
  - mypy src: PASS
  - pytest -q: PASS (4 tests)
- CLI quick checks
  - list --json: PASS (git=true, candidates=25, selected=25)
  - generate --json --index: PASS (1 part, ~130 KB, ~32.6k tokens, no overflows)
  - strict --json: PASS (0 overflows, exit=0 in this repo size)
  - changed-since HEAD~1: PASS (selected file_count=3)
  - prefix-file: PASS (preamble injected)
  - cache-dir: PASS (cache JSON created)
- Artifacts (for reference)
  - artifacts/bundle.md, artifacts/bundle.index.json
  - artifacts/strict.md, artifacts/inc.md, artifacts/pre.md, artifacts/cache.md

Competitor Landscape (notes)
- Compare against generic repo bundlers and MCP file servers. Important axes:
  - Token accounting accuracy/speed; incremental selection; machine-readable index/manifest; editor/agent integrations; observability.

Gaps vs. Market
- Exact-model tokenization across providers without optional installs (consider lazy plugin registry).
- Artifact manifest (JSON) with checksums, budgets, and reproducible inputs (source list + versions).
- Parallel bundling for very large repos (threaded IO + bounded memory).
- Zip/tar packaging option with manifest and index resource_link.
- Remote artifact store (S3/local cache) and signed provenance for CI handoffs.

Recommendations / Roadmap
- Now
  - Add manifest.json (inputs, versions, budgets, part list + checksums) and return as resource_link (alongside --index).
  - Add --zip/--tar packaging (parts + index + manifest).
  - Add simple progress/summary logging (files/min, tokens/part) with --verbose.
- Next
  - Parallel file read + tokenization pipeline (bounded workers); track rate metrics.
  - Estimator plugin registry: openai-tiktoken, anthropic-claude tokens, tokenizer.json fallback.
  - Git helpers: --changed-files-from <rev..rev>, --only-staged; MCP tool args to match.
- Later
  - Remote artifact publishing (S3/file server) with signed manifest; MCP list/pull resource.
  - Optional “source map” (file offsets) to support partial updates and rich navigation.

Metrics & SLIs (proposed)
- Bundle latency p50/p90; files/sec, bytes/sec.
- Tokens per part p50/p90; parts/run; overflow rate (strict hits).
- Incremental speedup vs. full; cache hit rate; estimator CPU time.
- MCP tool success rate; tool latency p50/p90; strict_failed frequency.

Risks & Mitigations
- Token estimator mismatch → default to char; document headroom; optional tiktoken flag.
- Very large repos → parallel IO; memory guards; enforce max_total_bytes/context_length.
- Path/line-ending quirks → normalize to 
; POSIX rel paths in JSON; tests enforce.
- Security (resource_links) → only file:// paths under root; respect .gitignore; redact logs.

References
- Code: src/shared_dev_tools/cli.py; mcp/bundle-files-mcp/index.mjs
- Docs: docs/token_limits.md
- Smokes: tests/smokes/
- Config: ~/.codex/config.toml (mcp_servers.bundle-files)

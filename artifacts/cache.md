# Project Bundle

- Generated: 2025-09-19T14:55:40Z
- Root: /home/graham/workspace/experiments/shared-dev-tools
- Git: 8fe4d9c+dirty
- Files: 25
- Bundle Part: 1
- Context Tokens Limit: 400000

---


====== BEGIN FILE: .github/CODEOWNERS ======
```
# Default reviewers who own all files in the repository.
* @grahamaco

```

====== END FILE ======


====== BEGIN FILE: .github/workflows/ci.yml ======
```yaml
name: CI

on:
  push:
    branches:
      - main
      - master
  pull_request:

jobs:
  tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.12"]

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up uv
        uses: astral-sh/setup-uv@v3

      - name: Install Python
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv pip install --system '.[dev]'

      - name: Ruff
        run: ruff check .

      - name: Black
        run: black --check .

      - name: MyPy
        run: mypy src

      - name: Pytest
        run: pytest -q

```

====== END FILE ======


====== BEGIN FILE: .gitignore ======
```
# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments and local configs
.venv
.env
*.env
.envrc

# Tool caches
.mypy_cache/
.pytest_cache/
.ruff_cache/
.coverage
.coverage.*
htmlcov/

# Editor/tooling data
.python-version
.idea/
.vscode/
.serena/

# Build artifacts
scripts/artifacts/

# uv lockfiles (optional)
uv.lock
```

====== END FILE ======


====== BEGIN FILE: .python-version ======
```
3.12
```

====== END FILE ======


====== BEGIN FILE: AGENTS.md ======
```markdown
# Automation Notes

This repository occasionally uses autonomous agents (e.g., Codex CLI, GitHub bots) to help with maintenance. The following guardrails keep those tools predictable and safe.

## Baseline Checklist for Agents

1. Activate the project environment as needed for the task at hand.
2. Use `uv` commands when installing dependencies (`uv pip install -e .[dev]`).
3. Run the full verification suite before reporting success:
   ```bash
   ruff check .
   black --check .
   mypy src
   pytest -q
   ```
4. Prefer `rg` for code search, `apply_patch` for edits, and keep diffs minimal.
5. Do not commit secrets; prefer local environment management tools instead of committing configuration files.

## Smoke Tests

- Implement new smokes in `tests/smokes/` alongside new CLI functionality.
- Keep run times under one second and avoid network calls.

## Pull Request Expectations

- Surface artifacts (bundle outputs, logs) when diagnosing failures.
- Reference related issues and summarize manual validation steps.

These notes are intentionally lightweight; see `CONTRIBUTING.md` for human contributor guidelines.
```

====== END FILE ======


====== BEGIN FILE: CODE_OF_CONDUCT.md ======
```markdown
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, caste, color, religion, or sexual identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming, diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our community include:

- Demonstrating empathy and kindness toward other people
- Being respectful of differing opinions, viewpoints, and experiences
- Giving and gracefully accepting constructive feedback
- Accepting responsibility and apologizing to those affected by our mistakes, and learning from the experience
- Focusing on what is best not just for us as individuals, but for the overall community

Examples of unacceptable behavior include:

- The use of sexualized language or imagery, and sexual attention or advances of any kind
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as a physical or email address, without their explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of acceptable behavior and will take appropriate and fair corrective action in response to any behavior that they deem inappropriate, threatening, offensive, or harmful.

Community leaders have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned with this Code of Conduct, and will communicate reasons for moderation decisions when appropriate.

## Scope

This Code of Conduct applies within all community spaces, and also applies when an individual is officially representing the community in public spaces. Examples of representing our community include using an official e-mail address, posting via an official social media account, or acting as an appointed representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the community leaders responsible for enforcement via GitHub issues or the contact information listed in the repository README. All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the reporter of any incident.

## Enforcement Guidelines

Community leaders will follow these Community Impact Guidelines in determining the consequences for any action they deem in violation of this Code of Conduct:

### 1. Correction

**Community Impact**: Use of inappropriate language or other behavior deemed unprofessional or unwelcome in the community.

**Consequence**: A private, written warning from community leaders, providing clarity around the nature of the violation and an explanation of why the behavior was inappropriate. A public apology may be requested.

### 2. Warning

**Community Impact**: A violation through a single incident or series of actions.

**Consequence**: A warning with consequences for continued behavior. No interaction with the people involved, including unsolicited interaction with those enforcing the Code of Conduct, for a specified period of time. This includes avoiding interactions in community spaces as well as external channels like social media. Violating these terms may lead to a temporary or permanent ban.

### 3. Temporary Ban

**Community Impact**: A serious violation of community standards, including sustained inappropriate behavior.

**Consequence**: A temporary ban from any sort of interaction or public communication with the community for a specified period of time. No public or private interaction with the people involved, including unsolicited interaction with those enforcing the Code of Conduct, is allowed during this period. Violating these terms may lead to a permanent ban.

### 4. Permanent Ban

**Community Impact**: Demonstrating a pattern of violation of community standards, including sustained inappropriate behavior, harassment of an individual, or aggression toward or disparagement of classes of individuals.

**Consequence**: A permanent ban from any sort of public interaction within the community.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 2.1, available at [https://www.contributor-covenant.org/version/2/1/code_of_conduct.html](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html).

Community Impact Guidelines were inspired by [Mozilla's code of conduct enforcement ladder](https://github.com/mozilla/diversity).

For answers to common questions about this code of conduct, see the [FAQ](https://www.contributor-covenant.org/faq). Translations are available at the [Contributor Covenant](https://www.contributor-covenant.org/translations).

[homepage]: https://www.contributor-covenant.org

```

====== END FILE ======


====== BEGIN FILE: CONTRIBUTING.md ======
```markdown
# Contributing to shared-dev-tools

Thanks for considering a contribution! This document outlines the process for proposing changes and keeping the toolkit healthy.

## Getting Started

1. **Fork and clone** the repository, then create a feature branch.
2. **Install dependencies**: `uv pip install -e .[dev]` (or `pip install -e .[dev]`).
3. **Configure environment variables** however you prefer for local testing (optional).

## Development Workflow

- Keep changes focused. If you are adding a new CLI, include at least one smoke test in `tests/smokes/` that exercises its primary flow.
- Follow the repository’s formatting and linting rules. We use Black, Ruff, and mypy, all configured with sensible defaults.
- Update documentation (README, usage guides) when behavior changes.

## Quality Gates

Run the full suite before opening a pull request:

```bash
ruff check .
black --check .
mypy src
pytest -q
```

GitHub Actions runs these same checks for every PR.

## Commit & PR Guidelines

- Use Conventional Commit prefixes (`feat:`, `fix:`, `docs:`, etc.) when possible.
- Provide context in the PR description, including screenshots or artifact paths if your change affects bundle output.
- Reference related issues with `Fixes #123` or `Refs #123`.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating you agree to abide by its terms.

## Questions or Feedback

Open a GitHub issue for bugs or feature requests. For security disclosures, please email the maintainers listed in `CODEOWNERS` once the project is public (planned for future iteration).

Happy hacking!
```

====== END FILE ======


====== BEGIN FILE: LICENSE ======
```
MIT License

Copyright (c) 2025 shared-dev-tools contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

====== END FILE ======


====== BEGIN FILE: PREAMBLE.md ======
```markdown
# Operator Notes
This is a preamble test.
```

====== END FILE ======


====== BEGIN FILE: README.md ======
```markdown
# shared-dev-tools

Utilities and command-line helpers for preparing repository artifacts for large-language-model workflows. The flagship command, `bundle-files`, scans a project, filters files using Git metadata and heuristics, and emits a single Markdown document with language-aware code fences that can be shared with review tools or LLMs.

---

## Features

- Respect `.gitignore` automatically when the target directory is a Git repository, with graceful fallbacks otherwise.
- Skip binary assets by extension/content and enforce per-file and total bundle size limits.
- Include or exclude files via glob patterns and explicit extension lists.
- Emit Markdown-formatted output with clear file delimiters and language hints.
- Print selection summaries (list mode) for quick inspection before writing bundles.

---

## Installation

The project targets Python 3.10+. Dependencies are managed with [uv](https://github.com/astral-sh/uv), but standard `pip` works as well.

```bash
# Clone the repository first
git clone https://github.com/grahama1970/shared-dev-tools.git
cd shared-dev-tools

# Install in editable mode with runtime + dev extras
uv pip install --editable .[dev]
# or, using pip
pip install -e .[dev]

# Once published, install globally via uv tools
uv tool install shared-dev-tools
```

---

## Usage

Run `bundle-files --help` to list all available options. Common patterns:

```bash
# Bundle the current repository respecting .gitignore
bundle-files --root . --output scripts/artifacts/bundle.md

# Inspect which files would be included without writing output
bundle-files --root . --output bundle.md --list

# Include additional file types and exclude generated folders
bundle-files \
  --root path/to/project \
  --output bundle.md \
  --include-ext ".proto,Justfile,vite.config.ts" \
  --extra-exclude-paths "**/snapshots/**,docs/tmp/**"
```

Sample output:

```
# Project Bundle

- Generated: 2025-09-16T00:00:00Z
- Root: /path/to/project
- Git: a1b2c3d
- Files: 12

---

====== BEGIN FILE: src/example.py ======
```python
...
```
====== END FILE ======
```

---

## Development

1. Create a virtual environment (`uv venv` or `python -m venv .venv`) and install dev dependencies: `uv pip install -e .[dev]`.
2. Make changes and run the checks below before sending a pull request.

### Quality Checks

```bash
ruff check .
black --check .
mypy src
pytest -q
```

Smoke tests live under `tests/smokes/` and should remain fast and deterministic.

### Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, including expectations for smokes, commit style, and PR reviews. All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Smoke Tests

See [docs/SMOKES_GUIDE.md](docs/SMOKES_GUIDE.md) for the philosophy and authoring patterns behind CLI smokes.

---

## Security

Report potential vulnerabilities privately—details are in [SECURITY.md](SECURITY.md). Please do not open public issues for sensitive disclosures.

---

## Roadmap

- Additional reusable utilities for LLM-oriented workflows (file summarizers, prompt templates).
- Richer smoke suites once more tools are added.
- Optional HTML/JSON bundle emitters.

Suggestions are welcome via GitHub issues.

---

## License

Released under the [MIT License](LICENSE).
```

====== END FILE ======


====== BEGIN FILE: SECURITY.md ======
```markdown
# Security Policy

## Supported Versions

The project aims to support the latest published release on PyPI (when available) and the `main` branch on GitHub. Older versions are not maintained.

## Reporting a Vulnerability

Please report suspected security issues privately:

1. Email the maintainers at `security@grahama.co` with a detailed description of the issue, proof-of-concept if available, and any suggested mitigations.
2. Alternatively, open a [GitHub Security Advisory](https://docs.github.com/en/code-security/security-advisories) pointing to this repository. Only maintainers will see your report.

We aim to acknowledge new reports within **3 business days** and keep you informed as we triage the issue.

If the vulnerability results in leaked credentials or other sensitive data, rotate those secrets immediately and include the steps you took in your report.

## Disclosure Policy

Maintainers will coordinate a disclosure timeline with the reporter. In general we prefer to publish fixes before announcing the vulnerability. Credit will be given to reporters unless they request anonymity.
```

====== END FILE ======


====== BEGIN FILE: STATE_OF_PROJECT.md ======
```markdown
Prompt: Generate/Update This Report Reliably

You are an operator agent asked to produce a fresh “State of Shared Dev Tools (Bundler + MCP)” report. Follow these exact steps and write your answer to STATE_of_PROJECT.md:

1) Validate repo + env
   - Confirm working dir contains this project (shared-dev-tools). Run:
     - uv pip install -e .[dev]
     - ruff check . && black --check . && mypy src && pytest -q
   - If any tooling is missing, install with: uv pip install ruff black mypy pytest

2) Verify CLI basics
   - Dry list in JSON:
     - python -m shared_dev_tools.cli --root . --output bundle.md --list --json
   - Generate a small bundle with headroom and JSON index:
     - python -m shared_dev_tools.cli \
       --root . --output bundle.md \
       --context-length 360000 --json --index artifacts/bundle.index.json

3) Verify new features (quick checks)
   - Strict mode error (non-zero exit but prints JSON):
     - python -m shared_dev_tools.cli --root . --output big.md --strict --json || echo ok
   - Incremental selection (Git only):
     - python -m shared_dev_tools.cli --root . --output inc.md --changed-since HEAD~1 --json
   - Token estimator switch:
     - python -m shared_dev_tools.cli --root . --output tok.md --token-estimator char --json
     - python -m shared_dev_tools.cli --root . --output tok.md --token-estimator tiktoken:gpt-4o --json
   - Preamble injection:
     - echo "# Operator Notes" > PREAMBLE.md
     - python -m shared_dev_tools.cli --root . --output pre.md --prefix-file PREAMBLE.md --json
   - Token cache (optional):
     - python -m shared_dev_tools.cli --root . --output c.md --cache-dir .cache --json

4) Verify MCP wrapper
   - Ensure ~/.codex/config.toml includes [mcp_servers.bundle-files] pointing to mcp/bundle-files-mcp/index.mjs.
   - From a client that supports MCP, call:
     - tool bundle.list → { root: "<abs/project>" }
     - tool bundle.generate → { root, output: "bundle.md", context_length: 400000, strict: true }
   - Expect JSON and resource_link entries (file://… for parts and optional index).

5) Optional competitor scan (use research tools; cite URLs)
   - Perplexity: “open-source CLI bundlers/packagers for LLM codebases 2024–2025; MCP file servers; what features matter?”
   - Brave: search “code repository bundler LLM”, “MCP server bundler”.
   - Context7: check modelcontextprotocol/typescript-sdk server docs for tool schemas/links.

6) Write the report with sections:
   - Executive Summary, Capabilities, Validation Status, Competitor Landscape,
     Gaps vs. Market, Recommendations/Roadmap (Now/Next/Later), Metrics & SLIs,
     Risks & Mitigations, References.

7) Keep it operator‑friendly
   - Terse bullets, copy‑paste commands (wrapped ~400px), minimal fluff.

---

# State of Shared Dev Tools (Bundler + MCP) — September 19, 2025

Executive Summary
- The bundle-files CLI now supports context-aware chunking (~token budget), JSON output, strict mode, incremental selection (Git), token estimator switching (char or tiktoken:<model>), preamble injection, and an optional token cache. Artifacts can be routed via --output-dir/--output-base and indexed with --index.
- A Node-based MCP wrapper exposes two tools (bundle.list, bundle.generate), returns structured JSON and resource_link entries, and provides usage/profile resources. Strict failures propagate as JSON (strict_failed with exit_code) so automations never lose diagnostics.
- Local quality gates and smokes pass (ruff, black, mypy, pytest). The design keeps dependencies minimal by default and adds model tokenizers only if requested.

Capabilities
- Selection & filtering
  - Respects .gitignore (authoritative via Git), best-effort fallback walk; default dir excludes and binary skip.
  - --include-ext, --extra-exclude-paths; --include-ignored and --no-respect-gitignore.
  - --changed-since <rev> (Git) incremental mode.
- Bundling & formatting
  - Clear file fence blocks with BEGIN/END markers; language fences by extension.
  - Context-length chunking (default 400k); per-part header with Git rev, file count, and budget.
  - --output-dir / --output-base for controlled artifact paths; .partN naming.
  - --prefix-file to inject operator preamble at top of each part.
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

Validation Status (local)
- Tooling gates:
  - ruff check .
  - black --check .
  - mypy src
  - pytest -q (includes smokes for CLI and JSON; Git incremental smoke guarded by git availability).
- Quick CLI sanity:
  - python -m shared_dev_tools.cli --root . --output bundle.md --list --json
  - python -m shared_dev_tools.cli --root . --output bundle.md --context-length 360000 --json --index artifacts/bundle.index.json
- MCP sanity:
  - bundle.list → returns selected files[]; bundle.generate → returns parts[] and resource_link(s).

Competitor Landscape (suggested scan)
- CLI “bundle for LLM” tools, packaging for MCP, and context-aware file packagers.
- What to compare:
  - Token accounting accuracy and speed; incremental selection; metadata/manifest support; machine-readable outputs; editor/agent integrations; observability.

Gaps vs. Market
- Exact-model tokenization (multi-provider) without optional installs (consider lazy plugin registry).
- Artifact manifest (JSON) with checksums, model budgets, and reproducible inputs.
- Parallel bundling for very large repos (threaded IO + controlled memory).
- Zip/tar packaging option with manifest and index resource_link.
- Remote artifact store (S3/local cache) and signed provenance for CI handoffs.

Recommendations / Roadmap
- Now
  - Add manifest.json (inputs, versions, budgets, part list + checksums) and return as resource_link (like --index).
  - Add --zip or --tar flag to package parts + index + manifest.
  - Add simple progress/summary logging (files/min, tokens/part) with --verbose.
- Next
  - Parallel file read + tokenization pipeline (bounded workers); optional rate metrics.
  - Estimator plugin registry: openai-tiktoken, anthropic-claude-tokens, tokenizer.json fallback.
  - Git-aware selection helpers: --changed-files-from <rev..rev>, --only-staged.
- Later
  - Remote artifact publishing (S3/file server) with signed manifest; MCP resource that lists/pulls latest bundle set.
  - Optional “source map” section (file offsets) to enable partial updates and rich navigation.

Metrics & SLIs (proposed)
- Bundle time (p50/p90), files/sec, bytes/sec.
- Tokens per part (p50/p90), parts per run, overflow rate (strict hits).
- Incremental speedup vs. full; cache hit rate; estimator CPU time.
- MCP tool success rate, tool latency (p50/p90), strict_failed frequency.

Risks & Mitigations
- Token estimator mismatch → default to char, provide tiktoken gate, document headroom guidance.
- Very large repos → add parallel readers and memory guards; enforce max_total_bytes and context_length.
- Path handling / Windows newlines → normalize to 
, POSIX rel paths used in JSON; tests enforce.
- Security (resource_links) → file:// URIs only reference paths under the requested root; avoid embedding secrets; respect .gitignore by default.

References
- Code: src/shared_dev_tools/cli.py; mcp/bundle-files-mcp/index.mjs
- Docs: docs/token_limits.md
- Smokes: tests/smokes/
- Config: ~/.codex/config.toml (mcp_servers.bundle-files)

```

====== END FILE ======


====== BEGIN FILE: docs/HAPPYPATH_GUIDE.md ======
```markdown
# Gamified — Happy Path Guide

Purpose
- Keep surface area minimal. Avoid option sprawl. Deliver a predictable, collaborative flow that works the first time and every time.
- This guide is for agents and engineers to stay on the paved road. If a step isn’t here, it’s likely out of scope for MVP.

Principles
- One spec. One command. One dashboard.
- Progressive disclosure: defaults always work; overrides are rare.
- Collaboration-by-default: runs are shareable, replayable, and annotated.
- Deterministic where possible: store seeds/spec snapshots for replay.
- Arango-only for MVP: no alternative backends, no graph authoring.

Golden Path Overview
- CLI verbs (only 4):
  - `init` — create a spec via a tiny TUI wizard
  - `run` — execute from a spec; auto-start backend; print URLs
  - `open` — open the dashboard filtered to a run
  - `replay` — re-run using the stored spec snapshot
- Single spec file: `gamified.yaml` (v1), Pydantic-validated.
- Backend: FastAPI + Arango (auto-starts on a free port).
- Dashboard: React/Tailwind/Shadcn (Status, Episodes, Logs, Run Notes).

Prerequisites
- ArangoDB running and reachable:
  - `ARANGO_HOST=127.0.0.1 ARANGO_PORT=8529 ARANGO_USERNAME=root ARANGO_PASSWORD=openSesame ARANGO_DB=marker`
- Codex CLI available:
  - `export CODEX_BINARY_PATH=/absolute/path/to/codex` (optional if `codex` is on PATH)
- uv (recommended) and Node (for dashboard dev only). The CLI auto-starts the backend; dashboard dev server is started by the orchestrator; you don’t need to run it manually.

Spec v1 (canonical example)
```yaml
version: 1
codebase:
  repo_root: .
approaches:
  - name: fueling_density_mpc
  - name: edge_stability_mhd
  - name: heat_extraction_adaptive
runner:
  type: analysis_sim
scoring:
  weights: { correctness: 35, robustness: 25, speed: 25, brevity: 15 }
constraints:
  edge_density_threshold: 1.0e19  # m^-3
  q_min: 2.0                      # safety factor lower bound
  beta_max: 0.04                  # fraction
  heat_flux_peak_max: 10.0        # MW/m^2
optimizer:
  rules: prototypes/gamified/rules/prompt_optimization.yaml
execution:
  concurrency: 3
  codex_exec: true
  autostart_backend: true
  autostart_dashboard: true
observability:
  backend: arango
  dashboard: true
```

SOPs (Step-by-Step)
1) Initialize a spec
- `python -m prototypes.gamified.cli init`
- Answer 3–4 prompts; writes `gamified.yaml`.

2) Run from the spec
- `python -m prototypes.gamified.cli run --spec gamified.yaml`
- What happens:
  - Backend autostarts on a free port.
  - Prompt is rendered from the spec and optimized (POP). Any hard errors are printed and the run exits.
  - A spec snapshot is saved to `workspace/runs/<run_id>/manifests/spec.yaml`.
  - The CLI prints the API scoreboard URL and the Dashboard URL.

3) Open the last run
- `python -m prototypes.gamified.cli open`
- Prints all URLs and attempts to open the backend dashboard proto. Use `--run-id` to pick a specific run.

4) Replay a run (deterministic)
- `python -m prototypes.gamified.cli replay <run_id>`
- Uses the stored spec snapshot for the run.

5) Annotate and share
- Dashboard → Status tab → Run Notes block
- Enter short context for teammates; click Save Notes. Copy/share the URL with filters.

Programmatic API (MVP)
- `GET /spec?path=gamified.yaml` → `{ ok, path, content }`
- `PUT /spec` with `{ path, content }` to persist changes
- `POST /runs` with `{ spec_path | spec_content, run_id?, fast? }` → `{ ok, run_id }`
- `GET /runs/{id}/notes` → `{ ok, notes }`
- `POST /runs/{id}/notes` with `{ notes }`
- `GET /stream` (SSE), `GET /scoreboard?run_id=...`, `GET /episodes?run_id=...`, `GET /logs?run_id=...`

CI Smokes (already wired)
- Prompt/spec validation (POP strict): `.github/workflows/gamified-prompts.yml`
- Fast run smoke (emit-only; artifacts): `.github/workflows/gamified-smoke.yml`

Do / Don’t (to avoid bloat)
- Do:
  - Use `--spec` for runs; prefer `gamified.yaml` at repo root.
  - Define all constraints as concrete numbers; keep 3–5 approaches.
  - Let POP normalize scoring to 100; keep runner = `analysis_sim` for MVP.
  - Use Run Notes instead of adding comment systems.
- Don’t:
  - Don’t add new flags or optional knobs unless they are absolutely necessary.
  - Don’t leave placeholders (e.g., "define") or ambiguous sections.
  - Don’t introduce new backends or graph flows in MVP.

Troubleshooting (fast)
- Backend failed to start: ensure Arango env vars set; the CLI prints `[backend] not reachable; starting…` and exits on failure.
- `codex` not found: set `CODEX_BINARY_PATH` or ensure `codex` on PATH.
- Ports busy: the CLI picks a free port; if conflicting, re-run.
- Artifacts: see `workspace/runs/<run_id>/manifests` and `api_base.txt`, `scorecard.json`.

Playbooks
- Fresh run for a teammate:
  - `git pull` → `python -m prototypes.gamified.cli run --spec gamified.yaml` → share the printed URLs.
- Quick iteration:
  - Edit `gamified.yaml` → re-run → annotate notes → share link.
- CI verification for PR:
  - Let the two workflows run; ensure POP strict passes and smoke artifacts upload.

Roadmap (v2, explicitly out-of-scope for MVP)
- “Optimize + Run” with diff + Accept in the dashboard (Write /spec then spawn /runs).
- A/B compare view and threaded comments.
- Graph workflows and alternative observability backends (Langfuse/OTLP) behind feature flags.

FAQ
- Why spec-first? Predictability, collaboration, and replayability with one source of truth.
- Why Arango only? Fewer moving parts; adapters can come later without changing the spec.
- Why only 4 CLI verbs? Reduces the cognitive footprint; everything maps to spec.
```

====== END FILE ======


====== BEGIN FILE: docs/SMOKES_GUIDE.md ======
```markdown
# Smoke Tests Guide

Smoke tests in **shared-dev-tools** verify that each CLI behaves correctly along its primary “happy path.” They should be fast, deterministic, and easy to run locally or in CI.

## Why Smokes?

- **Guard critical flows** – ensure commands launch, parse arguments, and touch the filesystem as expected.
- **Document behavior** – encode the acceptance criteria for new features so regressions surface quickly.
- **Stay lightweight** – run in under a second whenever possible so contributors can execute them frequently.

## Authoring Checklist

1. Place new tests inside `tests/smokes/`.
2. Use `pytest` + `tmp_path` fixtures to create isolated project structures.
3. Prefer driving CLIs through `typer.testing.CliRunner` to mimic real invocation.
4. Assert on observable outputs (exit status, stdout text, files created) rather than internal implementation details.
5. Keep external dependencies mocked or avoided entirely—smokes must succeed offline.

## Running Smokes

All smokes are executed via the standard pytest command:

```bash
pytest tests/smokes -q
```

They are also part of the default `pytest -q` run and enforced in CI.

## Adding New Commands

When introducing a new CLI or major option:

- Write the smoke in parallel with the implementation; it should fail before the feature exists and pass afterward.
- Update `README.md` and the command’s `--help` output so usage stays discoverable.
- If behavior depends on configuration files, document the expected format alongside the feature.

## Maintenance

- Update or remove smokes when acceptance criteria change.
- Keep tests deterministic—avoid time-of-day assertions or reliance on external network resources.
- If a smoke fails intermittently, open an issue immediately and either stabilize or temporarily mark it with `@pytest.mark.flaky` and a tracking ticket.

With this approach, contributors can add high confidence checks without slowing the development loop.
```

====== END FILE ======


====== BEGIN FILE: docs/comments.md ======
```markdown
I created a much smaller Tier‑1 “slim” bundle that fits
  comfortably under tight context limits.

  - Path: local/docs/review_bundle_tier1_slim.txt
  - Size: ~119 KB (well within typical web limits; far below
  400k tokens)
  - Contents: Only the most critical excerpts, plus both
  internal guides in full:
      - Guides (full): HAPPYPATH_GUIDE.md, SMOKES_GUIDE.md
      - Router (excerpts): acompletion(), aclose(), and context-
  manager region
      - Parallel ACompletions (full): litellm/router_utils/
  parallel_acompletion.py
      - HTTP transport (excerpts): core handler sections from
  http_handler.py and httpx_handler.py; support helpers included
  in full (async_client_cleanup.py, aiohttp_transport.py)
      - Optional-dep hotspots (excerpts): import regions
  (fastuuid) from types/utils.py, utils.py, litellm_logging.py,
  proxy/common_request_processing.py; bedrock/common_utils
  fastuuid region
      - MCP soft-deps (excerpts): imports + entrypoints from
  experimental_mcp_client/tools.py, client.py; responses/mcp/
  litellm_proxy_mcp_handler.py; types/mcp.py
      - Mini-Agent (core): arun_mcp_mini_agent() excerpt;
  full http_tools_invoker.py, agent_proxy.py, call_wrapper.py;
  research_tools.py call_openai_tool() excerpt

  How I pared it down

  - Large files (router.py, http handlers) are excerpted only
  around the critical functions with ±context.
  - Smaller helpers are included in full when safe and concise.
  - Optional-dep and MCP modules include just imports and
  entrypoints to review dependency guards.
  - Both guides are included in full so reviewers can judge
  alignment with your standards.

  If you want it even smaller

  - I can remove the full helpers and excerpt only the close/
  aclose regions.
  - I can trim the Mini-Agent adapters by excerpting only method
  signatures and error paths.
  - I can strip the guides to their “Principles” and “Smokes
  Checklist” sections (but generally reviewers need the full
  guides).

  Next steps

  - Submit local/docs/review_bundle_tier1_slim.txt to ChatGPT/
  Kimi-K2.
  - If the reviewer needs a “core-of-core” version (<50 KB),
  tell me your absolute size target and I’ll generate an ultra-
  slim version focusing on:
      - Router acompletion/aclose excerpts
      - One HTTP handler excerpt
      - fastuuid and MCP import regions
      - Mini-Agent loop excerpt only
      - Guides reduced to bullet checklists
```

====== END FILE ======


====== BEGIN FILE: docs/token_limits.md ======
```markdown
# Token Limits

The `bundle-files` CLI now chunk bundles by an approximate context length so that no single artifact is overwhelmingly large for an LLM.
By default the tool starts a new part whenever the estimated token usage for the current bundle would exceed about 400,000 tokens.

## How chunking works

- The command estimates tokens for the header metadata and each file block as it streams them into the bundle.
- When adding the next block would push the total above the configured `--context-length`, the current output file is finalized and the next block begins a new part.
- Additional parts reuse the base output name, inserting `.partN` before the extension. For example, `bundle.md` would produce `bundle.md`, `bundle.part2.md`, and so on.
- If a single file is larger than the configured limit, it is still emitted on its own part and the CLI prints a warning so you can revisit the selection or raise the limit.

## Configuring the context length

Use the `--context-length` option to control the approximate token budget per part:

```bash
# Lower the target to 200k tokens per part
bundle-files --context-length 200000

# Disable token-based chunking entirely
bundle-files --context-length 0
```

Because the token count is an estimate, keep some headroom below the actual model context that you intend to use.

## Token estimation details

The estimator is intentionally lightweight and does not require third-party tokenizers. It assumes roughly four characters per token.
That heuristic keeps the CLI dependency-free and fast, but it also means the reported token totals are approximate.
When you need an exact count for a specific model, run the generated bundle through the tokenizer provided by that model before uploading it.
```

====== END FILE ======


====== BEGIN FILE: mcp/bundle-files-mcp/index.mjs ======
```javascript
#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const here = dirname(fileURLToPath(import.meta.url));
const DEFAULT_PY_CLI = resolve(here, '../../src/shared_dev_tools/cli.py');
const PY_CLI = process.env.BUNDLE_PY_CLI && existsSync(process.env.BUNDLE_PY_CLI)
  ? process.env.BUNDLE_PY_CLI
  : DEFAULT_PY_CLI;

function arrify(x) { return Array.isArray(x) ? x : [x]; }

function runCli(args, { cwd } = {}) {
  const cmd = ['python3', PY_CLI];
  const res = spawnSync(cmd[0], [...cmd.slice(1), ...args], {
    cwd: cwd || process.cwd(),
    encoding: 'utf-8',
    stdio: ['ignore', 'pipe', 'pipe']
  });
  return res;
}

function parseJSON(stdout) { try { return JSON.parse(stdout); } catch { return null; } }

/* legacy parser removed */
function parseListOutput(stdout) {
  const lines = stdout.split(/\r?\n/).map(s => s.trim()).filter(Boolean);
  const idx = lines.findIndex(l => l.startsWith('Candidates:'));
  if (idx < 0) return { files: [] };
  const files = lines.slice(idx + 1).filter(l => !l.startsWith('[') && !l.includes(': '));
  return { files };
}

function partPath(base, index) {
  if (index === 1) return base;
  const name = basename(base);
  const dir = dirname(base);
  const firstDot = name.indexOf('.');
  if (firstDot >= 0) {
    const stem = name.slice(0, firstDot);
    const suffixes = name.slice(firstDot);
    return join(dir, `${stem}.part${index}${suffixes}`);
  }
  return join(dir, `${name}.part${index}`);
}

function listCreatedParts(basePath) {
  const parts = [];
  for (let i = 1; i < 1000; i++) {
    const p = partPath(basePath, i);
    if (existsSync(p)) parts.push(p); else break;
  }
  return parts;
}

function countOccurrences(hay, needle) {
  const m = hay.match(new RegExp(needle, 'g'));
  return m ? m.length : 0;
}

// MCP server
const server = new McpServer({ name: 'bundle-files-mcp', version: '0.1.0' });


// Provide clear, agent-readable usage instructions as a static resource.
const USAGE_URI = 'bundle-files://usage';
server.registerResource(
  'usage',
  USAGE_URI,
  {
    title: 'bundle-files MCP: Usage',
    description: 'How agents should call bundle.list and bundle.generate effectively',
  },
  async (uri) => ({
    contents: [
      {
        uri: typeof uri === 'string' ? USAGE_URI : uri.href,
        text: `# bundle-files MCP Usage

This server wraps the Python \`bundle-files\` CLI and exposes two tools for agents. Prefer \`bundle.list\` to preview selection, then \`bundle.generate\` to produce chunked bundles.

## Tools

- **bundle.list**
  - Purpose: dry-run selection without writing outputs.
  - Returns: { root, files[] } plus raw selection metadata.
  - Common args: { root, include_ext?, extra_exclude_paths?, include_ignored?, no_respect_gitignore? }.

- **bundle.generate**
  - Purpose: create one or more bundle parts based on size limits.
  - Returns: JSON with base_output and parts[{ path, file_count, bytes, tokens, exceeded_* }].
  - Common args: { root, output, context_length=400000, max_total_bytes=10000000, encoding='utf-8', include_* }.

## Recommended Flow

1. Call bundle.list with { root } to enumerate candidate files.
2. Decide a context budget: window_size * 0.9 (leave 10% headroom).
3. Call bundle.generate with:
   - output: a stable filename (e.g., 'bundle.md').
   - context_length: your computed budget.
   - include_ext / extra_exclude_paths as needed.
4. Consume parts[] from the JSON and stream each part to the model as needed.

## Notes

- Token estimation is heuristic (~4 chars/token). Keep headroom below model max.
- Set context_length = 0 to disable token-based chunking (bytes limit still applies).
- Paths are POSIX-relative in the JSON payload where applicable.
- The CLI respects .gitignore by default; pass include_ignored or no_respect_gitignore to override.

## Examples

- List candidates:

  {
    "tool": "bundle.list",
    "arguments": { "root": "/path/to/project" }
  }

- Generate bundles (400k token budget):

  {
    "tool": "bundle.generate",
    "arguments": {
      "root": "/path/to/project",
      "output": "bundle.md",
      "context_length": 400000
    }
  }

If unsure, fetch this resource again at '${USAGE_URI}'.
`,
      },
    ],
  })
);

// Provide a small profile resource with suggested defaults
server.registerResource(
  'profile',
  'bundle-files://profile',
  {
    title: 'bundle-files MCP: Profile',
    description: 'Defaults and capabilities summary',
  },
  async (uri) => ({
    contents: [
      {
        uri: typeof uri === 'string' ? 'bundle-files://profile' : uri.href,
        json: {
          default_context_length: 400000,
          recommended_headroom: 0.9,
          token_estimators: ['char', 'tiktoken:<model>'],
          supports_changed_since: true,
          supports_output_dir_base: true,
          strict_default: false
        }
      }
    ]
  })
);


server.registerTool(
  'bundle.list',
  {
    title: 'List files the bundler would include',
    description: 'Runs bundle-files in list mode and returns the selected file paths.',
    inputSchema: z.object({
      root: z.string().describe('Project root to scan'),
      include_ext: z.string().optional().describe('Comma-separated includes passed to --include-ext'),
      extra_exclude_paths: z.string().optional().describe('Comma-separated excludes'),
      include_ignored: z.boolean().optional().default(false),
      no_respect_gitignore: z.boolean().optional().default(false),
      changed_since: z.string().optional().describe('Git revision for incremental bundling'),
      strict: z.boolean().optional().default(false)
    })
  },
  async ({ root, include_ext, extra_exclude_paths, include_ignored, no_respect_gitignore, changed_since, strict = false }) => {
    const args = ['--root', root, '--output', '/dev/null', '--list', '--json'];
    if (strict) args.push('--strict');
    if (include_ext) args.push('--include-ext', include_ext);
    if (extra_exclude_paths) args.push('--extra-exclude-paths', extra_exclude_paths);
    if (include_ignored) args.push('--include-ignored');
    if (no_respect_gitignore) args.push('--no-respect-gitignore');
    if (changed_since) args.push('--changed-since', changed_since);
    if (index) args.push('--index', index);

    const { status, stdout, stderr } = runCli(args, { cwd: root });
    if (status !== 0) {
      return { content: [{ type: 'text', text: `bundle-files failed (exit ${status})\n${stderr}` }] };
    }
    const parsed = parseJSON(stdout);
    if (!parsed) {
      return { content: [{ type: 'text', text: `bundle-files returned invalid JSON` }] };
    }
    const filesAbs = parsed.files.map(rel => resolve(root, rel));
    return { content: [{ type: 'json', json: { root, files: filesAbs, raw: parsed } }] };
  }
);

server.registerTool(
  'bundle.generate',
  {
    title: 'Generate one or more bundle files',
    description: 'Runs bundle-files to produce chunked bundles and returns metadata about the parts.',
    inputSchema: z.object({
      root: z.string(),
      output: z.string().describe('Output file path (part files will derive from this)'),
      index: z.string().optional().describe('If set, CLI writes JSON summary to this path and MCP returns a link'),
      output_dir: z.string().optional().describe('Directory for outputs (overrides directory of output)'),
      output_base: z.string().optional().describe('Base filename for outputs, used with output_dir'),
      context_length: z.number().int().optional().default(400000),
      max_total_bytes: z.number().int().optional().default(10_000_000),
      encoding: z.string().optional().default('utf-8'),
      token_estimator: z.string().optional().describe("'char' or 'tiktoken:<model>'"),
      include_ext: z.string().optional(),
      extra_exclude_paths: z.string().optional(),
      include_ignored: z.boolean().optional().default(false),
      no_respect_gitignore: z.boolean().optional().default(false),
      changed_since: z.string().optional().describe('Git revision for incremental bundling'),
      strict: z.boolean().optional().default(false)
    })
  },
  async (input) => {
    const {
      root,
      output,
      index,
      output_dir,
      output_base,
      context_length = 400000,
      max_total_bytes = 10_000_000,
      encoding = 'utf-8',
      token_estimator,
      include_ext,
      extra_exclude_paths,
      include_ignored,
      no_respect_gitignore,
      changed_since,
      strict = false
    } = input;

    const args = ['--root', root, '--output', output, '--context-length', String(context_length), '--max-total-bytes', String(max_total_bytes), '--encoding', encoding, '--json'];
    if (strict) args.push('--strict');
    if (include_ext) args.push('--include-ext', include_ext);
    if (extra_exclude_paths) args.push('--extra-exclude-paths', extra_exclude_paths);
    if (include_ignored) args.push('--include-ignored');
    if (no_respect_gitignore) args.push('--no-respect-gitignore');
    if (changed_since) args.push('--changed-since', changed_since);
    if (index) args.push('--index', index);

    const { status, stdout, stderr } = runCli(args, { cwd: root });
    const parsed = parseJSON(stdout);
    if (status !== 0) {
      if (parsed) {
        parsed.strict_failed = true;
        parsed.exit_code = status;
        const links = (parsed.parts || []).map((p) => ({ type: 'resource_link', uri: 'file://' + p.path, name: p.path.split('/').pop(), description: 'Bundle part', mimeType: 'text/markdown' }));
    if (index) { links.unshift({ type: 'resource_link', uri: 'file://' + index, name: (index.split('/').pop()), description: 'Bundle index', mimeType: 'application/json' }); }
    return { content: [{ type: 'json', json: parsed }, ...links] };
      }
      return { content: [{ type: 'text', text: `bundle-files failed (exit ${status})\n${stderr}` }] };
    }

    if (!parsed) {
      return { content: [{ type: 'text', text: `bundle-files returned invalid JSON` }] };
    }
    const links = (parsed.parts || []).map((p) => ({ type: 'resource_link', uri: 'file://' + p.path, name: p.path.split('/').pop(), description: 'Bundle part', mimeType: 'text/markdown' }));
    if (index) { links.unshift({ type: 'resource_link', uri: 'file://' + index, name: (index.split('/').pop()), description: 'Bundle index', mimeType: 'application/json' }); }
    return { content: [{ type: 'json', json: parsed }, ...links] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

====== END FILE ======


====== BEGIN FILE: mcp/bundle-files-mcp/package-lock.json ======
```json
{
  "name": "bundle-files-mcp",
  "version": "0.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "bundle-files-mcp",
      "version": "0.1.0",
      "dependencies": {
        "@modelcontextprotocol/sdk": "^1.18.1",
        "zod": "^3.23.8"
      },
      "bin": {
        "bundle-files-mcp": "index.mjs"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@modelcontextprotocol/sdk": {
      "version": "1.18.1",
      "resolved": "https://registry.npmjs.org/@modelcontextprotocol/sdk/-/sdk-1.18.1.tgz",
      "integrity": "sha512-d//GE8/Yh7aC3e7p+kZG8JqqEAwwDUmAfvH1quogtbk+ksS6E0RR6toKKESPYYZVre0meqkJb27zb+dhqE9Sgw==",
      "license": "MIT",
      "dependencies": {
        "ajv": "^6.12.6",
        "content-type": "^1.0.5",
        "cors": "^2.8.5",
        "cross-spawn": "^7.0.5",
        "eventsource": "^3.0.2",
        "eventsource-parser": "^3.0.0",
        "express": "^5.0.1",
        "express-rate-limit": "^7.5.0",
        "pkce-challenge": "^5.0.0",
        "raw-body": "^3.0.0",
        "zod": "^3.23.8",
        "zod-to-json-schema": "^3.24.1"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/accepts": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/accepts/-/accepts-2.0.0.tgz",
      "integrity": "sha512-5cvg6CtKwfgdmVqY1WIiXKc3Q1bkRqGLi+2W/6ao+6Y7gu/RCwRuAhGEzh5B4KlszSuTLgZYuqFqo5bImjNKng==",
      "license": "MIT",
      "dependencies": {
        "mime-types": "^3.0.0",
        "negotiator": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/ajv": {
      "version": "6.12.6",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-6.12.6.tgz",
      "integrity": "sha512-j3fVLgvTo527anyYyJOGTYJbG+vnnQYvE0m5mmkc1TK+nxAppkCLMIL0aZ4dblVCNoGShhm+kzE4ZUykBoMg4g==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.1",
        "fast-json-stable-stringify": "^2.0.0",
        "json-schema-traverse": "^0.4.1",
        "uri-js": "^4.2.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/body-parser": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/body-parser/-/body-parser-2.2.0.tgz",
      "integrity": "sha512-02qvAaxv8tp7fBa/mw1ga98OGm+eCbqzJOKoRt70sLmfEEi+jyBYVTDGfCL/k06/4EMk/z01gCe7HoCH/f2LTg==",
      "license": "MIT",
      "dependencies": {
        "bytes": "^3.1.2",
        "content-type": "^1.0.5",
        "debug": "^4.4.0",
        "http-errors": "^2.0.0",
        "iconv-lite": "^0.6.3",
        "on-finished": "^2.4.1",
        "qs": "^6.14.0",
        "raw-body": "^3.0.0",
        "type-is": "^2.0.0"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/bytes": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/bytes/-/bytes-3.1.2.tgz",
      "integrity": "sha512-/Nf7TyzTx6S3yRJObOAV7956r8cr2+Oj8AC5dt8wSP3BQAoeX58NoHyCU8P8zGkNXStjTSi6fzO6F0pBdcYbEg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/call-bind-apply-helpers": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/call-bind-apply-helpers/-/call-bind-apply-helpers-1.0.2.tgz",
      "integrity": "sha512-Sp1ablJ0ivDkSzjcaJdxEunN5/XvksFJ2sMBFfq6x0ryhQV/2b/KwFe21cMpmHtPOSij8K99/wSfoEuTObmuMQ==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/call-bound": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/call-bound/-/call-bound-1.0.4.tgz",
      "integrity": "sha512-+ys997U96po4Kx/ABpBCqhA9EuxJaQWDQg7295H4hBphv3IZg0boBKuwYpt4YXp6MZ5AmZQnU/tyMTlRpaSejg==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "get-intrinsic": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/content-disposition": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/content-disposition/-/content-disposition-1.0.0.tgz",
      "integrity": "sha512-Au9nRL8VNUut/XSzbQA38+M78dzP4D+eqg3gfJHMIHHYa3bg067xj1KxMUWj+VULbiZMowKngFFbKczUrNJ1mg==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "5.2.1"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/content-type": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/content-type/-/content-type-1.0.5.tgz",
      "integrity": "sha512-nTjqfcBFEipKdXCv4YDQWCfmcLZKm81ldF0pAopTvyrFGVbcR6P/VAAd5G7N+0tTr8QqiU0tFadD6FK4NtJwOA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/cookie": {
      "version": "0.7.2",
      "resolved": "https://registry.npmjs.org/cookie/-/cookie-0.7.2.tgz",
      "integrity": "sha512-yki5XnKuf750l50uGTllt6kKILY4nQ1eNIQatoXEByZ5dWgnKqbnqmTrBE5B4N7lrMJKQ2ytWMiTO2o0v6Ew/w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/cookie-signature": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/cookie-signature/-/cookie-signature-1.2.2.tgz",
      "integrity": "sha512-D76uU73ulSXrD1UXF4KE2TMxVVwhsnCgfAyTg9k8P6KGZjlXKrOLe4dJQKI3Bxi5wjesZoFXJWElNWBjPZMbhg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.6.0"
      }
    },
    "node_modules/cors": {
      "version": "2.8.5",
      "resolved": "https://registry.npmjs.org/cors/-/cors-2.8.5.tgz",
      "integrity": "sha512-KIHbLJqu73RGr/hnbrO9uBeixNGuvSQjul/jdFvS/KFSIH1hWVd1ng7zOHx+YrEfInLG7q4n6GHQ9cDtxv/P6g==",
      "license": "MIT",
      "dependencies": {
        "object-assign": "^4",
        "vary": "^1"
      },
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/cross-spawn": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz",
      "integrity": "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==",
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.1.0",
        "shebang-command": "^2.0.0",
        "which": "^2.0.1"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/depd": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/depd/-/depd-2.0.0.tgz",
      "integrity": "sha512-g7nH6P6dyDioJogAAGprGpCtVImJhpPk/roCzdb3fIh61/s/nPsfR6onyMwkCAR/OlC3yBC0lESvUoQEAssIrw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/dunder-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/dunder-proto/-/dunder-proto-1.0.1.tgz",
      "integrity": "sha512-KIN/nDJBQRcXw0MLVhZE9iQHmG68qAVIBg9CqmUYjmQIhgij9U5MFvrqkUL5FbtyyzZuOeOt0zdeRe4UY7ct+A==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.1",
        "es-errors": "^1.3.0",
        "gopd": "^1.2.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/ee-first": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/ee-first/-/ee-first-1.1.1.tgz",
      "integrity": "sha512-WMwm9LhRUo+WUaRN+vRuETqG89IgZphVSNkdFgeb6sS/E4OrDIN7t48CAewSHXc6C8lefD8KKfr5vY61brQlow==",
      "license": "MIT"
    },
    "node_modules/encodeurl": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/encodeurl/-/encodeurl-2.0.0.tgz",
      "integrity": "sha512-Q0n9HRi4m6JuGIV1eFlmvJB7ZEVxu93IrMyiMsGC0lrMJMWzRgx6WGquyfQgZVb31vhGgXnfmPNNXmxnOkRBrg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/es-define-property": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/es-define-property/-/es-define-property-1.0.1.tgz",
      "integrity": "sha512-e3nRfgfUZ4rNGL232gUgX06QNyyez04KdjFrF+LTRoOXmrOgFKDg4BCdsjW8EnT69eqdYGmRpJwiPVYNrCaW3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-object-atoms": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/es-object-atoms/-/es-object-atoms-1.1.1.tgz",
      "integrity": "sha512-FGgH2h8zKNim9ljj7dankFPcICIK9Cp5bm+c2gQSYePhpaG5+esrLODihIorn+Pe6FGJzWhXQotPv73jTaldXA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/escape-html": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/escape-html/-/escape-html-1.0.3.tgz",
      "integrity": "sha512-NiSupZ4OeuGwr68lGIeym/ksIZMJodUGOSCZ/FSnTxcrekbvqrgdUxlJOMpijaKZVjAJrWrGs/6Jy8OMuyj9ow==",
      "license": "MIT"
    },
    "node_modules/etag": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/etag/-/etag-1.8.1.tgz",
      "integrity": "sha512-aIL5Fx7mawVa300al2BnEE4iNvo1qETxLrPI/o05L7z6go7fCw1J6EQmbK4FmJ2AS7kgVF/KEZWufBfdClMcPg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/eventsource": {
      "version": "3.0.7",
      "resolved": "https://registry.npmjs.org/eventsource/-/eventsource-3.0.7.tgz",
      "integrity": "sha512-CRT1WTyuQoD771GW56XEZFQ/ZoSfWid1alKGDYMmkt2yl8UXrVR4pspqWNEcqKvVIzg6PAltWjxcSSPrboA4iA==",
      "license": "MIT",
      "dependencies": {
        "eventsource-parser": "^3.0.1"
      },
      "engines": {
        "node": ">=18.0.0"
      }
    },
    "node_modules/eventsource-parser": {
      "version": "3.0.6",
      "resolved": "https://registry.npmjs.org/eventsource-parser/-/eventsource-parser-3.0.6.tgz",
      "integrity": "sha512-Vo1ab+QXPzZ4tCa8SwIHJFaSzy4R6SHf7BY79rFBDf0idraZWAkYrDjDj8uWaSm3S2TK+hJ7/t1CEmZ7jXw+pg==",
      "license": "MIT",
      "engines": {
        "node": ">=18.0.0"
      }
    },
    "node_modules/express": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/express/-/express-5.1.0.tgz",
      "integrity": "sha512-DT9ck5YIRU+8GYzzU5kT3eHGA5iL+1Zd0EutOmTE9Dtk+Tvuzd23VBU+ec7HPNSTxXYO55gPV/hq4pSBJDjFpA==",
      "license": "MIT",
      "dependencies": {
        "accepts": "^2.0.0",
        "body-parser": "^2.2.0",
        "content-disposition": "^1.0.0",
        "content-type": "^1.0.5",
        "cookie": "^0.7.1",
        "cookie-signature": "^1.2.1",
        "debug": "^4.4.0",
        "encodeurl": "^2.0.0",
        "escape-html": "^1.0.3",
        "etag": "^1.8.1",
        "finalhandler": "^2.1.0",
        "fresh": "^2.0.0",
        "http-errors": "^2.0.0",
        "merge-descriptors": "^2.0.0",
        "mime-types": "^3.0.0",
        "on-finished": "^2.4.1",
        "once": "^1.4.0",
        "parseurl": "^1.3.3",
        "proxy-addr": "^2.0.7",
        "qs": "^6.14.0",
        "range-parser": "^1.2.1",
        "router": "^2.2.0",
        "send": "^1.1.0",
        "serve-static": "^2.2.0",
        "statuses": "^2.0.1",
        "type-is": "^2.0.1",
        "vary": "^1.1.2"
      },
      "engines": {
        "node": ">= 18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/express-rate-limit": {
      "version": "7.5.1",
      "resolved": "https://registry.npmjs.org/express-rate-limit/-/express-rate-limit-7.5.1.tgz",
      "integrity": "sha512-7iN8iPMDzOMHPUYllBEsQdWVB6fPDMPqwjBaFrgr4Jgr/+okjvzAy+UHlYYL/Vs0OsOrMkwS6PJDkFlJwoxUnw==",
      "license": "MIT",
      "engines": {
        "node": ">= 16"
      },
      "funding": {
        "url": "https://github.com/sponsors/express-rate-limit"
      },
      "peerDependencies": {
        "express": ">= 4.11"
      }
    },
    "node_modules/fast-deep-equal": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/fast-deep-equal/-/fast-deep-equal-3.1.3.tgz",
      "integrity": "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==",
      "license": "MIT"
    },
    "node_modules/fast-json-stable-stringify": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/fast-json-stable-stringify/-/fast-json-stable-stringify-2.1.0.tgz",
      "integrity": "sha512-lhd/wF+Lk98HZoTCtlVraHtfh5XYijIjalXck7saUtuanSDyLMxnHhSXEDJqHxD7msR8D0uCmqlkwjCV8xvwHw==",
      "license": "MIT"
    },
    "node_modules/finalhandler": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/finalhandler/-/finalhandler-2.1.0.tgz",
      "integrity": "sha512-/t88Ty3d5JWQbWYgaOGCCYfXRwV1+be02WqYYlL6h0lEiUAMPM8o8qKGO01YIkOHzka2up08wvgYD0mDiI+q3Q==",
      "license": "MIT",
      "dependencies": {
        "debug": "^4.4.0",
        "encodeurl": "^2.0.0",
        "escape-html": "^1.0.3",
        "on-finished": "^2.4.1",
        "parseurl": "^1.3.3",
        "statuses": "^2.0.1"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/forwarded": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/forwarded/-/forwarded-0.2.0.tgz",
      "integrity": "sha512-buRG0fpBtRHSTCOASe6hD258tEubFoRLb4ZNA6NxMVHNw2gOcwHo9wyablzMzOA5z9xA9L1KNjk/Nt6MT9aYow==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/fresh": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/fresh/-/fresh-2.0.0.tgz",
      "integrity": "sha512-Rx/WycZ60HOaqLKAi6cHRKKI7zxWbJ31MhntmtwMoaTeF7XFH9hhBp8vITaMidfljRQ6eYWCKkaTK+ykVJHP2A==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-intrinsic": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.3.0.tgz",
      "integrity": "sha512-9fSjSaos/fRIVIp+xSJlE6lfwhES7LNtKaCBIamHsjr2na1BiABJPo0mOjjz8GJDURarmCPGqaiVg5mfjb98CQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "function-bind": "^1.1.2",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/get-proto/-/get-proto-1.0.1.tgz",
      "integrity": "sha512-sTSfBjoXBp89JvIKIefqw7U2CCebsc74kiY6awiGogKtoSGbgjYE/G/+l9sF3MWFPNc9IcoOC4ODfKHfxFmp0g==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/gopd": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/gopd/-/gopd-1.2.0.tgz",
      "integrity": "sha512-ZUKRh6/kUFoAiTAtTYPZJ3hw9wNxx+BIBOijnlG9PnrJsCcSjs1wyyD6vJpaYtgnzDrKYRSqf3OO6Rfa93xsRg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-symbols": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-symbols/-/has-symbols-1.1.0.tgz",
      "integrity": "sha512-1cDNdwJ2Jaohmb3sg4OmKaMBwuC48sYni5HUw2DvsC8LjGTLK9h+eb1X6RyuOHe4hT0ULCW68iomhjUoKUqlPQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/hasown": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.2.tgz",
      "integrity": "sha512-0hJU9SCPvmMzIBdZFqNPXWa6dqh7WdH0cII9y+CyS8rG3nL48Bclra9HmKhVVUHyPWNH5Y7xDwAB7bfgSjkUMQ==",
      "license": "MIT",
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/http-errors": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/http-errors/-/http-errors-2.0.0.tgz",
      "integrity": "sha512-FtwrG/euBzaEjYeRqOgly7G0qviiXoJWnvEH2Z1plBdXgbyjv34pHTSb9zoeHMyDy33+DWy5Wt9Wo+TURtOYSQ==",
      "license": "MIT",
      "dependencies": {
        "depd": "2.0.0",
        "inherits": "2.0.4",
        "setprototypeof": "1.2.0",
        "statuses": "2.0.1",
        "toidentifier": "1.0.1"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/http-errors/node_modules/statuses": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/statuses/-/statuses-2.0.1.tgz",
      "integrity": "sha512-RwNA9Z/7PrK06rYLIzFMlaF+l73iwpzsqRIFgbMLbTcLD6cOao82TaWefPXQvB2fOC4AjuYSEndS7N/mTCbkdQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/iconv-lite": {
      "version": "0.6.3",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.6.3.tgz",
      "integrity": "sha512-4fCk79wshMdzMp2rH06qWrJE4iolqLhCUH+OiuIgU++RB0+94NlDL81atO7GX55uUKueo0txHNtvEyI6D7WdMw==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3.0.0"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/inherits": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/inherits/-/inherits-2.0.4.tgz",
      "integrity": "sha512-k/vGaX4/Yla3WzyMCvTQOXYeIHvqOKtnqBduzTHpzpQZzAskKMhZ2K+EnBiSM9zGSoIFeMpXKxa4dYeZIQqewQ==",
      "license": "ISC"
    },
    "node_modules/ipaddr.js": {
      "version": "1.9.1",
      "resolved": "https://registry.npmjs.org/ipaddr.js/-/ipaddr.js-1.9.1.tgz",
      "integrity": "sha512-0KI/607xoxSToH7GjN1FfSbLoU0+btTicjsQSWQlh/hZykN8KpmMf7uYwPW3R+akZ6R/w18ZlXSHBYXiYUPO3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/is-promise": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/is-promise/-/is-promise-4.0.0.tgz",
      "integrity": "sha512-hvpoI6korhJMnej285dSg6nu1+e6uxs7zG3BYAm5byqDsgJNWwxzM6z6iZiAgQR4TJ30JmBTOwqZUw3WlyH3AQ==",
      "license": "MIT"
    },
    "node_modules/isexe": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/isexe/-/isexe-2.0.0.tgz",
      "integrity": "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw==",
      "license": "ISC"
    },
    "node_modules/json-schema-traverse": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-0.4.1.tgz",
      "integrity": "sha512-xbbCH5dCYU5T8LcEhhuh7HJ88HXuW3qsI3Y0zOZFKfZEHcpWiHU/Jxzk629Brsab/mMiHQti9wMP+845RPe3Vg==",
      "license": "MIT"
    },
    "node_modules/math-intrinsics": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/math-intrinsics/-/math-intrinsics-1.1.0.tgz",
      "integrity": "sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/media-typer": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/media-typer/-/media-typer-1.1.0.tgz",
      "integrity": "sha512-aisnrDP4GNe06UcKFnV5bfMNPBUw4jsLGaWwWfnH3v02GnBuXX2MCVn5RbrWo0j3pczUilYblq7fQ7Nw2t5XKw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/merge-descriptors": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/merge-descriptors/-/merge-descriptors-2.0.0.tgz",
      "integrity": "sha512-Snk314V5ayFLhp3fkUREub6WtjBfPdCPY1Ln8/8munuLuiYhsABgBVWsozAG+MWMbVEvcdcpbi9R7ww22l9Q3g==",
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/mime-db": {
      "version": "1.54.0",
      "resolved": "https://registry.npmjs.org/mime-db/-/mime-db-1.54.0.tgz",
      "integrity": "sha512-aU5EJuIN2WDemCcAp2vFBfp/m4EAhWJnUNSSw0ixs7/kXbd6Pg64EmwJkNdFhB8aWt1sH2CTXrLxo/iAGV3oPQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/mime-types": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/mime-types/-/mime-types-3.0.1.tgz",
      "integrity": "sha512-xRc4oEhT6eaBpU1XF7AjpOFD+xQmXNB5OVKwp4tqCuBpHLS/ZbBDrc07mYTDqVMg6PfxUjjNp85O6Cd2Z/5HWA==",
      "license": "MIT",
      "dependencies": {
        "mime-db": "^1.54.0"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "license": "MIT"
    },
    "node_modules/negotiator": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/negotiator/-/negotiator-1.0.0.tgz",
      "integrity": "sha512-8Ofs/AUQh8MaEcrlq5xOX0CQ9ypTF5dl78mjlMNfOK08fzpgTHQRQPBxcPlEtIw0yRpws+Zo/3r+5WRby7u3Gg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/object-assign": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz",
      "integrity": "sha512-rJgTQnkUnH1sFw8yT6VSU3zD3sWmu6sZhIseY8VX+GRu3P6F7Fu+JNDoXfklElbLJSnc3FUQHVe4cU5hj+BcUg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/object-inspect": {
      "version": "1.13.4",
      "resolved": "https://registry.npmjs.org/object-inspect/-/object-inspect-1.13.4.tgz",
      "integrity": "sha512-W67iLl4J2EXEGTbfeHCffrjDfitvLANg0UlX3wFUUSTx92KXRFegMHUVgSqE+wvhAbi4WqjGg9czysTV2Epbew==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/on-finished": {
      "version": "2.4.1",
      "resolved": "https://registry.npmjs.org/on-finished/-/on-finished-2.4.1.tgz",
      "integrity": "sha512-oVlzkg3ENAhCk2zdv7IJwd/QUD4z2RxRwpkcGY8psCVcCYZNq4wYnVWALHM+brtuJjePWiYF/ClmuDr8Ch5+kg==",
      "license": "MIT",
      "dependencies": {
        "ee-first": "1.1.1"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/once": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/once/-/once-1.4.0.tgz",
      "integrity": "sha512-lNaJgI+2Q5URQBkccEKHTQOPaXdUxnZZElQTZY0MFUAuaEqe1E+Nyvgdz/aIyNi6Z9MzO5dv1H8n58/GELp3+w==",
      "license": "ISC",
      "dependencies": {
        "wrappy": "1"
      }
    },
    "node_modules/parseurl": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/parseurl/-/parseurl-1.3.3.tgz",
      "integrity": "sha512-CiyeOxFT/JZyN5m0z9PfXw4SCBJ6Sygz1Dpl0wqjlhDEGGBP1GnsUVEL0p63hoG1fcj3fHynXi9NYO4nWOL+qQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/path-key": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-3.1.1.tgz",
      "integrity": "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-to-regexp": {
      "version": "8.3.0",
      "resolved": "https://registry.npmjs.org/path-to-regexp/-/path-to-regexp-8.3.0.tgz",
      "integrity": "sha512-7jdwVIRtsP8MYpdXSwOS0YdD0Du+qOoF/AEPIt88PcCFrZCzx41oxku1jD88hZBwbNUIEfpqvuhjFaMAqMTWnA==",
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/pkce-challenge": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/pkce-challenge/-/pkce-challenge-5.0.0.tgz",
      "integrity": "sha512-ueGLflrrnvwB3xuo/uGob5pd5FN7l0MsLf0Z87o/UQmRtwjvfylfc9MurIxRAWywCYTgrvpXBcqjV4OfCYGCIQ==",
      "license": "MIT",
      "engines": {
        "node": ">=16.20.0"
      }
    },
    "node_modules/proxy-addr": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/proxy-addr/-/proxy-addr-2.0.7.tgz",
      "integrity": "sha512-llQsMLSUDUPT44jdrU/O37qlnifitDP+ZwrmmZcoSKyLKvtZxpyV0n2/bD/N4tBAAZ/gJEdZU7KMraoK1+XYAg==",
      "license": "MIT",
      "dependencies": {
        "forwarded": "0.2.0",
        "ipaddr.js": "1.9.1"
      },
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/punycode": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/punycode/-/punycode-2.3.1.tgz",
      "integrity": "sha512-vYt7UD1U9Wg6138shLtLOvdAu+8DsC/ilFtEVHcH+wydcSpNE20AfSOduf6MkRFahL5FY7X1oU7nKVZFtfq8Fg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/qs": {
      "version": "6.14.0",
      "resolved": "https://registry.npmjs.org/qs/-/qs-6.14.0.tgz",
      "integrity": "sha512-YWWTjgABSKcvs/nWBi9PycY/JiPJqOD4JA6o9Sej2AtvSGarXxKC3OQSk4pAarbdQlKAh5D4FCQkJNkW+GAn3w==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">=0.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/range-parser": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/range-parser/-/range-parser-1.2.1.tgz",
      "integrity": "sha512-Hrgsx+orqoygnmhFbKaHE6c296J+HTAQXoxEF6gNupROmmGJRoyzfG3ccAveqCBrwr/2yxQ5BVd/GTl5agOwSg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/raw-body": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/raw-body/-/raw-body-3.0.1.tgz",
      "integrity": "sha512-9G8cA+tuMS75+6G/TzW8OtLzmBDMo8p1JRxN5AZ+LAp8uxGA8V8GZm4GQ4/N5QNQEnLmg6SS7wyuSmbKepiKqA==",
      "license": "MIT",
      "dependencies": {
        "bytes": "3.1.2",
        "http-errors": "2.0.0",
        "iconv-lite": "0.7.0",
        "unpipe": "1.0.0"
      },
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/raw-body/node_modules/iconv-lite": {
      "version": "0.7.0",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.7.0.tgz",
      "integrity": "sha512-cf6L2Ds3h57VVmkZe+Pn+5APsT7FpqJtEhhieDCvrE2MK5Qk9MyffgQyuxQTm6BChfeZNtcOLHp9IcWRVcIcBQ==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3.0.0"
      },
      "engines": {
        "node": ">=0.10.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/router": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/router/-/router-2.2.0.tgz",
      "integrity": "sha512-nLTrUKm2UyiL7rlhapu/Zl45FwNgkZGaCpZbIHajDYgwlJCOzLSk+cIPAnsEqV955GjILJnKbdQC1nVPz+gAYQ==",
      "license": "MIT",
      "dependencies": {
        "debug": "^4.4.0",
        "depd": "^2.0.0",
        "is-promise": "^4.0.0",
        "parseurl": "^1.3.3",
        "path-to-regexp": "^8.0.0"
      },
      "engines": {
        "node": ">= 18"
      }
    },
    "node_modules/safe-buffer": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/safe-buffer/-/safe-buffer-5.2.1.tgz",
      "integrity": "sha512-rp3So07KcdmmKbGvgaNxQSJr7bGVSVk5S9Eq1F+ppbRo70+YeaDxkw5Dd8NPN+GD6bjnYm2VuPuCXmpuYvmCXQ==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT"
    },
    "node_modules/safer-buffer": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/safer-buffer/-/safer-buffer-2.1.2.tgz",
      "integrity": "sha512-YZo3K82SD7Riyi0E1EQPojLz7kpepnSQI9IyPbHHg1XXXevb5dJI7tpyN2ADxGcQbHG7vcyRHk0cbwqcQriUtg==",
      "license": "MIT"
    },
    "node_modules/send": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/send/-/send-1.2.0.tgz",
      "integrity": "sha512-uaW0WwXKpL9blXE2o0bRhoL2EGXIrZxQ2ZQ4mgcfoBxdFmQold+qWsD2jLrfZ0trjKL6vOw0j//eAwcALFjKSw==",
      "license": "MIT",
      "dependencies": {
        "debug": "^4.3.5",
        "encodeurl": "^2.0.0",
        "escape-html": "^1.0.3",
        "etag": "^1.8.1",
        "fresh": "^2.0.0",
        "http-errors": "^2.0.0",
        "mime-types": "^3.0.1",
        "ms": "^2.1.3",
        "on-finished": "^2.4.1",
        "range-parser": "^1.2.1",
        "statuses": "^2.0.1"
      },
      "engines": {
        "node": ">= 18"
      }
    },
    "node_modules/serve-static": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/serve-static/-/serve-static-2.2.0.tgz",
      "integrity": "sha512-61g9pCh0Vnh7IutZjtLGGpTA355+OPn2TyDv/6ivP2h/AdAVX9azsoxmg2/M6nZeQZNYBEwIcsne1mJd9oQItQ==",
      "license": "MIT",
      "dependencies": {
        "encodeurl": "^2.0.0",
        "escape-html": "^1.0.3",
        "parseurl": "^1.3.3",
        "send": "^1.2.0"
      },
      "engines": {
        "node": ">= 18"
      }
    },
    "node_modules/setprototypeof": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/setprototypeof/-/setprototypeof-1.2.0.tgz",
      "integrity": "sha512-E5LDX7Wrp85Kil5bhZv46j8jOeboKq5JMmYM3gVGdGH8xFpPWXUMsNrlODCrkoxMEeNi/XZIwuRvY4XNwYMJpw==",
      "license": "ISC"
    },
    "node_modules/shebang-command": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-2.0.0.tgz",
      "integrity": "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA==",
      "license": "MIT",
      "dependencies": {
        "shebang-regex": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shebang-regex": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-3.0.0.tgz",
      "integrity": "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/side-channel": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/side-channel/-/side-channel-1.1.0.tgz",
      "integrity": "sha512-ZX99e6tRweoUXqR+VBrslhda51Nh5MTQwou5tnUDgbtyM0dBgmhEDtWGP/xbKn6hqfPRHujUNwz5fy/wbbhnpw==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3",
        "side-channel-list": "^1.0.0",
        "side-channel-map": "^1.0.1",
        "side-channel-weakmap": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-list": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/side-channel-list/-/side-channel-list-1.0.0.tgz",
      "integrity": "sha512-FCLHtRD/gnpCiCHEiJLOwdmFP+wzCmDEkc9y7NsYxeF4u7Btsn1ZuwgwJGxImImHicJArLP4R0yX4c2KCrMrTA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-map": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/side-channel-map/-/side-channel-map-1.0.1.tgz",
      "integrity": "sha512-VCjCNfgMsby3tTdo02nbjtM/ewra6jPHmpThenkTYh8pG9ucZ/1P8So4u4FGBek/BjpOVsDCMoLA/iuBKIFXRA==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-weakmap": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/side-channel-weakmap/-/side-channel-weakmap-1.0.2.tgz",
      "integrity": "sha512-WPS/HvHQTYnHisLo9McqBHOJk2FkHO/tlpvldyrnem4aeQp4hai3gythswg6p01oSoTl58rcpiFAjF2br2Ak2A==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3",
        "side-channel-map": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/statuses": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/statuses/-/statuses-2.0.2.tgz",
      "integrity": "sha512-DvEy55V3DB7uknRo+4iOGT5fP1slR8wQohVdknigZPMpMstaKJQWhwiYBACJE3Ul2pTnATihhBYnRhZQHGBiRw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/toidentifier": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/toidentifier/-/toidentifier-1.0.1.tgz",
      "integrity": "sha512-o5sSPKEkg/DIQNmH43V0/uerLrpzVedkUh8tGNvaeXpfpuwjKenlSox/2O/BTlZUtEe+JG7s5YhEz608PlAHRA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.6"
      }
    },
    "node_modules/type-is": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/type-is/-/type-is-2.0.1.tgz",
      "integrity": "sha512-OZs6gsjF4vMp32qrCbiVSkrFmXtG/AZhY3t0iAMrMBiAZyV9oALtXO8hsrHbMXF9x6L3grlFuwW2oAz7cav+Gw==",
      "license": "MIT",
      "dependencies": {
        "content-type": "^1.0.5",
        "media-typer": "^1.1.0",
        "mime-types": "^3.0.0"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/unpipe": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/unpipe/-/unpipe-1.0.0.tgz",
      "integrity": "sha512-pjy2bYhSsufwWlKwPc+l3cN7+wuJlK6uz0YdJEOlQDbl6jo/YlPi4mb8agUkVC8BF7V8NuzeyPNqRksA3hztKQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/uri-js": {
      "version": "4.4.1",
      "resolved": "https://registry.npmjs.org/uri-js/-/uri-js-4.4.1.tgz",
      "integrity": "sha512-7rKUyy33Q1yc98pQ1DAmLtwX109F7TIfWlW1Ydo8Wl1ii1SeHieeh0HHfPeL2fMXK6z0s8ecKs9frCuLJvndBg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "punycode": "^2.1.0"
      }
    },
    "node_modules/vary": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/vary/-/vary-1.1.2.tgz",
      "integrity": "sha512-BNGbWLfd0eUPabhkXUVm0j8uuvREyTh5ovRa/dyow/BqAbZJyC+5fU+IzQOzmAKzYqYRAISoRhdQr3eIZ/PXqg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/which": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/which/-/which-2.0.2.tgz",
      "integrity": "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA==",
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "node-which": "bin/node-which"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/wrappy": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz",
      "integrity": "sha512-l4Sp/DRseor9wL6EvV2+TuQn63dMkPjZ/sp9XkghTEbV9KlPS1xUsZ3u7/IQO4wxtcFB4bgpQPRcR3QCvezPcQ==",
      "license": "ISC"
    },
    "node_modules/zod": {
      "version": "3.25.76",
      "resolved": "https://registry.npmjs.org/zod/-/zod-3.25.76.tgz",
      "integrity": "sha512-gzUt/qt81nXsFGKIFcC3YnfEAx5NkunCfnDlvuBSSFS02bcXu4Lmea0AFIUwbLWxWPx3d9p8S5QoaujKcNQxcQ==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/colinhacks"
      }
    },
    "node_modules/zod-to-json-schema": {
      "version": "3.24.6",
      "resolved": "https://registry.npmjs.org/zod-to-json-schema/-/zod-to-json-schema-3.24.6.tgz",
      "integrity": "sha512-h/z3PKvcTcTetyjl1fkj79MHNEjm+HpD6NXheWjzOekY7kV+lwDYnHw+ivHkijnCSMz1yJaWBD9vu/Fcmk+vEg==",
      "license": "ISC",
      "peerDependencies": {
        "zod": "^3.24.1"
      }
    }
  }
}
```

====== END FILE ======


====== BEGIN FILE: mcp/bundle-files-mcp/package.json ======
```json
{
  "name": "bundle-files-mcp",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "description": "Light MCP wrapper around shared-dev-tools bundle-files CLI",
  "bin": {
    "bundle-files-mcp": "index.mjs"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.18.1",
    "zod": "^3.23.8"
  },
  "engines": {
    "node": ">=18"
  }
}
```

====== END FILE ======


====== BEGIN FILE: pyproject.toml ======
```toml
[project]
name = "shared-dev-tools"
version = "0.1.0"
description = "Utilities for bundling source files into LLM-friendly artifacts"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "typer>=0.16.0",
]

[project.scripts]
bundle-files = "shared_dev_tools.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/shared_dev_tools"]

[tool.hatch.build.targets.sdist]
include = ["src/shared_dev_tools", "README.md", "pyproject.toml"]
```

====== END FILE ======


====== BEGIN FILE: src/shared_dev_tools/__init__.py ======
```python
"""Shared developer tooling utilities."""

from .cli import app, main

__all__ = ["app", "main"]
```

====== END FILE ======


====== BEGIN FILE: src/shared_dev_tools/cli.py ======
```python
"""Command line entry point for building Markdown bundles from selected files.

Features
- Uses Git to respect .gitignore exactly when available (authoritative).
- Graceful fallback when not in Git: best-effort ignore based on root .gitignore and common folders.
- Skips binaries/images; size guards to avoid oversized inputs.
- Flexible selection: include extra filename globs or extensions; exclude paths; opt-in to include ignored files.
- Clear file boundaries with Markdown fences for LLM-friendly ingestion.

Examples
  # Standard run (respects .gitignore if in Git)
  bundle-files --root . --output bundle.txt

  # Include extra file types or special filenames (globs on names)
  bundle-files --include-ext ".proto,Justfile,vite.config.ts"

  # Add extra explicit path excludes
  bundle-files --extra-exclude-paths "misc/big_fixture.json,notes/tmp.txt"

  # Force include .gitignored files (audits)
  bundle-files --include-ignored

  # Ignore .gitignore entirely (fallback walk only)
  bundle-files --no-respect-gitignore
"""

from __future__ import annotations

import fnmatch
import json
import math
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Callable

import typer


# ---------------------------- Utility helpers ----------------------------


def _run_git(
    root: Path, args: Sequence[str], check: bool = False
) -> tuple[int, str, str]:
    """Run a git command from a specific root and capture output."""
    cmd = ["git", "-C", str(root), *args]
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.returncode, proc.stdout, proc.stderr


def _is_git_repo(root: Path) -> bool:
    code, out, _ = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    return code == 0 and out.strip() == "true"


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _posix_rel_path(path: Path, start: Path) -> str:
    return path.relative_to(start).as_posix()


def _read_text(path: Path, encoding: str = "utf-8") -> str:
    with path.open("r", encoding=encoding, errors="replace") as f:
        return f.read()


def _is_binary_by_content(path: Path, sample_bytes: int = 4096) -> bool:
    try:
        with path.open("rb") as f:
            chunk = f.read(sample_bytes)
        if b"\0" in chunk:
            return True
        # Heuristic: consider >30% of bytes outside typical text range as binary
        if not chunk:
            return False
        text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
        nontext = sum(b not in text_chars for b in chunk)
        return (nontext / len(chunk)) > 0.30
    except OSError:
        return True


# ---------------------------- Selection rules ----------------------------


DEFAULT_EXCLUDE_DIRS: Set[str] = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".output",
    ".svelte-kit",
    "coverage",
    ".cache",
    ".parcel-cache",
    ".turbo",
    ".vite",
    ".vercel",
    ".expo",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "artifacts",
}


DEFAULT_BINARY_EXTS: Set[str] = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".icns",
    ".bmp",
    ".tif",
    ".tiff",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".so",
    ".dylib",
    ".a",
    ".lib",
    ".exe",
    ".dll",
}


LANG_BY_EXT = {
    ".py": "python",
    ".rs": "rust",
    ".go": "go",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "ts",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "ini",
    ".md": "markdown",
    ".txt": "text",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".less": "less",
    ".xml": "xml",
    ".svg": "xml",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "zsh",
    ".dockerfile": "dockerfile",
    ".proto": "proto",
    ".java": "java",
    ".kt": "kotlin",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cs": "cs",
}


# ---------------------------- Token estimation ----------------------------


def _make_token_estimator(spec: Optional[str]) -> Callable[[str], int]:
    """Return a callable(text)->int based on estimator spec.

    - None or "char" => ~4 chars/token heuristic
    - "tiktoken:<model>" => use tiktoken encoding if available, else fallback
    """

    if not spec or spec == "char":
        return lambda s: math.ceil(len(s) / 4) if s else 0

    if spec.startswith("tiktoken:"):
        model = spec.split(":", 1)[1] or ""
        try:
            import tiktoken  # type: ignore

            enc = (
                tiktoken.get_encoding("cl100k_base")
                if not model
                else tiktoken.encoding_for_model(model)
            )

            def _tok(s: str) -> int:
                if not s:
                    return 0
                try:
                    return len(enc.encode(s))
                except Exception:
                    return math.ceil(len(s) / 4)

            return _tok
        except Exception:
            # Silent fallback to char heuristic
            return lambda s: math.ceil(len(s) / 4) if s else 0

    # Unknown spec => fallback
    return lambda s: math.ceil(len(s) / 4) if s else 0


@dataclass
class _TokenCacheEntry:
    size: int
    mtime_ns: int
    estimator: str
    tokens: int


class _TokenCache:
    def __init__(self, path: Optional[Path]) -> None:
        self.path = path
        self.data: dict[str, _TokenCacheEntry] = {}
        if path is not None and path.exists():
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                for k, v in raw.items():
                    self.data[k] = _TokenCacheEntry(**v)
            except Exception:
                self.data = {}

    def make_key(self, file_path: Path, estimator: str) -> str:
        try:
            st = file_path.stat()
            return f"{file_path.resolve()}::{st.st_size}::{st.st_mtime_ns}::{estimator}"
        except Exception:
            return f"{file_path.resolve()}::0::0::{estimator}"

    def get(self, key: str) -> Optional[int]:
        ent = self.data.get(key)
        return ent.tokens if ent else None

    def set(self, key: str, file_path: Path, estimator: str, tokens: int) -> None:
        try:
            st = file_path.stat()
            self.data[key] = _TokenCacheEntry(
                st.st_size, st.st_mtime_ns, estimator, tokens
            )
        except Exception:
            self.data[key] = _TokenCacheEntry(0, 0, estimator, tokens)

    def save(self) -> None:
        if self.path is None:
            return
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            payload = {k: vars(v) for k, v in self.data.items()}
            self.path.write_text(json.dumps(payload), encoding="utf-8")
        except Exception:
            pass


def _lang_for_file(path: Path) -> str:
    name = path.name.lower()
    if name == "dockerfile":
        return "dockerfile"
    return LANG_BY_EXT.get(path.suffix.lower(), "")


def _parse_csv_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _normalize_patterns(patterns: Iterable[str]) -> List[str]:
    norm: List[str] = []
    for p in patterns:
        p = p.strip()
        if not p or p.startswith("#"):
            continue
        norm.append(p)
    return norm


def _matches_any(path_rel: str, patterns: Sequence[str]) -> bool:
    # Try matching both on full relative path and the basename
    base = path_rel.split("/")[-1]
    for pat in patterns:
        # Support simple ".ext" include patterns
        if pat.startswith(".") and "." in base and base.endswith(pat):
            return True
        if "/" in pat:
            if fnmatch.fnmatch(path_rel, pat):
                return True
        else:
            if fnmatch.fnmatch(base, pat):
                return True
    return False


def _read_gitignore_patterns(root: Path) -> List[str]:
    patterns: List[str] = []
    gi = root / ".gitignore"
    if gi.is_file():
        patterns.extend(_normalize_patterns(_read_text(gi).splitlines()))
    # Also consider .git/info/exclude if present
    info_exclude = root / ".git" / "info" / "exclude"
    if info_exclude.is_file():
        patterns.extend(_normalize_patterns(_read_text(info_exclude).splitlines()))
    return patterns


def _ignored_by_patterns(path_rel: str, patterns: Sequence[str]) -> bool:
    # Naive best-effort: treat patterns as fnmatch globs relative to repo root
    # and directory suffixes ("dir/") as recursive dir ignores.
    for p in patterns:
        if p.endswith("/"):
            # directory pattern: ignore if path starts with that dir
            if path_rel.startswith(p[:-1]):
                return True
        else:
            if fnmatch.fnmatch(path_rel, p):
                return True
            # Also attempt basename match
            base = path_rel.split("/")[-1]
            if fnmatch.fnmatch(base, p):
                return True
    return False


# ---------------------------- Discovery ----------------------------


def discover_files(
    root: Path,
    respect_gitignore: bool,
    include_ignored: bool,
    extra_exclude_paths: Sequence[str],
) -> List[Path]:
    """Return a list of candidate files under root, relative to root.

    If inside a Git repo and respect_gitignore=True, uses git ls-files (authoritative).
    Otherwise, falls back to a best-effort os.walk with simple .gitignore glob handling.
    """
    root = root.resolve()

    # Git-based discovery
    if respect_gitignore and _is_git_repo(root):
        args = ["ls-files", "-co", "--exclude-standard"]
        if include_ignored:
            args = ["ls-files", "-coi", "--exclude-standard"]
        code, out, err = _run_git(root, args)
        if code != 0:
            print(
                f"Warning: git discovery failed, falling back to walk: {err.strip()}",
                file=sys.stderr,
            )
        else:
            rels = [line.strip() for line in out.splitlines() if line.strip()]
            # Filter: exclude paths containing any excluded directory at any depth
            rels = [
                r
                for r in rels
                if not any(part in DEFAULT_EXCLUDE_DIRS for part in r.split("/"))
            ]
            if extra_exclude_paths:
                rels = [r for r in rels if not _matches_any(r, extra_exclude_paths)]
            return [root / r for r in rels if (root / r).is_file()]

    # Fallback: os.walk with best-effort ignore handling
    ignore_patterns: List[str] = []
    if respect_gitignore:
        ignore_patterns = _read_gitignore_patterns(root)

    results: List[Path] = []
    for base, dirs, files in os.walk(root):
        # Prune excluded directories aggressively
        rel_base = _posix_rel_path(Path(base), root)
        # Rel path for base is "." for root; normalize
        if rel_base == ".":
            rel_base = ""

        # Prune default exclude dirs
        pruned_dirs = []
        for d in list(dirs):
            if d in DEFAULT_EXCLUDE_DIRS:
                pruned_dirs.append(d)
                continue
            full_rel = (Path(rel_base) / d).as_posix() if rel_base else d
            if respect_gitignore and _ignored_by_patterns(
                full_rel + "/", ignore_patterns
            ):
                pruned_dirs.append(d)
        for d in pruned_dirs:
            if d in dirs:
                dirs.remove(d)

        for fname in files:
            rel = (Path(rel_base) / fname).as_posix() if rel_base else fname
            if extra_exclude_paths and _matches_any(rel, extra_exclude_paths):
                continue
            if respect_gitignore and _ignored_by_patterns(rel, ignore_patterns):
                continue
            results.append(root / rel)

    return [p for p in results if p.is_file()]


# ---------------------------- Filtering ----------------------------


@dataclass
class FilterOptions:
    include_patterns: List[str]
    max_file_bytes: int
    allow_large: bool


def should_include_file(path: Path, rel: str, opts: FilterOptions) -> bool:
    # Include patterns bypass extension-based filtering only (not size or binary checks)
    matched_include = (
        _matches_any(rel, opts.include_patterns) if opts.include_patterns else False
    )

    # Skip binaries by extension first
    if path.suffix.lower() in DEFAULT_BINARY_EXTS and not matched_include:
        return False

    # Size guard
    try:
        size = path.stat().st_size
    except OSError:
        return False

    if not opts.allow_large and size > opts.max_file_bytes:
        return False

    # Content-based binary heuristic
    if _is_binary_by_content(path):
        return False

    return True


# ---------------------------- Concatenation ----------------------------


@dataclass
class BundleResult:
    path: Path
    file_count: int
    total_bytes: int
    total_tokens: int
    exceeded_token_limit: bool
    exceeded_byte_limit: bool
    skipped_unreadable: int


@dataclass
class _BundleBlock:
    text: str
    tokens: int
    bytes_len: int
    is_file: bool
    skip: bool = False


def _estimate_tokens(text: str) -> int:
    """Approximate token count using a simple character heuristic."""
    if not text:
        return 0
    return math.ceil(len(text) / 4)


def _format_bundle_header(
    *,
    root: Path,
    git_desc: str,
    file_count: int,
    part_index: int,
    generated_ts: str,
    max_tokens: Optional[int],
) -> str:
    lines = [
        "# Project Bundle",
        "",
        f"- Generated: {generated_ts}",
        f"- Root: {root}",
        f"- Git: {git_desc or 'n/a'}",
        f"- Files: {file_count}",
        f"- Bundle Part: {part_index}",
    ]
    if max_tokens:
        lines.append(f"- Context Tokens Limit: {max_tokens}")
    lines.extend(["", "---", ""])
    return "\n".join(lines)


def _part_output_path(base: Path, part_index: int) -> Path:
    if part_index == 1:
        return base
    suffixes = "".join(base.suffixes)
    if suffixes:
        stem = base.name[: -len(suffixes)]
        return base.with_name(f"{stem}.part{part_index}{suffixes}")
    return base.with_name(f"{base.name}.part{part_index}")


class _BundleWriter:
    """Accumulates bundle blocks and writes chunked outputs."""

    def __init__(
        self,
        *,
        root: Path,
        output: Path,
        encoding: str,
        max_total_bytes: int,
        max_total_tokens: Optional[int],
        git_desc: str,
        token_estimator: Callable[[str], int],
        prefix_text: Optional[str] = None,
    ) -> None:
        self.root = root
        self.base_output = output
        self.encoding = encoding
        self.max_total_bytes = max_total_bytes if max_total_bytes > 0 else None
        self.max_total_tokens = (
            max_total_tokens if max_total_tokens and max_total_tokens > 0 else None
        )
        self.git_desc = git_desc
        self.generated_ts = _now_utc_iso()
        self._tok = token_estimator
        self.prefix_text = prefix_text or ""
        self.results: List[BundleResult] = []
        self.part_index = 1
        self.current_blocks: List[_BundleBlock] = []
        self.current_tokens_sum = 0
        self.current_bytes_sum = 0
        self.current_file_count = 0
        self.current_overflow_tokens = False
        self.current_overflow_bytes = False
        self.current_skips_count = 0
        self.current_skips_count = 0

    def _header_for_count(self, file_count: int) -> str:
        return _format_bundle_header(
            root=self.root,
            git_desc=self.git_desc,
            file_count=file_count,
            part_index=self.part_index,
            generated_ts=self.generated_ts,
            max_tokens=self.max_total_tokens,
        )

    def _compute_totals(self, block: _BundleBlock) -> tuple[int, int]:
        file_count = self.current_file_count + (1 if block.is_file else 0)
        header = self._header_for_count(file_count) + (
            self.prefix_text if self.prefix_text else ""
        )
        header_tokens = self._tok(header)
        header_bytes = len(header.encode(self.encoding, errors="replace"))
        total_tokens = header_tokens + self.current_tokens_sum + block.tokens
        total_bytes = header_bytes + self.current_bytes_sum + block.bytes_len
        return total_tokens, total_bytes

    def add_block(self, block: _BundleBlock) -> None:
        total_tokens, total_bytes = self._compute_totals(block)
        exceeds_tokens = (
            self.max_total_tokens is not None and total_tokens > self.max_total_tokens
        )
        exceeds_bytes = (
            self.max_total_bytes is not None and total_bytes > self.max_total_bytes
        )

        if (exceeds_tokens or exceeds_bytes) and self.current_blocks:
            self._flush_current()
            total_tokens, total_bytes = self._compute_totals(block)
            exceeds_tokens = (
                self.max_total_tokens is not None
                and total_tokens > self.max_total_tokens
            )
            exceeds_bytes = (
                self.max_total_bytes is not None and total_bytes > self.max_total_bytes
            )

        self.current_blocks.append(block)
        self.current_tokens_sum += block.tokens
        self.current_bytes_sum += block.bytes_len
        if block.is_file:
            self.current_file_count += 1
        if block.skip:
            self.current_skips_count += 1
        if exceeds_tokens:
            self.current_overflow_tokens = True
        if exceeds_bytes:
            self.current_overflow_bytes = True

    def _flush_current(self) -> None:
        header = self._header_for_count(self.current_file_count)
        header_bytes = len(header.encode(self.encoding, errors="replace"))
        header_tokens = self._tok(header)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header)
            if self.prefix_text:
                out_f.write(self.prefix_text)
            if self.prefix_text:
                out_f.write(self.prefix_text)
            for block in self.current_blocks:
                out_f.write(block.text)

        total_tokens = header_tokens + self.current_tokens_sum
        total_bytes = header_bytes + self.current_bytes_sum
        self.results.append(
            BundleResult(
                path=output_path,
                file_count=self.current_file_count,
                total_bytes=total_bytes,
                total_tokens=total_tokens,
                exceeded_token_limit=self.current_overflow_tokens,
                exceeded_byte_limit=self.current_overflow_bytes,
                skipped_unreadable=self.current_skips_count,
            )
        )

        self.part_index += 1
        self.current_blocks = []
        self.current_tokens_sum = 0
        self.current_bytes_sum = 0
        self.current_file_count = 0
        self.current_overflow_tokens = False
        self.current_overflow_bytes = False

    def _flush_empty(self) -> None:
        header = self._header_for_count(0)
        header_bytes = len(header.encode(self.encoding, errors="replace"))
        header_tokens = self._tok(header)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header)
            if self.prefix_text:
                out_f.write(self.prefix_text)

        self.results.append(
            BundleResult(
                path=output_path,
                file_count=0,
                total_bytes=header_bytes,
                total_tokens=header_tokens,
                exceeded_token_limit=False,
                exceeded_byte_limit=False,
                skipped_unreadable=0,
            )
        )

        self.part_index += 1

    def finalize(self) -> List[BundleResult]:
        if self.current_blocks:
            self._flush_current()
        elif not self.results:
            self._flush_empty()
        return self.results


def write_bundles(
    root: Path,
    files: Sequence[Path],
    output: Path,
    encoding: str,
    max_total_bytes: int,
    max_total_tokens: Optional[int],
    token_estimator: Callable[[str], int],
    token_estimator_spec: Optional[str],
    cache_path: Optional[Path],
    prefix_text: Optional[str],
) -> List[BundleResult]:
    """Write one or more Markdown bundle files based on size constraints."""

    git_desc = ""
    if _is_git_repo(root):
        code, out, _ = _run_git(root, ["rev-parse", "--short", "HEAD"])
        rev = out.strip() if code == 0 else "unknown"
        code, out, _ = _run_git(root, ["status", "--porcelain"])
        dirty = "+dirty" if out.strip() else ""
        git_desc = f"{rev}{dirty}"

    cache = _TokenCache(cache_path) if cache_path is not None else _TokenCache(None)

    writer = _BundleWriter(
        root=root,
        output=output,
        encoding=encoding,
        max_total_bytes=max_total_bytes,
        max_total_tokens=max_total_tokens,
        git_desc=git_desc,
        token_estimator=token_estimator,
        prefix_text=prefix_text,
    )

    for path in files:
        rel = _posix_rel_path(path, root)
        try:
            content = _read_text(path, encoding=encoding)
        except Exception as exc:  # noqa: BLE001
            msg = f"[SKIP unreadable: {rel}: {exc}]\n\n"
            block = _BundleBlock(
                text=msg,
                tokens=token_estimator(msg),
                bytes_len=len(msg.encode(encoding, errors="replace")),
                is_file=False,
                skip=True,
            )
            key = cache.make_key(path, token_estimator_spec or "char")
            if cache.get(key) is None:
                cache.set(key, path, token_estimator_spec or "char", block.tokens)
            writer.add_block(block)
            continue

        lang = _lang_for_file(path)
        fence_open = f"```{lang}\n" if lang else "```\n"
        fence_close = "```\n"
        file_header = f"\n\n====== BEGIN FILE: {rel} ======\n"
        file_footer = "\n====== END FILE ======\n"

        block_text = (
            file_header
            + fence_open
            + content
            + ("\n" if not content.endswith("\n") else "")
            + fence_close
            + file_footer
        )
        block = _BundleBlock(
            text=block_text,
            tokens=(
                cache.get(cache.make_key(path, token_estimator_spec or "char"))
                or token_estimator(block_text)
            ),
            bytes_len=len(block_text.encode(encoding, errors="replace")),
            is_file=True,
        )
        key = cache.make_key(path, token_estimator_spec or "char")
        if cache.get(key) is None:
            cache.set(key, path, token_estimator_spec or "char", block.tokens)
        writer.add_block(block)

    res = writer.finalize()
    try:
        cache.save()
    except Exception:
        pass
    return res


# ---------------------------- Typer CLI ----------------------------


def build_cli() -> typer.Typer:
    app = typer.Typer(
        help="Concatenate selected project files into one or more bundles for LLMs"
    )

    @app.callback(invoke_without_command=True)
    def run(
        root: Path = typer.Option(Path("."), "--root", help="Project root to scan"),
        output: Path = typer.Option(
            Path("bundle.txt"),
            "--output",
            "-o",
            help="Output path for the concatenated bundle",
        ),
        include_ext: Optional[str] = typer.Option(
            None,
            "--include-ext",
            help="Comma-separated list of filename globs or extensions to force-include (e.g. '.proto,Justfile,vite.config.ts')",
        ),
        extra_exclude_paths: Optional[str] = typer.Option(
            None,
            "--extra-exclude-paths",
            help="Comma-separated relative path globs to exclude additionally",
        ),
        no_respect_gitignore: bool = typer.Option(
            False,
            "--no-respect-gitignore",
            help="Do not use .gitignore even if present; walk filesystem instead",
        ),
        include_ignored: bool = typer.Option(
            False,
            "--include-ignored",
            help="If in Git and respecting .gitignore, include ignored files too",
        ),
        max_file_bytes: int = typer.Option(
            512_000,
            "--max-file-bytes",
            help="Per-file size guard; files larger than this are skipped unless --allow-large",
        ),
        allow_large: bool = typer.Option(
            False,
            "--allow-large",
            help="Allow files larger than --max-file-bytes",
        ),
        max_total_bytes: int = typer.Option(
            10_000_000,
            "--max-total-bytes",
            help="Stop writing once total bytes in output reach this threshold",
        ),
        context_length: int = typer.Option(
            400_000,
            "--context-length",
            help="Approximate token capacity per bundle part before splitting; set 0 to disable token-based chunking.",
        ),
        token_estimator: Optional[str] = typer.Option(
            None,
            "--token-estimator",
            help="Token estimator to use: 'char' (default) or 'tiktoken:<model>' if tiktoken is available",
        ),
        changed_since: Optional[str] = typer.Option(
            None,
            "--changed-since",
            help="Limit selection to files changed since the given Git revision (requires Git repo)",
        ),
        output_dir: Optional[Path] = typer.Option(
            None,
            "--output-dir",
            help="If provided, write output under this directory using --output or --output-base",
        ),
        output_base: Optional[str] = typer.Option(
            None,
            "--output-base",
            help="Base name for output file (e.g., 'bundle.md'); used with --output-dir",
        ),
        prefix_file: Optional[Path] = typer.Option(
            None,
            "--prefix-file",
            help="Path to a file whose contents will be inserted at the top of each bundle part",
        ),
        cache_dir: Optional[Path] = typer.Option(
            None,
            "--cache-dir",
            help="Directory to store token estimation cache (optional)",
        ),
        encoding: str = typer.Option(
            "utf-8", "--encoding", help="Encoding used to read files and write output"
        ),
        json_output: bool = typer.Option(
            False,
            "--json",
            help="Emit machine-readable JSON to stdout instead of friendly text",
        ),
        index: Optional[Path] = typer.Option(
            None,
            "--index",
            help="Optional path to also write the JSON result (when --json)",
        ),
        strict: bool = typer.Option(
            False,
            "--strict",
            help="Exit non-zero if any part exceeds limits or if any files were skipped as unreadable",
        ),
        list_only: bool = typer.Option(
            False, "--list", help="List selected files and exit (no bundle writing)"
        ),
        dry_run: bool = typer.Option(
            False, "--dry-run", help="Do not write output, only print selection summary"
        ),
    ) -> None:
        """Create a bundle or list selected files."""

        root_resolved = root.resolve()
        include_patterns = _parse_csv_list(include_ext or "")
        extra_excludes = _parse_csv_list(extra_exclude_paths or "")

        files_all = discover_files(
            root=root_resolved,
            respect_gitignore=not no_respect_gitignore,
            include_ignored=include_ignored,
            extra_exclude_paths=extra_excludes,
        )

        # If changed_since provided and repo available, narrow to changed files
        if changed_since and _is_git_repo(root_resolved):
            code, out, err = _run_git(
                root_resolved, ["diff", "--name-only", f"{changed_since}", "--"]
            )
            if code == 0:
                changed = [
                    (root_resolved / line.strip())
                    for line in out.splitlines()
                    if line.strip()
                ]
                changed = [p for p in changed if p.is_file()]
                if extra_excludes:
                    changed = [
                        p
                        for p in changed
                        if not _matches_any(
                            _posix_rel_path(p, root_resolved), extra_excludes
                        )
                    ]
                if changed:
                    files_all = changed

        fopts = FilterOptions(
            include_patterns=include_patterns,
            max_file_bytes=max_file_bytes,
            allow_large=allow_large,
        )

        selected: List[Path] = []
        for p in files_all:
            rel = _posix_rel_path(p, root_resolved)
            if should_include_file(p, rel, fopts):
                selected.append(p)

        selected.sort(key=lambda x: _posix_rel_path(x, root_resolved))

        # Load optional prefix text
        prefix_text = ""
        if prefix_file is not None:
            try:
                prefix_text = _read_text(prefix_file, encoding=encoding)
                if prefix_text and not prefix_text.endswith("\n\n"):
                    prefix_text += "\n\n"
            except Exception:
                prefix_text = ""

        cache_path = None
        if cache_dir is not None:
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_path = (cache_dir / "token_cache.json").resolve()

        # Compute effective output path if output_dir/base provided
        effective_output = output
        if output_dir is not None or output_base is not None:
            base_name = output_base or output.name
            effective_output = (output_dir or output.parent) / base_name
        # Compute effective output path if output_dir/base provided
        effective_output = output
        if output_dir is not None or output_base is not None:
            base_name = output_base or output.name
            effective_output = (output_dir or output.parent) / base_name

        if list_only or dry_run:
            if json_output:
                payload = {
                    "root": str(root_resolved),
                    "git": bool(_is_git_repo(root_resolved)),
                    "respect_gitignore": not no_respect_gitignore,
                    "include_ignored": include_ignored,
                    "candidates": len(files_all),
                    "selected": len(selected),
                    "files": [_posix_rel_path(p, root_resolved) for p in selected],
                    "generated": _now_utc_iso(),
                }
                text = json.dumps(payload)
                typer.echo(text)
                if index is not None:
                    index.parent.mkdir(parents=True, exist_ok=True)
                    index.write_text(text, encoding="utf-8")
            else:
                typer.echo(f"Root: {root_resolved}")
                typer.echo(
                    f"Git: {'yes' if _is_git_repo(root_resolved) else 'no'} (respect={not no_respect_gitignore}, include_ignored={include_ignored})"
                )
                typer.echo(
                    f"Candidates: {len(files_all)}  -> Selected: {len(selected)}"
                )
                for p in selected:
                    typer.echo(_posix_rel_path(p, root_resolved))
            raise typer.Exit(0)

        token_limit = context_length if context_length > 0 else None
        tok = _make_token_estimator(token_estimator)

        results = write_bundles(
            root=root_resolved,
            files=selected,
            output=effective_output,
            encoding=encoding,
            max_total_bytes=max_total_bytes,
            max_total_tokens=token_limit,
            token_estimator=tok,
            token_estimator_spec=token_estimator,
            cache_path=cache_path,
            prefix_text=prefix_text,
        )

        if json_output:
            payload = {
                "root": str(root_resolved),
                "base_output": str((root_resolved / output).resolve()),
                "context_length": token_limit,
                "max_total_bytes": max_total_bytes,
                "encoding": encoding,
                "generated": _now_utc_iso(),
                "parts": [
                    {
                        "path": str(r.path),
                        "file_count": r.file_count,
                        "bytes": r.total_bytes,
                        "tokens": r.total_tokens,
                        "exceeded_token_limit": r.exceeded_token_limit,
                        "exceeded_byte_limit": r.exceeded_byte_limit,
                        "skipped_unreadable": r.skipped_unreadable,
                    }
                    for r in results
                ],
            }
            text = json.dumps(payload)
            typer.echo(text)
            if index is not None:
                index.parent.mkdir(parents=True, exist_ok=True)
                index.write_text(text, encoding="utf-8")
        else:
            total_files_written = sum(res.file_count for res in results)
            if len(results) == 1:
                res = results[0]
                typer.echo(
                    f"Wrote {res.file_count} files to {res.path} ({res.total_bytes} bytes, tokens~{res.total_tokens})"
                )
                if res.exceeded_token_limit:
                    typer.echo(
                        "Warning: bundle exceeds --context-length tokens; consider reducing selection or lowering the limit.",
                        err=True,
                    )
                if res.exceeded_byte_limit:
                    typer.echo(
                        "Warning: bundle exceeds --max-total-bytes; consider adjusting limits.",
                        err=True,
                    )
            else:
                limit_desc = "disabled" if token_limit is None else str(token_limit)
                typer.echo(
                    f"Wrote {total_files_written} files across {len(results)} bundles (context-length {limit_desc})"
                )
                for idx, res in enumerate(results, start=1):
                    flags = []
                    if res.exceeded_token_limit:
                        flags.append("tokens>limit")
                    if res.exceeded_byte_limit:
                        flags.append("bytes>limit")
                    suffix = f" [{', '.join(flags)}]" if flags else ""
                    typer.echo(
                        f"  part {idx}: {res.path} files={res.file_count} bytes={res.total_bytes} tokens~{res.total_tokens}{suffix}"
                    )

    return app


app = build_cli()


def main() -> None:
    """Entry point for executable scripts."""
    app()


if __name__ == "__main__":
    # VS Code-friendly: running this file directly uses option defaults.
    main()
```

====== END FILE ======


====== BEGIN FILE: tests/conftest.py ======
```python
"""Pytest configuration for shared-dev-tools tests."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
```

====== END FILE ======


====== BEGIN FILE: tests/smokes/test_cli_bundle_smoke.py ======
```python
"""Smoke tests for the bundle-files Typer CLI."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from shared_dev_tools.cli import app


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_bundle_cli_smoke(tmp_path: Path) -> None:
    """End-to-end smoke: CLI bundles non-ignored text files into Markdown."""

    root = tmp_path / "project"
    root.mkdir()

    _write_text(root / "keep.py", "print('hi')\n")
    _write_text(root / "README.md", "# Title\nBody\n")
    _write_text(root / "ignored.log", "secret\n")
    _write_text(root / "nested" / "notes.txt", "note\n")

    # Pretend to ignore the log file via gitignore even without a git repo present.
    _write_text(root / ".gitignore", "ignored.log\n")

    # Binary extension should be skipped automatically.
    (root / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")

    bundle_path = root / "bundle.md"

    runner = CliRunner()

    # Dry list first to verify the selection summary.
    list_result = runner.invoke(
        app,
        ["--root", str(root), "--output", str(bundle_path), "--list"],
    )
    assert list_result.exit_code == 0, list_result.stdout
    stdout = list_result.stdout
    assert "Root:" in stdout
    assert "keep.py" in stdout
    assert "README.md" in stdout
    assert "ignored.log" not in stdout

    # Now produce the actual bundle.
    result = runner.invoke(
        app,
        ["--root", str(root), "--output", str(bundle_path)],
    )
    assert result.exit_code == 0, result.stdout
    assert "Wrote" in result.stdout

    assert bundle_path.exists()
    bundle_text = bundle_path.read_text(encoding="utf-8")

    # Header + file sections present
    assert "# Project Bundle" in bundle_text
    assert "BEGIN FILE: keep.py" in bundle_text
    assert "print('hi')" in bundle_text
    assert "README.md" in bundle_text
    assert "notes.txt" in bundle_text
    # Ignored and binary files should not appear
    assert "BEGIN FILE: ignored.log" not in bundle_text
    assert "BEGIN FILE: image.png" not in bundle_text


def test_bundle_cli_splits_when_context_limit(tmp_path: Path) -> None:
    """Bundle splits into multiple parts when context-length is low."""

    root = tmp_path / "project"
    root.mkdir()

    big_line = "print('hello world')\\n" * 300
    _write_text(root / "alpha.py", big_line)
    _write_text(root / "beta.py", big_line)

    bundle_path = root / "bundle.md"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(bundle_path),
            "--context-length",
            "200",
        ],
    )

    assert result.exit_code == 0, result.stdout

    part_two = bundle_path.with_name("bundle.part2.md")
    assert bundle_path.exists()
    assert part_two.exists()

    first_text = bundle_path.read_text(encoding="utf-8")
    second_text = part_two.read_text(encoding="utf-8")

    assert "BEGIN FILE: alpha.py" in first_text
    assert "BEGIN FILE: beta.py" not in first_text
    assert "BEGIN FILE: beta.py" in second_text

    # CLI output should reflect multi-bundle summary
    assert "bundles" in result.stdout
    assert "part 2" in result.stdout


def test_bundle_cli_json_outputs(tmp_path: Path) -> None:
    """JSON mode returns machine-readable results for list and generate."""

    root = tmp_path / "project"
    root.mkdir()

    # A couple small files
    _write_text(root / "a.py", "print('a')\n")
    _write_text(root / "b.py", "print('b')\n")

    bundle_path = root / "bundle.md"
    runner = CliRunner()

    # List JSON
    list_res = runner.invoke(
        app,
        ["--root", str(root), "--output", str(bundle_path), "--list", "--json"],
    )
    assert list_res.exit_code == 0, list_res.stdout
    import json as _json

    list_payload = _json.loads(list_res.stdout)
    assert list_payload["root"].endswith("project")
    assert isinstance(list_payload["files"], list) and list_payload["files"]

    # Generate JSON
    gen_res = runner.invoke(
        app,
        ["--root", str(root), "--output", str(bundle_path), "--json"],
    )
    assert gen_res.exit_code == 0, gen_res.stdout
    gen_payload = _json.loads(gen_res.stdout)
    assert gen_payload["base_output"].endswith("bundle.md")
    assert isinstance(gen_payload["parts"], list) and gen_payload["parts"], gen_payload
    assert "file_count" in gen_payload["parts"][0]
```

====== END FILE ======


====== BEGIN FILE: tests/smokes/test_cli_changed_since_smoke.py ======
```python
"""Smoke test for --changed-since incremental selection.

Keeps runtime minimal by doing two small commits in a temp Git repo.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from shared_dev_tools.cli import app


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_changed_since_limits_selection(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()

    # init git repo
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(
        ["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True
    )
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)

    # commit 1
    _write_text(root / "a.py", "print('a')\n")
    _write_text(root / "b.py", "print('b')\n")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "init"], check=True)

    # commit 2: change b.py and add c.py
    _write_text(root / "b.py", "print('b2')\n")
    _write_text(root / "c.py", "print('c')\n")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "second"], check=True)

    runner = CliRunner()

    # list-only JSON with changed_since HEAD~1 → should show only b.py and c.py
    list_res = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(root / "bundle.md"),
            "--list",
            "--json",
            "--changed-since",
            "HEAD~1",
        ],
    )
    assert list_res.exit_code == 0, list_res.stdout
    import json as _json

    payload = _json.loads(list_res.stdout)
    files = set(payload["files"])  # relative paths
    assert files == {"b.py", "c.py"}
```

====== END FILE ======

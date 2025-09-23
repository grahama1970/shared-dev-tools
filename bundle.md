# Project Bundle

- Generated: 2025-09-22T15:11:08Z
- Root: /home/graham/workspace/experiments/shared-dev-tools
- Git: 8fe4d9c+dirty
- Files: 32
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
```

====== END FILE ======


====== BEGIN FILE: bundle.md ======
```markdown
# Project Bundle

- Generated: 2025-09-22T15:11:02Z
- Root: /home/graham/workspace/experiments/shared-dev-tools
- Git: 8fe4d9c+dirty
- Files: 31
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


====== BEGIN FILE: docs/MCP_USAGE.md ======
```markdown
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
    description: "Preview which files would be included in a code-review bundle.",
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
        if (!parsed) return { content: [{ type: "text", text: "bundle-files returned invalid JSON" }] };
        const filesAbs = (parsed.files || []).map(rel => resolve(root, rel));
        return { content: [{ type: "json", json: { root, files: filesAbs, raw: parsed } }] };
      }
      if (res.timeout) {
        return { content: [{ type: "text", text: `bundle-files timed out after ${TIMEOUT_MS}ms` }] };
      }
      if (res.parsed) {
        return { content: [{ type: "json", json: { ...res.parsed, strict_failed: true } }] };
      }
      return { content: [{ type: "text", text: "bundle-files ended unexpectedly." }] };
    }
  },
  {
    name: "bundle_generate",
    description: "Generate chunked Markdown bundle(s) for code review and return JSON + file links.",
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
        strict: { type: "boolean", default: false }
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
        strict = false
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
      if (parsed?.parts?.length) {
        for (const p of parsed.parts) {
          if (p?.path) {
            links.push({
              type: "resource_link",
              uri: "file://" + p.path,
              name: String(p.path).split("/").pop(),
              description: "Bundle part",
              mimeType: "text/markdown"
            });
          }
        }
      }
      if (index) {
        links.unshift({
          type: "resource_link",
          uri: "file://" + index,
          name: String(index).split("/").pop(),
          description: "Bundle index",
          mimeType: "application/json"
        });
      }
      const mp = parsed?.manifest_path || manifest;
      if (mp) {
        links.unshift({
          type: "resource_link",
          uri: "file://" + mp,
          name: String(mp).split("/").pop(),
          description: "Bundle manifest",
          mimeType: "application/json"
        });
      }
      if (parsed?.archive_path) {
        links.unshift({
          type: "resource_link",
          uri: "file://" + parsed.archive_path,
          name: String(parsed.archive_path).split("/").pop(),
          description: "Bundle archive",
          mimeType: "application/octet-stream"
        });
      }
      if (parsed?.files_archive_path) {
        links.unshift({
          type: "resource_link",
          uri: "file://" + parsed.files_archive_path,
          name: String(parsed.files_archive_path).split("/").pop(),
          description: "Files archive",
          mimeType: "application/octet-stream"
        });
      }

      if (res.ok) {
        if (!parsed) return { content: [{ type: "text", text: "bundle-files returned invalid JSON" }] };
        return { content: [{ type: "json", json: parsed }, ...links] };
      }
      if (res.timeout) {
        if (parsed) return { content: [{ type: "json", json: { ...parsed, timed_out: true } }, ...links] };
        return { content: [{ type: "text", text: `bundle-files timed out after ${TIMEOUT_MS}ms` }] };
      }
      if (parsed) {
        return { content: [{ type: "json", json: { ...parsed, strict_failed: true } }, ...links] };
      }
      return { content: [{ type: "text", text: "bundle-files ended unexpectedly." }] };
    }
  }
];

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
    return { isError: true, content: [{ type: "text", text: `Unknown tool '${req.params.name}'. Available: ${tools.map(x => x.name).join(", ")}` }] };
  }
  return withSlot(() => t.run(req.params.arguments || {}, req));
});

/* ───────────── Transport start ───────────── */
const transport = new StdioServerTransport();
await server.connect(transport);
try { console.error(JSON.stringify({ ev: "server_ready", tools: tools.map(t => t.name) })); } catch {}
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


====== BEGIN FILE: package-lock.json ======
```json
{
  "name": "shared-dev-tools",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "shared-dev-tools",
      "version": "1.0.0",
      "license": "ISC",
      "dependencies": {
        "@modelcontextprotocol/sdk": "^1.18.1"
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


====== BEGIN FILE: package.json ======
```json
{
  "name": "shared-dev-tools",
  "version": "1.0.0",
  "description": "Utilities and command-line helpers for preparing repository artifacts for large-language-model workflows. The flagship command, `bundle-files`, scans a project, filters files using Git metadata and heuristics, and emits a single Markdown document with language-aware code fences that can be shared with review tools or LLMs.",
  "main": "index.js",
  "directories": {
    "doc": "docs",
    "test": "tests"
  },
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/grahama1970/shared-dev-tools.git"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "bugs": {
    "url": "https://github.com/grahama1970/shared-dev-tools/issues"
  },
  "homepage": "https://github.com/grahama1970/shared-dev-tools#readme",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.18.1"
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


====== BEGIN FILE: scripts/run-bundle-mcp.sh ======
```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $(basename "$0") <node-path> <script-path> [args...]" >&2
  exit 2
fi

NODE_BIN=$1
SCRIPT=$2
shift 2

# Log to STDERR (never stdout)
printf '[bundle-wrapper] node=%s script=%s args=%s cwd=%s\n' \
  "$NODE_BIN" "$SCRIPT" "$*" "$(pwd)" >&2

exec "$NODE_BIN" --enable-source-maps --trace-warnings "$SCRIPT" "$@"
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

Examples (agent-friendly)
  # Standard run (respects .gitignore if in Git)
  bundle-files --root . --output bundle.md

  # Include extra file types or special filenames (globs on names)
  bundle-files --include-ext ".proto,Justfile,vite.config.ts"

  # Add extra explicit path excludes
  bundle-files --extra-exclude-paths "misc/big_fixture.json,notes/tmp.txt"

  # Force include .gitignored files (audits)
  bundle-files --include-ignored

  # Ignore .gitignore entirely (fallback walk only)
  bundle-files --no-respect-gitignore

  # Explicit file list (repeat --file) + persona preface, single concatenated output
  bundle-files --file a.py --file b.py --prefix-file scripts/review/persona.md \
               --single-file --output bundle.md

  # Large list from a file
  bundle-files --files-from scripts/review/files.txt --output bundle.md
"""

from __future__ import annotations

import fnmatch
import json
import math
import os
import io
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
    """Best-effort repo-relative path; falls back to absolute POSIX if outside root."""
    p = path.resolve()
    s = start.resolve()
    try:
        return p.relative_to(s).as_posix()
    except Exception:
        return p.as_posix()


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
        header_only = self._header_for_count(self.current_file_count)
        prefix = self.prefix_text if self.prefix_text else ""
        header_bytes = len(
            (header_only + prefix).encode(self.encoding, errors="replace")
        )
        header_tokens = self._tok(header_only + prefix)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header_only)
            if prefix:
                out_f.write(prefix)
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
        header_only = self._header_for_count(0)
        prefix = self.prefix_text if self.prefix_text else ""
        header_bytes = len(
            (header_only + prefix).encode(self.encoding, errors="replace")
        )
        header_tokens = self._tok(header_only + prefix)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header_only)
            if prefix:
                out_f.write(prefix)

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
        # Selection
        root: Path = typer.Option(Path("."), "--root", help="Project root to scan"),
        file: List[Path] = typer.Option(
            None,
            "--file",
            help="Explicit file to include (repeatable). When present, discovery is skipped.",
        ),
        files_from: Optional[Path] = typer.Option(
            None,
            "--files-from",
            help="Text file with one path per line (explicit selection).",
        ),
        output: Path = typer.Option(
            Path("bundle.md"),
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
        single_file: bool = typer.Option(
            False,
            "--single-file",
            help="Force a single concatenated Markdown file (disables token/byte splitting).",
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
        manifest: Optional[Path] = typer.Option(
            None,
            "--manifest",
            help="Optional path to write a manifest.json (inputs, parts, checksums, budgets)",
        ),
        archive: Optional[str] = typer.Option(
            None,
            "--archive",
            help="Package parts + index + manifest into an archive: 'zip' or 'tar'",
        ),
        archive_files: Optional[str] = typer.Option(
            None,
            "--archive-files",
            help="Package ORIGINAL selected files (preserving relative paths) plus BUNDLE_INSTRUCTIONS.md; also includes index/manifest if provided: 'zip' or 'tar'",
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

        # If explicit selection provided, use only that.
        explicit: List[Path] = []
        if file:
            explicit.extend(
                [p if p.is_absolute() else (root_resolved / p) for p in file]
            )
        if files_from and files_from.is_file():
            for line in _read_text(files_from).splitlines():
                s = line.strip()
                if s:
                    p = Path(s)
                    explicit.append(p if p.is_absolute() else (root_resolved / p))

        if explicit:
            files_all = [p.resolve() for p in explicit if p.exists()]
        else:
            files_all = discover_files(
                root=root_resolved,
                respect_gitignore=not no_respect_gitignore,
                include_ignored=include_ignored,
                extra_exclude_paths=extra_excludes,
            )

        # If changed_since provided and repo available, narrow to changed files
        if changed_since and _is_git_repo(root_resolved) and not explicit:
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

        # Limits: single-file disables token/byte splitting entirely
        token_limit = (
            None if single_file else (context_length if context_length > 0 else None)
        )
        effective_max_bytes = None if single_file else max_total_bytes
        tok = _make_token_estimator(token_estimator)

        results = write_bundles(
            root=root_resolved,
            files=selected,
            output=effective_output,
            encoding=encoding,
            max_total_bytes=(
                effective_max_bytes
                if effective_max_bytes is not None
                else max_total_bytes
            ),
            max_total_tokens=token_limit,
            token_estimator=tok,
            token_estimator_spec=token_estimator,
            cache_path=cache_path,
            prefix_text=prefix_text,
        )

        # Tool meta
        def _tool_meta() -> tuple[str, str]:
            tool_name = "bundle-files"
            tool_ver = "0.1.0"
            try:
                import tomllib  # py311+

                pyproj = root_resolved / "pyproject.toml"
                if pyproj.is_file():
                    data = tomllib.loads(pyproj.read_text(encoding="utf-8"))
                    tool_ver = data.get("project", {}).get("version", tool_ver)
            except Exception:
                pass
            return tool_name, tool_ver

        schema_version = "bundle_index_v1"
        tool_name, tool_version = _tool_meta()

        import hashlib
        import tarfile
        import zipfile

        manifest_path = None
        archive_path = None
        if manifest is not None:
            manifest.parent.mkdir(parents=True, exist_ok=True)
            parts_list = []
            for r in results:
                p = (
                    root_resolved / r.path
                    if not Path(r.path).is_absolute()
                    else Path(r.path)
                )
                try:
                    with open(p, "rb") as f:
                        h = hashlib.sha256()
                        for chunk in iter(lambda: f.read(8192), b""):
                            h.update(chunk)
                    sha256 = h.hexdigest()
                except Exception:
                    sha256 = ""
                parts_list.append(
                    {
                        "path": str(r.path),
                        "bytes": r.total_bytes,
                        "tokens": r.total_tokens,
                        "sha256": sha256,
                    }
                )
            manifest_payload = {
                "schema_version": "bundle_manifest_v1",
                "tool_name": tool_name,
                "tool_version": tool_version,
                "generated": _now_utc_iso(),
                "root": str(root_resolved),
                "base_output": str((root_resolved / effective_output).resolve()),
                "context_length": token_limit,
                "max_total_bytes": max_total_bytes,
                "selected_files": [_posix_rel_path(p, root_resolved) for p in selected],
                "parts": parts_list,
            }
            manifest.write_text(json.dumps(manifest_payload), encoding="utf-8")
            manifest_path = manifest

        if archive in {"zip", "tar"}:
            base = effective_output
            base_stem = base.with_suffix("") if base.suffix else base
            if archive == "zip":
                archive_path = base_stem.with_suffix(".zip")
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(
                    archive_path, "w", compression=zipfile.ZIP_DEFLATED
                ) as zf:
                    for r in results:
                        zf.write(r.path, arcname=Path(r.path).name)
                    if index is not None and index.exists():
                        zf.write(index, arcname=index.name)
                    if manifest_path is not None and manifest_path.exists():
                        zf.write(manifest_path, arcname=manifest_path.name)
            else:
                archive_path = base_stem.with_suffix(".tar")
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                with tarfile.open(archive_path, "w") as tf:
                    for r in results:
                        tf.add(r.path, arcname=Path(r.path).name)
                    if index is not None and index.exists():
                        tf.add(index, arcname=index.name)
                    if manifest_path is not None and manifest_path.exists():
                        tf.add(manifest_path, arcname=manifest_path.name)

        # Optional: package original selected files with directory structure + instructions
        files_archive_path = None
        if archive_files in {"zip", "tar"}:
            base = effective_output
            base_stem = base.with_suffix("") if base.suffix else base

            # Build a simple file list (repo-relative) for context
            rel_files = sorted(_posix_rel_path(p, root_resolved) for p in selected)
            file_list_section = "\n".join(f"- {rf}" for rf in rel_files)

            instruction_text = (
                "# Bundle Instructions\n\n"
                f"- Generated: {_now_utc_iso()}\n"
                f"- Root: {root_resolved}\n"
                f"- Files included: {len(selected)}\n"
                "- Structure: Original selected files under their repo-relative paths.\n"
                "- Sidecars: manifest.json (checksums), index.json (CLI JSON summary) if present.\n\n"
                "Directory structure (relative file list):\n"
                f"{file_list_section}\n\n"
                "Notes:\n"
                "- Use the Markdown bundle parts (*.md) alongside this archive for LLM ingestion.\n"
            )

            if archive_files == "zip":
                files_archive_path = base_stem.with_suffix(".files.zip")
                files_archive_path.parent.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(
                    files_archive_path, "w", compression=zipfile.ZIP_DEFLATED
                ) as zf:
                    # Instruction document
                    zf.writestr("BUNDLE_INSTRUCTIONS.md", instruction_text)
                    # Original files with relative paths
                    for p in selected:
                        rel = _posix_rel_path(p, root_resolved)
                        zf.write(p, arcname=rel)
                    # Include index/manifest sidecars if provided (index may be written after archiving)
                    if manifest_path is not None and manifest_path.exists():
                        zf.write(manifest_path, arcname=manifest_path.name)
                    if index is not None and index.exists():
                        zf.write(index, arcname=index.name)
            else:
                files_archive_path = base_stem.with_suffix(".files.tar")
                files_archive_path.parent.mkdir(parents=True, exist_ok=True)
                with tarfile.open(files_archive_path, "w") as tf2:
                    # Instruction document
                    ins_bytes = instruction_text.encode("utf-8")
                    ti = tarfile.TarInfo("BUNDLE_INSTRUCTIONS.md")
                    ti.size = len(ins_bytes)
                    tf2.addfile(ti, io.BytesIO(ins_bytes))
                    # Original files with relative paths
                    for p in selected:
                        rel = _posix_rel_path(p, root_resolved)
                        tf2.add(p, arcname=rel)
                    # Include index/manifest sidecars if provided (index may be written after archiving)
                    if manifest_path is not None and manifest_path.exists():
                        tf2.add(manifest_path, arcname=manifest_path.name)
                    if index is not None and index.exists():
                        tf2.add(index, arcname=index.name)

        # (keep the first “archive original files” block above; remove this duplicate)

        if json_output:
            reasons = []
            if any(r.exceeded_token_limit for r in results):
                reasons.append("tokens_over_limit")
            if any(r.exceeded_byte_limit for r in results):
                reasons.append("bytes_over_limit")
            if any(r.skipped_unreadable > 0 for r in results):
                reasons.append("skipped_unreadable")

            payload = {
                "schema_version": schema_version,
                "tool_name": tool_name,
                "tool_version": tool_version,
                "root": str(root_resolved),
                "base_output": str((root_resolved / effective_output).resolve()),
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
                "status": "strict_failed" if (strict and reasons) else "ok",
                "reasons": reasons,
            }
            if manifest_path is not None:
                payload["manifest_path"] = str(manifest_path)
            if archive_path is not None:
                payload["archive_path"] = str(archive_path)
            if "files_archive_path" in locals() and files_archive_path is not None:
                payload["files_archive_path"] = str(files_archive_path)
            text = json.dumps(payload)
            typer.echo(text)
            if index is not None:
                index.parent.mkdir(parents=True, exist_ok=True)
                index.write_text(text, encoding="utf-8")
            if strict and reasons:
                raise typer.Exit(1)
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

            # Enforce strict exit if any issues detected
            if strict and (
                any(r.exceeded_token_limit for r in results)
                or any(r.exceeded_byte_limit for r in results)
                or any(r.skipped_unreadable > 0 for r in results)
            ):
                raise typer.Exit(1)

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


====== BEGIN FILE: tests/smokes/test_cli_archive_files_smoke.py ======
```python
from __future__ import annotations
import zipfile
from pathlib import Path
from typer.testing import CliRunner
from shared_dev_tools.cli import app


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_archive_files_zip_preserves_structure_and_instructions(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    _write_text(root / "keep.py", "print('hi')\n")
    _write_text(root / "nested" / "notes.txt", "note\n")
    out_dir = root / "out"
    bundle_path = out_dir / "bundle.md"
    index_path = out_dir / "index.json"
    manifest_path = out_dir / "manifest.json"
    runner = CliRunner()
    res = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(bundle_path),
            "--index",
            str(index_path),
            "--manifest",
            str(manifest_path),
            "--archive-files",
            "zip",
            "--json",
        ],
    )
    assert res.exit_code == 0, res.stdout
    files_archive = bundle_path.with_suffix("").with_suffix(".files.zip")
    assert files_archive.exists()
    with zipfile.ZipFile(files_archive, "r") as zf:
        names = set(zf.namelist())
    assert "BUNDLE_INSTRUCTIONS.md" in names
    assert "keep.py" in names
    assert "nested/notes.txt" in names
    # Index may be written after archiving (same behavior as parts archive); manifest is written before and should be present
    assert manifest_path.name in names
    for n in names:
        assert not n.startswith("/")
        assert ".." not in n
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


====== BEGIN FILE: tests/smokes/test_cli_strict_and_archive_smokes.py ======
```python
"""Additional smokes for strict exit and archive arcnames.

These focus on happy-path behaviors and run quickly.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

from typer.testing import CliRunner

from shared_dev_tools.cli import app


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_strict_exits_nonzero_with_token_overflow_json(tmp_path: Path) -> None:
    """--strict + tiny context_length yields non-zero exit and strict_failed JSON."""

    root = tmp_path / "project"
    root.mkdir()

    # One small file is enough; the header alone will exceed very small token limit
    _write_text(root / "a.py", "print('ok')\n")

    bundle_path = root / "bundle.md"
    runner = CliRunner()

    res = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(bundle_path),
            "--context-length",
            "1",
            "--json",
            "--strict",
        ],
    )

    assert res.exit_code != 0, res.stdout
    payload = json.loads(res.stdout)
    assert payload.get("status") == "strict_failed"
    assert "tokens_over_limit" in set(payload.get("reasons", []))


def test_archive_contains_basenames_only(tmp_path: Path) -> None:
    """ZIP archive should contain only basenames for parts/index/manifest."""

    root = tmp_path / "project"
    root.mkdir()
    _write_text(root / "x.py", "print('x')\n")

    out_dir = root / "out"
    bundle_path = out_dir / "bundle.md"
    index_path = out_dir / "index.json"
    manifest_path = out_dir / "manifest.json"

    runner = CliRunner()
    res = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(bundle_path),
            "--index",
            str(index_path),
            "--manifest",
            str(manifest_path),
            "--archive",
            "zip",
            "--json",
        ],
    )
    assert res.exit_code == 0, res.stdout

    archive_file = bundle_path.with_suffix("") if bundle_path.suffix else bundle_path
    archive_file = archive_file.with_suffix(".zip")
    assert archive_file.exists()

    with zipfile.ZipFile(archive_file, "r") as zf:
        names = zf.namelist()

    # Ensure no entry contains path separators and expected basenames present
    assert names, names
    for n in names:
        assert "/" not in n, names
        assert not n.startswith("/"), names
    # Parts and manifest should be present; index may be written after archiving
    assert {"bundle.md", "manifest.json"}.issubset(set(names))
```

====== END FILE ======
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


====== BEGIN FILE: docs/MCP_USAGE.md ======
```markdown
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
    description: "Preview which files would be included in a code-review bundle.",
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
        if (!parsed) return { content: [{ type: "text", text: "bundle-files returned invalid JSON" }] };
        const filesAbs = (parsed.files || []).map(rel => resolve(root, rel));
        return { content: [{ type: "json", json: { root, files: filesAbs, raw: parsed } }] };
      }
      if (res.timeout) {
        return { content: [{ type: "text", text: `bundle-files timed out after ${TIMEOUT_MS}ms` }] };
      }
      if (res.parsed) {
        return { content: [{ type: "json", json: { ...res.parsed, strict_failed: true } }] };
      }
      return { content: [{ type: "text", text: "bundle-files ended unexpectedly." }] };
    }
  },
  {
    name: "bundle_generate",
    description: "Generate chunked Markdown bundle(s) for code review and return JSON + file links.",
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
        strict: { type: "boolean", default: false }
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
        strict = false
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
      if (parsed?.parts?.length) {
        for (const p of parsed.parts) {
          if (p?.path) {
            links.push({
              type: "resource_link",
              uri: "file://" + p.path,
              name: String(p.path).split("/").pop(),
              description: "Bundle part",
              mimeType: "text/markdown"
            });
          }
        }
      }
      if (index) {
        links.unshift({
          type: "resource_link",
          uri: "file://" + index,
          name: String(index).split("/").pop(),
          description: "Bundle index",
          mimeType: "application/json"
        });
      }
      const mp = parsed?.manifest_path || manifest;
      if (mp) {
        links.unshift({
          type: "resource_link",
          uri: "file://" + mp,
          name: String(mp).split("/").pop(),
          description: "Bundle manifest",
          mimeType: "application/json"
        });
      }
      if (parsed?.archive_path) {
        links.unshift({
          type: "resource_link",
          uri: "file://" + parsed.archive_path,
          name: String(parsed.archive_path).split("/").pop(),
          description: "Bundle archive",
          mimeType: "application/octet-stream"
        });
      }
      if (parsed?.files_archive_path) {
        links.unshift({
          type: "resource_link",
          uri: "file://" + parsed.files_archive_path,
          name: String(parsed.files_archive_path).split("/").pop(),
          description: "Files archive",
          mimeType: "application/octet-stream"
        });
      }

      if (res.ok) {
        if (!parsed) return { content: [{ type: "text", text: "bundle-files returned invalid JSON" }] };
        return { content: [{ type: "json", json: parsed }, ...links] };
      }
      if (res.timeout) {
        if (parsed) return { content: [{ type: "json", json: { ...parsed, timed_out: true } }, ...links] };
        return { content: [{ type: "text", text: `bundle-files timed out after ${TIMEOUT_MS}ms` }] };
      }
      if (parsed) {
        return { content: [{ type: "json", json: { ...parsed, strict_failed: true } }, ...links] };
      }
      return { content: [{ type: "text", text: "bundle-files ended unexpectedly." }] };
    }
  }
];

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
    return { isError: true, content: [{ type: "text", text: `Unknown tool '${req.params.name}'. Available: ${tools.map(x => x.name).join(", ")}` }] };
  }
  return withSlot(() => t.run(req.params.arguments || {}, req));
});

/* ───────────── Transport start ───────────── */
const transport = new StdioServerTransport();
await server.connect(transport);
try { console.error(JSON.stringify({ ev: "server_ready", tools: tools.map(t => t.name) })); } catch {}
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


====== BEGIN FILE: package-lock.json ======
```json
{
  "name": "shared-dev-tools",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "shared-dev-tools",
      "version": "1.0.0",
      "license": "ISC",
      "dependencies": {
        "@modelcontextprotocol/sdk": "^1.18.1"
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


====== BEGIN FILE: package.json ======
```json
{
  "name": "shared-dev-tools",
  "version": "1.0.0",
  "description": "Utilities and command-line helpers for preparing repository artifacts for large-language-model workflows. The flagship command, `bundle-files`, scans a project, filters files using Git metadata and heuristics, and emits a single Markdown document with language-aware code fences that can be shared with review tools or LLMs.",
  "main": "index.js",
  "directories": {
    "doc": "docs",
    "test": "tests"
  },
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/grahama1970/shared-dev-tools.git"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "bugs": {
    "url": "https://github.com/grahama1970/shared-dev-tools/issues"
  },
  "homepage": "https://github.com/grahama1970/shared-dev-tools#readme",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.18.1"
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


====== BEGIN FILE: scripts/run-bundle-mcp.sh ======
```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $(basename "$0") <node-path> <script-path> [args...]" >&2
  exit 2
fi

NODE_BIN=$1
SCRIPT=$2
shift 2

# Log to STDERR (never stdout)
printf '[bundle-wrapper] node=%s script=%s args=%s cwd=%s\n' \
  "$NODE_BIN" "$SCRIPT" "$*" "$(pwd)" >&2

exec "$NODE_BIN" --enable-source-maps --trace-warnings "$SCRIPT" "$@"
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

Examples (agent-friendly)
  # Standard run (respects .gitignore if in Git)
  bundle-files --root . --output bundle.md

  # Include extra file types or special filenames (globs on names)
  bundle-files --include-ext ".proto,Justfile,vite.config.ts"

  # Add extra explicit path excludes
  bundle-files --extra-exclude-paths "misc/big_fixture.json,notes/tmp.txt"

  # Force include .gitignored files (audits)
  bundle-files --include-ignored

  # Ignore .gitignore entirely (fallback walk only)
  bundle-files --no-respect-gitignore

  # Explicit file list (repeat --file) + persona preface, single concatenated output
  bundle-files --file a.py --file b.py --prefix-file scripts/review/persona.md \
               --single-file --output bundle.md

  # Large list from a file
  bundle-files --files-from scripts/review/files.txt --output bundle.md
"""

from __future__ import annotations

import fnmatch
import json
import math
import os
import io
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
    """Best-effort repo-relative path; falls back to absolute POSIX if outside root."""
    p = path.resolve()
    s = start.resolve()
    try:
        return p.relative_to(s).as_posix()
    except Exception:
        return p.as_posix()


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
        header_only = self._header_for_count(self.current_file_count)
        prefix = self.prefix_text if self.prefix_text else ""
        header_bytes = len(
            (header_only + prefix).encode(self.encoding, errors="replace")
        )
        header_tokens = self._tok(header_only + prefix)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header_only)
            if prefix:
                out_f.write(prefix)
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
        header_only = self._header_for_count(0)
        prefix = self.prefix_text if self.prefix_text else ""
        header_bytes = len(
            (header_only + prefix).encode(self.encoding, errors="replace")
        )
        header_tokens = self._tok(header_only + prefix)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header_only)
            if prefix:
                out_f.write(prefix)

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
        # Selection
        root: Path = typer.Option(Path("."), "--root", help="Project root to scan"),
        file: List[Path] = typer.Option(
            None,
            "--file",
            help="Explicit file to include (repeatable). When present, discovery is skipped.",
        ),
        files_from: Optional[Path] = typer.Option(
            None,
            "--files-from",
            help="Text file with one path per line (explicit selection).",
        ),
        output: Path = typer.Option(
            Path("bundle.md"),
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
        single_file: bool = typer.Option(
            False,
            "--single-file",
            help="Force a single concatenated Markdown file (disables token/byte splitting).",
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
        manifest: Optional[Path] = typer.Option(
            None,
            "--manifest",
            help="Optional path to write a manifest.json (inputs, parts, checksums, budgets)",
        ),
        archive: Optional[str] = typer.Option(
            None,
            "--archive",
            help="Package parts + index + manifest into an archive: 'zip' or 'tar'",
        ),
        archive_files: Optional[str] = typer.Option(
            None,
            "--archive-files",
            help="Package ORIGINAL selected files (preserving relative paths) plus BUNDLE_INSTRUCTIONS.md; also includes index/manifest if provided: 'zip' or 'tar'",
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

        # If explicit selection provided, use only that.
        explicit: List[Path] = []
        if file:
            explicit.extend(
                [p if p.is_absolute() else (root_resolved / p) for p in file]
            )
        if files_from and files_from.is_file():
            for line in _read_text(files_from).splitlines():
                s = line.strip()
                if s:
                    p = Path(s)
                    explicit.append(p if p.is_absolute() else (root_resolved / p))

        if explicit:
            files_all = [p.resolve() for p in explicit if p.exists()]
        else:
            files_all = discover_files(
                root=root_resolved,
                respect_gitignore=not no_respect_gitignore,
                include_ignored=include_ignored,
                extra_exclude_paths=extra_excludes,
            )

        # If changed_since provided and repo available, narrow to changed files
        if changed_since and _is_git_repo(root_resolved) and not explicit:
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

        # Limits: single-file disables token/byte splitting entirely
        token_limit = (
            None if single_file else (context_length if context_length > 0 else None)
        )
        effective_max_bytes = None if single_file else max_total_bytes
        tok = _make_token_estimator(token_estimator)

        results = write_bundles(
            root=root_resolved,
            files=selected,
            output=effective_output,
            encoding=encoding,
            max_total_bytes=(
                effective_max_bytes
                if effective_max_bytes is not None
                else max_total_bytes
            ),
            max_total_tokens=token_limit,
            token_estimator=tok,
            token_estimator_spec=token_estimator,
            cache_path=cache_path,
            prefix_text=prefix_text,
        )

        # Tool meta
        def _tool_meta() -> tuple[str, str]:
            tool_name = "bundle-files"
            tool_ver = "0.1.0"
            try:
                import tomllib  # py311+

                pyproj = root_resolved / "pyproject.toml"
                if pyproj.is_file():
                    data = tomllib.loads(pyproj.read_text(encoding="utf-8"))
                    tool_ver = data.get("project", {}).get("version", tool_ver)
            except Exception:
                pass
            return tool_name, tool_ver

        schema_version = "bundle_index_v1"
        tool_name, tool_version = _tool_meta()

        import hashlib
        import tarfile
        import zipfile

        manifest_path = None
        archive_path = None
        if manifest is not None:
            manifest.parent.mkdir(parents=True, exist_ok=True)
            parts_list = []
            for r in results:
                p = (
                    root_resolved / r.path
                    if not Path(r.path).is_absolute()
                    else Path(r.path)
                )
                try:
                    with open(p, "rb") as f:
                        h = hashlib.sha256()
                        for chunk in iter(lambda: f.read(8192), b""):
                            h.update(chunk)
                    sha256 = h.hexdigest()
                except Exception:
                    sha256 = ""
                parts_list.append(
                    {
                        "path": str(r.path),
                        "bytes": r.total_bytes,
                        "tokens": r.total_tokens,
                        "sha256": sha256,
                    }
                )
            manifest_payload = {
                "schema_version": "bundle_manifest_v1",
                "tool_name": tool_name,
                "tool_version": tool_version,
                "generated": _now_utc_iso(),
                "root": str(root_resolved),
                "base_output": str((root_resolved / effective_output).resolve()),
                "context_length": token_limit,
                "max_total_bytes": max_total_bytes,
                "selected_files": [_posix_rel_path(p, root_resolved) for p in selected],
                "parts": parts_list,
            }
            manifest.write_text(json.dumps(manifest_payload), encoding="utf-8")
            manifest_path = manifest

        if archive in {"zip", "tar"}:
            base = effective_output
            base_stem = base.with_suffix("") if base.suffix else base
            if archive == "zip":
                archive_path = base_stem.with_suffix(".zip")
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(
                    archive_path, "w", compression=zipfile.ZIP_DEFLATED
                ) as zf:
                    for r in results:
                        zf.write(r.path, arcname=Path(r.path).name)
                    if index is not None and index.exists():
                        zf.write(index, arcname=index.name)
                    if manifest_path is not None and manifest_path.exists():
                        zf.write(manifest_path, arcname=manifest_path.name)
            else:
                archive_path = base_stem.with_suffix(".tar")
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                with tarfile.open(archive_path, "w") as tf:
                    for r in results:
                        tf.add(r.path, arcname=Path(r.path).name)
                    if index is not None and index.exists():
                        tf.add(index, arcname=index.name)
                    if manifest_path is not None and manifest_path.exists():
                        tf.add(manifest_path, arcname=manifest_path.name)

        # Optional: package original selected files with directory structure + instructions
        files_archive_path = None
        if archive_files in {"zip", "tar"}:
            base = effective_output
            base_stem = base.with_suffix("") if base.suffix else base

            # Build a simple file list (repo-relative) for context
            rel_files = sorted(_posix_rel_path(p, root_resolved) for p in selected)
            file_list_section = "\n".join(f"- {rf}" for rf in rel_files)

            instruction_text = (
                "# Bundle Instructions\n\n"
                f"- Generated: {_now_utc_iso()}\n"
                f"- Root: {root_resolved}\n"
                f"- Files included: {len(selected)}\n"
                "- Structure: Original selected files under their repo-relative paths.\n"
                "- Sidecars: manifest.json (checksums), index.json (CLI JSON summary) if present.\n\n"
                "Directory structure (relative file list):\n"
                f"{file_list_section}\n\n"
                "Notes:\n"
                "- Use the Markdown bundle parts (*.md) alongside this archive for LLM ingestion.\n"
            )

            if archive_files == "zip":
                files_archive_path = base_stem.with_suffix(".files.zip")
                files_archive_path.parent.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(
                    files_archive_path, "w", compression=zipfile.ZIP_DEFLATED
                ) as zf:
                    # Instruction document
                    zf.writestr("BUNDLE_INSTRUCTIONS.md", instruction_text)
                    # Original files with relative paths
                    for p in selected:
                        rel = _posix_rel_path(p, root_resolved)
                        zf.write(p, arcname=rel)
                    # Include index/manifest sidecars if provided (index may be written after archiving)
                    if manifest_path is not None and manifest_path.exists():
                        zf.write(manifest_path, arcname=manifest_path.name)
                    if index is not None and index.exists():
                        zf.write(index, arcname=index.name)
            else:
                files_archive_path = base_stem.with_suffix(".files.tar")
                files_archive_path.parent.mkdir(parents=True, exist_ok=True)
                with tarfile.open(files_archive_path, "w") as tf2:
                    # Instruction document
                    ins_bytes = instruction_text.encode("utf-8")
                    ti = tarfile.TarInfo("BUNDLE_INSTRUCTIONS.md")
                    ti.size = len(ins_bytes)
                    tf2.addfile(ti, io.BytesIO(ins_bytes))
                    # Original files with relative paths
                    for p in selected:
                        rel = _posix_rel_path(p, root_resolved)
                        tf2.add(p, arcname=rel)
                    # Include index/manifest sidecars if provided (index may be written after archiving)
                    if manifest_path is not None and manifest_path.exists():
                        tf2.add(manifest_path, arcname=manifest_path.name)
                    if index is not None and index.exists():
                        tf2.add(index, arcname=index.name)

        # (keep the first “archive original files” block above; remove this duplicate)

        if json_output:
            reasons = []
            if any(r.exceeded_token_limit for r in results):
                reasons.append("tokens_over_limit")
            if any(r.exceeded_byte_limit for r in results):
                reasons.append("bytes_over_limit")
            if any(r.skipped_unreadable > 0 for r in results):
                reasons.append("skipped_unreadable")

            payload = {
                "schema_version": schema_version,
                "tool_name": tool_name,
                "tool_version": tool_version,
                "root": str(root_resolved),
                "base_output": str((root_resolved / effective_output).resolve()),
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
                "status": "strict_failed" if (strict and reasons) else "ok",
                "reasons": reasons,
            }
            if manifest_path is not None:
                payload["manifest_path"] = str(manifest_path)
            if archive_path is not None:
                payload["archive_path"] = str(archive_path)
            if "files_archive_path" in locals() and files_archive_path is not None:
                payload["files_archive_path"] = str(files_archive_path)
            text = json.dumps(payload)
            typer.echo(text)
            if index is not None:
                index.parent.mkdir(parents=True, exist_ok=True)
                index.write_text(text, encoding="utf-8")
            if strict and reasons:
                raise typer.Exit(1)
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

            # Enforce strict exit if any issues detected
            if strict and (
                any(r.exceeded_token_limit for r in results)
                or any(r.exceeded_byte_limit for r in results)
                or any(r.skipped_unreadable > 0 for r in results)
            ):
                raise typer.Exit(1)

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


====== BEGIN FILE: tests/smokes/test_cli_archive_files_smoke.py ======
```python
from __future__ import annotations
import zipfile
from pathlib import Path
from typer.testing import CliRunner
from shared_dev_tools.cli import app


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_archive_files_zip_preserves_structure_and_instructions(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    _write_text(root / "keep.py", "print('hi')\n")
    _write_text(root / "nested" / "notes.txt", "note\n")
    out_dir = root / "out"
    bundle_path = out_dir / "bundle.md"
    index_path = out_dir / "index.json"
    manifest_path = out_dir / "manifest.json"
    runner = CliRunner()
    res = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(bundle_path),
            "--index",
            str(index_path),
            "--manifest",
            str(manifest_path),
            "--archive-files",
            "zip",
            "--json",
        ],
    )
    assert res.exit_code == 0, res.stdout
    files_archive = bundle_path.with_suffix("").with_suffix(".files.zip")
    assert files_archive.exists()
    with zipfile.ZipFile(files_archive, "r") as zf:
        names = set(zf.namelist())
    assert "BUNDLE_INSTRUCTIONS.md" in names
    assert "keep.py" in names
    assert "nested/notes.txt" in names
    # Index may be written after archiving (same behavior as parts archive); manifest is written before and should be present
    assert manifest_path.name in names
    for n in names:
        assert not n.startswith("/")
        assert ".." not in n
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


====== BEGIN FILE: tests/smokes/test_cli_strict_and_archive_smokes.py ======
```python
"""Additional smokes for strict exit and archive arcnames.

These focus on happy-path behaviors and run quickly.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

from typer.testing import CliRunner

from shared_dev_tools.cli import app


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_strict_exits_nonzero_with_token_overflow_json(tmp_path: Path) -> None:
    """--strict + tiny context_length yields non-zero exit and strict_failed JSON."""

    root = tmp_path / "project"
    root.mkdir()

    # One small file is enough; the header alone will exceed very small token limit
    _write_text(root / "a.py", "print('ok')\n")

    bundle_path = root / "bundle.md"
    runner = CliRunner()

    res = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(bundle_path),
            "--context-length",
            "1",
            "--json",
            "--strict",
        ],
    )

    assert res.exit_code != 0, res.stdout
    payload = json.loads(res.stdout)
    assert payload.get("status") == "strict_failed"
    assert "tokens_over_limit" in set(payload.get("reasons", []))


def test_archive_contains_basenames_only(tmp_path: Path) -> None:
    """ZIP archive should contain only basenames for parts/index/manifest."""

    root = tmp_path / "project"
    root.mkdir()
    _write_text(root / "x.py", "print('x')\n")

    out_dir = root / "out"
    bundle_path = out_dir / "bundle.md"
    index_path = out_dir / "index.json"
    manifest_path = out_dir / "manifest.json"

    runner = CliRunner()
    res = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(bundle_path),
            "--index",
            str(index_path),
            "--manifest",
            str(manifest_path),
            "--archive",
            "zip",
            "--json",
        ],
    )
    assert res.exit_code == 0, res.stdout

    archive_file = bundle_path.with_suffix("") if bundle_path.suffix else bundle_path
    archive_file = archive_file.with_suffix(".zip")
    assert archive_file.exists()

    with zipfile.ZipFile(archive_file, "r") as zf:
        names = zf.namelist()

    # Ensure no entry contains path separators and expected basenames present
    assert names, names
    for n in names:
        assert "/" not in n, names
        assert not n.startswith("/"), names
    # Parts and manifest should be present; index may be written after archiving
    assert {"bundle.md", "manifest.json"}.issubset(set(names))
```

====== END FILE ======

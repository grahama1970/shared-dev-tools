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

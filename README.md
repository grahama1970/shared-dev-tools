# shared-dev-tools

Utilities and CLIs shared across projects for preparing artifacts for large-language-model workflows.

## Features
- `bundle-files` CLI bundles selected files into a single Markdown document with code fences.
- Respects `.gitignore` automatically when run inside a git repository, with fallbacks for non-git trees.
- Skips binary assets, enforces size guards, and supports custom include/exclude patterns.

## Quick Start
```bash
uv pip install --editable .
# or install globally
uv tool install shared-dev-tools

bundle-files --root . --output scripts/artifacts/bundle.txt
```

### CLI Options
Run `bundle-files --help` for the full flag list. Common examples:
- Include additional file types: `bundle-files --include-ext ".proto,Justfile"`
- Exclude custom paths: `bundle-files --extra-exclude-paths "docs/tmp/**"`
- Inspect selection without writing: `bundle-files --list`

## Development
- Python 3.10+
- Dependencies managed with [uv](https://github.com/astral-sh/uv)

```bash
uv pip install --editable .[dev]
uv run bundle-files --root path/to/repo --output bundle.txt
```

## License
MIT

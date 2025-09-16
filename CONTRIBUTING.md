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

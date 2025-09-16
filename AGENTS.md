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

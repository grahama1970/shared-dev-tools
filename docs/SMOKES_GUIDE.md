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

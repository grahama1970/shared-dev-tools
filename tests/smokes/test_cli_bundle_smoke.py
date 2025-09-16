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

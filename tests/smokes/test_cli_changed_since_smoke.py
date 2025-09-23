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

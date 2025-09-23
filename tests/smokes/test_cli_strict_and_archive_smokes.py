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

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

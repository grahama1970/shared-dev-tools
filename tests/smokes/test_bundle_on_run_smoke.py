import json
import os
import subprocess
from pathlib import Path


def test_bundle_created_on_run_repo_root(tmp_path: Path) -> None:
    """
    Spec-driven smoke: run the gamified CLI against the repo root and
    assert that a bundle is produced under workspace/runs/<run_id>/bundle.

    We pass a spec that enables bundling and includes a ubiquitous file (README.md)
    to ensure content exists without mutating the repo.
    """
    repo_root = Path.cwd()
    assert (repo_root / "README.md").exists(), "Expected README.md in repo root"

    # Create a temp spec file pointing includes at README.md (by basename)
    spec = {
        "version": 1,
        "approaches": [{"name": "demo"}],
        "runner": {"type": "noop"},
        "observability": {
            "backend": "arango",
            "dashboard": True,
            "bundle": {
                "enabled": True,
                "mode": "markdown",
                "include": ["README.md"],
                "exclude": ["**/__pycache__/**", "**/*.pyc", "**/.DS_Store"],
            },
        },
    }
    spec_path = tmp_path / "gamified.spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")

    # Run the CLI from the repo root so discovery uses the repository tree
    env = os.environ.copy()
    cmd = f"python -m prototypes.gamified.cli run --spec {spec_path.as_posix()}"
    proc = subprocess.run(
        cmd, shell=True, cwd=str(repo_root), env=env, capture_output=True, text=True
    )
    assert proc.returncode == 0, f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"

    # Validate the bundle directory and that at least one .md bundle exists
    bundle_dirs = sorted((repo_root / "workspace" / "runs").glob("*/bundle"))
    assert bundle_dirs, "No bundle directory found under workspace/runs/*/bundle"
    found_md = any(any(p.suffix == ".md" for p in d.glob("*.md")) for d in bundle_dirs)
    assert found_md, "No markdown bundle file found under bundle/"
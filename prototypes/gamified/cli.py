from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import typer


def _load_spec(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Spec not found: {path}")
    text = path.read_text(encoding="utf-8")
    # Try JSON first; optionally YAML if available.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise RuntimeError("Spec is not valid JSON and PyYAML is not available") from e
        return yaml.safe_load(text)


def _call_bundle_cli(root: Path, output_path: Path) -> int:
    """
    Invoke the existing shared_dev_tools CLI via module execution with JSON output.
    Ensures src/ is on PYTHONPATH so `python -m shared_dev_tools.cli` imports cleanly.
    """
    env = os.environ.copy()
    src_path = root / "src"
    env["PYTHONPATH"] = (
        (str(src_path) + os.pathsep + env["PYTHONPATH"]) if "PYTHONPATH" in env else str(src_path)
    )

    cmd = [
        sys.executable,
        "-m",
        "shared_dev_tools.cli",
        "--root",
        str(root),
        "--output",
        str(output_path),
        "--json",
    ]

    import subprocess

    proc = subprocess.run(cmd, cwd=str(root), env=env, capture_output=True, text=True)
    # Best-effort diagnostic on failure
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout or "")
        sys.stderr.write(proc.stderr or "")
        return proc.returncode

    # Validate JSON payload shape minimally (non-fatal if it prints)
    try:
        payload = json.loads(proc.stdout or "{}")
        # Optionally print a concise status line
        base = payload.get("base_output")
        parts = payload.get("parts")
        if base and isinstance(parts, list) and parts:
            typer.echo(f"[bundle] ok → {base} parts={len(parts)}")
    except Exception:
        # Ignore parse error; not required for smoke
        pass

    return 0


def cli(
    spec: Path = typer.Option(..., "--spec", help="Path to JSON or YAML spec file"),
) -> None:
    """
    Paved-road execution (minimal for smoke):
    - Load spec (JSON/YAML)
    - Create workspace/runs/<run_id>/bundle
    - Invoke shared_dev_tools CLI to produce a Markdown bundle there
    """
    repo_root = Path.cwd()

    # Load spec to honor bundle.enabled if present (softly)
    try:
        data = _load_spec(spec)
    except Exception as e:
        typer.secho(f"Failed to load spec: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=2)

    bundle_cfg: Dict[str, Any] = (data.get("observability") or {}).get("bundle") or {}
    enabled = bool(bundle_cfg.get("enabled", True))
    if not enabled:
        typer.echo("[bundle] skip → disabled by spec")
        raise typer.Exit(code=0)

    # Compute run directory
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    run_dir = repo_root / "workspace" / "runs" / run_id
    bundle_dir = run_dir / "bundle"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Always write a primary bundle.md; shared_dev_tools may split into parts if limits are set
    out_md = bundle_dir / "bundle.md"

    rc = _call_bundle_cli(root=repo_root, output_path=out_md)
    if rc != 0:
        raise typer.Exit(code=rc)


def main() -> None:
    # Compatibility shim: accept an optional "run" subcommand token.
    # This allows both:
    #   python -m prototypes.gamified.cli --spec file.json
    #   python -m prototypes.gamified.cli run --spec file.json
    argv = sys.argv[1:]
    if argv and argv[0] == "run":
        sys.argv = [sys.argv[0]] + argv[1:]
    typer.run(cli)


if __name__ == "__main__":
    main()
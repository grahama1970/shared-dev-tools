from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def _ensure_dir(p: str | Path) -> Path:
    path = Path(p)
    path.mkdir(parents=True, exist_ok=True)
    return path


def call_bundle_tool(
    *,
    run_id: str,
    include: List[str],
    exclude: List[str],
    mode: str = "markdown",
    out_dir: str | Path = "workspace/runs",
    python_bin: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Invoke the existing Python CLI (shared_dev_tools.cli) to build a bundle.

    Notes:
    - This is a pragmatic invoker that uses the already-available CLI.
    - It honors include/exclude via the CLI's include-ext and extra-exclude-paths.
    - It writes JSON to stdout and returns that parsed payload with an "ok" field.
    - Treats errors as soft-fail; callers should not crash on failure.

    MCP note:
    - The roadmap is to replace this subprocess CLI call with an MCP stdio client
      that calls the bundle-files-mcp tool (ListTools → CallTool). Until that thin
      client is landed, this function maintains the "tool boundary" behavior.
    """
    out_base = Path(out_dir) / run_id / "bundle"
    _ensure_dir(out_base)

    # For markdown mode, we still emit a .md base (archives optional)
    # (zip/tar modes could map to --archive later if desired)
    base_output = out_base / "bundle.md"

    py = python_bin or os.environ.get("PYTHON", sys.executable or "python3")
    base_root = Path(__file__).resolve().parents[2]
    cli_path = (base_root / "src" / "shared_dev_tools" / "cli.py").resolve()
    if not cli_path.exists():
        return {
            "ok": False,
            "error": "cli_not_found",
            "message": f"Expected CLI at {cli_path.as_posix()} not found",
            "out_dir": str(out_base),
        }

    cmd: List[str] = [
        py,
        cli_path.as_posix(),
        "--root",
        str(Path.cwd()),
        "--output",
        str(base_output),
        "--json",
        "--index",
        str(out_base / "index.json"),
        "--manifest",
        str(out_base / "manifest.json"),
    ]

    # Map include/exclude into CLI knobs:
    # - include-ext accepts filename/path globs; the CLI's matcher supports both basename and path globs
    if include:
        cmd += ["--include-ext", ",".join(include)]
    if exclude:
        cmd += ["--extra-exclude-paths", ",".join(exclude)]

    try:
        proc = subprocess.run(
            cmd, text=True, capture_output=True, check=False, cwd=str(Path.cwd())
        )
    except FileNotFoundError as e:
        return {
            "ok": False,
            "error": "python_not_found",
            "message": str(e),
            "out_dir": str(out_base),
        }

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()

    try:
        payload = json.loads(stdout) if stdout else {}
    except Exception:
        payload = {
            "ok": False,
            "error": "non_json_output",
            "stdout_preview": stdout[:2000],
            "stderr_preview": stderr[:2000],
            "exit_code": proc.returncode,
        }

    if isinstance(payload, dict) and "ok" not in payload:
        payload["ok"] = proc.returncode == 0

    payload.setdefault("out_dir", str(out_base))
    return payload


def report_bundle_result(res: Dict[str, Any], run_id: str) -> None:
    out = Path(res.get("out_dir", f"workspace/runs/{run_id}/bundle"))
    if res.get("ok"):
        print(f"[bundle] ok  → {out}")
    else:
        reason = res.get("error") or "unknown"
        msg = res.get("message") or res.get("stderr_preview") or ""
        print(f"[bundle] skip → {reason}{' — ' + msg if msg else ''}")

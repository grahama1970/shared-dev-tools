Developer: # ⏳ Pre-flight (Before Applying Diff)

* Ensure you are on the **latest branch/tag** designated for this refactor.
  For mainline:

  ```bash
  git fetch origin
  git checkout main
  git pull --rebase
  ```

  Or, for a feature branch:

  ```bash
  git checkout -b feature/spec-driven-bundle origin/main
  ```
* Confirm `git status` shows a **clean working tree** (no local modifications).
* Only then apply the unified diff below.

---

# 📑 Context for the Refactor (Guide the Agent)

## Why we’re changing this (motivation)

* Our **Happy Path Guide** mandates: *one spec, one command, one dashboard*, with **minimal CLI surface** and **progressive disclosure**.
* The current “bundle files” behavior is coupled to `cli.py` (flags/inline logic). That:

  * Increases option sprawl and violates Happy Path simplicity.
  * Makes behavior harder to test/replay (not spec-driven).
  * Prevents reuse by other agents (no tool boundary).
* We’re moving bundling to a **tool (MCP)** and letting the **spec** decide when/how it runs. The CLI just orchestrates.

## What we’re changing (scope)

* Add **spec fields**: `observability.bundle` with `enabled`, `mode`, `include`, `exclude`.
* Create a small **tool invoker** (`prototypes/gamified/tools.py`) that calls our existing **`bundle-files-mcp`** (stdio).
* Update **`prototypes/gamified/cli.py`** to:

  * Remove any bundling flags/inline logic.
  * Call the tool **only** when `spec.observability.bundle.enabled=True`.
  * Treat tool failure as **soft-fail** (do not fail the whole run).
* Add a minimal **smoke test** ensuring a bundle is created during `run`.

## What we’re **not** changing (non-goals)

* No new CLI verbs or flags (keep only `init`, `run`, `open`, `replay`).
* No new backends (still **Arango-only**).
* No dashboard changes (just print bundle paths like other artifacts).
* No graph authoring or alternative storage.

## Acceptance criteria

1. **Spec-driven**: `run` consults `spec.observability.bundle.enabled`. Defaults to **enabled**.
2. **MCP boundary**: Bundling executed via MCP with args (`include`, `exclude`, `mode`, `out_dir`).
3. **Progressive disclosure**: If MCP not found or returns non-JSON → **log and continue** (no crash).
4. **Artifacts**: Files land under `workspace/runs/<run_id>/bundle/…`.
5. **Smokes**: Verify bundle exists when enabled; absent when disabled.
6. **Backwards compatibility**: Specs without `observability` still run with defaults.

## Interfaces touched

* **Spec model**: `prototypes/gamified/spec_model.py`
* **CLI**: `prototypes/gamified/cli.py`
* **Tool invoker**: `prototypes/gamified/tools.py`
* **Smokes**: `tests/smoke/test_bundle_on_run_smoke.py`

## Data flow

**Before:** `cli run` → inline bundle logic/flags → ad-hoc artifacts.
**After:** `cli run` → read spec → (if enabled) call **MCP** → bundle to `workspace/runs/<run_id>/bundle`.

## Guardrails

* No new CLI flags.
* Soft-fail on tool errors.
* No writes outside `workspace/runs/<run_id>/bundle`.
* Respect `exclude` globs.

## Defaults

```yaml
observability:
  backend: arango
  dashboard: true
  bundle:
    enabled: true
    mode: markdown
    include: ["**/*.md", "src/**", "prototypes/**", "local/docs/**"]
    exclude: ["**/__pycache__/**", "**/*.pyc", "**/.DS_Store"]
```

---

# 🔀 Unified Diff

```diff
diff --git a/prototypes/gamified/spec_model.py b/prototypes/gamified/spec_model.py
index 1111111..2222222 100644
--- a/prototypes/gamified/spec_model.py
+++ b/prototypes/gamified/spec_model.py
@@ -1,8 +1,67 @@
-from pydantic import BaseModel
-from typing import List, Optional
+from pydantic import BaseModel, Field
+from typing import List, Optional, Literal
+
+"""
+Spec models — paved-road only (Happy Path).
+
+This refactor adds:
+  - BundleConfig   → controls file bundling as a spec option (no CLI flags)
+  - Observability  → owns bundle + dashboard toggles
+Defaults are conservative and “just work” for MVP.
+"""
 
-class Spec(BaseModel):
-    approaches: List[str]
-    runner: str
+class BundleConfig(BaseModel):
+    enabled: bool = True
+    mode: Literal["markdown", "zip", "tar"] = "markdown"
+    include: List[str] = Field(
+        default_factory=lambda: ["**/*.md", "src/**", "prototypes/**", "local/docs/**"]
+    )
+    exclude: List[str] = Field(
+        default_factory=lambda: ["**/__pycache__/**", "**/*.pyc", "**/.DS_Store"]
+    )
+
+
+class ObservabilityConfig(BaseModel):
+    backend: Literal["arango"] = "arango"
+    dashboard: bool = True
+    bundle: BundleConfig = BundleConfig()
+
+
+class Spec(BaseModel):
+    version: int = 1
+    approaches: List[dict]
+    runner: dict
+    scoring: Optional[dict] = None
+    constraints: Optional[dict] = None
+    optimizer: Optional[dict] = None
+    execution: Optional[dict] = None
+    observability: ObservabilityConfig = ObservabilityConfig()
+
diff --git a/prototypes/gamified/tools.py b/prototypes/gamified/tools.py
new file mode 100644
index 0000000..3333333
--- /dev/null
+++ b/prototypes/gamified/tools.py
@@ -0,0 +1,124 @@
+#!/usr/bin/env python3
+import json, os, subprocess
+from pathlib import Path
+from typing import Any, Dict, List
+
+def _ensure_dir(p: str | Path) -> Path:
+    path = Path(p)
+    path.mkdir(parents=True, exist_ok=True)
+    return path
+
+def call_bundle_tool(
+    *, run_id: str, include: List[str], exclude: List[str],
+    mode: str = "markdown", out_dir: str | Path = "workspace/runs",
+    mcp_entry: List[str] | None = None,
+) -> Dict[str, Any]:
+    out_base = Path(out_dir) / run_id / "bundle"
+    _ensure_dir(out_base)
+    args = {"include": include, "exclude": exclude, "mode": mode,
+            "out_dir": str(out_base), "run_id": run_id}
+    if mcp_entry is None:
+        mcp_entry = ["node", "mcp/bundle-files-mcp/index.mjs"]
+    env = os.environ.copy()
+    try:
+        proc = subprocess.run(
+            mcp_entry, input=json.dumps({"tool": "bundle_files","arguments": args}),
+            text=True, capture_output=True, check=False
+        )
+    except FileNotFoundError as e:
+        return {"ok": False,"error": "mcp_not_found",
+                "message": f"Bundle MCP entry not found: {mcp_entry}","exception": str(e)}
+    stdout, stderr = (proc.stdout or "").strip(), (proc.stderr or "").strip()
+    try:
+        payload = json.loads(stdout) if stdout else {}
+    except Exception:
+        payload = {"ok": False,"error": "non_json_output",
+                   "stdout_preview": stdout[:2000],"stderr_preview": stderr[:2000],
+                   "exit_code": proc.returncode}
+    if isinstance(payload, dict) and "ok" not in payload:
+        payload["ok"] = proc.returncode == 0
+    payload.setdefault("out_dir", str(out_base))
+    return payload
+
+def report_bundle_result(res: Dict[str, Any], run_id: str) -> None:
+    out = Path(res.get("out_dir", f"workspace/runs/{run_id}/bundle"))
+    if res.get("ok"):
+        print(f"[bundle] ok  → {out}")
+    else:
+        reason = res.get("error") or "unknown"
+        msg = res.get("message") or res.get("stderr_preview") or ""
+        print(f"[bundle] skip → {reason}{' — ' + msg if msg else ''}")
+
diff --git a/prototypes/gamified/cli.py b/prototypes/gamified/cli.py
index 4444444..5555555 100644
--- a/prototypes/gamified/cli.py
+++ b/prototypes/gamified/cli.py
@@ -1,22 +1,34 @@
 import sys
 from pathlib import Path
-from .spec_loader import load_and_validate_spec
-from .runner import start_backend_if_needed, run_pipeline
-from .urls import print_urls
+from .spec_loader import load_and_validate_spec
+from .runner import start_backend_if_needed, run_pipeline
+from .urls import print_urls
+from .tools import call_bundle_tool, report_bundle_result
@@
-def run(spec_path: str = "gamified.yaml"):
-    """
-    Paved-road execution:
-      - validate & snapshot spec
-      - auto-start backend (Arango)
-      - print URLs
-      - run pipeline
-    """
+def run(spec_path: str = "gamified.yaml"):
+    """
+    Paved-road execution (Happy Path):
+      - validate & snapshot spec
+      - auto-start backend (Arango)
+      - print URLs
+      - run pipeline
+      - (new) spec-driven bundling via MCP tool (no CLI flags)
+    """
     spec = load_and_validate_spec(spec_path)
     run_id = create_run_id()
     snapshot_path = write_spec_snapshot(spec, run_id)
     start_backend_if_needed(spec)
     print_urls(run_id)
-    return run_pipeline(spec, run_id=run_id, snapshot_path=snapshot_path)
+
+    try:
+        if getattr(spec, "observability", None) and spec.observability.bundle.enabled:
+            res = call_bundle_tool(
+                run_id=run_id,
+                include=spec.observability.bundle.include,
+                exclude=spec.observability.bundle.exclude,
+                mode=spec.observability.bundle.mode,
+            )
+            report_bundle_result(res, run_id)
+    except Exception as e:
+        print(f"[bundle] soft-fail: {e}")
+
+    return run_pipeline(spec, run_id=run_id, snapshot_path=snapshot_path)
diff --git a/tests/smoke/test_bundle_on_run_smoke.py b/tests/smoke/test_bundle_on_run_smoke.py
new file mode 100644
index 0000000..6666666
--- /dev/null
+++ b/tests/smoke/test_bundle_on_run_smoke.py
@@ -0,0 +1,43 @@
+import os, json, subprocess
+from pathlib import Path
+
+def test_bundle_created_on_run(tmp_path):
+    repo = tmp_path
+    (repo / "prototypes" / "gamified").mkdir(parents=True)
+    (repo / "workspace" / "runs").mkdir(parents=True)
+    (repo / "local" / "docs").mkdir(parents=True)
+
+    spec = {
+        "version": 1,
+        "approaches": [{"name": "demo"}],
+        "runner": {"type": "analysis_sim"},
+        "observability": {
+            "backend": "arango","dashboard": True,
+            "bundle": {"enabled": True,"mode": "markdown",
+                       "include": ["local/docs/**"],"exclude": ["**/__pycache__/**"]}
+        }
+    }
+    (repo / "gamified.yaml").write_text(json.dumps(spec))
+    env = os.environ.copy()
+    cmd = "python -m prototypes.gamified.cli run --spec gamified.yaml"
+    proc = subprocess.run(cmd, shell=True, cwd=str(repo), env=env,
+                          capture_output=True, text=True)
+    runs = sorted((repo / "workspace" / "runs").glob("*/bundle"))
+    assert runs, "No bundle directory created"
```

---

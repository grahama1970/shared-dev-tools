from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .spec_model import Spec


def load_and_validate_spec(path: str | Path) -> Spec:
    """
    Load a spec file and validate it into the Spec model.

    Behavior:
    - Try JSON first.
    - If JSON fails, try YAML if PyYAML is available.
    - On failure, fall back to empty dict (defaults apply).
    """
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    data: Any

    # Try JSON
    try:
        data = json.loads(text)
    except Exception:
        # Try YAML if available; otherwise fallback to {}
        try:
            import yaml  # type: ignore

            data = yaml.safe_load(text)
        except Exception:
            data = {}

    if not isinstance(data, dict):
        data = {}
    return Spec(**data)

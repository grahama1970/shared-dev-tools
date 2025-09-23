from __future__ import annotations

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class BundleConfig(BaseModel):
    enabled: bool = True
    mode: Literal["markdown", "zip", "tar"] = "markdown"
    include: List[str] = Field(
        default_factory=lambda: ["**/*.md", "src/**", "prototypes/**", "local/docs/**"]
    )
    exclude: List[str] = Field(
        default_factory=lambda: ["**/__pycache__/**", "**/*.pyc", "**/.DS_Store"]
    )


class ObservabilityConfig(BaseModel):
    backend: Literal["arango"] = "arango"
    dashboard: bool = True
    bundle: BundleConfig = BundleConfig()


class Spec(BaseModel):
    version: int = 1
    approaches: List[Dict[str, Any]] = Field(default_factory=list)
    runner: Dict[str, Any] = Field(default_factory=dict)
    scoring: Optional[Dict[str, Any]] = None
    constraints: Optional[Dict[str, Any]] = None
    optimizer: Optional[Dict[str, Any]] = None
    execution: Optional[Dict[str, Any]] = None
    observability: ObservabilityConfig = ObservabilityConfig()

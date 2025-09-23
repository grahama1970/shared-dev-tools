# Project Bundle

- Generated: 2025-09-19T14:55:39Z
- Root: /home/graham/workspace/experiments/shared-dev-tools
- Git: 8fe4d9c+dirty
- Files: 3
- Bundle Part: 1
- Context Tokens Limit: 400000

---


====== BEGIN FILE: SECURITY.md ======
```markdown
# Security Policy

## Supported Versions

The project aims to support the latest published release on PyPI (when available) and the `main` branch on GitHub. Older versions are not maintained.

## Reporting a Vulnerability

Please report suspected security issues privately:

1. Email the maintainers at `security@grahama.co` with a detailed description of the issue, proof-of-concept if available, and any suggested mitigations.
2. Alternatively, open a [GitHub Security Advisory](https://docs.github.com/en/code-security/security-advisories) pointing to this repository. Only maintainers will see your report.

We aim to acknowledge new reports within **3 business days** and keep you informed as we triage the issue.

If the vulnerability results in leaked credentials or other sensitive data, rotate those secrets immediately and include the steps you took in your report.

## Disclosure Policy

Maintainers will coordinate a disclosure timeline with the reporter. In general we prefer to publish fixes before announcing the vulnerability. Credit will be given to reporters unless they request anonymity.
```

====== END FILE ======


====== BEGIN FILE: src/shared_dev_tools/cli.py ======
```python
"""Command line entry point for building Markdown bundles from selected files.

Features
- Uses Git to respect .gitignore exactly when available (authoritative).
- Graceful fallback when not in Git: best-effort ignore based on root .gitignore and common folders.
- Skips binaries/images; size guards to avoid oversized inputs.
- Flexible selection: include extra filename globs or extensions; exclude paths; opt-in to include ignored files.
- Clear file boundaries with Markdown fences for LLM-friendly ingestion.

Examples
  # Standard run (respects .gitignore if in Git)
  bundle-files --root . --output bundle.txt

  # Include extra file types or special filenames (globs on names)
  bundle-files --include-ext ".proto,Justfile,vite.config.ts"

  # Add extra explicit path excludes
  bundle-files --extra-exclude-paths "misc/big_fixture.json,notes/tmp.txt"

  # Force include .gitignored files (audits)
  bundle-files --include-ignored

  # Ignore .gitignore entirely (fallback walk only)
  bundle-files --no-respect-gitignore
"""

from __future__ import annotations

import fnmatch
import json
import math
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Callable

import typer


# ---------------------------- Utility helpers ----------------------------


def _run_git(
    root: Path, args: Sequence[str], check: bool = False
) -> tuple[int, str, str]:
    """Run a git command from a specific root and capture output."""
    cmd = ["git", "-C", str(root), *args]
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.returncode, proc.stdout, proc.stderr


def _is_git_repo(root: Path) -> bool:
    code, out, _ = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    return code == 0 and out.strip() == "true"


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _posix_rel_path(path: Path, start: Path) -> str:
    return path.relative_to(start).as_posix()


def _read_text(path: Path, encoding: str = "utf-8") -> str:
    with path.open("r", encoding=encoding, errors="replace") as f:
        return f.read()


def _is_binary_by_content(path: Path, sample_bytes: int = 4096) -> bool:
    try:
        with path.open("rb") as f:
            chunk = f.read(sample_bytes)
        if b"\0" in chunk:
            return True
        # Heuristic: consider >30% of bytes outside typical text range as binary
        if not chunk:
            return False
        text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
        nontext = sum(b not in text_chars for b in chunk)
        return (nontext / len(chunk)) > 0.30
    except OSError:
        return True


# ---------------------------- Selection rules ----------------------------


DEFAULT_EXCLUDE_DIRS: Set[str] = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".output",
    ".svelte-kit",
    "coverage",
    ".cache",
    ".parcel-cache",
    ".turbo",
    ".vite",
    ".vercel",
    ".expo",
    ".pytest_cache",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "artifacts",
}


DEFAULT_BINARY_EXTS: Set[str] = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".icns",
    ".bmp",
    ".tif",
    ".tiff",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".so",
    ".dylib",
    ".a",
    ".lib",
    ".exe",
    ".dll",
}


LANG_BY_EXT = {
    ".py": "python",
    ".rs": "rust",
    ".go": "go",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "ts",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "ini",
    ".md": "markdown",
    ".txt": "text",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".less": "less",
    ".xml": "xml",
    ".svg": "xml",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "zsh",
    ".dockerfile": "dockerfile",
    ".proto": "proto",
    ".java": "java",
    ".kt": "kotlin",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cs": "cs",
}


# ---------------------------- Token estimation ----------------------------


def _make_token_estimator(spec: Optional[str]) -> Callable[[str], int]:
    """Return a callable(text)->int based on estimator spec.

    - None or "char" => ~4 chars/token heuristic
    - "tiktoken:<model>" => use tiktoken encoding if available, else fallback
    """

    if not spec or spec == "char":
        return lambda s: math.ceil(len(s) / 4) if s else 0

    if spec.startswith("tiktoken:"):
        model = spec.split(":", 1)[1] or ""
        try:
            import tiktoken  # type: ignore

            enc = (
                tiktoken.get_encoding("cl100k_base")
                if not model
                else tiktoken.encoding_for_model(model)
            )

            def _tok(s: str) -> int:
                if not s:
                    return 0
                try:
                    return len(enc.encode(s))
                except Exception:
                    return math.ceil(len(s) / 4)

            return _tok
        except Exception:
            # Silent fallback to char heuristic
            return lambda s: math.ceil(len(s) / 4) if s else 0

    # Unknown spec => fallback
    return lambda s: math.ceil(len(s) / 4) if s else 0


@dataclass
class _TokenCacheEntry:
    size: int
    mtime_ns: int
    estimator: str
    tokens: int


class _TokenCache:
    def __init__(self, path: Optional[Path]) -> None:
        self.path = path
        self.data: dict[str, _TokenCacheEntry] = {}
        if path is not None and path.exists():
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                for k, v in raw.items():
                    self.data[k] = _TokenCacheEntry(**v)
            except Exception:
                self.data = {}

    def make_key(self, file_path: Path, estimator: str) -> str:
        try:
            st = file_path.stat()
            return f"{file_path.resolve()}::{st.st_size}::{st.st_mtime_ns}::{estimator}"
        except Exception:
            return f"{file_path.resolve()}::0::0::{estimator}"

    def get(self, key: str) -> Optional[int]:
        ent = self.data.get(key)
        return ent.tokens if ent else None

    def set(self, key: str, file_path: Path, estimator: str, tokens: int) -> None:
        try:
            st = file_path.stat()
            self.data[key] = _TokenCacheEntry(
                st.st_size, st.st_mtime_ns, estimator, tokens
            )
        except Exception:
            self.data[key] = _TokenCacheEntry(0, 0, estimator, tokens)

    def save(self) -> None:
        if self.path is None:
            return
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            payload = {k: vars(v) for k, v in self.data.items()}
            self.path.write_text(json.dumps(payload), encoding="utf-8")
        except Exception:
            pass


def _lang_for_file(path: Path) -> str:
    name = path.name.lower()
    if name == "dockerfile":
        return "dockerfile"
    return LANG_BY_EXT.get(path.suffix.lower(), "")


def _parse_csv_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _normalize_patterns(patterns: Iterable[str]) -> List[str]:
    norm: List[str] = []
    for p in patterns:
        p = p.strip()
        if not p or p.startswith("#"):
            continue
        norm.append(p)
    return norm


def _matches_any(path_rel: str, patterns: Sequence[str]) -> bool:
    # Try matching both on full relative path and the basename
    base = path_rel.split("/")[-1]
    for pat in patterns:
        # Support simple ".ext" include patterns
        if pat.startswith(".") and "." in base and base.endswith(pat):
            return True
        if "/" in pat:
            if fnmatch.fnmatch(path_rel, pat):
                return True
        else:
            if fnmatch.fnmatch(base, pat):
                return True
    return False


def _read_gitignore_patterns(root: Path) -> List[str]:
    patterns: List[str] = []
    gi = root / ".gitignore"
    if gi.is_file():
        patterns.extend(_normalize_patterns(_read_text(gi).splitlines()))
    # Also consider .git/info/exclude if present
    info_exclude = root / ".git" / "info" / "exclude"
    if info_exclude.is_file():
        patterns.extend(_normalize_patterns(_read_text(info_exclude).splitlines()))
    return patterns


def _ignored_by_patterns(path_rel: str, patterns: Sequence[str]) -> bool:
    # Naive best-effort: treat patterns as fnmatch globs relative to repo root
    # and directory suffixes ("dir/") as recursive dir ignores.
    for p in patterns:
        if p.endswith("/"):
            # directory pattern: ignore if path starts with that dir
            if path_rel.startswith(p[:-1]):
                return True
        else:
            if fnmatch.fnmatch(path_rel, p):
                return True
            # Also attempt basename match
            base = path_rel.split("/")[-1]
            if fnmatch.fnmatch(base, p):
                return True
    return False


# ---------------------------- Discovery ----------------------------


def discover_files(
    root: Path,
    respect_gitignore: bool,
    include_ignored: bool,
    extra_exclude_paths: Sequence[str],
) -> List[Path]:
    """Return a list of candidate files under root, relative to root.

    If inside a Git repo and respect_gitignore=True, uses git ls-files (authoritative).
    Otherwise, falls back to a best-effort os.walk with simple .gitignore glob handling.
    """
    root = root.resolve()

    # Git-based discovery
    if respect_gitignore and _is_git_repo(root):
        args = ["ls-files", "-co", "--exclude-standard"]
        if include_ignored:
            args = ["ls-files", "-coi", "--exclude-standard"]
        code, out, err = _run_git(root, args)
        if code != 0:
            print(
                f"Warning: git discovery failed, falling back to walk: {err.strip()}",
                file=sys.stderr,
            )
        else:
            rels = [line.strip() for line in out.splitlines() if line.strip()]
            # Filter: exclude paths containing any excluded directory at any depth
            rels = [
                r
                for r in rels
                if not any(part in DEFAULT_EXCLUDE_DIRS for part in r.split("/"))
            ]
            if extra_exclude_paths:
                rels = [r for r in rels if not _matches_any(r, extra_exclude_paths)]
            return [root / r for r in rels if (root / r).is_file()]

    # Fallback: os.walk with best-effort ignore handling
    ignore_patterns: List[str] = []
    if respect_gitignore:
        ignore_patterns = _read_gitignore_patterns(root)

    results: List[Path] = []
    for base, dirs, files in os.walk(root):
        # Prune excluded directories aggressively
        rel_base = _posix_rel_path(Path(base), root)
        # Rel path for base is "." for root; normalize
        if rel_base == ".":
            rel_base = ""

        # Prune default exclude dirs
        pruned_dirs = []
        for d in list(dirs):
            if d in DEFAULT_EXCLUDE_DIRS:
                pruned_dirs.append(d)
                continue
            full_rel = (Path(rel_base) / d).as_posix() if rel_base else d
            if respect_gitignore and _ignored_by_patterns(
                full_rel + "/", ignore_patterns
            ):
                pruned_dirs.append(d)
        for d in pruned_dirs:
            if d in dirs:
                dirs.remove(d)

        for fname in files:
            rel = (Path(rel_base) / fname).as_posix() if rel_base else fname
            if extra_exclude_paths and _matches_any(rel, extra_exclude_paths):
                continue
            if respect_gitignore and _ignored_by_patterns(rel, ignore_patterns):
                continue
            results.append(root / rel)

    return [p for p in results if p.is_file()]


# ---------------------------- Filtering ----------------------------


@dataclass
class FilterOptions:
    include_patterns: List[str]
    max_file_bytes: int
    allow_large: bool


def should_include_file(path: Path, rel: str, opts: FilterOptions) -> bool:
    # Include patterns bypass extension-based filtering only (not size or binary checks)
    matched_include = (
        _matches_any(rel, opts.include_patterns) if opts.include_patterns else False
    )

    # Skip binaries by extension first
    if path.suffix.lower() in DEFAULT_BINARY_EXTS and not matched_include:
        return False

    # Size guard
    try:
        size = path.stat().st_size
    except OSError:
        return False

    if not opts.allow_large and size > opts.max_file_bytes:
        return False

    # Content-based binary heuristic
    if _is_binary_by_content(path):
        return False

    return True


# ---------------------------- Concatenation ----------------------------


@dataclass
class BundleResult:
    path: Path
    file_count: int
    total_bytes: int
    total_tokens: int
    exceeded_token_limit: bool
    exceeded_byte_limit: bool
    skipped_unreadable: int


@dataclass
class _BundleBlock:
    text: str
    tokens: int
    bytes_len: int
    is_file: bool
    skip: bool = False


def _estimate_tokens(text: str) -> int:
    """Approximate token count using a simple character heuristic."""
    if not text:
        return 0
    return math.ceil(len(text) / 4)


def _format_bundle_header(
    *,
    root: Path,
    git_desc: str,
    file_count: int,
    part_index: int,
    generated_ts: str,
    max_tokens: Optional[int],
) -> str:
    lines = [
        "# Project Bundle",
        "",
        f"- Generated: {generated_ts}",
        f"- Root: {root}",
        f"- Git: {git_desc or 'n/a'}",
        f"- Files: {file_count}",
        f"- Bundle Part: {part_index}",
    ]
    if max_tokens:
        lines.append(f"- Context Tokens Limit: {max_tokens}")
    lines.extend(["", "---", ""])
    return "\n".join(lines)


def _part_output_path(base: Path, part_index: int) -> Path:
    if part_index == 1:
        return base
    suffixes = "".join(base.suffixes)
    if suffixes:
        stem = base.name[: -len(suffixes)]
        return base.with_name(f"{stem}.part{part_index}{suffixes}")
    return base.with_name(f"{base.name}.part{part_index}")


class _BundleWriter:
    """Accumulates bundle blocks and writes chunked outputs."""

    def __init__(
        self,
        *,
        root: Path,
        output: Path,
        encoding: str,
        max_total_bytes: int,
        max_total_tokens: Optional[int],
        git_desc: str,
        token_estimator: Callable[[str], int],
        prefix_text: Optional[str] = None,
    ) -> None:
        self.root = root
        self.base_output = output
        self.encoding = encoding
        self.max_total_bytes = max_total_bytes if max_total_bytes > 0 else None
        self.max_total_tokens = (
            max_total_tokens if max_total_tokens and max_total_tokens > 0 else None
        )
        self.git_desc = git_desc
        self.generated_ts = _now_utc_iso()
        self._tok = token_estimator
        self.prefix_text = prefix_text or ""
        self.results: List[BundleResult] = []
        self.part_index = 1
        self.current_blocks: List[_BundleBlock] = []
        self.current_tokens_sum = 0
        self.current_bytes_sum = 0
        self.current_file_count = 0
        self.current_overflow_tokens = False
        self.current_overflow_bytes = False
        self.current_skips_count = 0
        self.current_skips_count = 0

    def _header_for_count(self, file_count: int) -> str:
        return _format_bundle_header(
            root=self.root,
            git_desc=self.git_desc,
            file_count=file_count,
            part_index=self.part_index,
            generated_ts=self.generated_ts,
            max_tokens=self.max_total_tokens,
        )

    def _compute_totals(self, block: _BundleBlock) -> tuple[int, int]:
        file_count = self.current_file_count + (1 if block.is_file else 0)
        header = self._header_for_count(file_count) + (
            self.prefix_text if self.prefix_text else ""
        )
        header_tokens = self._tok(header)
        header_bytes = len(header.encode(self.encoding, errors="replace"))
        total_tokens = header_tokens + self.current_tokens_sum + block.tokens
        total_bytes = header_bytes + self.current_bytes_sum + block.bytes_len
        return total_tokens, total_bytes

    def add_block(self, block: _BundleBlock) -> None:
        total_tokens, total_bytes = self._compute_totals(block)
        exceeds_tokens = (
            self.max_total_tokens is not None and total_tokens > self.max_total_tokens
        )
        exceeds_bytes = (
            self.max_total_bytes is not None and total_bytes > self.max_total_bytes
        )

        if (exceeds_tokens or exceeds_bytes) and self.current_blocks:
            self._flush_current()
            total_tokens, total_bytes = self._compute_totals(block)
            exceeds_tokens = (
                self.max_total_tokens is not None
                and total_tokens > self.max_total_tokens
            )
            exceeds_bytes = (
                self.max_total_bytes is not None and total_bytes > self.max_total_bytes
            )

        self.current_blocks.append(block)
        self.current_tokens_sum += block.tokens
        self.current_bytes_sum += block.bytes_len
        if block.is_file:
            self.current_file_count += 1
        if block.skip:
            self.current_skips_count += 1
        if exceeds_tokens:
            self.current_overflow_tokens = True
        if exceeds_bytes:
            self.current_overflow_bytes = True

    def _flush_current(self) -> None:
        header = self._header_for_count(self.current_file_count)
        header_bytes = len(header.encode(self.encoding, errors="replace"))
        header_tokens = self._tok(header)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header)
            if self.prefix_text:
                out_f.write(self.prefix_text)
            if self.prefix_text:
                out_f.write(self.prefix_text)
            for block in self.current_blocks:
                out_f.write(block.text)

        total_tokens = header_tokens + self.current_tokens_sum
        total_bytes = header_bytes + self.current_bytes_sum
        self.results.append(
            BundleResult(
                path=output_path,
                file_count=self.current_file_count,
                total_bytes=total_bytes,
                total_tokens=total_tokens,
                exceeded_token_limit=self.current_overflow_tokens,
                exceeded_byte_limit=self.current_overflow_bytes,
                skipped_unreadable=self.current_skips_count,
            )
        )

        self.part_index += 1
        self.current_blocks = []
        self.current_tokens_sum = 0
        self.current_bytes_sum = 0
        self.current_file_count = 0
        self.current_overflow_tokens = False
        self.current_overflow_bytes = False

    def _flush_empty(self) -> None:
        header = self._header_for_count(0)
        header_bytes = len(header.encode(self.encoding, errors="replace"))
        header_tokens = self._tok(header)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header)
            if self.prefix_text:
                out_f.write(self.prefix_text)

        self.results.append(
            BundleResult(
                path=output_path,
                file_count=0,
                total_bytes=header_bytes,
                total_tokens=header_tokens,
                exceeded_token_limit=False,
                exceeded_byte_limit=False,
                skipped_unreadable=0,
            )
        )

        self.part_index += 1

    def finalize(self) -> List[BundleResult]:
        if self.current_blocks:
            self._flush_current()
        elif not self.results:
            self._flush_empty()
        return self.results


def write_bundles(
    root: Path,
    files: Sequence[Path],
    output: Path,
    encoding: str,
    max_total_bytes: int,
    max_total_tokens: Optional[int],
    token_estimator: Callable[[str], int],
    token_estimator_spec: Optional[str],
    cache_path: Optional[Path],
    prefix_text: Optional[str],
) -> List[BundleResult]:
    """Write one or more Markdown bundle files based on size constraints."""

    git_desc = ""
    if _is_git_repo(root):
        code, out, _ = _run_git(root, ["rev-parse", "--short", "HEAD"])
        rev = out.strip() if code == 0 else "unknown"
        code, out, _ = _run_git(root, ["status", "--porcelain"])
        dirty = "+dirty" if out.strip() else ""
        git_desc = f"{rev}{dirty}"

    cache = _TokenCache(cache_path) if cache_path is not None else _TokenCache(None)

    writer = _BundleWriter(
        root=root,
        output=output,
        encoding=encoding,
        max_total_bytes=max_total_bytes,
        max_total_tokens=max_total_tokens,
        git_desc=git_desc,
        token_estimator=token_estimator,
        prefix_text=prefix_text,
    )

    for path in files:
        rel = _posix_rel_path(path, root)
        try:
            content = _read_text(path, encoding=encoding)
        except Exception as exc:  # noqa: BLE001
            msg = f"[SKIP unreadable: {rel}: {exc}]\n\n"
            block = _BundleBlock(
                text=msg,
                tokens=token_estimator(msg),
                bytes_len=len(msg.encode(encoding, errors="replace")),
                is_file=False,
                skip=True,
            )
            key = cache.make_key(path, token_estimator_spec or "char")
            if cache.get(key) is None:
                cache.set(key, path, token_estimator_spec or "char", block.tokens)
            writer.add_block(block)
            continue

        lang = _lang_for_file(path)
        fence_open = f"```{lang}\n" if lang else "```\n"
        fence_close = "```\n"
        file_header = f"\n\n====== BEGIN FILE: {rel} ======\n"
        file_footer = "\n====== END FILE ======\n"

        block_text = (
            file_header
            + fence_open
            + content
            + ("\n" if not content.endswith("\n") else "")
            + fence_close
            + file_footer
        )
        block = _BundleBlock(
            text=block_text,
            tokens=(
                cache.get(cache.make_key(path, token_estimator_spec or "char"))
                or token_estimator(block_text)
            ),
            bytes_len=len(block_text.encode(encoding, errors="replace")),
            is_file=True,
        )
        key = cache.make_key(path, token_estimator_spec or "char")
        if cache.get(key) is None:
            cache.set(key, path, token_estimator_spec or "char", block.tokens)
        writer.add_block(block)

    res = writer.finalize()
    try:
        cache.save()
    except Exception:
        pass
    return res


# ---------------------------- Typer CLI ----------------------------


def build_cli() -> typer.Typer:
    app = typer.Typer(
        help="Concatenate selected project files into one or more bundles for LLMs"
    )

    @app.callback(invoke_without_command=True)
    def run(
        root: Path = typer.Option(Path("."), "--root", help="Project root to scan"),
        output: Path = typer.Option(
            Path("bundle.txt"),
            "--output",
            "-o",
            help="Output path for the concatenated bundle",
        ),
        include_ext: Optional[str] = typer.Option(
            None,
            "--include-ext",
            help="Comma-separated list of filename globs or extensions to force-include (e.g. '.proto,Justfile,vite.config.ts')",
        ),
        extra_exclude_paths: Optional[str] = typer.Option(
            None,
            "--extra-exclude-paths",
            help="Comma-separated relative path globs to exclude additionally",
        ),
        no_respect_gitignore: bool = typer.Option(
            False,
            "--no-respect-gitignore",
            help="Do not use .gitignore even if present; walk filesystem instead",
        ),
        include_ignored: bool = typer.Option(
            False,
            "--include-ignored",
            help="If in Git and respecting .gitignore, include ignored files too",
        ),
        max_file_bytes: int = typer.Option(
            512_000,
            "--max-file-bytes",
            help="Per-file size guard; files larger than this are skipped unless --allow-large",
        ),
        allow_large: bool = typer.Option(
            False,
            "--allow-large",
            help="Allow files larger than --max-file-bytes",
        ),
        max_total_bytes: int = typer.Option(
            10_000_000,
            "--max-total-bytes",
            help="Stop writing once total bytes in output reach this threshold",
        ),
        context_length: int = typer.Option(
            400_000,
            "--context-length",
            help="Approximate token capacity per bundle part before splitting; set 0 to disable token-based chunking.",
        ),
        token_estimator: Optional[str] = typer.Option(
            None,
            "--token-estimator",
            help="Token estimator to use: 'char' (default) or 'tiktoken:<model>' if tiktoken is available",
        ),
        changed_since: Optional[str] = typer.Option(
            None,
            "--changed-since",
            help="Limit selection to files changed since the given Git revision (requires Git repo)",
        ),
        output_dir: Optional[Path] = typer.Option(
            None,
            "--output-dir",
            help="If provided, write output under this directory using --output or --output-base",
        ),
        output_base: Optional[str] = typer.Option(
            None,
            "--output-base",
            help="Base name for output file (e.g., 'bundle.md'); used with --output-dir",
        ),
        prefix_file: Optional[Path] = typer.Option(
            None,
            "--prefix-file",
            help="Path to a file whose contents will be inserted at the top of each bundle part",
        ),
        cache_dir: Optional[Path] = typer.Option(
            None,
            "--cache-dir",
            help="Directory to store token estimation cache (optional)",
        ),
        encoding: str = typer.Option(
            "utf-8", "--encoding", help="Encoding used to read files and write output"
        ),
        json_output: bool = typer.Option(
            False,
            "--json",
            help="Emit machine-readable JSON to stdout instead of friendly text",
        ),
        index: Optional[Path] = typer.Option(
            None,
            "--index",
            help="Optional path to also write the JSON result (when --json)",
        ),
        strict: bool = typer.Option(
            False,
            "--strict",
            help="Exit non-zero if any part exceeds limits or if any files were skipped as unreadable",
        ),
        list_only: bool = typer.Option(
            False, "--list", help="List selected files and exit (no bundle writing)"
        ),
        dry_run: bool = typer.Option(
            False, "--dry-run", help="Do not write output, only print selection summary"
        ),
    ) -> None:
        """Create a bundle or list selected files."""

        root_resolved = root.resolve()
        include_patterns = _parse_csv_list(include_ext or "")
        extra_excludes = _parse_csv_list(extra_exclude_paths or "")

        files_all = discover_files(
            root=root_resolved,
            respect_gitignore=not no_respect_gitignore,
            include_ignored=include_ignored,
            extra_exclude_paths=extra_excludes,
        )

        # If changed_since provided and repo available, narrow to changed files
        if changed_since and _is_git_repo(root_resolved):
            code, out, err = _run_git(
                root_resolved, ["diff", "--name-only", f"{changed_since}", "--"]
            )
            if code == 0:
                changed = [
                    (root_resolved / line.strip())
                    for line in out.splitlines()
                    if line.strip()
                ]
                changed = [p for p in changed if p.is_file()]
                if extra_excludes:
                    changed = [
                        p
                        for p in changed
                        if not _matches_any(
                            _posix_rel_path(p, root_resolved), extra_excludes
                        )
                    ]
                if changed:
                    files_all = changed

        fopts = FilterOptions(
            include_patterns=include_patterns,
            max_file_bytes=max_file_bytes,
            allow_large=allow_large,
        )

        selected: List[Path] = []
        for p in files_all:
            rel = _posix_rel_path(p, root_resolved)
            if should_include_file(p, rel, fopts):
                selected.append(p)

        selected.sort(key=lambda x: _posix_rel_path(x, root_resolved))

        # Load optional prefix text
        prefix_text = ""
        if prefix_file is not None:
            try:
                prefix_text = _read_text(prefix_file, encoding=encoding)
                if prefix_text and not prefix_text.endswith("\n\n"):
                    prefix_text += "\n\n"
            except Exception:
                prefix_text = ""

        cache_path = None
        if cache_dir is not None:
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_path = (cache_dir / "token_cache.json").resolve()

        # Compute effective output path if output_dir/base provided
        effective_output = output
        if output_dir is not None or output_base is not None:
            base_name = output_base or output.name
            effective_output = (output_dir or output.parent) / base_name
        # Compute effective output path if output_dir/base provided
        effective_output = output
        if output_dir is not None or output_base is not None:
            base_name = output_base or output.name
            effective_output = (output_dir or output.parent) / base_name

        if list_only or dry_run:
            if json_output:
                payload = {
                    "root": str(root_resolved),
                    "git": bool(_is_git_repo(root_resolved)),
                    "respect_gitignore": not no_respect_gitignore,
                    "include_ignored": include_ignored,
                    "candidates": len(files_all),
                    "selected": len(selected),
                    "files": [_posix_rel_path(p, root_resolved) for p in selected],
                    "generated": _now_utc_iso(),
                }
                text = json.dumps(payload)
                typer.echo(text)
                if index is not None:
                    index.parent.mkdir(parents=True, exist_ok=True)
                    index.write_text(text, encoding="utf-8")
            else:
                typer.echo(f"Root: {root_resolved}")
                typer.echo(
                    f"Git: {'yes' if _is_git_repo(root_resolved) else 'no'} (respect={not no_respect_gitignore}, include_ignored={include_ignored})"
                )
                typer.echo(
                    f"Candidates: {len(files_all)}  -> Selected: {len(selected)}"
                )
                for p in selected:
                    typer.echo(_posix_rel_path(p, root_resolved))
            raise typer.Exit(0)

        token_limit = context_length if context_length > 0 else None
        tok = _make_token_estimator(token_estimator)

        results = write_bundles(
            root=root_resolved,
            files=selected,
            output=effective_output,
            encoding=encoding,
            max_total_bytes=max_total_bytes,
            max_total_tokens=token_limit,
            token_estimator=tok,
            token_estimator_spec=token_estimator,
            cache_path=cache_path,
            prefix_text=prefix_text,
        )

        if json_output:
            payload = {
                "root": str(root_resolved),
                "base_output": str((root_resolved / output).resolve()),
                "context_length": token_limit,
                "max_total_bytes": max_total_bytes,
                "encoding": encoding,
                "generated": _now_utc_iso(),
                "parts": [
                    {
                        "path": str(r.path),
                        "file_count": r.file_count,
                        "bytes": r.total_bytes,
                        "tokens": r.total_tokens,
                        "exceeded_token_limit": r.exceeded_token_limit,
                        "exceeded_byte_limit": r.exceeded_byte_limit,
                        "skipped_unreadable": r.skipped_unreadable,
                    }
                    for r in results
                ],
            }
            text = json.dumps(payload)
            typer.echo(text)
            if index is not None:
                index.parent.mkdir(parents=True, exist_ok=True)
                index.write_text(text, encoding="utf-8")
        else:
            total_files_written = sum(res.file_count for res in results)
            if len(results) == 1:
                res = results[0]
                typer.echo(
                    f"Wrote {res.file_count} files to {res.path} ({res.total_bytes} bytes, tokens~{res.total_tokens})"
                )
                if res.exceeded_token_limit:
                    typer.echo(
                        "Warning: bundle exceeds --context-length tokens; consider reducing selection or lowering the limit.",
                        err=True,
                    )
                if res.exceeded_byte_limit:
                    typer.echo(
                        "Warning: bundle exceeds --max-total-bytes; consider adjusting limits.",
                        err=True,
                    )
            else:
                limit_desc = "disabled" if token_limit is None else str(token_limit)
                typer.echo(
                    f"Wrote {total_files_written} files across {len(results)} bundles (context-length {limit_desc})"
                )
                for idx, res in enumerate(results, start=1):
                    flags = []
                    if res.exceeded_token_limit:
                        flags.append("tokens>limit")
                    if res.exceeded_byte_limit:
                        flags.append("bytes>limit")
                    suffix = f" [{', '.join(flags)}]" if flags else ""
                    typer.echo(
                        f"  part {idx}: {res.path} files={res.file_count} bytes={res.total_bytes} tokens~{res.total_tokens}{suffix}"
                    )

    return app


app = build_cli()


def main() -> None:
    """Entry point for executable scripts."""
    app()


if __name__ == "__main__":
    # VS Code-friendly: running this file directly uses option defaults.
    main()
```

====== END FILE ======


====== BEGIN FILE: tests/smokes/test_cli_bundle_smoke.py ======
```python
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


def test_bundle_cli_splits_when_context_limit(tmp_path: Path) -> None:
    """Bundle splits into multiple parts when context-length is low."""

    root = tmp_path / "project"
    root.mkdir()

    big_line = "print('hello world')\\n" * 300
    _write_text(root / "alpha.py", big_line)
    _write_text(root / "beta.py", big_line)

    bundle_path = root / "bundle.md"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "--root",
            str(root),
            "--output",
            str(bundle_path),
            "--context-length",
            "200",
        ],
    )

    assert result.exit_code == 0, result.stdout

    part_two = bundle_path.with_name("bundle.part2.md")
    assert bundle_path.exists()
    assert part_two.exists()

    first_text = bundle_path.read_text(encoding="utf-8")
    second_text = part_two.read_text(encoding="utf-8")

    assert "BEGIN FILE: alpha.py" in first_text
    assert "BEGIN FILE: beta.py" not in first_text
    assert "BEGIN FILE: beta.py" in second_text

    # CLI output should reflect multi-bundle summary
    assert "bundles" in result.stdout
    assert "part 2" in result.stdout


def test_bundle_cli_json_outputs(tmp_path: Path) -> None:
    """JSON mode returns machine-readable results for list and generate."""

    root = tmp_path / "project"
    root.mkdir()

    # A couple small files
    _write_text(root / "a.py", "print('a')\n")
    _write_text(root / "b.py", "print('b')\n")

    bundle_path = root / "bundle.md"
    runner = CliRunner()

    # List JSON
    list_res = runner.invoke(
        app,
        ["--root", str(root), "--output", str(bundle_path), "--list", "--json"],
    )
    assert list_res.exit_code == 0, list_res.stdout
    import json as _json

    list_payload = _json.loads(list_res.stdout)
    assert list_payload["root"].endswith("project")
    assert isinstance(list_payload["files"], list) and list_payload["files"]

    # Generate JSON
    gen_res = runner.invoke(
        app,
        ["--root", str(root), "--output", str(bundle_path), "--json"],
    )
    assert gen_res.exit_code == 0, gen_res.stdout
    gen_payload = _json.loads(gen_res.stdout)
    assert gen_payload["base_output"].endswith("bundle.md")
    assert isinstance(gen_payload["parts"], list) and gen_payload["parts"], gen_payload
    assert "file_count" in gen_payload["parts"][0]
```

====== END FILE ======

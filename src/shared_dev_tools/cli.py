"""Command line entry point for building Markdown bundles from selected files.

Features
- Uses Git to respect .gitignore exactly when available (authoritative).
- Graceful fallback when not in Git: best-effort ignore based on root .gitignore and common folders.
- Skips binaries/images; size guards to avoid oversized inputs.
- Flexible selection: include extra filename globs or extensions; exclude paths; opt-in to include ignored files.
- Clear file boundaries with Markdown fences for LLM-friendly ingestion.

Examples (agent-friendly)
  # Standard run (respects .gitignore if in Git)
  bundle-files --root . --output bundle.md

  # Include extra file types or special filenames (globs on names)
  bundle-files --include-ext ".proto,Justfile,vite.config.ts"

  # Add extra explicit path excludes
  bundle-files --extra-exclude-paths "misc/big_fixture.json,notes/tmp.txt"

  # Force include .gitignored files (audits)
  bundle-files --include-ignored

  # Ignore .gitignore entirely (fallback walk only)
  bundle-files --no-respect-gitignore

  # Explicit file list (repeat --file) + persona preface, single concatenated output
  bundle-files --file a.py --file b.py --prefix-file scripts/review/persona.md \
               --single-file --output bundle.md

  # Large list from a file
  bundle-files --files-from scripts/review/files.txt --output bundle.md
"""

from __future__ import annotations

import fnmatch
import json
import math
import os
import io
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
    """Best-effort repo-relative path; falls back to absolute POSIX if outside root."""
    p = path.resolve()
    s = start.resolve()
    try:
        return p.relative_to(s).as_posix()
    except Exception:
        return p.as_posix()


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
        header_only = self._header_for_count(self.current_file_count)
        prefix = self.prefix_text if self.prefix_text else ""
        header_bytes = len(
            (header_only + prefix).encode(self.encoding, errors="replace")
        )
        header_tokens = self._tok(header_only + prefix)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header_only)
            if prefix:
                out_f.write(prefix)
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
        header_only = self._header_for_count(0)
        prefix = self.prefix_text if self.prefix_text else ""
        header_bytes = len(
            (header_only + prefix).encode(self.encoding, errors="replace")
        )
        header_tokens = self._tok(header_only + prefix)
        output_path = _part_output_path(self.base_output, self.part_index)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open(
            "w", encoding=self.encoding, errors="replace", newline="\n"
        ) as out_f:
            out_f.write(header_only)
            if prefix:
                out_f.write(prefix)

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
        # Selection
        root: Path = typer.Option(Path("."), "--root", help="Project root to scan"),
        file: List[Path] = typer.Option(
            None,
            "--file",
            help="Explicit file to include (repeatable). When present, discovery is skipped.",
        ),
        files_from: Optional[Path] = typer.Option(
            None,
            "--files-from",
            help="Text file with one path per line (explicit selection).",
        ),
        output: Path = typer.Option(
            Path("bundle.md"),
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
        single_file: bool = typer.Option(
            False,
            "--single-file",
            help="Force a single concatenated Markdown file (disables token/byte splitting).",
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
        manifest: Optional[Path] = typer.Option(
            None,
            "--manifest",
            help="Optional path to write a manifest.json (inputs, parts, checksums, budgets)",
        ),
        archive: Optional[str] = typer.Option(
            None,
            "--archive",
            help="Package parts + index + manifest into an archive: 'zip' or 'tar'",
        ),
        archive_files: Optional[str] = typer.Option(
            None,
            "--archive-files",
            help="Package ORIGINAL selected files (preserving relative paths) plus BUNDLE_INSTRUCTIONS.md; also includes index/manifest if provided: 'zip' or 'tar'",
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

        # If explicit selection provided, use only that.
        explicit: List[Path] = []
        if file:
            explicit.extend(
                [p if p.is_absolute() else (root_resolved / p) for p in file]
            )
        if files_from and files_from.is_file():
            for line in _read_text(files_from).splitlines():
                s = line.strip()
                if s:
                    p = Path(s)
                    explicit.append(p if p.is_absolute() else (root_resolved / p))

        if explicit:
            files_all = [p.resolve() for p in explicit if p.exists()]
        else:
            files_all = discover_files(
                root=root_resolved,
                respect_gitignore=not no_respect_gitignore,
                include_ignored=include_ignored,
                extra_exclude_paths=extra_excludes,
            )

        # If changed_since provided and repo available, narrow to changed files
        if changed_since and _is_git_repo(root_resolved) and not explicit:
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

        # Limits: single-file disables token/byte splitting entirely
        token_limit = (
            None if single_file else (context_length if context_length > 0 else None)
        )
        effective_max_bytes = None if single_file else max_total_bytes
        tok = _make_token_estimator(token_estimator)

        results = write_bundles(
            root=root_resolved,
            files=selected,
            output=effective_output,
            encoding=encoding,
            max_total_bytes=(
                effective_max_bytes
                if effective_max_bytes is not None
                else max_total_bytes
            ),
            max_total_tokens=token_limit,
            token_estimator=tok,
            token_estimator_spec=token_estimator,
            cache_path=cache_path,
            prefix_text=prefix_text,
        )

        # Tool meta
        def _tool_meta() -> tuple[str, str]:
            tool_name = "bundle-files"
            tool_ver = "0.1.0"
            try:
                import tomllib  # py311+

                pyproj = root_resolved / "pyproject.toml"
                if pyproj.is_file():
                    data = tomllib.loads(pyproj.read_text(encoding="utf-8"))
                    tool_ver = data.get("project", {}).get("version", tool_ver)
            except Exception:
                pass
            return tool_name, tool_ver

        schema_version = "bundle_index_v1"
        tool_name, tool_version = _tool_meta()

        import hashlib
        import tarfile
        import zipfile

        manifest_path = None
        archive_path = None
        if manifest is not None:
            manifest.parent.mkdir(parents=True, exist_ok=True)
            parts_list = []
            for r in results:
                p = (
                    root_resolved / r.path
                    if not Path(r.path).is_absolute()
                    else Path(r.path)
                )
                try:
                    with open(p, "rb") as f:
                        h = hashlib.sha256()
                        for chunk in iter(lambda: f.read(8192), b""):
                            h.update(chunk)
                    sha256 = h.hexdigest()
                except Exception:
                    sha256 = ""
                parts_list.append(
                    {
                        "path": str(r.path),
                        "bytes": r.total_bytes,
                        "tokens": r.total_tokens,
                        "sha256": sha256,
                    }
                )
            manifest_payload = {
                "schema_version": "bundle_manifest_v1",
                "tool_name": tool_name,
                "tool_version": tool_version,
                "generated": _now_utc_iso(),
                "root": str(root_resolved),
                "base_output": str((root_resolved / effective_output).resolve()),
                "context_length": token_limit,
                "max_total_bytes": max_total_bytes,
                "selected_files": [_posix_rel_path(p, root_resolved) for p in selected],
                "parts": parts_list,
            }
            manifest.write_text(json.dumps(manifest_payload), encoding="utf-8")
            manifest_path = manifest

        if archive in {"zip", "tar"}:
            base = effective_output
            base_stem = base.with_suffix("") if base.suffix else base
            if archive == "zip":
                archive_path = base_stem.with_suffix(".zip")
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(
                    archive_path, "w", compression=zipfile.ZIP_DEFLATED
                ) as zf:
                    for r in results:
                        zf.write(r.path, arcname=Path(r.path).name)
                    if index is not None and index.exists():
                        zf.write(index, arcname=index.name)
                    if manifest_path is not None and manifest_path.exists():
                        zf.write(manifest_path, arcname=manifest_path.name)
            else:
                archive_path = base_stem.with_suffix(".tar")
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                with tarfile.open(archive_path, "w") as tf:
                    for r in results:
                        tf.add(r.path, arcname=Path(r.path).name)
                    if index is not None and index.exists():
                        tf.add(index, arcname=index.name)
                    if manifest_path is not None and manifest_path.exists():
                        tf.add(manifest_path, arcname=manifest_path.name)

        # Optional: package original selected files with directory structure + instructions
        files_archive_path = None
        if archive_files in {"zip", "tar"}:
            base = effective_output
            base_stem = base.with_suffix("") if base.suffix else base

            # Build a simple file list (repo-relative) for context
            rel_files = sorted(_posix_rel_path(p, root_resolved) for p in selected)
            file_list_section = "\n".join(f"- {rf}" for rf in rel_files)

            instruction_text = (
                "# Bundle Instructions\n\n"
                f"- Generated: {_now_utc_iso()}\n"
                f"- Root: {root_resolved}\n"
                f"- Files included: {len(selected)}\n"
                "- Structure: Original selected files under their repo-relative paths.\n"
                "- Sidecars: manifest.json (checksums), index.json (CLI JSON summary) if present.\n\n"
                "Directory structure (relative file list):\n"
                f"{file_list_section}\n\n"
                "Notes:\n"
                "- Use the Markdown bundle parts (*.md) alongside this archive for LLM ingestion.\n"
            )

            if archive_files == "zip":
                files_archive_path = base_stem.with_suffix(".files.zip")
                files_archive_path.parent.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(
                    files_archive_path, "w", compression=zipfile.ZIP_DEFLATED
                ) as zf:
                    # Instruction document
                    zf.writestr("BUNDLE_INSTRUCTIONS.md", instruction_text)
                    # Original files with relative paths
                    for p in selected:
                        rel = _posix_rel_path(p, root_resolved)
                        zf.write(p, arcname=rel)
                    # Include index/manifest sidecars if provided (index may be written after archiving)
                    if manifest_path is not None and manifest_path.exists():
                        zf.write(manifest_path, arcname=manifest_path.name)
                    if index is not None and index.exists():
                        zf.write(index, arcname=index.name)
            else:
                files_archive_path = base_stem.with_suffix(".files.tar")
                files_archive_path.parent.mkdir(parents=True, exist_ok=True)
                with tarfile.open(files_archive_path, "w") as tf2:
                    # Instruction document
                    ins_bytes = instruction_text.encode("utf-8")
                    ti = tarfile.TarInfo("BUNDLE_INSTRUCTIONS.md")
                    ti.size = len(ins_bytes)
                    tf2.addfile(ti, io.BytesIO(ins_bytes))
                    # Original files with relative paths
                    for p in selected:
                        rel = _posix_rel_path(p, root_resolved)
                        tf2.add(p, arcname=rel)
                    # Include index/manifest sidecars if provided (index may be written after archiving)
                    if manifest_path is not None and manifest_path.exists():
                        tf2.add(manifest_path, arcname=manifest_path.name)
                    if index is not None and index.exists():
                        tf2.add(index, arcname=index.name)

        # (keep the first “archive original files” block above; remove this duplicate)

        if json_output:
            reasons = []
            if any(r.exceeded_token_limit for r in results):
                reasons.append("tokens_over_limit")
            if any(r.exceeded_byte_limit for r in results):
                reasons.append("bytes_over_limit")
            if any(r.skipped_unreadable > 0 for r in results):
                reasons.append("skipped_unreadable")

            payload = {
                "schema_version": schema_version,
                "tool_name": tool_name,
                "tool_version": tool_version,
                "root": str(root_resolved),
                "base_output": str((root_resolved / effective_output).resolve()),
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
                "status": "strict_failed" if (strict and reasons) else "ok",
                "reasons": reasons,
            }
            if manifest_path is not None:
                payload["manifest_path"] = str(manifest_path)
            if archive_path is not None:
                payload["archive_path"] = str(archive_path)
            if "files_archive_path" in locals() and files_archive_path is not None:
                payload["files_archive_path"] = str(files_archive_path)
            text = json.dumps(payload)
            typer.echo(text)
            if index is not None:
                index.parent.mkdir(parents=True, exist_ok=True)
                index.write_text(text, encoding="utf-8")
            if strict and reasons:
                raise typer.Exit(1)
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

            # Enforce strict exit if any issues detected
            if strict and (
                any(r.exceeded_token_limit for r in results)
                or any(r.exceeded_byte_limit for r in results)
                or any(r.skipped_unreadable > 0 for r in results)
            ):
                raise typer.Exit(1)

    return app


app = build_cli()


def main() -> None:
    """Entry point for executable scripts."""
    app()


if __name__ == "__main__":
    # VS Code-friendly: running this file directly uses option defaults.
    main()

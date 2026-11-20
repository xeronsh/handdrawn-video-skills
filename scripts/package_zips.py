#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Build clean, deterministic, Gemini-Web-Tasks-ready `.zip` archives for:
- Track A (`generic`): `skills/` -> `dist/generic/`
- Track B (`xeron`):   `presets/xeron/` -> `dist/xeron/`

Usage:
    uv run scripts/package_zips.py
    uv run scripts/package_zips.py --track xeron
    uv run scripts/package_zips.py --track generic --out dist
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)

EXCLUDED_DIR_NAMES = {"__pycache__", ".git", ".pytest_cache", ".mypy_cache"}
EXCLUDED_FILE_NAMES = {".DS_Store", "Thumbs.db"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}

TRACK_SPECS: dict[str, dict[str, object]] = {
    "generic": {
        "src_root": REPO_ROOT / "skills",
        "subdir": "generic",
        "skills": [
            "selfmedia-pipeline",
            "script-storyboard",
            "mascot-illustrations",
            "handdrawn-motion",
        ],
        "bundle_name": "handdrawn-video-skills-generic-suite",
        "extra_bundle_files": [
            (REPO_ROOT / "templates" / "ip-profile.example.yaml", "templates/ip-profile.example.yaml"),
        ],
    },
    "xeron": {
        "src_root": REPO_ROOT / "presets" / "xeron",
        "subdir": "xeron",
        "skills": [
            "xeron-selfmedia-pipeline",
            "xeron-script-storyboard",
            "xeron-cat-illustrations",
            "xeron-cat-motion",
        ],
        "bundle_name": "xeron-skills-suite",
        "extra_bundle_files": [
            (REPO_ROOT / "presets" / "xeron" / "README.md", "README.md"),
        ],
    },
}


def _is_excluded(path: Path) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True
    if path.name in EXCLUDED_FILE_NAMES:
        return True
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True
    return False


def _collect_files(base_dir: Path) -> list[tuple[Path, str]]:
    entries: list[tuple[Path, str]] = []
    for p in sorted(base_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(base_dir)
        if _is_excluded(rel):
            continue
        entries.append((p, rel.as_posix()))
    return entries


def _write_deterministic_zip(zip_path: Path, entries: list[tuple[Path, str]]) -> tuple[int, int]:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    sorted_entries = sorted(entries, key=lambda item: item[1])
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.comment = b""
        for src_file, arcname in sorted_entries:
            data = src_file.read_bytes()
            zi = zipfile.ZipInfo(filename=arcname, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 3  # Unix
            zi.external_attr = 0o644 << 16
            zi.extra = b""
            zi.comment = b""
            zf.writestr(zi, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return len(sorted_entries), zip_path.stat().st_size


def _format_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} B"
    if n_bytes < 1024 * 1024:
        return f"{n_bytes / 1024:.1f} KiB ({n_bytes:,} B)"
    return f"{n_bytes / (1024 * 1024):.2f} MiB ({n_bytes:,} B)"


def build_track(track_name: str, out_root: Path) -> list[tuple[Path, int, int]]:
    spec = TRACK_SPECS[track_name]
    src_root = Path(spec["src_root"])  # type: ignore[arg-type]
    subdir = str(spec["subdir"])
    skills = list(spec["skills"])  # type: ignore[arg-type]
    bundle_name = str(spec["bundle_name"])
    extra_bundle_files = list(spec["extra_bundle_files"])  # type: ignore[arg-type]

    if not src_root.is_dir():
        print(f"[skip] track '{track_name}': source directory not found ({src_root})")
        return []

    track_out = out_root / subdir
    built: list[tuple[Path, int, int]] = []
    bundle_entries: list[tuple[Path, str]] = []

    for extra_src, extra_rel in extra_bundle_files:
        if extra_src.is_file():
            bundle_entries.append((extra_src, f"{bundle_name}/{extra_rel}"))

    for skill_name in skills:
        skill_dir = src_root / skill_name
        if not skill_dir.is_dir():
            print(f"[warn] track '{track_name}': skill directory missing ({skill_dir}), skipping")
            continue
        skill_files = _collect_files(skill_dir)
        if not any(arc == "SKILL.md" for _, arc in skill_files):
            print(f"[warn] track '{track_name}': {skill_dir} has no root SKILL.md")

        # Individual flat-root skill zip (SKILL.md directly at archive root)
        zip_path = track_out / f"{skill_name}.zip"
        n_files, n_bytes = _write_deterministic_zip(zip_path, skill_files)
        built.append((zip_path, n_files, n_bytes))

        # Add to combined bundle under <bundle_name>/<skill_name>/...
        for src_file, rel_arc in skill_files:
            bundle_entries.append((src_file, f"{bundle_name}/{skill_name}/{rel_arc}"))

    if bundle_entries:
        bundle_zip = track_out / f"{bundle_name}.zip"
        n_files, n_bytes = _write_deterministic_zip(bundle_zip, bundle_entries)
        built.append((bundle_zip, n_files, n_bytes))

    return built


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Package deterministic flat-root skill .zip files for Gemini Web Tasks.",
    )
    parser.add_argument(
        "--track",
        choices=("all", "generic", "xeron"),
        default="all",
        help="Which track to package (default: all).",
    )
    parser.add_argument(
        "--out",
        default="dist",
        help="Output root directory (default: dist).",
    )
    args = parser.parse_args(argv)

    out_root = Path(args.out)
    tracks = ["generic", "xeron"] if args.track == "all" else [args.track]

    all_built: list[tuple[Path, int, int]] = []
    for t in tracks:
        all_built.extend(build_track(t, out_root))

    if not all_built:
        print(f"[error] No archives were built for --track {args.track}.", file=sys.stderr)
        return 1

    print(f"Built {len(all_built)} deterministic zip archive(s):")
    for zp, n_files, n_bytes in all_built:
        print(f"  - {zp}  [{n_files} files, {_format_size(n_bytes)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

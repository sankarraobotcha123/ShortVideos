from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist_release" / "edu-content-platform-mvp-v33.zip"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "ENV",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist_release",
}

EXCLUDED_FILE_NAMES = {
    ".env",
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
}

EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".log",
}

GENERATED_STORAGE_DIRS = {
    "storage/exports",
    "storage/audio",
    "storage/video_drafts",
    "storage/asset_library",
    "storage/thumbnails",
    "storage/source_safety",
    "storage/trust_reviews",
    "storage/learning_outputs",
    "storage/handoffs",
    "storage/release_reports",
    "storage/youtube_oauth",
    "storage/raw_uploads",
    "storage/scene_library",
}


def should_include(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    parts = relative.parts

    if any(part in EXCLUDED_DIR_NAMES for part in parts):
        return False
    if path.name in EXCLUDED_FILE_NAMES:
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    if path.name.endswith("~"):
        return False

    relative_posix = relative.as_posix()
    for generated_dir in GENERATED_STORAGE_DIRS:
        if relative_posix.startswith(f"{generated_dir}/") and path.name != ".gitkeep":
            return False
    if relative_posix == "storage/app.db":
        return False
    if relative_posix.startswith("frontend/dist/"):
        return False
    return True


def collect_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if path.is_file() and should_include(path):
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def build_package(output: Path, *, dry_run: bool = False) -> list[str]:
    files = collect_files()
    names = [path.relative_to(ROOT).as_posix() for path in files]
    if dry_run:
        return names

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a clean release ZIP for the Edu Content Platform MVP.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output ZIP path.")
    parser.add_argument("--dry-run", action="store_true", help="Print files that would be included without creating a ZIP.")
    args = parser.parse_args()

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output

    names = build_package(output, dry_run=args.dry_run)
    if args.dry_run:
        print("Release package dry run")
        print("=" * 28)
        for name in names:
            print(name)
        print(f"Total files: {len(names)}")
        return 0

    print("Release package created")
    print("=" * 25)
    print(f"Output: {output}")
    print(f"Files: {len(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CACHE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
LOCAL_DIRS = [
    "dist_release",
    "frontend/dist",
]
LOCAL_FILES = [
    ".coverage",
]


def collect_targets(include_release_outputs: bool = True) -> list[Path]:
    targets: list[Path] = []
    for path in ROOT.rglob("*"):
        if path.is_dir() and path.name in CACHE_DIR_NAMES:
            targets.append(path)
    for relative in LOCAL_DIRS:
        path = ROOT / relative
        if path.exists():
            if relative == "dist_release" and not include_release_outputs:
                continue
            targets.append(path)
    for relative in LOCAL_FILES:
        path = ROOT / relative
        if path.exists():
            targets.append(path)
    return sorted(set(targets), key=lambda item: item.relative_to(ROOT).as_posix())


def remove_target(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove local cache/build artifacts before pushing to Git.")
    parser.add_argument("--apply", action="store_true", help="Actually delete files. Without this flag, only prints what would be removed.")
    parser.add_argument("--keep-release-output", action="store_true", help="Keep dist_release while still listing/removing caches.")
    args = parser.parse_args()

    targets = collect_targets(include_release_outputs=not args.keep_release_output)
    print("Local artifact cleanup")
    print("=" * 24)
    if not targets:
        print("No removable cache/build artifacts found.")
        return 0

    for target in targets:
        print(target.relative_to(ROOT).as_posix())

    if not args.apply:
        print()
        print("Dry run only. Re-run with --apply to delete these local artifacts.")
        return 0

    for target in targets:
        remove_target(target)
    print()
    print(f"Removed {len(targets)} local artifact path(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

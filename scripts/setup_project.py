from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STORAGE_DIRS = [
    "storage",
    "storage/raw_uploads",
    "storage/scene_library",
    "storage/exports",
    "storage/audio",
    "storage/video_drafts",
    "storage/asset_library",
    "storage/thumbnails",
    "storage/source_safety",
    "storage/trust_reviews",
    "storage/learning_outputs",
    "storage/release_reports",
]


def run(command: list[str], *, check: bool = True) -> int:
    print("$ " + " ".join(command))
    completed = subprocess.run(command, cwd=ROOT)
    if check and completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed.returncode


def ensure_env(copy_env: bool = True) -> str:
    env_path = ROOT / ".env"
    example_path = ROOT / ".env.example"
    if env_path.exists():
        return ".env already exists"
    if not copy_env:
        return ".env missing; skipped copy"
    if not example_path.exists():
        return ".env.example missing; cannot create .env"
    shutil.copyfile(example_path, env_path)
    return "created .env from .env.example"


def ensure_storage_dirs() -> list[str]:
    messages: list[str] = []
    for relative in STORAGE_DIRS:
        path = ROOT / relative
        path.mkdir(parents=True, exist_ok=True)
        gitkeep = path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")
        messages.append(f"ready: {relative}")
    return messages


def check_status() -> int:
    required = [
        ".env.example",
        "requirements.txt",
        "package.json",
        "frontend/package.json",
        "scripts/init_db.py",
        "scripts/seed_demo_data.py",
        "scripts/setup_project.py",
    ]
    missing = [item for item in required if not (ROOT / item).exists()]
    print("Fresh-clone setup check")
    print("=" * 32)
    print(f"Project root: {ROOT}")
    print(f"Python: {sys.version.split()[0]}")
    print(f".env exists: {(ROOT / '.env').exists()}")
    print(f"database exists: {(ROOT / 'storage' / 'app.db').exists()}")
    print(f"frontend/node_modules exists: {(ROOT / 'frontend' / 'node_modules').exists()}")
    if missing:
        print("Missing required files:")
        for item in missing:
            print(f"- {item}")
        return 1
    print("Required setup files found.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap the Edu Content Platform after a fresh Git clone.")
    parser.add_argument("--check-only", action="store_true", help="Only print setup status. Do not create files or run init scripts.")
    parser.add_argument("--skip-env-copy", action="store_true", help="Do not create .env from .env.example.")
    parser.add_argument("--install-backend", action="store_true", help="Run pip install -r requirements.txt.")
    parser.add_argument("--install-frontend", action="store_true", help="Run npm install inside frontend.")
    parser.add_argument("--seed-demo", action="store_true", help="Seed demo data after initializing the database.")
    parser.add_argument("--reset-demo", action="store_true", help="Reset demo data when seeding demo rows.")
    args = parser.parse_args()

    if args.check_only:
        return check_status()

    print("Fresh-clone setup automation")
    print("=" * 34)
    print(f"Project root: {ROOT}")
    print(f"Python: {sys.version.split()[0]}")
    print()

    print(ensure_env(copy_env=not args.skip_env_copy))
    for message in ensure_storage_dirs():
        print(message)

    if args.install_backend:
        run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    run([sys.executable, "scripts/init_db.py"])

    if args.seed_demo or args.reset_demo:
        seed_command = [sys.executable, "scripts/seed_demo_data.py"]
        if args.reset_demo:
            seed_command.append("--reset-demo")
        run(seed_command)

    if args.install_frontend:
        npm = "npm.cmd" if os.name == "nt" else "npm"
        run([npm, "--prefix", "frontend", "install"])

    print()
    print("Setup complete.")
    print("Next terminals:")
    print(r"1) .venv\\Scripts\\activate && uvicorn app.main:app --reload")
    print("2) npm run frontend:dev")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.release_check_service import build_release_checklist


def main() -> int:
    checklist = build_release_checklist(ROOT)
    summary = checklist["summary"]
    print("Production cleanup and release checklist")
    print("=" * 48)
    print(f"Passed : {summary['pass_count']}")
    print(f"Warnings: {summary['warn_count']}")
    print(f"Failures: {summary['fail_count']}")
    print()

    for group_name in ["file_checks", "directory_checks", "gitignore_checks", "env_example_checks"]:
        failing = [item for item in checklist[group_name] if item["status"] == "fail"]
        warnings = [item for item in checklist[group_name] if item["status"] == "warn"]
        if failing or warnings:
            print(group_name)
            for item in failing + warnings:
                print(f"- [{item['status']}] {item['label']}: {item['detail']}")
                if item.get("fix"):
                    print(f"  fix: {item['fix']}")
            print()

    print("Recommended Git commands:")
    for command in checklist["git_commands"]:
        print(f"  {command}")
    print()

    if summary["fail_count"]:
        print("Result: NOT READY. Fix failures before pushing.")
        return 1
    print("Result: READY, but still run tests and frontend build before push.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

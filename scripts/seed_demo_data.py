from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.session import db_session, init_db
from app.services.demo_seed_service import seed_demo_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed demo data for the Edu Content Platform MVP.")
    parser.add_argument("--reset-demo", action="store_true", help="Delete existing demo rows and recreate them.")
    args = parser.parse_args()

    init_db()
    with db_session() as conn:
        result = seed_demo_data(conn, reset_demo=args.reset_demo)
    print(result["message"])
    print(f"Batch: {result.get('batch', {}).get('name') if result.get('batch') else 'not created'}")
    print(f"Packages: {result.get('package_count', 0)}")
    print(f"Package IDs: {result.get('package_ids', [])}")


if __name__ == "__main__":
    main()

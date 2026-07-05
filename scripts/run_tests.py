from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Run backend tests with stable local defaults.

    Some Python installations auto-load third-party pytest plugins from the
    global environment. Those plugins are useful in their own projects, but they
    can slow or hang a small MVP test run. This wrapper disables external plugin
    autoload before importing pytest, so test behavior stays focused on this
    repository only.
    """
    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    os.chdir(ROOT)
    try:
        import pytest
    except ImportError:
        print("pytest is not installed. Run: pip install pytest", file=sys.stderr)
        return 1

    args = ["-q", *sys.argv[1:]]
    print("$ python -m pytest " + " ".join(args), flush=True)
    return int(pytest.main(args))


if __name__ == "__main__":
    raise SystemExit(main())

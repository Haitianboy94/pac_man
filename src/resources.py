"""Locate files bundled with the game or present in the source tree."""

import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """Return an absolute path usable both normally and under PyInstaller."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    root = (
        Path(bundle_root)
        if bundle_root
        else Path(__file__).resolve().parent.parent
    )
    return str(root / relative_path)

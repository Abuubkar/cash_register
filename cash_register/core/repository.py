"""
repository.py — All disk I/O in one place.
Swap the backend (JSON → SQLite, cloud, etc.) by replacing only this file.
"""

import json
import os
from pathlib import Path

from cash_register.core.models import LedgerState

# Default storage path — can be overridden for testing
DEFAULT_DATA_FILE = Path.home() / "cash_register_data.json"


class LedgerRepository:
    def __init__(self, path: Path = DEFAULT_DATA_FILE):
        self._path = path

    def get_mtime(self) -> float:
        """Return the last modification time of the data file."""
        if self._path.exists():
            return self._path.stat().st_mtime
        return 0.0

    def load(self) -> LedgerState:
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    return LedgerState.from_dict(json.load(f))
            except (json.JSONDecodeError, KeyError):
                pass   # corrupted file → fresh state
        return LedgerState()

    def save(self, state: LedgerState) -> None:
        """Atomic save: write to temp file then rename."""
        temp_path = self._path.with_suffix(".tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(state.to_dict(), f, indent=2, ensure_ascii=False)
            
            # Atomic swap
            temp_path.replace(self._path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise


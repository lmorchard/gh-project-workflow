#!/usr/bin/env python3
"""Run the source checkout CLI without changing the caller's directory."""
import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[3] / "cli/ghflow.py"), run_name="__main__")

"""Load and validate spec files into Python objects."""

from pathlib import Path
from typing import Any


def load_spec(path: Path | str) -> dict[str, Any]:
    """Load a YAML spec file and return a dict. Stub."""
    raise NotImplementedError("Use PyYAML to load; validate required keys.")


def validate_spec(spec: dict[str, Any]) -> bool:
    """Validate spec has required fields (e.g. objective, entities, steps). Stub."""
    raise NotImplementedError("Check required keys and types.")

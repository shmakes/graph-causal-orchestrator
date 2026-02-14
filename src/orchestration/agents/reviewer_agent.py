"""Validates outputs against the spec."""

from typing import Any


def validate_against_spec(spec: dict[str, Any], outputs: dict[str, Any]) -> dict[str, Any]:
    """Check that outputs satisfy spec (objective, steps, entities). Stub."""
    raise NotImplementedError("Compare outputs to spec; return validation result with errors.")

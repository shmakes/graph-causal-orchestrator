"""Builds reports and code from investigation results."""

from typing import Any


def build_report(findings: list[dict], spec: dict[str, Any]) -> str:
    """Produce a markdown or structured report. Stub."""
    raise NotImplementedError("Template or LLM-generated report from findings + spec.")


def build_code_artifact(findings: list[dict], language: str = "python") -> str:
    """Produce code (e.g. notebook or script) from findings. Stub."""
    raise NotImplementedError("LLM-generated code stub.")

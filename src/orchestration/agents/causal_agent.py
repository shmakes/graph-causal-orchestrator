"""Causal reasoning and explanations agent."""

from typing import Any


def explain_causal_paths(source_id: str, target_id: str, client: Any) -> list[dict]:
    """Return causal paths and human-readable explanations. Stub."""
    raise NotImplementedError("Use causal_kg + optional LLM for explanations.")


def suggest_interventions(node_id: str, client: Any) -> list[dict]:
    """Suggest interventions based on causal parents/children. Stub."""
    raise NotImplementedError("Use causal_kg.intervention_effect and LLM.")

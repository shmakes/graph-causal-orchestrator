"""Structured schema for why-aware causal responses.

These typed dicts keep causal outputs machine-readable so orchestration and
prompt assembly can cleanly separate observations ("what") from causal
hypotheses ("why"), intervention options, and uncertainty disclosures.
"""

from __future__ import annotations

from typing import TypedDict


class CausalMechanism(TypedDict):
    """A single graph-derived causal chain."""

    path: list[str]
    mechanism: str
    confidence: float
    assumptions: list[str]


class InterventionOption(TypedDict):
    """A candidate action to alter an outcome."""

    node_id: str
    recommendation: str
    expected_direction: str
    expected_effect_score: float
    confidence: float
    caveats: list[str]


class WhyAwareContext(TypedDict):
    """Context object passed into response generation."""

    query: str
    what_evidence: list[dict]
    why_hypotheses: list[CausalMechanism]
    interventions: list[InterventionOption]
    uncertainty: list[str]


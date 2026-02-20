"""Causal reasoning and explanations agent."""

from __future__ import annotations

from typing import Any

from graph.causal_kg import intervention_effect
from orchestration.causal_schema import CausalMechanism, InterventionOption


def _path_confidence(path: list[str]) -> float:
    """Heuristic confidence: shorter paths are generally less speculative."""
    if not path:
        return 0.0
    depth = max(1, len(path) - 1)
    return round(max(0.25, min(0.95, 1.0 / depth + 0.2)), 4)


def _build_mechanism(path: list[str]) -> str:
    if len(path) < 2:
        return "Insufficient causal chain length to describe a mechanism."
    chain = " -> ".join(path)
    return (
        f"The graph indicates a causal chain {chain}. "
        "This is treated as a candidate mechanism, not definitive proof."
    )


def explain_causal_paths(
    source_id: str,
    target_id: str,
    client: Any,
    max_depth: int = 5,
) -> list[CausalMechanism]:
    """Return graph-derived causal paths with structured explanations."""
    paths = client.causal_paths(source_id=source_id, target_id=target_id, max_depth=max_depth)
    explanations: list[CausalMechanism] = []
    for item in paths:
        path = [p for p in (item.get("path") or []) if p]
        if not path:
            continue
        explanations.append(
            CausalMechanism(
                path=path,
                mechanism=_build_mechanism(path),
                confidence=_path_confidence(path),
                assumptions=[
                    "CAUSES edges reflect directionality in the source graph.",
                    "Unobserved confounders may still exist.",
                ],
            )
        )
    return explanations


def suggest_interventions(
    node_id: str,
    client: Any,
    depth: int = 2,
    limit: int = 5,
) -> list[InterventionOption]:
    """Suggest interventions by scoring upstream causes of an outcome node."""
    rows = client.run_cypher(
        f"""
        MATCH (n)
        WHERE n.id = $node_id OR n.name = $node_id
        MATCH (x)-[:CAUSES*1..{max(1, min(int(depth), 20))}]->(n)
        RETURN DISTINCT x, labels(x)[0] AS label
        """,
        {"node_id": node_id},
    )
    candidates: list[InterventionOption] = []
    for row in rows:
        node = row.get("x")
        if not node:
            continue
        candidate_id = node.get("id") or node.get("name")
        if not candidate_id:
            continue
        effect = intervention_effect(client, candidate_id, node_id) or {}
        score = float(effect.get("estimated_effect") or 0.0)
        confidence = float(effect.get("confidence") or 0.0)
        candidates.append(
            InterventionOption(
                node_id=candidate_id,
                recommendation=f"Prioritize mitigation on '{candidate_id}' to influence '{node_id}'.",
                expected_direction=str(effect.get("direction") or "unknown"),
                expected_effect_score=score,
                confidence=confidence,
                caveats=[
                    "Effect size is heuristic until statistical causal estimation is added.",
                    str(effect.get("rationale") or "No rationale provided."),
                ],
            )
        )
    ranked = sorted(
        candidates,
        key=lambda x: (x["expected_effect_score"], x["confidence"]),
        reverse=True,
    )
    return ranked[: max(1, limit)]

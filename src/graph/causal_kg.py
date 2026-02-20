"""Causal edges, interventions API for the knowledge graph."""

from typing import Any, Optional


def _node_identity(record: dict, key: str = "node") -> str:
    """Return stable id for a node: id or name (works with Neo4j Node or dict)."""
    n = record.get(key)
    if n is None:
        return ""
    getter = getattr(n, "get", None)
    if getter:
        return getter("id") or getter("name") or ""
    if isinstance(n, dict):
        return n.get("id") or n.get("name") or ""
    return ""


def get_causal_children(client: Any, node_id: str, depth: int = 1) -> list[dict]:
    """Return nodes that are causally downstream of node_id (traverse CAUSES edges from node_id)."""
    d = max(1, min(int(depth), 20))
    rows = client.run_cypher(
        f"""
        MATCH (n)
        WHERE n.id = $node_id OR n.name = $node_id
        MATCH (n)-[:CAUSES*1..{d}]->(x)
        RETURN DISTINCT x, labels(x)[0] AS label
        """,
        {"node_id": node_id},
    )
    return [
        {"id": _node_identity(r, "x"), "label": r.get("label")}
        for r in rows
    ]


def get_causal_parents(client: Any, node_id: str, depth: int = 1) -> list[dict]:
    """Return nodes that are causally upstream of node_id (traverse CAUSES edges to node_id)."""
    d = max(1, min(int(depth), 20))
    rows = client.run_cypher(
        f"""
        MATCH (n)
        WHERE n.id = $node_id OR n.name = $node_id
        MATCH (x)-[:CAUSES*1..{d}]->(n)
        RETURN DISTINCT x, labels(x)[0] AS label
        """,
        {"node_id": node_id},
    )
    return [
        {"id": _node_identity(r, "x"), "label": r.get("label")}
        for r in rows
    ]


def intervention_effect(client: Any, intervention_node_id: str, outcome_node_id: str) -> Optional[dict]:
    """Estimate intervention impact via graph-distance heuristic.

    This is an intentionally simple baseline until do-calculus / statistical
    estimation is introduced. Shorter causal distance implies stronger expected
    effect.
    """
    # Backward-compatible behavior for tests and dry-run callers that
    # intentionally pass no client.
    if client is None:
        return {"estimated_effect": None}

    rows = client.run_cypher(
        """
        MATCH (intervention), (outcome)
        WHERE (intervention.id = $intervention_node_id OR intervention.name = $intervention_node_id)
          AND (outcome.id = $outcome_node_id OR outcome.name = $outcome_node_id)
        OPTIONAL MATCH p = shortestPath((intervention)-[:CAUSES*1..20]->(outcome))
        RETURN p IS NOT NULL AS has_path,
               CASE WHEN p IS NULL THEN NULL ELSE length(p) END AS path_length
        """,
        {
            "intervention_node_id": intervention_node_id,
            "outcome_node_id": outcome_node_id,
        },
    )
    row = rows[0] if rows else {}
    has_path = bool(row.get("has_path"))
    path_length = row.get("path_length")
    if not has_path or not path_length:
        return {
            "estimated_effect": 0.0,
            "direction": "unknown",
            "confidence": 0.0,
            "method": "graph_distance_heuristic",
            "rationale": "No CAUSES path detected between intervention and outcome.",
        }

    distance = float(path_length)
    estimated_effect = round(1.0 / distance, 4)
    confidence = round(max(0.2, min(1.0, 1.0 / distance + 0.2)), 4)
    return {
        "estimated_effect": estimated_effect,
        "direction": "risk_decrease_if_mitigated",
        "confidence": confidence,
        "method": "graph_distance_heuristic",
        "rationale": f"Shortest causal path length={path_length}; shorter paths are scored higher.",
    }

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
    """Estimate effect of intervening on intervention_node on outcome_node. Placeholder for do-calculus or graph-based effect."""
    return {"estimated_effect": None}

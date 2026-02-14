"""Causal edges, interventions API for the knowledge graph."""

from typing import Any, Optional


def get_causal_children(client: Any, node_id: str, depth: int = 1) -> list[dict]:
    """Return nodes that are causally downstream of node_id. Stub."""
    raise NotImplementedError("Traverse CAUSES edges from node_id.")


def get_causal_parents(client: Any, node_id: str, depth: int = 1) -> list[dict]:
    """Return nodes that are causally upstream of node_id. Stub."""
    raise NotImplementedError("Traverse CAUSES edges to node_id.")


def intervention_effect(client: Any, intervention_node_id: str, outcome_node_id: str) -> Optional[dict]:
    """Estimate effect of intervening on intervention_node on outcome_node. Stub."""
    raise NotImplementedError("Implement do-calculus or graph-based effect estimation.")

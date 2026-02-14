"""Write nodes and edges to Neo4j."""

from typing import Any

from .schemas import NodeBase, EdgeBase


def load_nodes(driver: Any, nodes: list[NodeBase], label: str = "Node") -> int:
    """Upsert nodes into Neo4j. Returns count. Stub."""
    raise NotImplementedError("Implement Neo4j node load (MERGE).")


def load_edges(driver: Any, edges: list[EdgeBase], rel_type: str | None = None) -> int:
    """Upsert edges into Neo4j. Returns count. Stub."""
    raise NotImplementedError("Implement Neo4j edge load (MERGE).")

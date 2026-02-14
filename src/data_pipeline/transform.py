"""Map raw data to graph model (nodes/edges)."""

from .schemas import NodeBase, EdgeBase


def to_nodes(raw: list[dict], id_field: str = "id", label_field: str = "label") -> list[NodeBase]:
    """Map raw records to node models. Stub."""
    raise NotImplementedError("Implement mapping to NodeBase.")


def to_edges(raw: list[dict], source_key: str, target_key: str, relation_type: str) -> list[EdgeBase]:
    """Map raw records to edge models. Stub."""
    raise NotImplementedError("Implement mapping to EdgeBase.")

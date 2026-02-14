"""Node and edge models for the graph (Pydantic)."""

from pydantic import BaseModel, Field
from typing import Optional


class NodeBase(BaseModel):
    """Base for graph nodes."""
    id: str
    label: str
    properties: dict = Field(default_factory=dict)


class EdgeBase(BaseModel):
    """Base for graph edges."""
    source_id: str
    target_id: str
    relation_type: str
    properties: dict = Field(default_factory=dict)


class CausalEdge(EdgeBase):
    """Causal edge: source -> target (source causes target)."""
    relation_type: str = "CAUSES"

"""Tests for data_pipeline.schemas."""

import pytest
from data_pipeline.schemas import NodeBase, EdgeBase, CausalEdge


def test_node_base():
    n = NodeBase(id="n1", label="Customer", properties={"name": "Acme"})
    assert n.id == "n1"
    assert n.label == "Customer"
    assert n.properties["name"] == "Acme"


def test_edge_base():
    e = EdgeBase(source_id="a", target_id="b", relation_type="PURCHASED")
    assert e.source_id == "a"
    assert e.target_id == "b"
    assert e.relation_type == "PURCHASED"


def test_causal_edge_default():
    c = CausalEdge(source_id="x", target_id="y")
    assert c.relation_type == "CAUSES"

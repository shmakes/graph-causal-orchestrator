"""Tests for graph.causal_kg."""

import pytest
from graph import causal_kg


def test_get_causal_children_returns_list():
    mock_client = type("MockClient", (), {"run_cypher": lambda self, q, p=None: []})()
    assert causal_kg.get_causal_children(mock_client, "churn:xyz") == []


def test_get_causal_parents_returns_list():
    mock_client = type("MockClient", (), {"run_cypher": lambda self, q, p=None: []})()
    assert causal_kg.get_causal_parents(mock_client, "churn:xyz") == []


def test_get_causal_parents_with_mock_rows():
    mock_client = type("MockClient", (), {"run_cypher": lambda self, q, p=None: [{"x": {"id": "ct1", "name": None}, "label": "Contract"}]})()
    result = causal_kg.get_causal_parents(mock_client, "churn:abc")
    assert len(result) == 1
    assert result[0]["id"] == "ct1"
    assert result[0]["label"] == "Contract"


def test_intervention_effect_returns_placeholder():
    assert causal_kg.intervention_effect(None, "n1", "n2") == {"estimated_effect": None}

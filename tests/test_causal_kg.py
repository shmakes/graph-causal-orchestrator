"""Tests for graph.causal_kg."""

import pytest
from graph import causal_kg


def test_get_causal_children_stub_raises():
    with pytest.raises(NotImplementedError):
        causal_kg.get_causal_children(None, "n1")


def test_get_causal_parents_stub_raises():
    with pytest.raises(NotImplementedError):
        causal_kg.get_causal_parents(None, "n1")


def test_intervention_effect_stub_raises():
    with pytest.raises(NotImplementedError):
        causal_kg.intervention_effect(None, "n1", "n2")

"""Tests for graph.neo4j_client."""

import pytest
from graph.neo4j_client import Neo4jClient


def test_client_init():
    c = Neo4jClient("bolt://localhost:7687", "neo4j", "secret")
    assert c.uri == "bolt://localhost:7687"
    assert c.user == "neo4j"


def test_run_cypher_stub_raises():
    c = Neo4jClient("bolt://localhost:7687", "neo4j", "secret")
    with pytest.raises(NotImplementedError):
        c.run_cypher("RETURN 1")

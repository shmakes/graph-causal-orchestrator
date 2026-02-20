"""Tests for graph.neo4j_client."""

import pytest
from graph.neo4j_client import Neo4jClient


def test_client_init():
    c = Neo4jClient("bolt://localhost:7687", "neo4j", "secret")
    assert c.uri == "bolt://localhost:7687"
    assert c.user == "neo4j"


@pytest.mark.functional
def test_run_cypher_executes_and_returns_list():
    from config.settings import get_settings
    settings = get_settings()
    client = Neo4jClient(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)
    try:
        client.connect()
        rows = client.run_cypher("RETURN 1 AS n")
        assert rows == [{"n": 1}]
    finally:
        client.close()

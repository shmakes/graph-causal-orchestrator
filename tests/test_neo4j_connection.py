"""Functional test: Neo4j is reachable at the URI in .env and credentials work."""

import pytest
from neo4j import GraphDatabase

from config.settings import get_settings


@pytest.mark.functional
def test_neo4j_reachable_and_credentials_work():
    """Verify Neo4j at NEO4J_URI in .env is present and NEO4J_USER/NEO4J_PASSWORD work."""
    settings = get_settings()
    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS n")
            row = result.single()
            assert row is not None
            assert row["n"] == 1
    finally:
        driver.close()

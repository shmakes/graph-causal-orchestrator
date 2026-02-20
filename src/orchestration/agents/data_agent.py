"""ETL and graph querying agent."""

from typing import Any

from config.settings import get_settings
from graph.neo4j_client import Neo4jClient


def run_etl_step(config: dict[str, Any]) -> dict[str, Any]:
    """Run extract/transform/load step. Stub."""
    raise NotImplementedError("Call data_pipeline extract, transform, load_neo4j.")


def _client_from_env() -> Neo4jClient:
    settings = get_settings()
    client = Neo4jClient(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )
    client.connect()
    return client


def query_graph(
    cypher: str,
    params: dict[str, Any] | None = None,
    client: Neo4jClient | None = None,
) -> list[dict]:
    """Execute Cypher and return results."""
    owns_client = client is None
    active_client = client or _client_from_env()
    try:
        return active_client.run_cypher(cypher, params or {})
    finally:
        if owns_client:
            active_client.close()

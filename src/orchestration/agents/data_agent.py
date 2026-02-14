"""ETL and graph querying agent."""

from typing import Any


def run_etl_step(config: dict[str, Any]) -> dict[str, Any]:
    """Run extract/transform/load step. Stub."""
    raise NotImplementedError("Call data_pipeline extract, transform, load_neo4j.")


def query_graph(cypher: str, params: dict[str, Any] | None = None) -> list[dict]:
    """Execute Cypher and return results. Stub."""
    raise NotImplementedError("Use neo4j_client.run_cypher.")

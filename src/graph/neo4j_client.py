"""Cypher helpers and causal query helpers for Neo4j."""

from typing import Any, Optional


class Neo4jClient:
    """Neo4j driver wrapper with Cypher and causal query helpers."""

    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self._driver: Any = None

    def connect(self) -> None:
        """Create driver connection. Stub."""
        raise NotImplementedError("Use neo4j.GraphDatabase.driver(uri, auth=(user, password)).")

    def close(self) -> None:
        """Close driver. Stub."""
        if self._driver:
            self._driver.close()

    def run_cypher(self, query: str, parameters: Optional[dict] = None) -> list[dict]:
        """Execute Cypher and return records as list of dicts. Stub."""
        raise NotImplementedError("Execute query with session.run().")

    def causal_paths(self, source_id: str, target_id: str, max_depth: int = 5) -> list[dict]:
        """Return causal paths from source to target. Stub."""
        raise NotImplementedError("Use variable-length CAUSES path in Cypher.")

"""Cypher helpers and causal query helpers for Neo4j."""

from typing import Any, Optional

from neo4j import GraphDatabase


class Neo4jClient:
    """Neo4j driver wrapper with Cypher and causal query helpers."""

    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self._driver: Any = None

    def connect(self) -> None:
        """Create driver connection."""
        self._driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password),
        )

    def close(self) -> None:
        """Close driver."""
        if self._driver:
            self._driver.close()
            self._driver = None

    def run_cypher(self, query: str, parameters: Optional[dict] = None) -> list[dict]:
        """Execute Cypher and return records as list of dicts."""
        if not self._driver:
            self.connect()
        with self._driver.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]

    def causal_paths(self, source_id: str, target_id: str, max_depth: int = 5) -> list[dict]:
        """Return causal paths from source to target (variable-length CAUSES traversal)."""
        d = max(1, min(int(max_depth), 20))
        rows = self.run_cypher(
            f"""
            MATCH (source), (target)
            WHERE (source.id = $source_id OR source.name = $source_id)
              AND (target.id = $target_id OR target.name = $target_id)
            MATCH path = (source)-[:CAUSES*1..{d}]->(target)
            RETURN [node IN nodes(path) | coalesce(node.id, node.name)] AS pathIds
            """,
            {"source_id": source_id, "target_id": target_id},
        )
        return [{"path": r.get("pathIds") or []} for r in rows]

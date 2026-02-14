"""LangGraph / AutoGen tools for Neo4j (Cypher, causal queries)."""

from typing import Any


def get_neo4j_tools(client: Any) -> list[Any]:
    """Return list of tool definitions for Neo4j (run_cypher, causal_paths, etc.). Stub."""
    raise NotImplementedError("Wrap neo4j_client and causal_kg in LangChain/AutoGen tools.")

#!/usr/bin/env python3
"""
Explore the telecom graph in Neo4j: node/relationship counts, churn breakdown, sample subgraphs.
Read-only Cypher. Run from project root: uv run python scripts/explore_telecom_graph.py
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from graph.neo4j_client import Neo4jClient


def load_settings():
    from config.settings import get_settings
    return get_settings()


def main():
    settings = load_settings()
    client = Neo4jClient(
        settings.neo4j_uri,
        settings.neo4j_user,
        settings.neo4j_password,
    )

    try:
        client.connect()
        run = client.run_cypher
        print("=== Node counts (by label) ===")
        for r in run("MATCH (n) RETURN labels(n)[0] AS label, count(*) AS cnt ORDER BY cnt DESC"):
            print(f"  {r['label']}: {r['cnt']}")

        print("\n=== Relationship counts ===")
        for r in run("MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS cnt ORDER BY cnt DESC"):
            print(f"  {r['type']}: {r['cnt']}")

        print("\n=== Churn vs stayed ===")
        for r in run("MATCH (c:Customer) RETURN c.customerStatus AS status, count(*) AS cnt ORDER BY cnt"):
            print(f"  {r['status']}: {r['cnt']}")

        print("\n=== Churn by contract ===")
        for r in run("""
            MATCH (c:Customer)-[:HAS_CONTRACT]->(ct:Contract)
            RETURN ct.name AS contract, c.customerStatus AS status, count(*) AS cnt
            ORDER BY contract, status
        """):
            print(f"  {r['contract']} | {r['status']}: {r['cnt']}")

        print("\n=== Sample churned customers (id, contract, churnCategory, churnReason) ===")
        for r in run("""
            MATCH (c:Customer)
            WHERE c.customerStatus = 'Churned'
            RETURN c.id AS id, c.contract AS contract, c.churnCategory AS churnCategory, c.churnReason AS churnReason
            LIMIT 5
        """):
            print(f"  {r}")

        print("\n=== One churned customer with 1-hop relationships (id, rel types, neighbor labels) ===")
        rows = run("""
            MATCH (c:Customer {customerStatus: 'Churned'})
            OPTIONAL MATCH (c)-[r]->(n)
            WITH c, type(r) AS relType, labels(n)[0] AS neighborLabel
            RETURN c.id AS customerId, collect(relType + '->' + neighborLabel) AS rels
            LIMIT 3
        """)
        for r in rows:
            print(f"  {r}")

    finally:
        client.close()

    print("\nDone.")


if __name__ == "__main__":
    main()

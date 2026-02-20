#!/usr/bin/env python3
"""
Add the causal overlay to the telecom graph:
  - ChurnOutcome node per churned customer (id = "churn:<customerId>")
  - Customer -[:HAS_OUTCOME]-> ChurnOutcome
  - Contract -[:CAUSES]-> ChurnOutcome, Offer -[:CAUSES]-> ChurnOutcome for each churned customer

Run after import_telecom_data.py. From project root: uv run python scripts/add_causal_overlay.py
See docs/causal_overlay_schema.md for the schema.
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

        # Remove existing causal overlay so we can re-run
        client.run_cypher("MATCH (co:ChurnOutcome) DETACH DELETE co")

        # Create ChurnOutcome per churned customer and HAS_OUTCOME
        client.run_cypher("""
            MATCH (c:Customer {customerStatus: 'Churned'})
            MERGE (co:ChurnOutcome {id: 'churn:' + c.id})
            SET co.customerId = c.id
            MERGE (c)-[:HAS_OUTCOME]->(co)
        """)

        # Contract -[:CAUSES]-> ChurnOutcome for each churned customer
        client.run_cypher("""
            MATCH (c:Customer {customerStatus: 'Churned'})-[:HAS_OUTCOME]->(co:ChurnOutcome),
                  (c)-[:HAS_CONTRACT]->(ct:Contract)
            MERGE (ct)-[:CAUSES]->(co)
        """)

        # Offer -[:CAUSES]-> ChurnOutcome for each churned customer (only when they have an offer)
        client.run_cypher("""
            MATCH (c:Customer {customerStatus: 'Churned'})-[:HAS_OUTCOME]->(co:ChurnOutcome),
                  (c)-[:HAS_OFFER]->(o:Offer)
            MERGE (o)-[:CAUSES]->(co)
        """)

        n_outcomes = client.run_cypher("MATCH (co:ChurnOutcome) RETURN count(co) AS n")[0]["n"]
        n_causes = client.run_cypher("MATCH ()-[r:CAUSES]->() RETURN count(r) AS n")[0]["n"]
        print(f"ChurnOutcome nodes: {n_outcomes}")
        print(f"CAUSES edges: {n_causes}")

    finally:
        client.close()

    print("Done. Causal overlay added.")


if __name__ == "__main__":
    main()

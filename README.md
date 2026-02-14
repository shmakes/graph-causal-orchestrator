# graph-causal-orchestrator
Explore full path from data source ingestion to causal overlay to orchestrating agents to build a solution from spec to delivery.

## Python (pyenv, project-local)

To use the latest stable Python 3 for this project only (other projects unchanged):

```bash
bash scripts/setup-pyenv-python.sh
```

This installs the latest 3.13.x via pyenv and writes `.python-version` in this repo so only this directory uses it. Verify with `python --version` and `which python`.

## Import IBM Telco data into Neo4j

With Neo4j running and `.env` set (e.g. `NEO4J_URI`, `NEO4J_PASSWORD`), from project root:

```bash
uv run python scripts/import_telecom_data.py
```

Uses local CSVs in `scripts/`:

| File | Neo4j model |
|------|-------------|
| `telecom_customer_churn.csv` | **Customer** nodes + **Contract**, **Offer**, **City**, **InternetType**, **PaymentMethod** + relationships |
| `telecom_zipcode_population.csv` | **ZipCode** nodes; customers linked via `IN_ZIPCODE` |
| `telecom_data_dictionary.csv` | **Table** and **Field** nodes with descriptions |

Example Cypher in Neo4j Browser: `MATCH (c:Customer)-[:IN_ZIPCODE]->(z:ZipCode) WHERE c.customerStatus = 'Churned' RETURN c, z LIMIT 10`

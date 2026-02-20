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

## Scripts

All runnable scripts currently in `scripts/`:

- `scripts/import_telecom_data.py` - Loads the three IBM Telco CSV datasets into Neo4j.
  - Run: `uv run python scripts/import_telecom_data.py`
- `scripts/explore_telecom_graph.py` - Read-only graph exploration (counts, churn breakdowns, sample subgraphs).
  - Run: `uv run python scripts/explore_telecom_graph.py`
- `scripts/add_causal_overlay.py` - Adds `ChurnOutcome` nodes and `CAUSES` edges for churned customers.
  - Run: `uv run python scripts/add_causal_overlay.py`
- `scripts/evaluate_why_aware.py` - Scores model answers against the why-aware rubric.
  - Run: `uv run python scripts/evaluate_why_aware.py --responses-file responses.json`

## Why-aware evaluation

The evaluation script scores model answers against a fixed rubric so that “why-aware” responses (causal chains, interventions, uncertainty) can be regression-tested.

- **Eval spec:** `src/specs/examples/why_aware_eval.yml` — defines cases and required checks (causal chain, intervention mention, uncertainty disclosure).
- **Script:** `scripts/evaluate_why_aware.py` — reads a JSON file of case id → response text and prints scores.

Create a responses file (e.g. `responses.json`) keyed by case id from the spec:

```json
{
  "churn_why_customer": "Customer 0004-TLHLJ churned because...",
  "churn_why_contract": "Month-to-month contract is associated with churn...",
  "churn_counterfactual": "If we change offers..."
}
```

Then run:

```bash
uv run python scripts/evaluate_why_aware.py --responses-file responses.json
```

Optional: `--eval-spec path/to/why_aware_eval.yml` to use a different rubric. Use the **Evaluate why-aware** launch configuration in VS Code to run the script under the debugger (edit `args` in `.vscode/launch.json` if your responses file is elsewhere).

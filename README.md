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
- **Responses file:** `responses.json` (sample in repo root) — maps each case id to your model's answer text.
- **Script:** `scripts/evaluate_why_aware.py` — reads the spec + responses and prints per-case and aggregate scores.

### How the files fit together

1. `src/specs/examples/why_aware_eval.yml` defines the test cases and rubric.
2. `responses.json` contains your generated answers for those case ids.
3. `scripts/evaluate_why_aware.py` compares the answers to rubric keywords and outputs JSON results.

### Prepare or edit `responses.json`

Use the repo-root `responses.json` as a starting point, or create your own file with the same case ids:

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

Optional:

- Use a different rubric file:
  - `uv run python scripts/evaluate_why_aware.py --eval-spec path/to/why_aware_eval.yml --responses-file responses.json`
- Use the **Evaluate why-aware** launch configuration in VS Code (edit `args` in `.vscode/launch.json` if your responses file is elsewhere).

### How to interpret results

The script prints JSON like:

```json
{
  "cases": [
    {
      "id": "churn_why_customer",
      "query": "Why did customer 0004-TLHLJ churn?",
      "score": 1.0,
      "passed_checks": [
        "causal_chain",
        "intervention_option",
        "uncertainty_disclosure"
      ],
      "missing_response": false
    }
  ],
  "mean_score": 0.89
}
```

- `cases`: one entry per case id from the eval spec
  - `score`: fraction of rubric checks passed for that case (`0.0` to `1.0`)
  - `passed_checks`: which checks were satisfied (`causal_chain`, `intervention_option`, `uncertainty_disclosure`)
  - `missing_response`: `true` if the case id was absent from your responses file
- `mean_score`: average of all case scores

Practical reading guide:

- `mean_score` close to `1.0`: responses consistently include causal reasoning, interventions, and uncertainty language.
- Low `score` on a case: inspect `passed_checks` to see what is missing (for example, no uncertainty caveat).
- `missing_response: true`: add that case id to `responses.json` and rerun.

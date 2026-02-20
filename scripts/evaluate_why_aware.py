"""Evaluate why-aware answer quality against a fixed YAML rubric.

Usage:
  uv run python scripts/evaluate_why_aware.py --responses-file responses.json

`responses.json` format:
{
  "churn_why_customer": "model answer text...",
  "churn_why_contract": "model answer text..."
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def _contains_any(text: str, options: list[str]) -> bool:
    normalized = text.lower()
    return any(token.lower() in normalized for token in options)


def _score_case(case: dict[str, Any], response: str) -> tuple[float, list[str]]:
    checks: list[tuple[str, bool]] = [
        ("causal_chain", _contains_any(response, case.get("must_include_any") or [])),
        ("intervention_option", _contains_any(response, case.get("intervention_any") or [])),
        (
            "uncertainty_disclosure",
            _contains_any(response, ["assumption", "uncertain", "confound", "caveat"]),
        ),
    ]
    passed = [name for name, ok in checks if ok]
    return len(passed) / len(checks), passed


def evaluate(eval_spec: dict[str, Any], responses: dict[str, str]) -> dict[str, Any]:
    output: dict[str, Any] = {"cases": [], "mean_score": 0.0}
    case_rows = []
    for case in eval_spec.get("cases", []):
        case_id = case["id"]
        response = responses.get(case_id, "")
        score, passed = _score_case(case, response)
        case_rows.append(
            {
                "id": case_id,
                "query": case["query"],
                "score": round(score, 4),
                "passed_checks": passed,
                "missing_response": response == "",
            }
        )
    output["cases"] = case_rows
    output["mean_score"] = round(
        sum(row["score"] for row in case_rows) / max(1, len(case_rows)),
        4,
    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate why-aware response quality.")
    parser.add_argument(
        "--eval-spec",
        default="src/specs/examples/why_aware_eval.yml",
        help="Path to YAML eval spec.",
    )
    parser.add_argument(
        "--responses-file",
        required=True,
        help="Path to JSON file keyed by case id -> response text.",
    )
    args = parser.parse_args()

    eval_spec = yaml.safe_load(Path(args.eval_spec).read_text(encoding="utf-8"))
    responses = json.loads(Path(args.responses_file).read_text(encoding="utf-8"))
    result = evaluate(eval_spec=eval_spec, responses=responses)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

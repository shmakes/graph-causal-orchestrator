"""Tools to call LLMs, RAG, etc."""

from __future__ import annotations

from typing import Any

from orchestration.causal_schema import CausalMechanism, InterventionOption, WhyAwareContext


def assemble_causal_context(
    query: str,
    what_evidence: list[dict] | None = None,
    why_hypotheses: list[CausalMechanism] | None = None,
    interventions: list[InterventionOption] | None = None,
    uncertainty: list[str] | None = None,
) -> WhyAwareContext:
    """Build a structured context payload for why-aware answer generation."""
    evidence = what_evidence or []
    hypotheses = why_hypotheses or []
    options = interventions or []
    known_uncertainty = uncertainty or []
    if not known_uncertainty:
        known_uncertainty = [
            "The graph structure alone does not prove effect magnitude.",
            "Potential confounders may be unobserved in the current dataset.",
        ]
    return WhyAwareContext(
        query=query,
        what_evidence=evidence,
        why_hypotheses=hypotheses,
        interventions=options,
        uncertainty=known_uncertainty,
    )


def render_why_aware_prompt(context: WhyAwareContext) -> str:
    """Render a deterministic prompt for an LLM or templated response layer."""
    lines: list[str] = [
        f"User query: {context['query']}",
        "",
        "Observed facts (what):",
    ]
    if context["what_evidence"]:
        for row in context["what_evidence"]:
            lines.append(f"- {row}")
    else:
        lines.append("- No factual rows were retrieved.")

    lines.append("")
    lines.append("Causal hypotheses (why):")
    if context["why_hypotheses"]:
        for item in context["why_hypotheses"]:
            lines.append(f"- Path: {' -> '.join(item['path'])}")
            lines.append(f"  Mechanism: {item['mechanism']}")
            lines.append(f"  Confidence: {item['confidence']:.2f}")
    else:
        lines.append("- No causal path hypothesis was found.")

    lines.append("")
    lines.append("Candidate interventions:")
    if context["interventions"]:
        for item in context["interventions"]:
            lines.append(
                "- "
                f"{item['recommendation']} "
                f"(effect={item['expected_effect_score']:.2f}, confidence={item['confidence']:.2f})"
            )
    else:
        lines.append("- No intervention candidate could be ranked.")

    lines.append("")
    lines.append("Uncertainty and caveats:")
    for item in context["uncertainty"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def get_llm_tools(**kwargs: Any) -> list[Any]:
    """Return core callable tools used by orchestration layers."""
    _ = kwargs
    return [
        {
            "name": "assemble_causal_context",
            "description": "Build structured what/why/intervention context payload.",
            "callable": assemble_causal_context,
        },
        {
            "name": "render_why_aware_prompt",
            "description": "Render deterministic prompt text from context payload.",
            "callable": render_why_aware_prompt,
        },
    ]

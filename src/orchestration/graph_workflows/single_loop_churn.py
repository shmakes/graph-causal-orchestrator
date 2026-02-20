"""LangGraph: single agent loop for churn investigation."""

from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from orchestration.agents.causal_agent import explain_causal_paths, suggest_interventions
from orchestration.agents.data_agent import query_graph
from orchestration.tools.llm_tools import assemble_causal_context, render_why_aware_prompt


class SingleLoopState(TypedDict, total=False):
    query: str
    cypher: str
    params: dict[str, Any]
    source_id: str
    target_id: str
    data: list[dict]
    causal_explanations: list[dict]
    interventions: list[dict]
    response: str
    error: str


def build_single_loop_graph(config: dict[str, Any] | None = None):
    """Build a minimal facts -> causality -> response LangGraph pipeline."""
    cfg = config or {}
    client = cfg.get("client")
    max_depth = int(cfg.get("max_depth", 5))
    intervention_limit = int(cfg.get("intervention_limit", 5))

    def retrieve_facts(state: SingleLoopState) -> dict[str, Any]:
        cypher = state.get("cypher")
        if not cypher:
            return {"data": []}
        params = state.get("params") or {}
        rows = query_graph(cypher=cypher, params=params, client=client)
        return {"data": rows}

    def explain_node(state: SingleLoopState) -> dict[str, Any]:
        source_id = state.get("source_id")
        target_id = state.get("target_id")
        if not (source_id and target_id and client):
            return {"causal_explanations": []}
        explanations = explain_causal_paths(
            source_id=source_id,
            target_id=target_id,
            client=client,
            max_depth=max_depth,
        )
        return {"causal_explanations": explanations}

    def intervention_node(state: SingleLoopState) -> dict[str, Any]:
        target_id = state.get("target_id")
        if not (target_id and client):
            return {"interventions": []}
        ranked = suggest_interventions(
            node_id=target_id,
            client=client,
            limit=intervention_limit,
        )
        return {"interventions": ranked}

    def compose_node(state: SingleLoopState) -> dict[str, Any]:
        context = assemble_causal_context(
            query=state.get("query", ""),
            what_evidence=state.get("data") or [],
            why_hypotheses=state.get("causal_explanations") or [],
            interventions=state.get("interventions") or [],
        )
        return {"response": render_why_aware_prompt(context)}

    graph = StateGraph(SingleLoopState)
    graph.add_node("retrieve_facts", retrieve_facts)
    graph.add_node("explain_causality", explain_node)
    graph.add_node("rank_interventions", intervention_node)
    graph.add_node("compose_response", compose_node)
    graph.set_entry_point("retrieve_facts")
    graph.add_edge("retrieve_facts", "explain_causality")
    graph.add_edge("explain_causality", "rank_interventions")
    graph.add_edge("rank_interventions", "compose_response")
    graph.add_edge("compose_response", END)
    return graph.compile()

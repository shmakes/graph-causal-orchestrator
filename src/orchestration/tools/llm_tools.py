"""Tools to call LLMs, RAG, etc."""

from typing import Any


def get_llm_tools(**kwargs: Any) -> list[Any]:
    """Return list of LLM-related tools (e.g. summarize, RAG query). Stub."""
    raise NotImplementedError("Wrap LLM calls as LangChain/AutoGen tools.")

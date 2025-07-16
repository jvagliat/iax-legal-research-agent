"""Define the configurable parameters for the index graph."""

from __future__ import annotations

from dataclasses import dataclass, field

from iax_legal_lg_rag_research_agent.shared.configuration import BaseConfiguration

# This file contains sample documents to index, based on the following LangChain and LangGraph documentation pages:
# - https://python.langchain.com/v0.3/docs/concepts/
# - https://langchain-ai.github.io/langgraph/concepts/low_level/
#DEFAULT_DOCS_FILE = "src/sample_docs.json"
DEFAULT_DOCS_FILE = "src/iax_legal_lg_rag_research_agent/tesis_from_csv_to_ingest_claude_enhanced.json"
import langchain
langchain.debug = True

import asyncio
import json

def load_json_sync(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@dataclass(kw_only=True)
class IndexConfiguration(BaseConfiguration):
    """Configuration class for indexing and retrieval operations.

    This class defines the parameters needed for configuring the indexing and
    retrieval processes, including embedding model selection, retriever provider choice, and search parameters.
    """

    docs_file: str = field(
        default=DEFAULT_DOCS_FILE,
        metadata={
            "description": "Path to a JSON file containing default documents to index."
        },
    )

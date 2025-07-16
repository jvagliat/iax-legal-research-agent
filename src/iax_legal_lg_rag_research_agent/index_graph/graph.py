"""This "graph" simply exposes an endpoint for a user to upload docs to be indexed."""

import json
from typing import Optional

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

from iax_legal_lg_rag_research_agent.index_graph.configuration import IndexConfiguration, load_json_sync
from iax_legal_lg_rag_research_agent.index_graph.state import IndexState
from iax_legal_lg_rag_research_agent.shared import retrieval
from iax_legal_lg_rag_research_agent.shared.state import reduce_docs
import asyncio


async def index_docs(
    state: IndexState, *, config: Optional[RunnableConfig] = None
) -> dict[str, str]:
    """Asynchronously index documents in the given state using the configured retriever.

    This function takes the documents from the state, ensures they have a user ID,
    adds them to the retriever's index, and then signals for the documents to be
    deleted from the state.

    If docs are not provided in the state, they will be loaded
    from the configuration.docs_file JSON file.

    Args:
        state (IndexState): The current state containing documents and retriever.
        config (Optional[RunnableConfig]): Configuration for the indexing process.r
    """
    if not config:
        raise ValueError("Configuration required to run index_docs.")

    configuration = IndexConfiguration.from_runnable_config(config)
    docs = state.docs
    if not docs:
        docs = reduce_docs([], await asyncio.to_thread(load_json_sync, configuration.docs_file))

    def _create_retriever_and_add_docs_batch(batch_docs):
        with retrieval.make_retriever(config) as retriever:
            return retriever.add_documents(batch_docs)
    
    # Process documents in batches to avoid exceeding OpenAI's token limit
    batch_size = 150  # Process 150 documents at a time
    total_docs = len(docs)
    
    for i in range(0, total_docs, batch_size):
        batch_docs = docs[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size}: {len(batch_docs)} documents")
        await asyncio.to_thread(_create_retriever_and_add_docs_batch, batch_docs)

    return {"docs": "delete"}


# Define the graph
builder = StateGraph(IndexState, config_schema=IndexConfiguration)
builder.add_node(index_docs)
builder.add_edge(START, "index_docs")
builder.add_edge("index_docs", END)
# Compile into a graph object that you can invoke and deploy.
graph = builder.compile()
graph.name = "IndexGraph"

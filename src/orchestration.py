import asyncio
from src.mcp_client import mcp
from src.retrieval import ArxivRetrievalAgent, PubmedRetrievalAgent
from src import summarization, insights

def merge_results(local, mcp_result):
    if not mcp_result or (isinstance(mcp_result, dict) and mcp_result.get("_fallback")):
        return local
    return mcp_result or local

async def run_pipeline(query: str, sources: list[str], max_papers: int = 10):
    # Step 1: Retrieval using class-based agents
    arxiv_agent = ArxivRetrievalAgent()
    pubmed_agent = PubmedRetrievalAgent()

    local_papers = []
    if "arxiv" in sources:
        local_papers += arxiv_agent.get_papers(query, max_papers)
    if "pubmed" in sources:
        local_papers += pubmed_agent.get_papers(query, max_papers)

    mcp_papers = mcp.call("retrieval.get_papers", {"query": query, "sources": sources, "max_papers": max_papers})
    papers = merge_results(local_papers, mcp_papers)

    # Step 2: Summarization
    local_summaries = summarization.summarize_documents(papers)
    mcp_summaries = mcp.call("summarization.summarize", {"docs": papers})
    summaries = merge_results(local_summaries, mcp_summaries)

    # Step 3: Insight generation
    summaries_text = [s.get("summary") for s in summaries if s.get("summary")]
    local_insights = insights.generate_insights(summaries_text)
    mcp_insights = mcp.call("insight.generate", {"summaries": summaries_text})
    insights_final = merge_results(local_insights, mcp_insights)

    return {
        "query": query,
        "total_papers": len(papers),
        "papers": papers,
        "summaries": summaries,
        "insights": insights_final,
    }

"""
Example: Parallel Multi-Agent Workflow
=======================================
This example shows how to run multiple research branches in parallel
using ThreadPoolExecutor, then merge results into a single report.

Run: python examples/multi_agent_workflow.py
"""

import sys
import os
import concurrent.futures
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module_03_multi_agent import (
    ResearcherAgent, WriterAgent, ResearchResult, ResearchPlan
)


PARALLEL_TOPICS = [
    "What is RAG and how does it work?",
    "What are the main failure modes of LLM agents?",
    "How do vector databases enable semantic search?",
]


def research_topic(question: str) -> ResearchResult:
    """Worker function — runs in a thread pool."""
    agent = ResearcherAgent()
    plan = ResearchPlan(goal=question, questions=[question])
    results = agent.run(plan)
    return results[0]


def parallel_research(topics: list[str]) -> list[ResearchResult]:
    """Run all topics in parallel and collect results."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(topics)) as executor:
        futures = {executor.submit(research_topic, t): t for t in topics}
        results = []
        for future in concurrent.futures.as_completed(futures):
            topic = futures[future]
            try:
                result = future.result()
                print(f"  [done] {topic[:50]}...")
                results.append(result)
            except Exception as exc:
                print(f"  [error] {topic}: {exc}")
    return results


if __name__ == "__main__":
    print("Running parallel research on multiple topics...")
    results = parallel_research(PARALLEL_TOPICS)

    writer = WriterAgent()
    report = writer.run(
        goal="Overview of LLM Agent Architecture and Challenges",
        research=results,
    )

    print("\n=== Merged Report ===")
    print(report.content)

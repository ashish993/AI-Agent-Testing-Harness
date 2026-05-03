"""
Example: Deep Research Agent
============================
This example extends the basic pipeline with a recursive planner that can
generate follow-up questions based on initial research findings.

Run: python examples/deep_research.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module_03_multi_agent import (
    PlannerAgent, ResearcherAgent, WriterAgent,
    ResearchPlan, ResearchResult
)


class DeepResearchPipeline:
    """
    Two-pass research pipeline:
      Pass 1 — initial plan and research
      Pass 2 — identify gaps, generate follow-up questions, research again
    """

    def __init__(self, follow_up_count: int = 2):
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.follow_up_count = follow_up_count

    def identify_gaps(self, results: list[ResearchResult]) -> list[str]:
        """
        Stub: in production, call an LLM to identify unanswered sub-questions.
        Here we generate simple follow-up questions from the stubs.
        """
        follow_ups = []
        for r in results[:self.follow_up_count]:
            follow_ups.append(f"Can you elaborate further on: {r.question[:60]}?")
        return follow_ups

    def run(self, goal: str):
        print(f"\n=== Deep Research: {goal} ===")

        # Pass 1
        print("\n[Pass 1] Initial research...")
        plan = self.planner.run(goal)
        results = self.researcher.run(plan)

        # Identify gaps and do pass 2
        follow_ups = self.identify_gaps(results)
        if follow_ups:
            print(f"\n[Pass 2] Follow-up research ({len(follow_ups)} questions)...")
            follow_plan = ResearchPlan(goal=goal, questions=follow_ups)
            follow_results = self.researcher.run(follow_plan)
            results.extend(follow_results)

        # Write final report
        print("\n[Writing] Synthesising all findings...")
        report = self.writer.run(goal, results)

        print("\n=== Final Report ===")
        print(report.content)
        return report


if __name__ == "__main__":
    pipeline = DeepResearchPipeline(follow_up_count=2)
    pipeline.run("What are the main security challenges in deploying LLM-based agents?")

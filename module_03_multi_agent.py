"""
Module 03 — Multi-Agent Pipeline: Planner → Researcher → Writer
===============================================================
Real-world tasks are too complex for a single agent. This module shows
how to split work across three specialised agents that hand off results:

  Planner   — breaks a high-level goal into a list of research questions
  Researcher — answers each question (stub: replace with web search / RAG)
  Writer     — synthesises answers into a final report

The pipeline is purely sequential here.  To add parallelism, replace the
for-loop in Researcher with concurrent.futures.ThreadPoolExecutor.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol


# ---------------------------------------------------------------------------
# Shared data model
# ---------------------------------------------------------------------------

@dataclass
class ResearchPlan:
    goal: str
    questions: list[str] = field(default_factory=list)


@dataclass
class ResearchResult:
    question: str
    answer: str


@dataclass
class FinalReport:
    goal: str
    content: str


# ---------------------------------------------------------------------------
# Agent protocol (any object with a .run() method qualifies)
# ---------------------------------------------------------------------------

class Agent(Protocol):
    name: str
    def run(self, *args, **kwargs): ...


# ---------------------------------------------------------------------------
# Agent implementations (stubs — swap call_llm() for a real API)
# ---------------------------------------------------------------------------

def call_llm(prompt: str) -> str:
    """Stub LLM — replace with real model call."""
    if "break this goal" in prompt:
        return "1. What is prompt injection?\n2. What are common defences?\n3. Any recent incidents?"
    if "answer this question" in prompt:
        q = prompt.split("Question:")[-1].strip()
        return f"[Stub answer for: {q}]"
    if "write a report" in prompt:
        return "# Report\n\nBased on the research, here is a comprehensive summary...\n(stub)"
    return "(stub response)"


class PlannerAgent:
    name = "Planner"

    def run(self, goal: str) -> ResearchPlan:
        prompt = (
            f"You are a research planner. Break this goal into 2-4 focused research questions.\n"
            f"Goal: {goal}\nRespond with a numbered list."
        )
        raw = call_llm(prompt)
        questions = []
        for line in raw.strip().splitlines():
            line = line.strip()
            if line and line[0].isdigit():
                # Remove leading "1. " etc.
                questions.append(line.split(". ", 1)[-1])
        return ResearchPlan(goal=goal, questions=questions)


class ResearcherAgent:
    name = "Researcher"

    def run(self, plan: ResearchPlan) -> list[ResearchResult]:
        results = []
        for q in plan.questions:
            prompt = f"You are a researcher. Answer this question concisely.\nQuestion: {q}"
            answer = call_llm(prompt)
            results.append(ResearchResult(question=q, answer=answer))
        return results


class WriterAgent:
    name = "Writer"

    def run(self, goal: str, research: list[ResearchResult]) -> FinalReport:
        context = "\n\n".join(
            f"Q: {r.question}\nA: {r.answer}" for r in research
        )
        prompt = (
            f"You are a technical writer. write a report on: {goal}\n\n"
            f"Research findings:\n{context}\n\n"
            "Write a clear, structured report."
        )
        content = call_llm(prompt)
        return FinalReport(goal=goal, content=content)


# ---------------------------------------------------------------------------
# Pipeline orchestrator
# ---------------------------------------------------------------------------

class MultiAgentPipeline:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()

    def run(self, goal: str) -> FinalReport:
        print(f"[{self.planner.name}] Planning...")
        plan = self.planner.run(goal)
        print(f"  Questions: {plan.questions}")

        print(f"[{self.researcher.name}] Researching {len(plan.questions)} questions...")
        results = self.researcher.run(plan)
        for r in results:
            print(f"  Q: {r.question[:60]}... => {r.answer[:60]}...")

        print(f"[{self.writer.name}] Writing report...")
        report = self.writer.run(goal, results)
        return report


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pipeline = MultiAgentPipeline()
    report = pipeline.run("Explain prompt injection attacks and how to defend against them")
    print("\n=== Final Report ===")
    print(report.content)

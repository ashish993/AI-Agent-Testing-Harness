"""
Module 01 — Build Your First ReAct Agent From Scratch
======================================================
This module shows how to implement a simple ReAct (Reason + Act) loop
without any framework. You will understand exactly what happens inside
tools like LangChain or AutoGen before using them.

ReAct pattern:
  Thought → Action → Observation → Thought → ... → Final Answer
"""

import json
import re
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOLS: dict[str, dict] = {}


def tool(name: str, description: str):
    """Decorator to register a callable as a tool."""
    def decorator(fn: Callable):
        TOOLS[name] = {"fn": fn, "description": description}
        return fn
    return decorator


@tool("calculator", "Evaluate a simple arithmetic expression. Input: string like '3 * (4 + 2)'")
def calculator(expression: str) -> str:
    try:
        # Restrict to safe characters only
        safe = re.sub(r"[^0-9+\-*/().\s]", "", expression)
        result = eval(safe, {"__builtins__": {}})  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@tool("reverse_string", "Reverse a string. Input: any string.")
def reverse_string(text: str) -> str:
    return text[::-1]


@tool("word_count", "Count words in a sentence. Input: the sentence.")
def word_count(text: str) -> str:
    return str(len(text.split()))


# ---------------------------------------------------------------------------
# A minimal LLM stub (replace with real OpenAI / Ollama call)
# ---------------------------------------------------------------------------

def call_llm(prompt: str) -> str:
    """
    Stub LLM. In a real implementation swap this for:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(...)
        return response.choices[0].message.content
    """
    # Very simple rule-based stub so the demo runs without an API key
    if "what is 6 * 7" in prompt.lower():
        return "Thought: I need to multiply 6 by 7.\nAction: calculator\nAction Input: 6 * 7"
    if "observation: 42" in prompt.lower():
        return "Thought: The calculator returned 42, which is the answer.\nFinal Answer: 42"
    if "reverse" in prompt.lower() and "hello" in prompt.lower():
        return "Thought: I will reverse the word hello.\nAction: reverse_string\nAction Input: hello"
    if "observation: olleh" in prompt.lower():
        return "Thought: The reversed string is olleh.\nFinal Answer: olleh"
    return "Final Answer: I don't know."


# ---------------------------------------------------------------------------
# ReAct agent loop
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a helpful assistant that reasons step by step.
Available tools:
{tools}

Always respond in this format:
  Thought: <your reasoning>
  Action: <tool name>
  Action Input: <input to the tool>

Or, when done:
  Thought: <final reasoning>
  Final Answer: <your answer>
"""

def build_tool_descriptions() -> str:
    lines = []
    for name, info in TOOLS.items():
        lines.append(f"  - {name}: {info['description']}")
    return "\n".join(lines)


def parse_llm_output(text: str):
    """Return (action, action_input) or (None, final_answer)."""
    if "Final Answer:" in text:
        answer = text.split("Final Answer:")[-1].strip()
        return None, answer
    action_match = re.search(r"Action:\s*(.+)", text)
    input_match = re.search(r"Action Input:\s*(.+)", text)
    if action_match and input_match:
        return action_match.group(1).strip(), input_match.group(1).strip()
    return None, "Could not parse LLM output."


def run_agent(question: str, max_steps: int = 6) -> str:
    tool_desc = build_tool_descriptions()
    messages = SYSTEM_PROMPT.format(tools=tool_desc) + f"\nUser: {question}\n"

    print(f"\n=== Running agent on: {question!r} ===")
    for step in range(max_steps):
        response = call_llm(messages)
        print(f"\n[Step {step + 1}] LLM:\n{response}")

        action, value = parse_llm_output(response)
        if action is None:
            print(f"\n>>> Final Answer: {value}")
            return value

        if action not in TOOLS:
            observation = f"Unknown tool: {action}"
        else:
            observation = TOOLS[action]["fn"](value)

        print(f"Observation: {observation}")
        messages += response + f"\nObservation: {observation}\n"

    return "Agent exceeded max steps without a final answer."


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_agent("What is 6 * 7?")
    run_agent("Please reverse the word hello.")
